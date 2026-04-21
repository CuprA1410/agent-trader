"""
Tracks daily P&L and enforces the 10% drawdown circuit breaker.

Usage:
    from utils.circuit_breaker import CircuitBreaker
    cb = CircuitBreaker()
    cb.record_pnl(-8.5)
    if cb.is_triggered():
        # stop trading
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, date
from config import cfg

STATE_FILE = cfg.log_dir / "circuit_breaker.json"


class CircuitBreaker:
    def __init__(self):
        self._load()

    def _load(self):
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                self._state = json.load(f)
        else:
            self._state = {}
        # Reset if new day
        today = date.today().isoformat()
        if self._state.get("date") != today:
            self._state = {
                "date":         today,
                "daily_pnl":    0.0,
                "triggered":    False,
                "triggered_at": None,
            }
            self._save()

    def _save(self):
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump(self._state, f, indent=2)

    def record_pnl(self, pnl_usd: float):
        """Call this after every closed trade."""
        self._load()
        self._state["daily_pnl"] = round(self._state["daily_pnl"] + pnl_usd, 4)
        # Check trigger
        drop_pct = abs(self._state["daily_pnl"]) / cfg.portfolio_value_usd
        if self._state["daily_pnl"] < 0 and drop_pct >= cfg.drawdown_limit_pct:
            self._state["triggered"]    = True
            self._state["triggered_at"] = datetime.now().isoformat()
        self._save()

    def is_triggered(self) -> bool:
        self._load()
        return self._state.get("triggered", False)

    def daily_pnl(self) -> float:
        self._load()
        return self._state.get("daily_pnl", 0.0)

    def daily_pnl_pct(self) -> float:
        return (self.daily_pnl() / cfg.portfolio_value_usd) * 100

    def status(self) -> dict:
        self._load()
        return {
            **self._state,
            "daily_pnl_pct": round(self.daily_pnl_pct(), 2),
            "limit_pct":     cfg.drawdown_limit_pct * 100,
        }

    def reset(self):
        """Manually reset (use at start of new day)."""
        today = date.today().isoformat()
        self._state = {
            "date":         today,
            "daily_pnl":    0.0,
            "triggered":    False,
            "triggered_at": None,
        }
        self._save()
