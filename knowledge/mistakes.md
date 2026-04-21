# Mistakes Log

*Lessons are observations. Mistakes are decisions that were wrong in hindsight and now have a rule attached.*

---

## How To Use This File

Use `mistakes.md` as the active incident log for repeatable decision errors.

### Rules

1. One mistake pattern = one entry.
   Do not create duplicate entries for the same mistake type.

2. If the same mistake happens again, update the existing entry:
   - increase the `Count`
   - update `Last seen`
   - add the latest example in `Examples`
   - tighten the rule if needed

3. Only create a new mistake entry when:
   - the decision was actually wrong, not just unlucky
   - it produced a concrete behavioral rule

4. Promote repeated mistakes into `knowledge/checklists.md`.
   If a mistake pattern happens **2 times or more**, add or strengthen a checklist rule so it is enforced every cycle.

5. Keep this file short.
   This is not a trade diary. It is a compact list of recurring failure patterns.

### Relationship To Other Files

- `mistakes.md` = what went wrong in decisions
- `checklists.md` = how future behavior is enforced
- `lessons.md` = broader market insight, whether or not a mistake was involved

---

## Active Mistakes

### Mistake: Worse fill without resizing

- **Count:** 1
- **First seen:** 2026-04-20
- **Last seen:** 2026-04-20
- **Rule:** If entry is materially different from plan, recalculate quantity before sending the order.
- **Checklist status:** Added
- **Examples:**
  - 2026-04-20 | SOLUSDT SHORT | Accepted a materially worse fill and did not resize down.

### Mistake: Using an unclosed bar as confirmation

- **Count:** 1
- **First seen:** 2026-04-20
- **Last seen:** 2026-04-20
- **Rule:** No thesis confirmation or invalidation is allowed from an unclosed bar.
- **Checklist status:** Added
- **Examples:**
  - 2026-04-20 | BTC/SOL management | Treated a partial bar as a confirmed close.

### Mistake: Minimum-confidence setup not reduced in size

- **Count:** 1
- **First seen:** 2026-04-21
- **Last seen:** 2026-04-21
- **Rule:** 7/10 setups are always reduced size. No exceptions.
- **Checklist status:** Added
- **Examples:**
  - 2026-04-21 | BNBUSDT LONG | Entered a 7/10 setup without the reduced-size rule.

### Mistake: Open-position protection not checked fast enough

- **Count:** 1
- **First seen:** 2026-04-21
- **Last seen:** 2026-04-21
- **Rule:** While in any live demo trade, verify plan orders every 30-60 minutes.
- **Checklist status:** Added
- **Examples:**
  - 2026-04-21 | BNBUSDT LONG | Did not have a fast enough protection-check cadence for a live position on BitGet demo.

### Mistake: Failed setup not downgraded after stronger opposite-volume bar

- **Count:** 1
- **First seen:** 2026-04-21
- **Last seen:** 2026-04-21
- **Rule:** If the first full bar after entry closes opposite the position with higher volume than the entry bar, downgrade immediately and be ready to exit.
- **Checklist status:** Added
- **Examples:**
  - 2026-04-21 | BNBUSDT LONG | Did not treat the higher-volume reversal bar as a setup failure fast enough.

### Mistake: Only one side of the market was considered

- **Count:** 1
- **First seen:** 2026-04-18
- **Last seen:** 2026-04-18
- **Rule:** Every cycle scores both long and short paths before deciding.
- **Checklist status:** Added
- **Examples:**
  - 2026-04-18 | Process | Considered only one side of the market during scan.
