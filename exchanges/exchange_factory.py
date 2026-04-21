from __future__ import annotations
import ccxt
from config import cfg


def get_exchange() -> ccxt.Exchange:
    """Return a configured ccxt exchange instance."""
    exchange_id = cfg.exchange.lower()

    params: dict = {
        "apiKey":    cfg.exchange_api_key,
        "secret":    cfg.exchange_secret,
        "enableRateLimit": True,
    }
    if cfg.exchange_passphrase:
        params["password"] = cfg.exchange_passphrase

    exchange_cls = getattr(ccxt, exchange_id)
    exchange: ccxt.Exchange = exchange_cls(params)

    # Demo / sandbox
    if cfg.exchange_demo:
        if hasattr(exchange, "set_sandbox_mode"):
            exchange.set_sandbox_mode(True)
        else:
            exchange.urls["api"] = exchange.urls.get("test", exchange.urls["api"])

    exchange.load_markets()
    return exchange
