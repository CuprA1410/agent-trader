"""
CLI wrapper for PortfolioService.get_live_positions()

Usage:
    python scripts/positions.py                  # all live positions
    python scripts/positions.py --symbol BTCUSDT # specific symbol
    python scripts/positions.py --tracked        # locally tracked positions
"""
from __future__ import annotations
import sys, json, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from exchanges.exchange_factory import get_exchange
from repositories.position_repository import PositionRepository
from services.portfolio_service import PortfolioService


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol",  default=None)
    parser.add_argument("--tracked", action="store_true",
                        help="Show locally tracked positions instead of live exchange data")
    args = parser.parse_args()

    if args.tracked:
        repo = PositionRepository()
        positions = repo.all()
        result = [p.to_dict() for p in positions]
    else:
        ex  = get_exchange()
        svc = PortfolioService(ex)
        syms = [args.symbol] if args.symbol else None
        positions = svc.get_live_positions(syms)
        result = [p.to_dict() for p in positions]

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
