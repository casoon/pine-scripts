# Changelog

## v1.3.0 — 2026-11-17
Rebuilt as a display of the current wave count: no score, no "setup" calls. **Existing alerts must be recreated** — titles and messages changed.
- New event "Close beyond W1 end" fires on a break observed after the W1-W2 count appears, not on the count bar when the pivot lag already placed the close beyond W1
- Removed: Fibonacci guideline score (0–100, incl. alternation bonus) and its gate input "Min count score (0-100)". The score measured closeness to ideal ratios and read as a quality verdict; the dashboard "Score" row now shows the raw ratios (W2/W1, W3/W1, W4/W3, W5/W1, B/A, C/A)
- Count selection no longer ranks by score + bonus: the most complete rule-valid interpretation wins in a fixed order (impulse, zigzag/flat, A-B after impulse, W1-W4, W1-W2); the next valid one is the alt count. Without the score gate, every count that passes the hard rules can be shown
- Removed alerts: "EW: Wave-3 setup", "EW: Wave-5 setup", "EW: C-wave setup", "EW: Impulse complete", "EW: ABC complete", "EW: Flat complete"
- New event alerts: "EW: Impulse count complete", "EW: Zigzag count complete", "EW: Flat count complete", "EW: A-B count active", "EW: W1-W2 count active", "EW: W1-W4 count active", "EW: Close beyond W1 end" (once per W1-W2 count). "EW: Count invalidated" is unchanged
- Count alerts now also fire when a new count of the same type replaces the previous one (different first point); before, a same-type sequence was suppressed
- Dashboard status reads "<count> ▲/▼ complete" or "… counted" instead of "→ W3/W5/C setup"; post-impulse levels relabelled "Retr 38.2/50/61.8%"
- Header: Data Contract block added

## v1.2.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.2.1 — 2026-06-29
- Alerts: messages standardized to `EWR · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.2 — 2026-06-11
- Fix: wave points now anchor to the TRUE extreme since the previous pivot. Sharp counter-swings that never confirm as pivots (shorter than Pivot Length on either side) were invisible to the engine, so e.g. Wave 2 could land on a later, lower high instead of the strongest pullback. Each accepted pivot now scans the actual high/low of the gap and uses that price/bar.

## v1.1 — 2026-06-11
- Flat correction detection (regular ≈ B 1.0×A, expanded ≈ B 1.05–1.38×A), disjoint from the zigzag eval (B ≤ 0.886)
- C-wave setup: after a completed impulse, a confirmed A-B sequence projects C targets (×1.0 / ×1.618 of A) with the impulse extreme as monitored invalidation level
- New alerts: "Flat complete" and "C-wave setup"
- Candidate selection refactored (array-based ranking with correct runner-up tracking)

## v1.0 — 2026-06-11
- Initial release
- ZigZag pivot engine (two degrees) with ATR noise filter
- Hard-rule validation for impulses (W2/W3/W4 rules, diagonal toggle) and zigzag A-B-C
- Fibonacci guideline scoring 0–100 with alternation bonus, configurable score gate
- Developing counts: W3 setup (after W1-W2) and W5 setup (after W1-W4) with Fib target projections
- Post-impulse correction targets (38.2 / 50 / 61.8 %)
- Invalidation level drawn and monitored; broken level clears the count
- Sub-wave labels (i)-(iv) / (a)-(b) from the sub degree, W1/W3 leg check in dashboard
- Alternate count in dashboard; "No valid count" state instead of forced labels
- Alerts: impulse complete, ABC complete, W3 setup, W5 setup, count invalidated
