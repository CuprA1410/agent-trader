# Exchange Quirks And Operating Manual

*This file is for platform behavior, not market analysis.*

---

## 1. Confirmed BitGet Demo Behaviors

### SL/TP parameter quirk

- `stopLossPrice` and `takeProfitPrice` failed with BitGet futures error `43011`
- `stopPrice` works and is the required parameter in this project

### Plan orders disappear

- Demo can silently delete SL and TP orders
- This has happened overnight and intraday
- Confirmed deletion window can be under 2 hours
- SOL TP has been especially fragile

### Cancel can remove both orders

- Cancelling one plan order can also remove the paired one
- After any cancel action, immediately verify both remaining SL and TP orders

### Local tracking can drift from exchange

- Local `data/positions.json` can become stale if trades are closed outside the expected path
- Exchange reality is authoritative

---

## 2. Operating Rules

### Before every cycle

- Verify all live exchange positions first
- Verify all SL and TP plan orders first
- Re-place any missing order before scanning for new setups

### While any position is open

- Review cadence must be 30-60 minutes
- 2-hour cadence is only acceptable when fully in cash

### After any manual cancel

- Re-query order state immediately
- Assume the other protective order may also have disappeared

### After any manual close

- Cancel any orphaned plan order
- Reconcile local positions
- Write the journal entry immediately

---

## 3. Known Safe Practices

### Entry flow

1. Place entry
2. Confirm fill
3. Place SL
4. Place TP
5. Confirm both exist
6. Save IDs locally

### Active trade flow

1. Check position still exists
2. Check SL still exists
3. Check TP still exists
4. If either is missing, re-place immediately
5. Update cycle log with status

### Exit flow

1. Close the position
2. Cancel leftover protective orders
3. Confirm position is flat on exchange
4. Update local files

---

## 4. Flash Close / Emergency Behavior

Use manual close logic when:

- SL is missing and price is already through the intended stop
- Macro invalidation triggers on confirmed close
- Exchange protective orders are unreliable in a fast move

Emergency priority:

1. Flatten risk
2. Cancel orphaned orders
3. Record what happened
4. Learn from it

---

## 5. Reconciliation Procedure

When local state and exchange disagree:

1. Trust live exchange positions, not local JSON
2. Clear or correct stale local tracked positions
3. Update `data/session_state.md`
4. Update `data/cycle_log.md`
5. Note the discrepancy here if it reveals a process weakness

---

## 6. Current Known Weak Spots

- Demo plan-order persistence is unreliable
- Protective orders close to current mark may disappear sooner
- Local tracking depends on discipline and can drift without reconciliation
- Exchange quirks can turn a valid setup into a larger-than-planned loss

---

## 7. Non-Negotiable Platform Rules

- Never assume a protective order still exists just because it was placed
- Never leave an open position unchecked for 2 hours on demo
- Never cancel one protective order without verifying the other still exists
- Never let exchange quirks stay buried inside trade lessons only
