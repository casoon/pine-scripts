# S/R Zones MTF v2

Multi-timeframe support/resistance zones built from ATR-reversal structure swings. For each configured timeframe the script tracks swing highs/lows where the reversal exceeded an ATR-based threshold; these become zone boundaries that are scored, merged across timeframes, and tracked through tests, sweeps, breaks (with role reversal) and retests.

## Features

- Up to two configurable higher timeframes plus the chart timeframe (all `lookahead_off`)
- ATR-based reversal swing engine — zone boundaries from volatility-relative reversals, not fixed pivot counts
- Zone merging: overlapping same-side zones consolidated, with a too-close filter against duplicates
- Zone scoring: touch, rejection wick, close location, impulse, age penalty — weights configurable
- Event detection per zone: Test (T), Sweep (SW), Break (B↑/B↓ with role reversal), Retest (R) with min-bars delay and label cooldown
- Break rules: wick or close invalidation, optional volume confirmation, ATR break buffer
- Optional faded snapshot of invalidated zones
- Score filter: zones below the minimum score are faded out
- Alerts: zone break up/down, retest, sweep

## Scoring

Each zone starts with a timeframe boost (Chart 0.5, HTF1 1.0, HTF2 2.0) and accumulates:

- `+ wTouch` per test, plus quality bonuses for close location, rejection wick and impulse
- `+ 0.7 × wTouch` per sweep
- `+ 1.5 × wImpulse + 0.5 × wCloseLoc` per break
- `+ 1.2 × wTouch` per confirmed retest
- `− wAge` per bar (age decay)

When the zone limit is reached, the lowest-scoring zone is dropped (or the oldest, when the filter is off).
