"""
Repository pattern for trade persistence.
Stores closed trades as CSV. Provides query methods.
"""
from __future__ import annotations
import csv
from pathlib import Path
from typing import List, Optional
from datetime import date

from models.trade import Trade
from config import cfg

_FIELDS = [
    "date", "symbol", "side", "strategy", "confidence",
    "entry", "exit", "quantity", "pnl_usd", "pnl_pct",
    "outcome", "screenshot", "notes",
]


class TradeRepository:
    """Persists and queries closed trades."""

    def __init__(self, path: Optional[Path] = None):
        self._path = path or (cfg.log_dir / "journal" / "trades.csv")
        self._ensure_file()

    def _ensure_file(self):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            with open(self._path, "w", newline="") as f:
                csv.DictWriter(f, fieldnames=_FIELDS).writeheader()

    # ── Write ──────────────────────────────────────────────────────────────────

    def save(self, trade: Trade) -> None:
        self._ensure_file()
        with open(self._path, "a", newline="") as f:
            csv.DictWriter(f, fieldnames=_FIELDS).writerow(trade.to_dict())

    # ── Read ───────────────────────────────────────────────────────────────────

    def all(self) -> List[Trade]:
        self._ensure_file()
        rows = []
        with open(self._path, newline="") as f:
            for row in csv.DictReader(f):
                try:
                    rows.append(Trade.from_dict(row))
                except Exception:
                    pass
        return rows

    def recent(self, n: int = 10) -> List[Trade]:
        return self.all()[-n:]

    def by_symbol(self, symbol: str) -> List[Trade]:
        return [t for t in self.all() if t.symbol.upper() == symbol.upper()]

    def today(self) -> List[Trade]:
        today = date.today()
        return [t for t in self.all() if t.date.date() == today]

    # ── Stats ──────────────────────────────────────────────────────────────────

    def stats(self, trades: Optional[List[Trade]] = None) -> dict:
        trades = trades if trades is not None else self.all()
        if not trades:
            return {"trades": 0}

        wins   = [t for t in trades if t.outcome == "WIN"]
        losses = [t for t in trades if t.outcome == "LOSS"]
        pnls   = [t.pnl_usd for t in trades]

        return {
            "trades":    len(trades),
            "wins":      len(wins),
            "losses":    len(losses),
            "win_rate":  round(len(wins) / len(trades) * 100, 1),
            "total_pnl": round(sum(pnls), 2),
            "avg_win":   round(sum(t.pnl_usd for t in wins) / len(wins), 2) if wins else 0,
            "avg_loss":  round(sum(t.pnl_usd for t in losses) / len(losses), 2) if losses else 0,
            "best":      round(max(pnls), 2) if pnls else 0,
            "worst":     round(min(pnls), 2) if pnls else 0,
            "avg_r":     round(sum(t.r_multiple for t in trades) / len(trades), 2),
        }

    def stats_today(self) -> dict:
        return self.stats(self.today())
