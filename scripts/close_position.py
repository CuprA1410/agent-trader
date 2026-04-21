"""
CLI wrapper for TradingService.close_position()

Usage:
    python scripts/close_position.py --symbol BTCUSDT --exit 86400
    python scripts/close_position.py --symbol BTCUSDT --exit 83100 --reason "Manual stop"
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
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--exit",   required=True, type=float)
    parser.add_argument("--reason", default="Manual close")
    args = parser.parse_args()

    ex       = get_exchange()
    pos_repo = PositionRepository()
    tr_repo  = TradeRepository()
    svc      = TradingService(ex, pos_repo, tr_repo)

    success, trade, error = svc.close_position(
        symbol=args.symbol,
        exit_price=args.exit,
        reason=args.reason,
    )

    result = {
        "success": success,
        "error":   error,
        "trade":   trade.to_dict() if trade else None,
    }
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
