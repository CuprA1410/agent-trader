"""
CLI wrapper for PortfolioService.summary()

Usage:
    python scripts/portfolio.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from exchanges.exchange_factory import get_exchange
from services.portfolio_service import PortfolioService
from config import cfg


def main():
    ex  = get_exchange()
    svc = PortfolioService(ex)
    data = svc.summary()
    data["portfolio_config_usd"] = cfg.portfolio_value_usd
    data["risk_per_trade_usd"]   = cfg.risk_amount_usd
    print(json.dumps(data, indent=2, default=str))


if __name__ == "__main__":
    main()
