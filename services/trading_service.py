"""
Trading service — place and close futures orders.
Encapsulates all order logic: sizing, leverage, SL/TP placement.
"""
from __future__ import annotations
import logging
from typing import Optional, Tuple

import ccxt

from config import cfg
from models.position import Position
from models.trade import Trade
from repositories.position_repository import PositionRepository
from repositories.trade_repository import TradeRepository

log = logging.getLogger(__name__)


class TradingService:
    """
    Handles order lifecycle: open → monitor → close.

    Responsibilities:
    - Calculate position size from risk %
    - Place market orders with SL / TP
    - Close positions
    - Record trades to repository
    """

    def __init__(
        self,
        exchange: ccxt.Exchange,
        position_repo: PositionRepository,
        trade_repo: TradeRepository,
    ):
        self._ex           = exchange
        self._pos_repo     = position_repo
        self._trade_repo   = trade_repo

    # ── Open ───────────────────────────────────────────────────────────────────

    def open_position(
        self,
        symbol: str,
        side: str,
        entry: float,
        sl: float,
        tp: float,
        strategy: str = "",
        confidence: int = 0,
        dry_run: bool = False,
    ) -> Tuple[bool, Position, str]:
        """
        Open a futures position.

        Returns (success, position, error_message).
        """
        # Guard: already in this symbol?
        if self._pos_repo.has(symbol):
            return False, None, f"Already have an open position in {symbol}"

        # Guard: max positions
        if self._pos_repo.count() >= cfg.max_positions:
            return False, None, f"Max positions ({cfg.max_positions}) reached"

        # Guard: confidence
        if confidence < 7:
            return False, None, f"Confidence {confidence}/10 is below threshold (7)"

        quantity, notional = self._calc_quantity(entry, sl)
        ccxt_sym = self._to_ccxt(symbol)

        position = Position(
            symbol=symbol.upper(),
            side=side.lower(),
            quantity=quantity,
            entry_price=entry,
            sl_price=sl,
            tp_price=tp,
            strategy=strategy,
            confidence=confidence,
        )

        if dry_run:
            log.info(f"DRY RUN — would open {side.upper()} {symbol} "
                     f"qty={quantity} entry={entry} sl={sl} tp={tp}")
            return True, position, "DRY RUN"

        try:
            # Set leverage first
            try:
                self._ex.set_leverage(cfg.futures_leverage, ccxt_sym)
            except Exception:
                pass

            ccxt_side = "buy" if side.lower() == "long" else "sell"

            # Market order
            order = self._ex.create_order(
                symbol=ccxt_sym,
                type="market",
                side=ccxt_side,
                amount=quantity,
                params={"tradeSide": "open"},
            )
            position.order_id = order.get("id", "")

            # SL
            close_side = "sell" if side.lower() == "long" else "buy"
            try:
                sl_order = self._ex.create_order(
                    symbol=ccxt_sym, type="market", side=close_side,
                    amount=quantity,
                    params={"stopPrice": sl, "tradeSide": "close", "reduceOnly": True},
                )
                position.sl_order_id = sl_order.get("id", "")
            except Exception as e:
                log.warning(f"SL order failed: {e}")

            # TP
            try:
                tp_order = self._ex.create_order(
                    symbol=ccxt_sym, type="market", side=close_side,
                    amount=quantity,
                    params={"stopPrice": tp, "tradeSide": "close", "reduceOnly": True},
                )
                position.tp_order_id = tp_order.get("id", "")
            except Exception as e:
                log.warning(f"TP order failed: {e}")

            # Persist
            self._pos_repo.save(position)
            log.info(f"Opened {side.upper()} {symbol} | qty={quantity} | "
                     f"notional=${notional:.2f} | margin=${notional/cfg.futures_leverage:.2f}")
            return True, position, ""

        except Exception as e:
            log.error(f"Failed to open position: {e}")
            return False, None, str(e)

    # ── Close ──────────────────────────────────────────────────────────────────

    def close_position(
        self,
        symbol: str,
        exit_price: float,
        reason: str = "",
    ) -> Tuple[bool, Optional[Trade], str]:
        """
        Close an open position and record the trade.

        Returns (success, trade, error_message).
        """
        pos = self._pos_repo.get(symbol)
        if not pos:
            return False, None, f"No tracked position for {symbol}"

        ccxt_sym   = self._to_ccxt(symbol)
        close_side = "sell" if pos.is_long else "buy"

        try:
            order = self._ex.create_order(
                symbol=ccxt_sym,
                type="market",
                side=close_side,
                amount=pos.quantity,
                params={"tradeSide": "close", "reduceOnly": True},
            )
        except Exception as e:
            return False, None, str(e)

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

        self._trade_repo.save(trade)
        self._pos_repo.remove(symbol)

        log.info(f"Closed {symbol} {outcome} | P&L=${pnl:+.2f}")
        return True, trade, ""

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _calc_quantity(self, entry: float, sl: float) -> Tuple[float, float]:
        """Return (quantity, notional_usd) using 1% risk rule."""
        risk_usd  = cfg.risk_amount_usd
        sl_dist   = abs(entry - sl)
        if sl_dist == 0:
            raise ValueError("SL distance is zero")
        quantity  = risk_usd / sl_dist
        notional  = quantity * entry
        # Safety cap: max margin = 30× risk (e.g. $300 margin = $1500 notional at 5x).
        # This allows proper 1% sizing even with tight SLs, while still preventing
        # absurdly large positions if SL distance is near-zero.
        max_margin   = risk_usd * 30
        max_notional = max_margin * cfg.futures_leverage
        if notional > max_notional:
            quantity = max_notional / entry
            notional = max_notional
        return round(quantity, 6), round(notional, 4)

    @staticmethod
    def _to_ccxt(symbol: str) -> str:
        if "/" in symbol:
            return symbol
        base = symbol.upper().replace("USDT", "").replace("PERP", "")
        return f"{base}/USDT:USDT"
