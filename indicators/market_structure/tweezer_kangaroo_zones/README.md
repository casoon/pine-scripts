# Tweezer & Kangaroo Zones

Detects two specific reversal candlestick patterns — tweezer tops/bottoms and kangaroo tails (pin bars) — and converts them into scored supply and demand zones that persist and decay over time. Instead of just marking the pattern, the script uses it as the origin of a dynamic zone whose score decays with age and touches, producing a living map of supply/demand levels grounded in actual rejection events.

## Features

- Tweezer top/bottom detection with flexible lookback, level tolerance, wick-similarity check, and volume validation
- Kangaroo tail (pin bar) detection with wick/body ratio, body fraction, and body position thresholds
- Timeframe sensitivity: pattern thresholds auto-adjust to the chart timeframe (stricter on low TFs, looser on high TFs)
- Auto-tuning of kangaroo thresholds based on choppiness regime
- 5-component zone scoring (0–100): rejection quality, extreme proximity, impulse before, freshness, cleanliness
- Zone freshness decay (configurable half-life) and Top-N filtering of active zones
- Zone grading (A/B/C) with labels and detailed tooltips, reversal bonus / continuation penalty
- Zone merging on overlap, cluster limit, TTL, and close-through invalidation
- Structure context: HH/HL/LH/LL swing detection with score bonus
- Trend gate: EMA + HTF regime, optional Supertrend and MOST (local/HTF/both scopes)
- Confluence scoring on zone retests (regime, HTF stack, structure, relative volume, chop, zone thinness, ST, MOST, pattern strength) with normalized 0–10 output
- HTF Stack panel (3 timeframes) plus session, chop, and score readouts (light-theme table)
- Buy/sell alerts on scored zone retests; hidden plots export signals and scores for external consumers
- Optional session filter (RTH/ETH profiles) and daily zone reset
- Debug logging for pattern tuning

## Scoring

A zone is created when a pattern fires and the initial score clears `Min Zone Score`. The base score weights five components: rejection 30%, extreme proximity 25%, impulse 20%, freshness 15%, cleanliness 10%. The result is multiplied by the pattern weight (kangaroo default 1.2, tweezer 0.8), gets a structure bonus when aligned with swing structure, and a reversal bonus or continuation penalty depending on zone classification. Scores update every bar as freshness decays and touches accumulate; grade and color follow the score.

Retest signals fire when price re-enters an active zone and the confluence score clears `Min Score BUY` / `Min Score SELL`. Choppiness acts as a hard block above the hard threshold and a soft gate below it.
