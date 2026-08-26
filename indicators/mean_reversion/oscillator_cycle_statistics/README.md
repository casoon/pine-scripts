# Oscillator Cycle Statistics

Oscillator Cycle Statistics is a statistics engine, not a trading signal. It answers one question: given where a bounded oscillator (RSI, Stochastic RSI, Stochastic, normalized Williams %R, MFI, CCI, WaveTrend, DeMarker, RVI, EOM, or Klinger) came from, how often did it historically complete the move to the opposite extreme under comparable conditions? It runs an explicit cycle state machine, stores every completed attempt in persistent arrays, and reports empirical, sample-sized-qualified probabilities — deliberately without generating entries, exits, or a composite score.

## Features

- RSI, Stochastic RSI, smoothed Stochastic %K, normalized Williams %R, MFI, CCI, WaveTrend, DeMarker, RVI, EOM, Klinger — selectable single oscillator; normalized Williams %R is explicitly identified as equivalent to raw Fast Stochastic %K, and all volume-dependent choices are labeled
- Oscillator-specific default zones: 80/20 for Stochastic RSI, Stochastic, normalized Williams %R, and MFI; 70/30 for RSI, DeMarker, and reference-normalized oscillators; optional custom zones remain available
- MFI, EOM, and Klinger are volume-dependent and labeled `(volume)` in the dropdown; on zero-volume CFD/index feeds (Capital.com, FOREX.com, and similar) they sit at a constant neutral 50 — no crash, but no cycles detected either
- Explicit OB → OS / OS → OB cycle state machine: origin → armed → success / failure / timeout
- Progress-conditioned probability — matches the current cycle to historical cycles using time-consistent 10-percentage-point progress buckets
- Age-conditioned probability — requires a historical cycle to have reached the matching progress bucket by the current age and to have remained unresolved beyond that age
- Regime-conditioned probability — Bull Trend / Bear Trend / Range, derived from EMA position + slope/ATR
- Recent / Medium / Long lookback comparison to expose drift in cycle behavior over time
- Descriptive Wilson interval and an explicit minimum-sample status; consecutive cycles can be dependent, so the interval is not presented as a guaranteed confidence band
- Median time-to-target and origin-based median price MFE/MAE in ATR, shown separately for successful and failed cycles
- Separate OB → OS and OS → OB base rates across the medium lookback
- Walk-forward reliability table — average forecast, observed rate, calibration error, and sample size per bucket, restricted to the same Medium lookback as the live model
- Base Brier score plus a fair paired base/regime Brier comparison using only cycles for which both forecasts existed
- Naive direction-base-rate Brier score and Brier Skill Score, both walk-forward correct — the naive benchmark is snapshotted at forecast-capture time, not re-derived from today's base rate — so the paired comparison has an actual floor to beat
- Cycle zigzag lines drawn directly on the oscillator — origin extreme to resolution, royal blue for completed successes, light gray dashed for failures/timeouts (deliberately not red/green, which read as a price call), width scaled by how far the cycle actually got, reverted-failure V-shapes anchored at the exact maximum-progress bar, a live line tracking the active cycle to the current bar, a target marker, and a dashed Expected Target Time projection to when a typical cycle would complete (skipped once the cycle is overdue)
- Edge (Conditional minus the direction's plain base rate) drives the live label (`UP/DOWN CYCLE` · `Edge` · state word) and a once-per-cycle Opportunity marker — both gated on the identical sample-size, Wilson-interval-width, and progress-zone conditions, so the label can never claim a state the marker itself would refuse to fire on
- Label states: `LOW DATA` (below sample minimum), `STALLED` (past the historical median completion duration), `UNCERTAIN` (Wilson interval still too wide), `LATE` (past the opportunity zone), `OPPORTUNITY`, `WATCH`, `WAIT`
- Recent mutable straight cycle lines stay full color; older straight lines fade, while reverted-failure V-shapes remain low-weight gray
- Cycle Start and Success/Failure markers off by default — outcome is already encoded in the completed line's color/style; Opportunity marker (▲/▼) on by default, the one meant to draw the eye
- Three dashboard modes: `Visual` (one-line confirmation tag, default), `Compact` (decision-relevant two-column table), `Research` (full statistics dashboard)
- Cycle-stage and evidence readout — clearly states that fresh-entry and price-exit quality have not yet been validated
- Confirmed-bar processing by default (toggle) to avoid intrabar cycle events

## Cycle Model

A cycle starts on fresh entry into Overbought (or Oversold). Staying inside the zone does not create additional samples. Once the oscillator leaves the zone, the cycle becomes "armed." From there:

- Reaching the opposite extreme = **success**.
- Returning to the origin extreme before that = **failure** (and simultaneously starts the next attempt from that point).
- Exceeding the maximum cycle length = **timeout failure**, and the cycle resets.

OS → OB works symmetrically. This prevents repeated counting while the oscillator sits at an extreme, overlapping attempts, and hindsight target selection.

Each completed sample stores: direction, success/failure, failure reason, start regime, duration, completion bar, maximum normalized progress reached, the first age at which each 10-percentage-point progress bucket was reached, and price MFE/MAE in ATR.

## Reading the Chart

The oscillator line is context; the cycle lines are the primary read. A completed **success** draws a straight royal-blue line from its origin extreme to the opposite rail. A completed **failure** draws differently depending on how it failed: a **reverted** failure (origin extreme revisited) draws a dashed gray V-shape — origin → the deepest point the attempt actually reached → back to origin — rather than a straight line, because a straight line from origin back to origin would land on the exact same rail it started on and render perfectly horizontal, camouflaged against the OB/OS gridline it sits on top of. A **timeout** failure draws a straight dashed gray line to wherever the oscillator actually was when time ran out (never forced onto a rail, so never camouflaged) — that distinct landing position is itself the tell for "expired mid-flight" vs. "reversed cleanly." Colors avoid red/green on purpose — a cycle's own success or failure is not a bullish/bearish price call. Line width scales with how far the cycle actually got (successes are always full width, failures thin out the earlier they reverted), and recent mutable line objects (`Prominent Recent Cycles`) stay full color while older ones fade. One unified rolling limit caps all completed straight lines and V-shapes; V-shapes retain their low-weight gray because Pine polylines cannot be recolored in place.

The active cycle draws as a live line from its origin to the current bar, extending every bar, with a `TARGET` marker and a dashed **Expected Target Time** projection running from the current point to `bar_index + median remaining duration` at the target extreme — a time projection, not a price forecast; it says "if this cycle runs a typical length, the target would land around here." The projection disappears once the cycle is `STALLED` (age already past the historical median completion duration) — drawing it there would collapse into a near-vertical line to the target on the current bar, which reads as "arriving now" rather than "overdue."

The live label reads `UP CYCLE` / `DOWN CYCLE` plus `Edge` and a state word. It deliberately does not lead with the raw Conditional percentage — a "100%" backed by one historical case reads as a strong signal when it's actually no evidence at all. **Edge** (Conditional minus the direction's own plain base rate) is the number that answers "does this situation tell me more than just knowing the market's normal up/down cycle odds" — a Conditional of 72% against a base rate of 68% is barely informative; the same 72% against a base rate of 36% is a different story entirely.

The label's state word uses the exact same gates as the Opportunity marker below, evaluated live, in this priority order: `LOW DATA` (sample below `Minimum Conditional Samples`) → `STALLED` (age past the historical median duration) → `UNCERTAIN` (Wilson interval wider than `Max Wilson CI Width`) → `LATE` (progress past `Opportunity Zone Max Progress %`) → `OPPORTUNITY` (Edge above `Edge Threshold`, still inside the zone) → `WATCH` (Edge above half the threshold) → `WAIT`. This ordering means the label can never say `OPPORTUNITY` in a situation where the marker itself would refuse to fire.

The **Opportunity marker** (▲/▼) fires at most once per cycle, evaluated at progress-bucket crossings inside a configurable zone (`Opportunity Zone Min/Max Progress %`, default 30–65%) — a cycle that's already mostly done no longer qualifies just because its raw completion number looks good. It requires Edge above `Edge Threshold`, sample size at or above `Minimum Conditional Samples`, and a Wilson interval width at or below `Max Wilson CI Width` — all three, not just a probability threshold. `Show Cycle Start Markers` and `Show Success/Failure Markers` are off by default (that information is already in the completed line's color and style); `Show Opportunity Markers` is on by default and is the one meant to draw the eye.

Answering "where did the current cycle start, where is it now, where would it complete, how much historical weight backs the assumption that it gets there, and is it still early enough to matter" is the design goal — with the zigzag and the Opportunity marker as the primary vehicle, this should be readable directly off the chart without opening the dashboard at all. `Dashboard Detail = Visual` (the default) reflects that: the table becomes a one-line confirmation tag.

## Reading the Dashboard

`Compact` mode uses two columns, readable small text, and eight rows:

- cycle direction and stage
- completion frequency with sample-size warning
- fresh-entry validation status
- progress and age
- directional base rates
- successful- and failed-cycle MFE/MAE
- the origin-price/entry-model limitation

`Research` restores the full three-column dashboard. Its leading rows deliberately separate facts from trading conclusions:

- `Overall` names the active upward/downward cycle, its lifecycle stage, or the latest cycle event.
- `Cycle Evidence` reports the age- and progress-conditioned completion frequency, sample size, and Wilson interval. `COMPLETION >=50%` is descriptive, not permission to trade.
- `Fresh Entry` remains `NOT VALIDATED` while no price outcome from the actual decision checkpoint exists.
- `If in Position` describes cycle maturity or the latest cycle event, while explicitly noting that a price exit has not been evaluated.
- `Evidence Limits` flags that current MFE/MAE begins at the cycle origin and that no entry/exit model exists.

`EARLY`, `DEVELOPING`, `MATURE`, and `LATE` describe progress bands based on the cycle's *current* position, not the best it ever reached — a cycle that peaked at 80% and has since retraced to 40% is `DEVELOPING`, not `LATE`. They are not optimized entry gates. The historical-evidence conditioning behind `Conditional` still compares against each historical cycle's peak progress, since that's the correct like-for-like comparison against a fully resolved cycle.

The `Conditional` row is the primary read: among historical same-direction cycles within the medium lookback that had reached the same 10-percentage-point progress bucket by the current age and were still unresolved after that age, what percentage ultimately completed to the opposite extreme. The descriptive `Wilson interval` and explicit minimum-sample status make the available sample size visible without claiming that consecutive cycles are statistically independent.

The compact `Lookbacks R / M / L` row compares Recent, Medium, and Long behavior as a structure rather than inviting selection of the highest number. `Base Down / Up` exposes directional asymmetry. `Regime` narrows the same query to cycles that started in the same market regime (Bull Trend / Bear Trend / Range) as the current one.

`MFE / MAE (won)` and `MFE / MAE (failed)` show price excursion aligned with the oscillator direction, measured from the cycle origin. These are descriptive distributions, not results from a tradable entry, stop, or exit rule.

## Reliability Table

The main dashboard's `Conditional` row answers "how often did comparable historical cycles complete" — but that alone doesn't tell you whether the number itself is trustworthy as a forecast. The optional Reliability table is off by default. Once enabled, it tracks the forecast separately: once per cycle, the first time it crosses `calibCheckpoint` progress (default 50%), the exact progress- and age-conditioned forecast shown at that moment is snapshotted using only samples completed so far. Forecasts with fewer than `Minimum Conditional Samples` are excluded. Resolved forecasts are retained in the table only while their completion bar remains inside the current `Medium Lookback`, so live statistics and forecast assessment refer to the same time window.

Below the configured sample minimum, Reliability displays only a compact `Collecting n / minimum` row. Once enough observations exist, each bucket reports `Avg Forecast`, `Observed`, error, and `n` in readable small text. The base Brier score summarizes squared forecast error; lower is better. The regime Brier score is compared with a base score calculated on the exact same cycles. A percentage improvement is withheld until the paired sample reaches the configured minimum.

`Naive Brier` scores a constant, direction-specific base-rate forecast — no progress, age, or regime conditioning at all — against the same outcomes, using the base rate exactly as it was at the moment the forecast was captured (not today's base rate applied retroactively, which would leak hindsight into the naive benchmark). `Skill Score` (`1 - modelBrier/naiveBrier`) answers the question the base Brier score alone cannot: does the conditioned model actually beat just knowing the direction's long-run completion rate, or is it no better than that naive floor?

## Explicitly Out of Scope

This version intentionally omits divergence detection, volume, ADX, or any other confirming factor, a composite "cycle health" score, and trading signals/alerts beyond the raw cycle events. It does not infer trade profitability from oscillator completion. The goal is to first establish whether the cycle forecast is stable and whether later price-outcome testing from a realistic entry checkpoint shows an edge.

Percentages shown are empirical historical frequencies, not automatically calibrated forecasts — use the Reliability table to check how well that empirical read actually held up.
