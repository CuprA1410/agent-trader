"""
Portfolio service — fetches balance and live positions from the exchange.
Uses the Facade pattern over ccxt.
"""
from __future__ import annotations
import logging
from typing import List, Optional

import ccxt

from config import cfg
from models.position import Position

log = logging.getLogger(__name__)


class PortfolioService:
    """Provides portfolio balance and live exchange position data."""

    def __init__(self, exchange: ccxt.Exchange):
        self._exchange = exchange

    # ── Balance ────────────────────────────────────────────────────────────────

    def get_balance(self) -> dict:
        """Return USDT balance dict: {total, free, used}."""
        params = {"type": "swap" if cfg.is_futures else "spot"}
        balance = self._exchange.fetch_balance(params)
        usdt = balance.get("USDT", {})
        return {
            "total": float(usdt.get("total", 0)),
            "free":  float(usdt.get("free",  0)),
            "used":  float(usdt.get("used",  0)),
        }

    # ── Live Positions ─────────────────────────────────────────────────────────

    def get_live_positions(self, symbols: Optional[List[str]] = None) -> List[Position]:
        """
        Fetch all open futures positions from the exchange.
        Returns Position objects with live mark price and PnL.
        """
        if not cfg.is_futures:
            return []
        try:
            if symbols:
                ccxt_syms = [self._to_ccxt(s) for s in symbols]
                raw = self._exchange.fetch_positions(ccxt_syms)
            else:
                raw = self._exchange.fetch_positions()

            positions = []
            for p in raw:
                contracts = float(p.get("contracts") or 0)
                if contracts <= 0:
                    continue
                pos = Position(
                    symbol=self._from_ccxt(p["symbol"]),
                    side=p.get("side", "long"),
                    quantity=contracts,
                    entry_price=float(p.get("entryPrice") or 0),
                    sl_price=0.0,
                    tp_price=0.0,
                    leverage=int(p.get("leverage") or cfg.futures_leverage),
                )
                pos.mark_price     = p.get("markPrice")
                pos.unrealised_pnl = p.get("unrealizedPnl")
                pos.liquidation    = p.get("liquidationPrice")
                positions.append(pos)
            return positions
        except Exception as e:
            log.error(f"Failed to fetch positions: {e}")
            return []

    def is_position_open(self, symbol: str) -> bool:
        """Quick check: is there an open position for this symbol on the exchange?"""
        sym = self._to_ccxt(symbol)
        try:
            positions = self._exchange.fetch_positions([sym])
            return any(float(p.get("contracts") or 0) > 0 for p in positions)
        except Exception:
            return False

    # ── Summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        balance   = self.get_balance()
        positions = self.get_live_positions()
        return {
            "balance":              balance,
            "open_positions_count": len(positions),
            "open_positions":       [p.to_dict() for p in positions],
            "risk_per_trade_usd":   cfg.risk_amount_usd,
        }

    # ── Helpers ────────────────────────────────────────────────────────────────

    @staticmethod
    def _to_ccxt(symbol: str) -> str:
        if "/" in symbol:
            return symbol
        base = symbol.upper().replace("USDT", "").replace("PERP", "")
        return f"{base}/USDT:USDT"

    @staticmethod
    def _from_ccxt(symbol: str) -> str:
        """'BTC/USDT:USDT' → 'BTCUSDT'"""
        return symbol.split("/")[0].replace("/", "") + "USDT"
