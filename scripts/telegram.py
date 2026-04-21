"""
Usage:
    python scripts/telegram.py --message "🟢 LONG BTCUSDT opened"
    python scripts/telegram.py --message "..." --parse-mode HTML

Sends a Telegram message to the configured chat.
"""
from __future__ import annotations
import sys, json, argparse, requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import cfg


def send_message(text: str, parse_mode: str = "Markdown") -> dict:
    if not cfg.telegram_bot_token or not cfg.telegram_chat_id:
        return {"status": "SKIPPED", "reason": "No Telegram credentials configured"}

    url = f"https://api.telegram.org/bot{cfg.telegram_bot_token}/sendMessage"
    payload = {
        "chat_id":    cfg.telegram_chat_id,
        "text":       text,
        "parse_mode": parse_mode,
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        data = resp.json()
        if data.get("ok"):
            return {"status": "SENT", "message_id": data["result"]["message_id"]}
        else:
            return {"status": "ERROR", "detail": data}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--message",    required=True)
    parser.add_argument("--parse-mode", default="Markdown")
    args = parser.parse_args()

    result = send_message(args.message, args.parse_mode)
    print(json.dumps(result, indent=2))
