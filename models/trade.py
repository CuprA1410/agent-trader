from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Trade:
    """Represents a completed (closed) trade."""
    symbol:     str
    side:       str          # "long" | "short"
    entry:      float
    exit:       float
    quantity:   float
    pnl_usd:    float
    outcome:    str          # "WIN" | "LOSS" | "BREAKEVEN"
    strategy:   str          = ""
    confidence: int          = 0
    screenshot: str          = ""
    notes:      str          = ""
    date:       datetime     = field(default_factory=datetime.now)
    portfolio_value: float   = 1000.0

    @property
    def pnl_pct(self) -> float:
        return round((self.pnl_usd / self.portfolio_value) * 100, 4)

    @property
    def r_multiple(self) -> float:
        """R multiple: how many R did this trade make/lose."""
        risk = self.portfolio_value * 0.01  # 1% risk
        return round(self.pnl_usd / risk, 2) if risk else 0

    def to_dict(self) -> dict:
        return {
            "date":           self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "symbol":         self.symbol,
            "side":           self.side,
            "strategy":       self.strategy,
            "confidence":     self.confidence,
            "entry":          self.entry,
            "exit":           self.exit,
            "quantity":       self.quantity,
            "pnl_usd":        self.pnl_usd,
            "pnl_pct":        self.pnl_pct,
            "outcome":        self.outcome,
            "screenshot":     self.screenshot,
            "notes":          self.notes,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Trade:
        return cls(
            symbol=d["symbol"],
            side=d["side"],
            entry=float(d["entry"]),
            exit=float(d["exit"]),
            quantity=float(d["quantity"]),
            pnl_usd=float(d["pnl_usd"]),
            outcome=d["outcome"],
            strategy=d.get("strategy", ""),
            confidence=int(d.get("confidence", 0)),
            screenshot=d.get("screenshot", ""),
            notes=d.get("notes", ""),
            date=datetime.strptime(d["date"], "%Y-%m-%d %H:%M:%S"),
        )
