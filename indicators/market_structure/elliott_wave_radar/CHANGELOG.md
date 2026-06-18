# Changelog

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
