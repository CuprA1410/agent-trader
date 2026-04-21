# Trading Fundamentals — Claude's Knowledge Base

*Pre-seeded knowledge. Claude adds to this over time.*

---

## 1. Market Structure

### Trend Identification
A market is in an **uptrend** when it makes Higher Highs (HH) and Higher Lows (HL).
A market is in a **downtrend** when it makes Lower Highs (LH) and Lower Lows (LL).
A market is **ranging** when highs and lows are at similar levels — price bounces between two zones.

**How to use it:**
- Only trade LONG in uptrends (buy the dips to HL)
- Only trade SHORT in downtrends (sell the rallies to LH)
- In ranges: trade the extremes (buy support, sell resistance) or wait for a breakout
- When structure is unclear → no trade

### Break of Structure (BOS)
A Break of Structure happens when price breaks a previous swing high (in an uptrend)
or a previous swing low (in a downtrend). This confirms the trend continues.

A **Change of Character (CHoCH)** happens when an uptrend breaks a previous HL
(or a downtrend breaks a previous LH). This signals a potential trend reversal.
Be cautious on the first CHoCH — wait for confirmation.

### Support and Resistance
**Support** = a price level where buyers historically stepped in. Price tends to bounce up.
**Resistance** = a price level where sellers historically stepped in. Price tends to bounce down.

Key rule: **old resistance becomes new support** after a breakout (and vice versa).

How to draw S/R:
- Look for areas where price spent time or repeatedly reversed
- Zones are more reliable than exact lines (price doesn't respect exact numbers)
- The more times a level has been tested, the more significant it is

---

## 2. Candlestick Patterns

### Reversal Candles (high significance)
- **Pin bar / Hammer**: long wick, small body. Shows rejection of a price level.
  - Bullish pin bar at support = strong long signal
  - Bearish pin bar at resistance = strong short signal
- **Engulfing candle**: current candle's body fully engulfs previous candle.
  - Bullish engulfing at support = buy signal
  - Bearish engulfing at resistance = sell signal
- **Doji**: open and close nearly equal. Shows indecision. Significant only at key levels.

### Continuation Candles
- **Strong bullish candle** (large green body, small wicks) = momentum is strong, trend likely continues
- **Strong bearish candle** (large red body, small wicks) = momentum is strong, trend likely continues
- **Inside bar**: current candle is entirely within previous candle's range. Signals consolidation before a move.

### What to look for
- Never trade a candlestick pattern in isolation
- Always combine with structure (is this pin bar AT support? or in the middle of nowhere?)
- Higher timeframe patterns are more significant than lower timeframe patterns

---

## 3. Key Indicators

### EMA (Exponential Moving Average)
EMAs show trend direction and act as dynamic support/resistance.

**Common EMAs:**
- EMA 20/21: short-term trend, used for scalping and swing entries
- EMA 50: medium-term trend
- EMA 200: long-term trend — the most important. Price above = bullish bias, below = bearish.

**How to use:**
- Price above EMA200 → prefer LONG trades
- Price below EMA200 → prefer SHORT trades
- EMA crossovers: EMA20 crosses above EMA50 = bullish momentum shift
- Price pulling back to EMA in an uptrend = potential LONG entry (buying the dip)

### RSI (Relative Strength Index) — period 14
Measures momentum. Range 0-100.
- Above 70 = overbought (momentum strong but may reverse soon)
- Below 30 = oversold (momentum weak but may reverse soon)
- 50 line = neutral. Above 50 = bullish momentum, below 50 = bearish momentum

**Most powerful RSI signals:**
- Divergence: price makes higher high but RSI makes lower high = bearish divergence (hidden weakness)
- Divergence: price makes lower low but RSI makes higher low = bullish divergence (hidden strength)
- RSI holding above 40 in an uptrend = trend still healthy

### MACD (Moving Average Convergence Divergence)
Shows momentum shifts. Made of MACD line, signal line, and histogram.
- MACD line crossing above signal line = bullish momentum
- MACD line crossing below signal line = bearish momentum
- Histogram growing = momentum increasing
- Histogram shrinking = momentum fading (possible reversal)
- MACD divergence = same as RSI divergence, very powerful

### Volume
**The most honest indicator.** Price moves on volume mean something. Price moves without volume are suspicious.

- High volume on breakout = real breakout, likely to continue
- Low volume on breakout = false breakout, likely to reverse
- High volume on reversal candle = strong rejection, likely reversal
- Declining volume in a trend = trend is weakening
- Volume spike after a long move = possible exhaustion/climax

**Always check volume before entering.** A setup with no volume confirmation is a lower quality trade.

### Bollinger Bands
Three lines: middle (EMA20) + upper and lower bands (2 standard deviations).
- Price touching upper band = overbought relative to recent range
- Price touching lower band = oversold relative to recent range
- **Band squeeze**: bands narrow = low volatility, big move coming soon
- Band expansion: bands widen = high volatility, trend in motion

---

## 4. Fibonacci Retracements

When price makes a significant move (swing low to swing high, or vice versa),
it often pulls back to specific Fibonacci levels before continuing.

**Key levels:**
- 0.236 (23.6%) — shallow retracement, strong trend
- 0.382 (38.2%) — common retracement in strong trends
- 0.5 (50%) — powerful level, not technically Fibonacci but very respected
- 0.618 (61.8%) — the "golden ratio", most important Fibonacci level
- 0.786 (78.6%) — deep retracement, still valid in strong trends

**How to draw:**
- In an uptrend: drag from swing LOW to swing HIGH. Look for price to pull back to fib levels and bounce.
- In a downtrend: drag from swing HIGH to swing LOW. Look for price to rally to fib levels and reject.

**Best entries:** look for fib level + S/R zone + reversal candle all at the same place.
This is called a "confluence zone" — when multiple things agree on a level, it's high probability.

---

## 5. Multi-Timeframe Analysis (MTF)

The golden rule: **always trade in the direction of the higher timeframe trend.**

### Top-Down Framework
```
1D (Daily)    → What is the big picture trend?
               → Are we near major S/R on the daily?
               → Avoid trading against this

4H            → What setup is forming?
               → Where are the 4H S/R levels?
               → Is there momentum on 4H?

1H            → Is the setup triggered?
               → Confirm momentum alignment
               → Identify precise entry zone

15m/5m        → Find the entry candle
               → Place SL just beyond the 15m structure
               → Enter with the best possible risk:reward
```

**Practical example:**
- 1D: BTC in uptrend, pulling back to 1D support
- 4H: forming a bullish engulfing at the 1D support level
- 1H: RSI bouncing from oversold, MACD crossing bullish
- 15m: pin bar forms at the 4H support zone
→ HIGH CONFIDENCE LONG — all timeframes agree

---

## 6. Risk Management

### The 1% Rule
Never risk more than 1% of your portfolio on any single trade.
On a $1000 portfolio: max loss per trade = $10.

This means you can lose 10 trades in a row and still have 90% of your capital.
10 losses in a row at 1% risk = -9.56% total (compounded).
This is survivable. 10 losses at 10% risk = -65% total. This is catastrophic.

### Stop Loss Placement
- Place SL beyond the nearest structural level (S/R, swing high/low)
- Never place SL at a round number (everyone else's SL is there too — you'll get hunted)
- SL should invalidate your trade idea. If price reaches SL, your thesis was wrong.
- Never move SL further away from entry to avoid being stopped out. This is how accounts blow up.

### Take Profit and R:R (Risk:Reward)
Minimum acceptable R:R = 1.5:1 (make $15 to risk $10)
Good trades: 2:1 or better
Excellent trades: 3:1 or better

Where to place TP:
- Next major resistance (for longs) or support (for shorts)
- Key Fibonacci extension level
- Round psychological number ($80,000, $3,000, $200, etc.)
- Never place TP in the middle of a range — put it AT the next level

### Partial Exits
On high conviction trades, consider taking partial profits:
- Take 50% at 1R (e.g. if risking $10, take $10 profit on half the position)
- Move SL to breakeven on the remaining 50%
- Let the rest run to 2R or 3R
This guarantees profit on the trade even if it eventually reverses.

---

## 7. Futures-Specific Knowledge

### Leverage
Leverage amplifies both gains and losses.
At 5x leverage:
- A 1% move in your favour = 5% profit on your margin
- A 1% move against you = 5% loss on your margin
- A 20% move against you = 100% loss on your margin (liquidation)

The SL distance matters more than the leverage. With proper SL placement and 1% risk,
leverage only affects how much margin is used, not how much you can lose.

### Liquidation Price
On futures, if price moves far enough against you, your position is liquidated
(forcibly closed at a loss equal to your entire margin).

Always calculate liquidation price before entering:
- At 5x leverage, you have a 20% buffer before liquidation
- Your SL should be much closer than your liquidation price
- If SL is beyond liquidation price, the exchange closes you before your SL — very bad

### Funding Rate
Perpetual futures contracts charge a funding rate every 8 hours.
- Positive funding = longs pay shorts (market is bullish, expensive to hold longs)
- Negative funding = shorts pay longs (market is bearish)
- Very high positive funding often precedes sharp corrections (longs are too crowded)
- Very high negative funding often precedes sharp bounces (shorts are too crowded)
Extreme funding rates are a contrarian signal — check them before entering.

### Long vs Short
- LONG: profit when price goes UP. Risk: price goes down.
- SHORT: profit when price goes DOWN. Risk: price goes up.
In a trending market, prefer trading WITH the trend:
- Uptrend → prefer LONG (buy dips to S/R)
- Downtrend → prefer SHORT (sell rallies to S/R)
Counter-trend trades (shorting in an uptrend) require higher conviction (confidence ≥ 8).

---

## 8. Market Psychology

### Why Levels Work
Round numbers ($80,000, $3,000, $100) attract orders because humans think in round numbers.
This makes them self-fulfilling — they work because everyone expects them to work.

### Fear and Greed
- **Extreme greed** (everyone is bullish, making money, crypto is all over news) → often near a top
- **Extreme fear** (everyone is selling, doom headlines, retail panic) → often near a bottom
Contrarian thinking: the best time to buy is when everyone is scared. The best time to be cautious is when everyone is greedy.

### Stop Hunts
Large players (whales, market makers) know where retail stop losses are clustered:
- Below obvious support levels
- Below round numbers
They sometimes push price through these levels to trigger stops, collect liquidity,
then reverse price sharply.

Recognition: a wick that pierces a key level then immediately reverses = possible stop hunt.
Strategy: place stops slightly beyond the obvious level, not exactly at it.

---

## 9. Common Mistakes to Avoid

1. **Overtrading** — taking every setup, even mediocre ones. Quality > quantity.
2. **Chasing price** — entering after a big move has already happened. FOMO is expensive.
3. **Moving your SL** — if you're stopped out, that's the trade. Don't move SL to avoid it.
4. **Revenge trading** — doubling down after a loss to "get it back". This destroys accounts.
5. **Ignoring the trend** — fighting the major trend on lower timeframes is low probability.
6. **No volume confirmation** — entering breakouts with no volume is entering false breakouts.
7. **Trading during major news** — earnings, Fed decisions, etc. cause unpredictable spikes.
8. **Overleveraging** — using high leverage with wide SLs. Always size by risk, not leverage.
9. **Not respecting confluence** — one signal is weak. Wait for 2-3 things to agree.
10. **Trading when tired or emotional** — machines don't get tired, but decision quality matters.
