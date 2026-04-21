"""
CLI wrapper for TradeRepository

Usage:
    python scripts/journal.py write \
        --symbol BTCUSDT --side long \
        --entry 84200 --exit 86400 \
        --quantity 0.012 --pnl 26.40 --outcome WIN \
        --strategy "S/R Breakout" --confidence 8 \
        --notes "Clean breakout above 4H resistance"

    python scripts/journal.py list         # last 10 trades
    python scripts/journal.py stats        # overall stats
    python scripts/journal.py stats-today  # today's stats
"""
from __future__ import annotations
import sys, json, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from models.trade import Trade
from repositories.trade_repository import TradeRepository


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    w = sub.add_parser("write")
    w.add_argument("--symbol",     required=True)
    w.add_argument("--side",       required=True)
    w.add_argument("--entry",      required=True, type=float)
    w.add_argument("--exit",       required=True, type=float)
    w.add_argument("--quantity",   required=True, type=float)
    w.add_argument("--pnl",        required=True, type=float)
    w.add_argument("--outcome",    required=True)
    w.add_argument("--strategy",   default="")
    w.add_argument("--confidence", default=0, type=int)
    w.add_argument("--screenshot", default="")
    w.add_argument("--notes",      default="")

    sub.add_parser("list")
    sub.add_parser("stats")
    sub.add_parser("stats-today")

    args = parser.parse_args()
    repo = TradeRepository()

    if args.cmd == "write":
        trade = Trade(
            symbol=args.symbol,
            side=args.side,
            entry=args.entry,
            exit=args.exit,
            quantity=args.quantity,
            pnl_usd=args.pnl,
            outcome=args.outcome.upper(),
            strategy=args.strategy,
            confidence=args.confidence,
            screenshot=args.screenshot,
            notes=args.notes,
        )
        repo.save(trade)
        result = {"status": "WRITTEN", "trade": trade.to_dict()}

    elif args.cmd == "list":
        result = [t.to_dict() for t in repo.recent(10)]

    elif args.cmd == "stats":
        result = repo.stats()

    elif args.cmd == "stats-today":
        result = repo.stats_today()

    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
