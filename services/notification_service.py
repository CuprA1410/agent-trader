"""
Notification service — Telegram.
Uses the Facade pattern to hide API details from callers.
"""
from __future__ import annotations
import requests
import logging

from config import cfg
from models.trade import Trade
from models.position import Position

log = logging.getLogger(__name__)


class NotificationService:
    """Sends Telegram messages. Silently no-ops if credentials are missing."""

    BASE_URL = "https://api.telegram.org/bot{token}/sendMessage"

    def __init__(self):
        self._token   = cfg.telegram_bot_token
        self._chat_id = cfg.telegram_chat_id
        self._enabled = bool(self._token and self._chat_id)

    # ── Public API ─────────────────────────────────────────────────────────────

    def trade_opened(self, position: Position) -> bool:
        emoji = "🟢" if position.is_long else "🔴"
        direction = "LONG" if position.is_long else "SHORT"
        text = (
            f"{emoji} *{direction} {position.symbol} opened*\n"
            f"Entry: `${position.entry_price:,.4f}` | "
            f"SL: `${position.sl_price:,.4f}` | "
            f"TP: `${position.tp_price:,.4f}`\n"
            f"Confidence: {position.confidence}/10\n"
            f"Risk: `${cfg.risk_amount_usd:.2f}` (1%)\n"
            f"Setup: _{position.strategy}_"
        )
        return self.send(text)

    def trade_closed(self, trade: Trade) -> bool:
        emoji = "✅" if trade.outcome == "WIN" else "❌"
        text = (
            f"{emoji} *{trade.symbol} {trade.side.upper()} closed — {trade.outcome}*\n"
            f"Entry: `${trade.entry:,.4f}` → Exit: `${trade.exit:,.4f}`\n"
            f"P&L: `${trade.pnl_usd:+.2f}` ({trade.pnl_pct:+.2f}%) "
            f"| {trade.r_multiple:+.1f}R\n"
            f"Strategy: _{trade.strategy}_"
        )
        return self.send(text)

    def daily_summary(
        self,
        date_str: str,
        stats: dict,
        portfolio: float,
        regime: str = "",
        lesson: str = "",
    ) -> bool:
        pnl      = stats.get("total_pnl", 0)
        pnl_pct  = round((pnl / portfolio) * 100, 2) if portfolio else 0
        win_rate = stats.get("win_rate", 0)
        trades   = stats.get("trades", 0)
        wins     = stats.get("wins", 0)
        losses   = stats.get("losses", 0)

        text = (
            f"📊 *Daily Summary — {date_str}*\n"
            f"Trades: {trades} ({wins} wins, {losses} losses)\n"
            f"P&L: `${pnl:+.2f}` ({pnl_pct:+.2f}%)\n"
            f"Portfolio: `${portfolio:,.2f}`\n"
            f"Win rate: {win_rate:.1f}%\n"
        )
        if regime:
            text += f"Market: _{regime}_\n"
        if lesson:
            text += f"Key lesson: _{lesson}_"
        return self.send(text)

    def alert(self, message: str) -> bool:
        return self.send(f"⚠️ *ALERT*\n{message}")

    def circuit_breaker(self, pnl_usd: float, pnl_pct: float, analysis: str = "") -> bool:
        text = (
            f"🛑 *CIRCUIT BREAKER TRIGGERED*\n"
            f"Daily loss: `${pnl_usd:+.2f}` ({pnl_pct:+.2f}%)\n"
            f"Trading paused until tomorrow.\n"
        )
        if analysis:
            text += f"\nAnalysis: _{analysis}_"
        return self.send(text)

    def send(self, text: str, parse_mode: str = "Markdown") -> bool:
        if not self._enabled:
            log.debug("Telegram not configured — skipping notification")
            return False
        url = self.BASE_URL.format(token=self._token)
        try:
            resp = requests.post(
                url,
                json={"chat_id": self._chat_id, "text": text, "parse_mode": parse_mode},
                timeout=10,
            )
            data = resp.json()
            if not data.get("ok"):
                log.warning(f"Telegram error: {data}")
                return False
            return True
        except Exception as e:
            log.warning(f"Telegram send failed: {e}")
            return False
