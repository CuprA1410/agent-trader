# Lessons Learned — Claude's Trade Journal Insights

*Claude writes here after every closed trade and daily review.*
*This file is the most valuable knowledge asset — it contains real lessons from real trades.*

---

## How to Write a Lesson

Each lesson should be specific and actionable. Not:
> "I should be more careful next time"

But:
> "2026-04-18 | BTCUSDT SHORT | When BTC is within 2% of a major weekly resistance,
> shorting gives a very tight TP with high risk of reversal. Avoid shorting AT resistance —
> wait for a confirmed rejection candle, not just a touch."

---

## Lessons Log

### 2026-04-18 — Session 1 (First live trading day)

- **2026-04-18 | SETUP | BitGet SL/TP bug:** The `stopLossPrice` and `takeProfitPrice` params fail on BitGet futures with error 43011. Use `stopPrice` instead for both SL and TP orders. Fix applied to `trading_service.py`.

- **2026-04-18 | SIZING | Safety cap too aggressive:** The `max_notional = risk × leverage × 2 = $100` cap creates undersized positions when SL is tight. A $0.019 SL on XRP gives qty=526 (correct for 1% risk) but cap reduces to 69 XRP (~$1.30 actual risk instead of $10). Need to rethink cap formula — either raise multiplier or express cap as max margin, not notional.

- **2026-04-18 | ENTRY | Don't chase distribution shorts — wait for the relief rally:** XRP distributed at $1.51 with 11.2M vol (5.6× avg). Ideal short entry was $1.47–$1.48 right after the dump candle. By the time I analyzed it, price was at $1.432 and R:R was only 1:1. The relief rally to $1.45–$1.47 never came — sellers were too aggressive. Next time: if the bounce is too weak to reach resistance, enter the momentum short at current price with a tight SL above the post-dump high.

- **2026-04-18 | SIGNAL | Low-volume bounce = counter-trend, not reversal:** After BTC dropped to $75,763 (Fib 0.5), it bounced on only 93–225 volume (12–28% of avg 400–800). All 5 coins (BTC/ETH/SOL/XRP/BNB) bounced simultaneously on 8–15% of their average volume. This is a textbook low-conviction counter-trend bounce — hold shorts through it, don't panic-close.

- **2026-04-18 | MACRO | Synchronised pullback = market-wide signal:** When all coins pull back at the same time with the same distribution pattern (high-volume down candle followed by low-volume bounce), that's a macro signal, not coin-specific. In this case all 5 coins peaked within the same hour and distributed together. Macro shorts work best in this environment; longs should wait for BTC to show confirmed reversal with volume.

- **2026-04-18 | PROCESS | Always look for both LONG and SHORT setups:** First cycle only considered longs (waiting for support bounce). User correctly pointed out the short thesis was stronger given 1H momentum. From now on: score both directions for every coin every cycle.

### 2026-04-20 — BTC Breakdown Trade Closes (SOL/ETH/XRP SHORTs)

- **2026-04-20 | CRITICAL | BitGet demo silently deletes plan orders overnight:** SOL TP ($84.00) and ETH TP ($2285) both disappeared between Apr 19 16:46 UTC and Apr 20 09:15 UTC. ETH low was $2,281 (through TP) and SOL mark reached ~$83.50 (through TP) while orders were gone. This is a demo-specific bug. Fix: verify ALL plan orders at the VERY START of each cycle, before anything else. Re-place any missing TPs immediately. Do not assume orders persist.

- **2026-04-20 | CRITICAL | SOL TP specifically keeps disappearing:** SOL TP $84.00 disappeared 3 separate times in 24 hours. It must be treated as a fragile order and re-placed every cycle proactively. Probable cause: demo exchange auto-cancels TP orders that are very close to current mark price.

- **2026-04-20 | PATTERN | The triple shooting star at resistance is a very reliable SHORT signal:** BTC bars 13-15 all rejected $76,000-$76,215 with lower closes. All 3 SHORT positions (SOL/ETH/XRP) turned profitable after this pattern confirmed. When you see 3 consecutive failed breakouts at the same level with declining closes, the bear thesis is confirmed — add conviction and hold.

- **2026-04-20 | RISK | XRP trail SL cancel accidentally cancelled TP too:** When cancelling XRP SL (order 1429734989956149248) via cancel_plan_order API, it cancelled BOTH the SL and TP simultaneously. BitGet's cancel API can cancel multiple orders in one call. Always verify remaining orders immediately after any cancel. Re-place anything that disappeared.

- **2026-04-20 | MANAGEMENT | At 80%+ to TP, seriously consider manual close:** SOL reached 82% to TP at bar 07:00 low ($84.37) in Cycle 23 — didn't take profit. Then a $1,383 BTC counter-rally pushed SOL back above entry. We recovered, but the lesson stands: when unrealized P&L is at $15–20+ on a $10 risk, the remaining potential gain doesn't justify holding through a bounce. Consider partial close or manual TP at 80%+.

- **2026-04-20 | PROCESS | Mid-bar readings are not closes:** Cycle 27 recorded bar 15 closes based on mid-bar data (written 41 min into the bar). Final closes came in $127 higher on BTC, $0.40 higher on SOL. Trail and step-3 decisions that rely on "confirmed close" must only be made after the bar fully closes. Never treat a partial bar as a confirmed candle.

- **2026-04-20 | MACRO | BTC staircase down pattern works — trust the thesis:** The setup was: high-vol breakdown → low-vol dead-cat → confirmed close below trigger → acceleration. This played out exactly over Apr 18-20. BTC went from $76,000 to $74,063 while all 3 positions moved to profit. When the macro thesis is built on multiple confirmations (volume, pattern, level breaks), hold through the noise and let it work.

### 2026-04-20 — SOL SHORT Loss (Cycle 34-36)

- **2026-04-20 | EXIT RULE | Volume divergence is a warning, not a reversal signal:** In Cycle 35, BTC made a new high at $75,839 on lower volume and I held the position as a "divergence." The next bar CLOSED above $75,750, triggering exit. Volume divergence means conviction is weakening — it does not mean price will reverse. Price is the final arbiter. Apply exit rules mechanically on closes; treat divergence as a yellow flag only.

- **2026-04-20 | ENTRY | Worse fill = wider risk = smaller position needed:** Planned entry was $85.50 last price. Got filled at $84.761. Because entry was lower, the SL distance (to mark $86.00) increased from ~$1.10 to ~$1.84 per SOL. Should have sized DOWN from 10 SOL to 5-6 SOL to keep risk at 1%. Instead placed 9 SOL = 1.6% risk. When entry is significantly worse than planned, recalculate and reduce qty before placing the order.

- **2026-04-20 | DISCIPLINE | Rule-based exit at -$3.61 saved $13:** SL at mark $86.00 would have been a max loss of ~$16.55. By having a clear macro exit rule (BTC close above $75,750) and applying it immediately, we exited at -$3.61 instead. Having macro-level exit conditions independent of the SL adds a second layer of capital protection and forces regular re-evaluation of the trade thesis.

- **2026-04-20 | CONFIDENCE | 7/10 minimum threshold setups have lower follow-through:** All three winning trades (Apr 18-20) had 8-9/10 confluence. This SOL trade was entered at 7/10 — the minimum acceptable. The setup did form (double top, BTC rejection) but wasn't as clean or as high-conviction. Going forward: 7/10 = reduced size (5-6 SOL), 8/10 = full size (9-10 SOL).

### 2026-04-21 — BNB LONG Loss (Cycle 39-40)

- **2026-04-21 | CRITICAL | Demo SL orders get deleted within 2 hours — not just overnight:** The BNB LONG SL (mark $636) was placed at 16:07 and was gone by 18:07 — deleted in <2 hours. Previously we thought this was an overnight issue. It happens intraday too. **New rule: when an active position exists, verify plan orders every 30-60 minutes, not every 2 hours. The 2h cron is only safe when in cash.**

- **2026-04-21 | PATTERN | Bull trap: high vol entry bar → even higher vol reversal bar = failed breakout:** BNB entry bar (16:00-17:00) had 37,084 volume and pushed to $640.78. The NEXT bar (17:00-18:00) had 45,926 volume (24% MORE) and collapsed to $633.76. When a breakout bar is immediately followed by a bar with higher volume on the reversal, the breakout is a bull trap. This pattern retroactively reduces setup quality from 7/10 to 5/10.

- **2026-04-21 | SIZING | 1.25% risk on a 7/10 setup compounded the loss:** Entered 4 BNB (1.25% risk). Session CLAUDE.md says: 7/10 = reduced size. Should have been 3 BNB (1% exactly). In absolute terms -$3 extra. More importantly, the principle: never exceed 1% at minimum confidence.

- **2026-04-21 | INFRASTRUCTURE | Use 30-min cron when position is open, 2h when in cash:** The 2h loop fires at fixed odd hours. When in a trade, I cannot control when checks happen within that 2h window. Solution: after entering any position, programmatically check orders every 30 minutes until the position closes, then revert to 2h cadence.
