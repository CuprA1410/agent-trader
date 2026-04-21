# Trading Checklists

*Use these as pass/fail gates. If a required box fails, skip the trade.*

---

## 1. Cycle Start Checklist

Run this before scanning for new trades.

- [ ] Read the last 3-5 entries in `data/cycle_log.md`
- [ ] Read `knowledge/lessons.md`
- [ ] Read `knowledge/symbols.md`
- [ ] Read `knowledge/performance.md`
- [ ] Read `data/session_state.md`
- [ ] Check circuit breaker status
- [ ] Check live BitGet positions with `python scripts/positions.py`
- [ ] If any local tracked positions exist, reconcile them with exchange reality
- [ ] If any live position exists, verify SL and TP plan orders before doing anything else
- [ ] Run TradingView `tv_health_check` and confirm `api_available: true`

If any open position exists:

- [ ] Verify every symbol has both SL and TP in place
- [ ] Re-place any missing plan order immediately
- [ ] Set next review cadence to 30-60 minutes, not 2 hours

---

## 2. Macro Regime Checklist

Use BTC first. No alt trade without BTC context.

- [ ] 1D structure classified: uptrend / downtrend / range
- [ ] 4H structure classified: uptrend / downtrend / range
- [ ] 1H momentum classified: expanding / fading / choppy
- [ ] Key BTC levels marked on chart
- [ ] Current regime chosen from `knowledge/regimes.md`

Hard fail:

- [ ] If BTC regime is unclear, do not take an alt trade based on a weak standalone signal

---

## 3. Setup Qualification Checklist

Every candidate trade must pass these filters.

- [ ] Trade is with the higher-timeframe bias, or has explicit counter-trend justification
- [ ] 4H level or zone is clear
- [ ] 1H confirms the thesis
- [ ] Entry is at a level or on a retest, not in the middle of nowhere
- [ ] Entry is not a chase after the move already happened
- [ ] Volume supports the thesis
- [ ] R:R is at least 2:1
- [ ] Stop loss is beyond structure, not arbitrary
- [ ] Take profit is at a real target level
- [ ] Setup quality is genuinely 7/10 or better

Current operating rule:

- [ ] If the session state says confidence bar is raised to 8/10, 7/10 setups are auto-skip

Hard fail:

- [ ] Do not enter if the bar used for confirmation has not closed
- [ ] Do not enter if BTC is actively invalidating the setup during evaluation
- [ ] Do not enter if volume confirmation is missing

---

## 4. Entry Execution Checklist

Only run this after the setup qualifies.

- [ ] Chart drawings completed before screenshot
- [ ] Screenshot taken with analysis visible
- [ ] Position size recalculated from actual planned entry and SL distance
- [ ] If fill is materially different from planned entry, resize before sending
- [ ] 7/10 setup = reduced size only
- [ ] 8/10+ setup = full size allowed, but still max 1% risk
- [ ] Max positions not exceeded
- [ ] No open position already exists in the same coin
- [ ] Telegram message prepared

Order integrity:

- [ ] Entry order placed successfully
- [ ] SL placed successfully
- [ ] TP placed successfully
- [ ] Order IDs recorded
- [ ] Position saved locally
- [ ] Telegram sent

Hard fail:

- [ ] Never leave a live position without immediately checking that SL and TP both exist

---

## 5. Active Position Checklist

Run this every review cycle while in a trade.

- [ ] Position still exists on exchange
- [ ] SL still exists
- [ ] TP still exists
- [ ] No cancel action accidentally removed the opposite plan order
- [ ] Current price vs thesis reviewed
- [ ] BTC macro still supports the trade
- [ ] Progress to TP measured
- [ ] If trade reached 80%+ to TP, consider manual management

Pattern danger checks:

- [ ] If breakout entry is followed by opposite-direction bar with higher volume, downgrade the setup immediately
- [ ] If a macro invalidation rule triggered on a confirmed close, exit without debate
- [ ] Treat divergence as a warning only, not as a reason by itself to stay in a broken trade

---

## 6. Exit Checklist

When closing a position manually or after detecting exchange closure:

- [ ] Confirm actual exit reason: TP / SL / manual / invalidation
- [ ] Record exit price from exchange if possible
- [ ] Cancel orphaned plan orders if needed
- [ ] Write the trade immediately with `scripts/journal.py write`
- [ ] Update `data/session_state.md`
- [ ] Update `data/cycle_log.md`
- [ ] Send Telegram close notification
- [ ] Record lesson if the trade taught anything specific

If the trade was wrong because of execution, not analysis:

- [ ] Record it in `knowledge/mistakes.md`
- [ ] Record the platform behavior in `knowledge/exchange_quirks.md`

---

## 7. Auto-Skip Conditions

Skip without negotiation if any of these are true:

- [ ] BTC regime is unclear or choppy and the setup depends on BTC continuation
- [ ] Setup relies on an unclosed candle
- [ ] R:R is below 2:1
- [ ] Entry is a chase, not a level-based entry
- [ ] Confidence is 7/10 during a raised-confidence session
- [ ] Both sides of the market have not been considered
- [ ] Plan-order integrity cannot be verified on an open position
- [ ] You are trying to trade because the market is active, not because the setup is clear
