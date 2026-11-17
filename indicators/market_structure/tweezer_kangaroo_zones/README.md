# Tweezer & Kangaroo Zones

Detects two specific reversal candlestick patterns — tweezer tops/bottoms and kangaroo tails (pin bars) — and converts them into supply and demand zones that persist over time. Instead of just marking the pattern, the script uses it as the origin of a dynamic zone, producing a living map of supply/demand levels grounded in actual rejection events.

## Features

- Tweezer top/bottom detection with flexible lookback, level tolerance, wick-similarity check, and volume validation
- Kangaroo tail (pin bar) detection with wick/body ratio, body fraction, and body position thresholds
- Timeframe sensitivity: pattern thresholds auto-adjust to the chart timeframe (stricter on low TFs, looser on high TFs)
- Auto-tuning of kangaroo thresholds based on choppiness regime
- Internal zone ranking from five components (rejection, extreme proximity, impulse before, freshness, cleanliness) — used only to highlight the Top N active zones
- Zone labels (direction + pattern) with tooltips showing the raw zone measures, touches, age and invalidation level
- Zone merging on overlap, cluster limit, TTL, and close-through invalidation
- `Max stored zones` (default 100) caps the zones kept in memory: above it the oldest inactive zone is removed first, otherwise the oldest zone, together with its box and label
- Structure context: HH/HL/LH/LL swing detection with a ranking bonus
- Trend gate: EMA + HTF regime, optional Supertrend and MOST (local/HTF/both scopes)
- Retest signals: first retest of a zone, optionally only with the HTF trend on the signal's side
- HTF Stack panel (3 timeframes) plus session, chop, signal-HTF and zone-ranking readouts (light-theme table)
- Buy/sell alerts on zone retests; hidden plots export signals, regime, chop, HTF direction and top zone ranking values for external consumers
- Optional session filter (RTH/ETH profiles) and daily zone reset
- Debug logging for pattern tuning

## Zone ranking

Every pattern that passes the cluster and overlap checks creates (or merges into) a zone — there is no minimum score. The ranking only decides which active zones are highlighted as the Top N; the others are dimmed. It does not create, remove or label zones and does not affect retest signals. The ranking weights five components: rejection 30%, extreme proximity 25%, impulse 20%, freshness 15%, cleanliness 10%. The result is multiplied by the pattern weight (kangaroo default 1.2, tweezer 0.8), gets a structure bonus when aligned with swing structure, and a reversal bonus or continuation penalty depending on zone classification. Scores update every bar as freshness decays and touches accumulate — pattern weight and structure bonus are kept in those updates. Zone fill and label color depend only on direction (supply/demand). Impulse is measured over the five bars before the pattern bar, so the pattern's own wick is not counted as impulse.

## Retest signals

A retest signal fires when price re-enters an active zone on a later bar (the bar whose pattern created or reinforced the zone is not a retest). With `Only first retest can signal` on, each zone signals once. A BUY retest (demand zone) needs no new 5-bar low on the retest bar, a SELL retest (supply zone) no new 5-bar high.

`Require HTF trend in signal direction` (default on) adds one side-specific condition: BUY only while the last closed bar of the Trend Detection HTF closes above its EMA, SELL only while it closes below. Turned off, every first retest signals. Choppiness acts as a hard block above the hard threshold and a soft gate below it; the optional session filter applies as well.
