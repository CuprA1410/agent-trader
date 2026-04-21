from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Position:
    """Represents an open trade position."""
    symbol:       str
    side:         str          # "long" | "short"
    quantity:     float
    entry_price:  float
    sl_price:     float
    tp_price:     float
    strategy:     str          = ""
    confidence:   int          = 0
    order_id:     str          = ""
    sl_order_id:  str          = ""
    tp_order_id:  str          = ""
    opened_at:    datetime     = field(default_factory=datetime.now)

    # Live data (fetched from exchange, not persisted)
    mark_price:       Optional[float] = None
    unrealised_pnl:   Optional[float] = None
    liquidation:      Optional[float] = None
    leverage:         Optional[int]   = None

    @property
    def is_long(self) -> bool:
        return self.side.lower() == "long"

    @property
    def ccxt_symbol(self) -> str:
        """Convert 'BTCUSDT' → 'BTC/USDT:USDT'"""
        if "/" in self.symbol:
            return self.symbol
        base = self.symbol.upper().replace("USDT", "").replace("PERP", "")
        return f"{base}/USDT:USDT"

    def to_dict(self) -> dict:
        return {
            "symbol":       self.symbol,
            "side":         self.side,
            "quantity":     self.quantity,
            "entry_price":  self.entry_price,
            "sl_price":     self.sl_price,
            "tp_price":     self.tp_price,
            "strategy":     self.strategy,
            "confidence":   self.confidence,
            "order_id":     self.order_id,
            "sl_order_id":  self.sl_order_id,
            "tp_order_id":  self.tp_order_id,
            "opened_at":    self.opened_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> Position:
        return cls(
            symbol=d["symbol"],
            side=d["side"],
            quantity=float(d["quantity"]),
            entry_price=float(d["entry_price"]),
            sl_price=float(d["sl_price"]),
            tp_price=float(d["tp_price"]),
            strategy=d.get("strategy", ""),
            confidence=int(d.get("confidence", 0)),
            order_id=d.get("order_id", ""),
            sl_order_id=d.get("sl_order_id", ""),
            tp_order_id=d.get("tp_order_id", ""),
            opened_at=datetime.fromisoformat(d["opened_at"]) if d.get("opened_at") else datetime.now(),
        )
