"""
CLI wrapper for TradingService.open_position()

Usage:
    python scripts/place_order.py \
        --symbol BTCUSDT --side long \
        --entry 84200 --sl 83100 --tp 86400 \
        --strategy "S/R Breakout" --confidence 8

    python scripts/place_order.py ... --dry-run
"""
from __future__ import annotations
import sys, json, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from exchanges.exchange_factory import get_exchange
from repositories.position_repository import PositionRepository
from repositories.trade_repository import TradeRepository
from services.trading_service import TradingService


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol",     required=True)
    parser.add_argument("--side",       required=True, choices=["long", "short"])
    parser.add_argument("--entry",      required=True, type=float)
    parser.add_argument("--sl",         required=True, type=float)
    parser.add_argument("--tp",         required=True, type=float)
    parser.add_argument("--strategy",   default="")
    parser.add_argument("--confidence", default=7, type=int)
    parser.add_argument("--dry-run",    action="store_true")
    args = parser.parse_args()

    ex       = get_exchange()
    pos_repo = PositionRepository()
    tr_repo  = TradeRepository()
    svc      = TradingService(ex, pos_repo, tr_repo)

    success, position, error = svc.open_position(
        symbol=args.symbol,
        side=args.side,
        entry=args.entry,
        sl=args.sl,
        tp=args.tp,
        strategy=args.strategy,
        confidence=args.confidence,
        dry_run=args.dry_run,
    )

    result = {
        "success":  success,
        "error":    error,
        "position": position.to_dict() if position else None,
    }
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
