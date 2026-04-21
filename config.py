from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")


class Config:
    # Anthropic
    anthropic_api_key: str = os.environ["ANTHROPIC_API_KEY"]

    # Exchange
    exchange: str          = os.getenv("EXCHANGE", "bitget")
    exchange_api_key: str  = os.environ["EXCHANGE_API_KEY"]
    exchange_secret: str   = os.environ["EXCHANGE_SECRET_KEY"]
    exchange_passphrase: str = os.getenv("EXCHANGE_PASSPHRASE", "")
    exchange_demo: bool    = os.getenv("EXCHANGE_DEMO", "true").lower() == "true"
    trade_mode: str        = os.getenv("TRADE_MODE", "futures")   # "futures" | "spot"
    futures_leverage: int  = int(os.getenv("FUTURES_LEVERAGE", "5"))

    # Portfolio & Risk
    portfolio_value_usd: float = float(os.getenv("PORTFOLIO_VALUE_USD", "1000"))
    risk_pct: float            = float(os.getenv("RISK_PCT", "0.01"))
    max_positions: int         = int(os.getenv("MAX_POSITIONS", "10"))
    drawdown_limit_pct: float  = float(os.getenv("DRAWDOWN_LIMIT_PCT", "0.10"))

    # Telegram
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str   = os.getenv("TELEGRAM_CHAT_ID", "")

    # Storage
    log_dir: Path = Path(os.getenv("LOG_DIR", "data"))

    @property
    def is_futures(self) -> bool:
        return self.trade_mode.lower() == "futures"

    @property
    def risk_amount_usd(self) -> float:
        return self.portfolio_value_usd * self.risk_pct


cfg = Config()
