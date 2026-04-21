"""
Position monitor service.
Queries the exchange directly to detect when positions close (TP/SL hit natively).
"""
from __future__ import annotations
import logging
from typing import List, Tuple

import ccxt

from config import cfg
from models.position import Position
from models.trade import Trade
from repositories.position_repository import PositionRepository
from repositories.trade_repository import TradeRepository
from services.notification_service import NotificationService
from utils.circuit_breaker import CircuitBreaker

log = logging.getLogger(__name__)


class PositionMonitor:
    """
    Checks all tracked positions against the live exchange state.
    When a position is no longer open on the exchange, it was closed
    (via TP, SL, or liquidation). Records the trade and sends notification.
    """

    def __init__(
        self,
        exchange: ccxt.Exchange,
        position_repo: PositionRepository,
        trade_repo: TradeRepository,
        notifier: NotificationService,
        circuit_breaker: CircuitBreaker,
    ):
        self._ex       = exchange
        self._pos_repo = position_repo
        self._trade_repo = trade_repo
        self._notifier = notifier
        self._cb       = circuit_breaker

    # ── Public ─────────────────────────────────────────────────────────────────

    def check_all(self) -> List[Trade]:
        """
        Check all tracked positions. Returns list of trades that were closed.
        """
        closed_trades = []
        positions = self._pos_repo.all()

        for pos in positions:
            trade = self._check_position(pos)
            if trade:
                closed_trades.append(trade)

        return closed_trades

    # ── Private ────────────────────────────────────────────────────────────────

    def _check_position(self, pos: Position) -> None | Trade:
        """Returns a Trade if position was closed, else None."""
        ccxt_sym = pos.ccxt_symbol
        try:
            live = self._ex.fetch_positions([ccxt_sym])
            open_contracts = sum(
                float(p.get("contracts") or 0)
                for p in live
                if float(p.get("contracts") or 0) > 0
            )
        except Exception as e:
            log.warning(f"Could not fetch position for {pos.symbol}: {e}")
            return None

        if open_contracts > 0:
            return None  # Still open

        # Position closed — find exit price
        exit_price, reason = self._get_exit_price(pos)

        # Calculate P&L
        if pos.is_long:
            pnl = (exit_price - pos.entry_price) * pos.quantity
        else:
            pnl = (pos.entry_price - exit_price) * pos.quantity

        outcome = "WIN" if pnl > 0 else ("LOSS" if pnl < 0 else "BREAKEVEN")

        trade = Trade(
            symbol=pos.symbol,
            side=pos.side,
            entry=pos.entry_price,
            exit=exit_price,
            quantity=pos.quantity,
            pnl_usd=round(pnl, 4),
            outcome=outcome,
            strategy=pos.strategy,
            confidence=pos.confidence,
            notes=reason,
        )

        # Persist
        self._trade_repo.save(trade)
        self._pos_repo.remove(pos.symbol)
        self._cb.record_pnl(pnl)

        # Notify
        self._notifier.trade_closed(trade)

        # Circuit breaker
        if self._cb.is_triggered():
            self._notifier.circuit_breaker(
                self._cb.daily_pnl(),
                self._cb.daily_pnl_pct(),
            )
            log.warning("CIRCUIT BREAKER TRIGGERED — trading paused")

        log.info(f"Position closed: {pos.symbol} {outcome} P&L=${pnl:+.2f}")
        return trade

    def _get_exit_price(self, pos: Position) -> Tuple[float, str]:
        """
        Try to find actual exit price from recent trade history.
        Falls back to TP or SL price based on which is closer to current mark.
        """
        ccxt_sym = pos.ccxt_symbol

        # Try recent trades
        try:
            trades = self._ex.fetch_my_trades(ccxt_sym, limit=5)
            close_trades = [
                t for t in reversed(trades)
                if t.get("info", {}).get("tradeSide") == "close"
                or t.get("side") != ("buy" if pos.is_long else "sell")
            ]
            if close_trades:
                price = float(close_trades[-1]["price"])
                return price, "Exchange fill price"
        except Exception:
            pass

        # Heuristic fallback: compare mark to SL/TP
        try:
            ticker = self._ex.fetch_ticker(ccxt_sym)
            mark = float(ticker.get("last") or ticker.get("close") or 0)
            if mark > 0:
                dist_sl = abs(mark - pos.sl_price)
                dist_tp = abs(mark - pos.tp_price)
                if dist_tp < dist_sl:
                    return pos.tp_price, "Estimated TP hit"
                else:
                    return pos.sl_price, "Estimated SL hit"
        except Exception:
            pass

        # Last resort
        return pos.sl_price, "Exit price unknown — using SL"
