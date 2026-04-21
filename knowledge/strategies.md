# Strategy Library

*This file should describe the setups actually being traded, not generic labels that sound good.*

---

## Strategy 1: BTC Breakdown Continuation SHORT

**Status:** Live-tested  
**Type:** Intraday continuation  
**Bias:** With macro weakness

### Setup

BTC prints a high-volume breakdown from a key level, then the bounce is weak or low volume.
Alts show relative weakness and fail to reclaim supply.

### Entry Conditions

- BTC breaks a meaningful support level on volume
- Bounce after the breakdown is weak, low-volume, or both
- BTC confirms with a close below the trigger level
- ETH, SOL, or XRP lag during the bounce
- Entry is on the relief rally into resistance or on failed reclaim

### Stop Loss

- Above the failed reclaim level
- Or above the relief-rally swing high

### Take Profit

- Next major support on the alt
- Manual management allowed at 80%+ of TP move

### Notes

- This is the clearest winning pattern in the current history
- Do not confuse a low-volume bounce with a true reversal
- Confirmed closes matter more than intrabar drama

---

## Strategy 2: Supply Zone Rejection SHORT

**Status:** Emerging  
**Type:** Intraday reversal from supply  
**Bias:** Prefer with BTC weakness or failed reclaim

### Setup

Price bounces into a well-defined supply zone and gets rejected with a bearish close.
Best version is when the rejection prints on high volume.

### Entry Conditions

- Supply zone is clear on 4H or 1H
- Price trades into the zone, not below it in the middle of nowhere
- Bearish rejection candle forms at the zone
- Volume expands on the rejection bar
- BTC is not actively reclaiming higher at the same time

### Stop Loss

- Above the top of the supply zone

### Take Profit

- Prior flush low
- Next major support

### Notes

- ETH is currently the best candidate for this setup
- If BTC is bouncing hard while the rejection is forming, downgrade confidence

---

## Strategy 3: Trend Pullback LONG

**Status:** Lightly tested, needs cleaner samples  
**Type:** Trend continuation  
**Bias:** With higher-timeframe uptrend only

### Setup

BTC or an alt is in a clean uptrend, pulls back into support, and holds that zone.
The long is taken on the bounce from the level, not after the move is already running.

### Entry Conditions

- 4H uptrend is clean
- Pullback reaches a real support zone, not just a random mid-range price
- 1H confirms hold or reclaim
- Volume on the pullback is not impulsively bearish
- Entry is near the support zone with defined invalidation

### Stop Loss

- Below support / below the pullback low

### Take Profit

- Prior swing high
- Next resistance

### Notes

- The failed BNB long is a reminder that breakout energy must survive the next bar
- If the first full bar after entry reverses on higher volume, reassess immediately

---

## Strategy 4: Breakout Retest LONG

**Status:** Not validated yet  
**Type:** Breakout continuation  
**Bias:** Only in supportive macro

### Setup

A resistance level breaks on strong volume, then price retests the broken level and holds.

### Entry Conditions

- Resistance tested multiple times before break
- Breakout bar closes clean above the level
- Volume is meaningfully above average
- Retest holds the broken level
- Rejection candle forms at the retest

### Stop Loss

- Below the reclaimed level

### Take Profit

- Next resistance
- Measured move if structure is clean

### Notes

- Do not buy the initial breakout candle just because it looks strong
- The retest is the preferred entry
- If reversal volume exceeds breakout volume on the next bar, treat as probable bull trap

---

## Strategy 5: Range Extreme Reversal

**Status:** Not tested  
**Type:** Mean reversion  
**Bias:** Neutral, only in confirmed chop

### Setup

BTC or the coin is clearly range-bound and price reaches an extreme with rejection.

### Entry Conditions

- Range boundaries are obvious
- Price is trading at the edge, not in the middle
- Rejection candle forms at the extreme
- R:R is still at least 2:1

### Stop Loss

- Outside the range boundary

### Take Profit

- Opposite side of range or midpoint if conditions are poor

### Notes

- This setup is inferior to continuation setups in the current sample
- Skip if breakout risk is high or macro is shifting

---

## Naming Rules

Use these names in logs and journals:

- `BTC Breakdown Continuation SHORT`
- `Supply Zone Rejection SHORT`
- `Trend Pullback LONG`
- `Breakout Retest LONG`
- `Range Extreme Reversal`

Do not log trades under vague names like `Trend Pullback EMA` unless the EMA itself was central to the setup.

---

## Strategy Rating Tracker

| Strategy | Trades | Win Rate | Confidence | Notes |
|---|---|---|---|---|
| BTC Breakdown Continuation SHORT | 4 | 75% | Highest so far | Current best real edge |
| Supply Zone Rejection SHORT | 0 | - | Promising | ETH watch candidate |
| Trend Pullback LONG | 1 | 0% | Unclear | BNB sample failed, not enough data |
| Breakout Retest LONG | 0 | - | Unproven | Keep selective |
| Range Extreme Reversal | 0 | - | Unproven | Only trade with clear boundaries |
