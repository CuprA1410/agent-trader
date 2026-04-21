"""
Claude Trader v3 — Entry Point

This file is a quick diagnostic / setup verifier.
The actual trading loop runs inside Claude Code using CLAUDE.md as instructions.

Usage:
    python main.py           # verify setup, show portfolio, open positions
    python main.py --test    # also send a Telegram test message
"""
from __future__ import annotations
import sys, json, argparse, io
from pathlib import Path

# Fix Windows console encoding for unicode output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent))

from config import cfg
from utils.circuit_breaker import CircuitBreaker


def main():
    parser = argparse.ArgumentParser(description="Claude Trader v3 setup check")
    parser.add_argument("--test", action="store_true", help="Send Telegram test message")
    args = parser.parse_args()

    print("=" * 60)
    print("  Claude Trader v3 — Setup Check")
    print("=" * 60)

    # Config
    print(f"\n📋 Config")
    print(f"   Exchange:        {cfg.exchange} ({'DEMO' if cfg.exchange_demo else 'LIVE'})")
    print(f"   Trade mode:      {cfg.trade_mode}")
    print(f"   Leverage:        {cfg.futures_leverage}x")
    print(f"   Portfolio:       ${cfg.portfolio_value_usd:,.2f}")
    print(f"   Risk per trade:  ${cfg.risk_amount_usd:.2f} ({cfg.risk_pct*100:.1f}%)")
    print(f"   Max positions:   {cfg.max_positions}")
    print(f"   Circuit breaker: {cfg.drawdown_limit_pct*100:.0f}% daily drawdown")

    # Circuit breaker
    cb = CircuitBreaker()
    status = cb.status()
    print(f"\n🔴 Circuit Breaker")
    print(f"   Today's P&L:   ${status['daily_pnl']:+.2f} ({status['daily_pnl_pct']:+.2f}%)")
    print(f"   Triggered:     {'YES ⚠️' if status['triggered'] else 'No'}")

    # Exchange connectivity
    print(f"\n🔌 Exchange Connectivity")
    try:
        from exchanges.exchange_factory import get_exchange
        from services.portfolio_service import PortfolioService
        ex      = get_exchange()
        svc     = PortfolioService(ex)
        summary = svc.summary()
        print(f"   ✅ Connected to {cfg.exchange}")
        b = summary["balance"]
        print(f"   Balance:       ${b['total']:,.2f} USDT (free: ${b['free']:,.2f})")
        print(f"   Open positions: {summary['open_positions_count']}")
        for p in summary["open_positions"]:
            pnl = p.get("unrealised_pnl") or 0
            print(f"     • {p['symbol']} {p['side'].upper()} "
                  f"× {p.get('quantity')} @ {p.get('entry_price')} | PnL: ${float(pnl):+.2f}")
    except Exception as e:
        print(f"   ❌ Exchange error: {e}")

    # Telegram
    if args.test:
        print(f"\n📱 Telegram Test")
        try:
            from services.notification_service import NotificationService
            notifier = NotificationService()
            ok = notifier.send("✅ *Claude Trader v3* is online and connected\\!")
            print(f"   {'✅ Message sent' if ok else '❌ Send failed'}")
        except Exception as e:
            print(f"   ❌ Telegram error: {e}")

    # Knowledge files
    print(f"\n📚 Knowledge Files")
    kdir = Path("knowledge")
    for fname in ["fundamentals.md", "strategies.md", "lessons.md", "symbols.md", "performance.md"]:
        fpath = kdir / fname
        exists = "✅" if fpath.exists() else "❌"
        size   = f"({fpath.stat().st_size:,} bytes)" if fpath.exists() else ""
        print(f"   {exists} {fname} {size}")

    print(f"\n{'='*60}")
    print(f"  Setup check complete. Claude Trader v3 is ready.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
