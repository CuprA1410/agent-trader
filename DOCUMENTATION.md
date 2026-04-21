# Agent Trader v3 — Full System Documentation

## Overview

Agent Trader v3 is an autonomous AI trading system where Agent is the brain.
Unlike traditional bots that use fixed coded strategies, Agent reads live TradingView
charts, interprets price action and indicators, makes trading decisions, and continuously
learns from every trade it makes.

The goal is a self-improving trading agent that gets better with every session.

---

## Core Philosophy

- **Agent is the trader** — not a rule executor. He reads charts like a human would.
- **Learning compounds** — every trade teaches something. Knowledge is never lost between sessions.
- **Risk first** — 1% portfolio risk per trade, always. Profits are variable. Losses are controlled.
- **No restrictions on coins** — Agent picks what to trade based on what the market offers.
- **Full autonomy** — no human confirmation needed. Agent executes, notifies, learns.

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  KNOWLEDGE BASE                      │
│  fundamentals.md  strategies.md  lessons.md          │
│  symbols.md       performance.md                     │
└───────────────────────┬─────────────────────────────┘
                        │ loaded at session start
                        ▼
┌─────────────────────────────────────────────────────┐
│                    Agent (brain)                    │
│                                                      │
│  1. Reads charts via TradingView MCP                 │
│  2. Draws on charts (S/R, trend lines, fib levels)   │
│  3. Scores confidence (1-10)                         │
│  4. Decides: trade, wait, skip                       │
│  5. Places orders via BitGet API                     │
│  6. Monitors positions                               │
│  7. Learns from every closed trade                   │
│  8. Sends Telegram notifications                     │
└────┬───────────────────────────┬────────────────────┘
     │                           │
     ▼                           ▼
┌─────────────┐         ┌────────────────┐
│ TradingView │         │ BitGet Futures │
│    MCP      │         │  (demo/live)   │
└─────────────┘         └────────────────┘
                                │
                                ▼
                    ┌────────────────────┐
                    │   Trade Journal    │
                    │  + Screenshots     │
                    │  + Drawings        │
                    └─────────┬──────────┘
                              │ daily review
                              ▼
                    ┌────────────────────┐
                    │  Knowledge Update  │
                    │  Lessons Learned   │
                    └────────────────────┘
```

---

## The Trading Loop

### Every Cycle (self-paced by Agent)

```
1. LOAD
   └─ Read all knowledge files
   └─ Check circuit breaker (portfolio down >10% today? → PAUSE)
   └─ Check open positions on BitGet

2. MARKET REGIME (1D + 4H on BTC as market leader)
   └─ Is crypto overall trending UP, DOWN, or RANGING?
   └─ This sets the bias for all coins this cycle

3. COIN SELECTION (pick 5 best opportunities)
   └─ Scan top coins by volume on TradingView
   └─ Look for coins with clear setups
   └─ Avoid coins with no clear structure

4. ANALYSIS (per coin, multi-timeframe)
   └─ 4H: trend direction, key S/R levels
   └─ 1H: setup formation
   └─ 15m or 5m: entry trigger
   └─ Score confidence 1-10

5. DECISION (per coin)
   └─ Confidence ≥ 7 AND no open position on this coin → TRADE
   └─ Confidence < 7 → SKIP (log reason)
   └─ Already have position → MONITOR only

6. EXECUTION (when trading)
   └─ Draw on chart: trend lines, S/R zones, fib levels, entry/SL/TP
   └─ Take screenshot (chart WITH all drawings)
   └─ Place order on BitGet with 1% risk sizing
   └─ Send Telegram notification

7. SELF-PACE
   └─ Scalping setup found → wait 5 min before next cycle
   └─ Day trade setup → wait 15-30 min
   └─ Quiet market → wait 60 min
   └─ Log reasoning for chosen interval
```

### Every 24 Hours (Learning Review)

```
1. Collect all trades closed in last 24h
2. For each closed trade:
   └─ Review the journal entry
   └─ Review the screenshot
   └─ What went right / wrong?
   └─ Write specific lesson to lessons.md
3. Update performance.md with new stats
4. Update symbols.md with any new coin behavior observations
5. Review strategies.md — are any strategies not working? note it
6. Send daily Telegram summary
```

---

## Risk Management Rules

| Parameter | Value |
|---|---|
| Risk per trade | 1% of portfolio ($10 on $1000) |
| Position sizing | `quantity = risk_amount / sl_distance` |
| Max open positions | 10 total |
| Max per coin | 1 |
| Daily drawdown limit | 10% → circuit breaker |
| Confidence threshold | ≥ 7/10 to trade |
| Leverage | 5x (adjustable) |

**Position sizing formula:**
```
risk_amount  = portfolio_value × 0.01        → $10
sl_distance  = abs(entry_price - sl_price)   → $ per unit
quantity     = risk_amount / sl_distance     → units to buy
notional     = quantity × entry_price        → total exposure
margin       = notional / leverage           → capital used
```

---

## Circuit Breaker

If total portfolio drops more than 10% in a 24h window:
1. All new trading stops immediately
2. Existing positions are NOT closed (let them play out)
3. Agent writes an analysis: what went wrong, what to do differently
4. Trading resumes the next calendar day
5. Telegram notification sent

---

## Journal System

Every closed trade generates:
- **Markdown file**: `data/journal/YYYY-MM-DD_HHMM_SYMBOL_SIDE_OUTCOME.md`
- **Screenshot**: `data/screenshots/SYMBOL_SIDE_ENTRY.png`

The screenshot is taken AFTER Agent draws on the chart:
- Trend lines connecting key highs/lows
- Support/resistance rectangles
- Fibonacci levels as horizontal lines (0.236, 0.382, 0.5, 0.618, 0.786)
- Entry price line
- Stop loss line
- Take profit line(s)
- Text labels explaining the setup

---

## Knowledge Base Files

| File | Purpose                               | Updated by                    |
|---|---------------------------------------|-------------------------------|
| `knowledge/fundamentals.md` | TA fundamentals, patterns, indicators | Pre-seeded (us) + Agent adds  |
| `knowledge/strategies.md` | Trading setups Agent uses             | Agent builds and refines      |
| `knowledge/lessons.md` | Specific lessons from real trades     | Agent after each closed trade |
| `knowledge/symbols.md` | How each coin behaves                 | Agent as it learns each coin |
| `knowledge/performance.md` | Stats, win rates, best conditions     | Agent updates daily          |
| `knowledge/checklists.md` | Pass/fail operating checklists        | Agent updates when process rules harden |
| `knowledge/regimes.md` | Consistent market-regime definitions   | Agent refines from live trading |
| `knowledge/exchange_quirks.md` | Exchange/platform operating rules | Agent updates after platform issues |
| `knowledge/mistakes.md` | Repeatable decision errors + counters | Agent updates when mistakes recur |

---

## Telegram Notifications

| Event | Message |
|---|---|
| Trade opened | Symbol, side, entry, SL, TP, confidence score, reasoning |
| Trade closed | Symbol, outcome (WIN/LOSS), P&L, portfolio total |
| Trade skipped | Symbol, reason, confidence score |
| Circuit breaker | Portfolio drop %, analysis summary |
| Daily summary | Trades today, P&L, win rate, market observations, lessons |

---

## Backtesting / Practice Mode

Agent can replay historical charts on TradingView to practice reading setups
without placing real orders. This is used to:
- Learn a new coin's behavior
- Test a new strategy idea before using real demo money
- Rebuild confidence after a losing streak

To activate: Agent sets `practice_mode = true` for a cycle and logs observations
to `knowledge/strategies.md` instead of placing trades.

---

## Multi-Timeframe Framework

```
1D  → Market bias (bull/bear/sideways)
      "Is the overall trend in my favour?"

4H  → Structure and key levels
      "Where are the major support/resistance zones?"
      "Is a setup forming?"

1H  → Setup confirmation
      "Is price behaving as expected at these levels?"
      "Is momentum aligned?"

15m → Entry timing (day trades)
 5m → Entry timing (scalps)
      "Where exactly do I enter with the tightest SL?"
```

Agent always works top-down. Never enter on 5m without checking 1H and 4H first.

---

## Exchange Abstraction

The system uses ccxt which supports 100+ exchanges. To switch exchange:
```env
EXCHANGE=bitget          # or binance, bybit, okx, etc.
EXCHANGE_DEMO=true       # demo/sandbox mode
TRADE_MODE=futures       # spot | futures | margin
FUTURES_LEVERAGE=5
```

---

## Configuration (.env)

```env
# Anthropic
ANTHROPIC_API_KEY=

# Exchange
EXCHANGE=bitget
EXCHANGE_API_KEY=
EXCHANGE_SECRET_KEY=
EXCHANGE_PASSPHRASE=
EXCHANGE_DEMO=true
TRADE_MODE=futures
FUTURES_LEVERAGE=5

# Portfolio
PORTFOLIO_VALUE_USD=1000
RISK_PCT=0.01
MAX_POSITIONS=10
DRAWDOWN_LIMIT_PCT=0.10

# Telegram
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Storage
LOG_DIR=data
```

---

## Project File Structure

```
claude-trader-v3/
├── AGENTS.md                  ← Agent identity, mission, workflow, and operating rules
├── CLAUDE.md                  ← parallel instruction file used in earlier sessions
├── DOCUMENTATION.md           ← this file
├── config.py                  ← env-backed configuration
├── main.py                    ← setup / connectivity check entry point
├── requirements.txt
├── .env / .env.example
├── .mcp.json                  ← project MCP config
├── knowledge/
│   ├── fundamentals.md
│   ├── strategies.md
│   ├── lessons.md
│   ├── symbols.md
│   ├── performance.md
│   ├── checklists.md
│   ├── regimes.md
│   ├── exchange_quirks.md
│   └── mistakes.md
├── services/
│   ├── trading_service.py
│   ├── portfolio_service.py
│   ├── position_monitor.py
│   └── notification_service.py
├── exchanges/
│   └── exchange_factory.py
├── models/
│   ├── trade.py
│   └── position.py
├── repositories/
│   ├── position_repository.py
│   └── trade_repository.py
├── utils/
│   ├── circuit_breaker.py
│   └── knowledge_manager.py
├── scripts/
│   ├── positions.py
│   ├── place_order.py
│   ├── close_position.py
│   ├── fix_sl_tp.py
│   ├── journal.py
│   ├── portfolio.py
│   ├── telegram.py
│   ├── notify_trade.py
│   ├── notify_eth.py
│   ├── save_position.py
│   └── cb_status.py
└── data/
    ├── cycle_log.md
    ├── session_state.md
    ├── positions.json
    ├── circuit_breaker.json
    └── journal/
        └── trades.csv
```

---

## Setup Guide (Local)

### Prerequisites
- Python 3.11+
- Agent CLI installed (`npm install -g @anthropic-ai/Agent-code`)
- Google Chrome available on this machine
- TradingView opened in Chrome with CDP on port `9222`
- Codex / Claude configured with the TradingView MCP server

### First Run
```bash
# 1. Clone / create project
cd E:\Projects\claude-trader-v3

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy and fill .env
copy .env.example .env

# 4. Run setup / connectivity check
python main.py
```

### TradingView Setup On This Machine

This project does **not** use TradingView Desktop on this machine.
The working path is Chrome CDP.

Launch Chrome like this:

```powershell
Start-Process 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe' -ArgumentList '--remote-debugging-port=9222 --user-data-dir=C:\Users\popes\AppData\Local\Google\Chrome\CDP https://www.tradingview.com/chart/'
```

Then verify the MCP connection with:

```text
tv_health_check
```

Success criteria:

- `success: true`
- `cdp_connected: true`
- `api_available: true`

### What `main.py` Actually Does

`main.py` is a setup and connectivity check, not the autonomous trading loop itself.

When you run `python main.py`, it:

1. Loads config
2. Checks circuit-breaker state
3. Connects to BitGet through ccxt
4. Prints balance and live open positions
5. Verifies the core knowledge files exist
6. Optionally sends a Telegram test message with `--test`

The actual trading cycle is driven by the agent workflow in `AGENTS.md` together with TradingView MCP and the helper scripts/services in this repo.

---

## Roadmap

### Done

- [x] Architecture design
- [x] Documentation
- [x] Knowledge base (pre-seeded and extended with operating files)
- [x] Core services implementation
- [x] BitGet order execution
- [x] Telegram notifications
- [x] Circuit breaker

### Partial

- [~] TradingView chart drawing + screenshot
  TradingView MCP is connected and usable, but this is driven through the agent workflow rather than a dedicated Python chart service in the repo.

- [~] Daily learning review
  The process exists in `AGENTS.md` and the knowledge files are actively updated, but there is no dedicated automated `daily_reviewer.py` implementation.

- [~] Backtesting practice mode
  The operating concept exists and TradingView replay can support it, but there is no dedicated repo implementation that orchestrates it end to end.

### Not Done

- [ ] Deploy to VPS (after local testing)
