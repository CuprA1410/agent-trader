"""
Repository pattern for open position tracking.
Stores open positions as JSON so they survive restarts.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Optional

from models.position import Position
from config import cfg


class PositionRepository:
    """Persists and queries open positions."""

    def __init__(self, path: Optional[Path] = None):
        self._path = path or (cfg.log_dir / "positions.json")
        self._positions: Dict[str, Position] = {}
        self._load()

    def _load(self):
        if self._path.exists():
            with open(self._path) as f:
                data = json.load(f)
            self._positions = {
                sym: Position.from_dict(d) for sym, d in data.items()
            }
        else:
            self._positions = {}

    def _save(self):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "w") as f:
            json.dump(
                {sym: p.to_dict() for sym, p in self._positions.items()},
                f, indent=2,
            )

    # ── Write ──────────────────────────────────────────────────────────────────

    def save(self, position: Position) -> None:
        self._positions[position.symbol.upper()] = position
        self._save()

    def remove(self, symbol: str) -> Optional[Position]:
        sym = symbol.upper()
        pos = self._positions.pop(sym, None)
        if pos:
            self._save()
        return pos

    # ── Read ───────────────────────────────────────────────────────────────────

    def get(self, symbol: str) -> Optional[Position]:
        return self._positions.get(symbol.upper())

    def all(self) -> List[Position]:
        return list(self._positions.values())

    def count(self) -> int:
        return len(self._positions)

    def symbols(self) -> List[str]:
        return list(self._positions.keys())

    def has(self, symbol: str) -> bool:
        return symbol.upper() in self._positions
