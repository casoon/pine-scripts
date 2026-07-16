# Changelog

## v2.2.1 — 2026-07-16 (`market_tradability_engine_v2.pine`, Beta)
- Fix: transition markers (`R`, `BREAK`, `STOP`, `AM`, `EX`) used `textcolor = color.white`. Unlike a table cell, `plotshape`'s `text` has no background fill behind it — it's drawn directly on the chart pane, so white text sat straight on TradingView's light-theme chart background and was effectively invisible (confirmed via a zoomed screenshot). Changed to a dark charcoal (`color.rgb(40, 44, 51)`) that reads on both themes

## v2.2.0 — 2026-07-16 (`market_tradability_engine_v2.pine`, Beta)
- Added: `Reactivity` preset (`Early` / `Balanced` / `Conservative` / `Custom`), independent of `Preset` (lookback lengths only) — resolves Structure Threshold, all three Energy thresholds, all four Acceptance thresholds, and Confirmation Bars / Minimum State Duration / Breakout Acceptance Bars in one dial, so states can be tuned to trigger sooner off softer evidence (`Early`) or wait for stronger sustained evidence (`Conservative`) without touching ten individual inputs by hand. `Custom` falls through to the renamed `(Custom)`-labeled individual inputs, mirroring how `Preset`'s `Custom` option already works
- Added: `Baseline Type` selector (`EMA`/`SMA`/`RMA`/`WMA`/`SuperSmoother`/`T3`/`KAMA`/`JMA Approx`, `JMA Phase`/`JMA Power` when JMA Approx is chosen) for the Quality Baseline, using this repo's 8-kernel "Advanced family" pattern (`rsi_advanced.pine`, `wavetrend_advanced_smoothing.pine`, and others) rather than the smaller 6-option EMA/RMA/SMA/WMA/HMA/JMA set — SuperSmoother/T3/KAMA are adaptive/filter-based and behave meaningfully differently from the plain MA family. Scoped to the baseline only, not every internal reference EMA
- Calibration log: `MTE2 CONFIG` now includes `reactivity` and `baselineType`

## v2.1.1 — 2026-07-16 (`market_tradability_engine_v2.pine`, Beta)
- Fix: the `candidateState` fallback (reached when nothing more specific matched) defaulted to `BALANCE` whenever Structure happened to read range-flavored, without checking that Energy/Acceptance actually met Balance's own criteria — visibly wrong on a live WTI chart (Structure/Energy/Acceptance all mediocre-to-bad, state still showed `BALANCE`). Fallback now defaults to `NO TRADE`, matching the indicator's own philosophy: an ambiguous reading isn't a Balance reading. Removed the now-dead `noTradeCondition` (its only effect was already superseded by the corrected fallback)

## v2.1.0 — 2026-07-16 (`market_tradability_engine_v2.pine`, Beta)
- Changed: ratio-based score components (volatility expansion, Structure's trend-cleanliness reading, Energy's efficiency and candle-commitment readings, the Exhaustion wick/ATR-spike gates) now use `ta.percentrank(..., rankLength)` instead of fixed constants, so the same defaults work across timeframes and instruments instead of only the one they were eyeballed on. New "Rank Window" input (preset-scaled, default 150 bars on Balanced)
- Changed: bar offsets that were hardcoded to 3 or 5 bars (energy-building trough window, momentum/energy decay comparison) now scale with the Quality Window via a derived `shortWindow`, so they represent a comparable amount of real time regardless of timeframe
- `dataReady` now also requires the rank window to be filled before the state machine starts classifying
- Calibration log: `MTE2 CONFIG` now includes `rankLen`

## v1.3.2 — 2026-07-16
- Fix: same transition-marker text-color bug as v2.2.1 — `textcolor = color.white` on `plotshape` labels (`R`, `BREAK`, `STOP`, `AM`, `EX`) sat directly on the chart background (no fill behind `plotshape` text, unlike a table cell) and was unreadable on TradingView's light theme. Changed to a dark charcoal (`color.rgb(40, 44, 51)`)

## v1.3.1 — 2026-07-16
- Fix: same `candidateState` fallback bug as v2.1.1 — defaulted to `BALANCE` whenever `tradabilityScore >= 50`, without checking `balanceScore` against its own threshold. Fallback now defaults to `NO TRADE`. Removed the now-dead `noTradeCondition` and the "No-Trade Below" input it depended on (its only effect was already superseded by the corrected fallback and `establishedCompression`'s own gating)

## v1.3.0 — 2026-07-16
- Changed: same percentile-rank conversion as v2.1.0, applied to v1's Tradability/Balance/Compression component formulas (ATR/bandwidth contraction, range compactness, efficiency, ADX, baseline cleanliness, candle quality, compression-energy, participation) and the Breakout body-ratio / Exhaustion wick-ratio / ATR-spike gates. New "Rank Window" input, `shortWindow`-scaled bar offsets, `dataReady` extended, `MTE CONFIG` now includes `rankLen`

## v2.0.0 — 2026-07-16 (`market_tradability_engine_v2.pine`, Beta)
- Initial parallel research build: reduces v1's four scores (Tradability/Balance/Compression/Direction) to three fundamental properties — Structure (0-100, coherent framework), Energy (0-100, movement intensity building/fading), Acceptance (-100..100, are new prices held or rejected, and which way) — and derives all eight states from combinations of them
- New raw sensor: per-bar acceptance (does the bar close near its favorable extreme or get wicked back), smoothed and folded into Acceptance
- Reuses v1's state-machine mechanics unchanged (disagreement-streak confirmation, minimum-duration hysteresis, breakout hold, post-breakout Balance lock, breakout acceptance bars, Ready energy-building check) and v1's raw sensors (ATR, efficiency ratio, ADX/DI, candle/range/volume metrics)
- Six-row dashboard (Market State, Candidate, Structure, Energy, Acceptance, Action), down from v1's nine
- Pine-Log calibration logging with an `MTE2` event prefix (`MTE2 CONFIG` / `MTE2 CAL` / `MTE2 TRANSITION`) so it can log alongside v1's `MTE` events on the same chart for side-by-side comparison
- Not yet calibrated against real data — thresholds are carried over analogously from v1 where a direct mapping exists

## v1.2.0 — 2026-07-16
- Added: breakout acceptance — a new "Breakout Acceptance Bars" input (default 2) requires price to hold beyond the boundary for several consecutive bars before Breakout confirms, instead of a single spike candle
- Added: Ready now also requires volatility (ATR/bandwidth) to be ticking up off its recent trough ("energy building"), not just directional pressure near a boundary — pressure without energy behind it produced Ready states that just sat at the boundary without resolving
- Added: Compression score gained a coiling-energy component (shrinking candle bodies + growing wicks), reweighting the existing ATR/bandwidth/range/boundary/efficiency components to make room for it
- Calibration log: `MTE CONFIG` now includes `breakoutAcceptanceBars`; `MTE CAL` now includes `compressionEnergy`

## v1.1.0 — 2026-07-16
- Added: `AFTERMATH` state — a recent directional impulse (high direction + tradability within an "Impulse Lookback" window) has gone quiet: ADX is still elevated but the fast efficiency ratio has collapsed and volatility isn't expanding again. Sits between Ready and Compression/Balance in the state priority so a post-impulse pause is no longer forced into a generic No Trade or, worse, misread as a fresh Balance. New "Impulse Aftermath" input group, dashboard action hint, transition markers, and alert
- Added: dual-window efficiency ratio — a new "Fast Efficiency Length" (default 8 bars) reading alongside the existing Quality-Window efficiency ratio, used to tell a genuine range apart from a pause right after an impulse. Exposed in the calibration log and the data window
- Changed: all input labels, group names, dashboard text, state/direction names, plot/alert titles and messages translated from German to English, matching the rest of the repo's indicators
- Fix: `ta.sum` isn't a Pine v6 function — replaced with `math.sum` (efficiency ratio, directional consistency, baseline cross rate)
- Fix: exhaustion marker's `location` argument used a series ternary, which `plotshape` rejects — split into two fixed-location calls gated by `activeDirection`
- Fix: state-confirmation counter reset on every candidate flip, so a confirmed state (e.g. Balance) could get stuck long after every underlying score had moved on if the live candidate kept changing between different alternates. Replaced with a disagreement-streak counter that accumulates on any bar where the candidate disagrees with the confirmed state, regardless of which specific alternate it is
- Added: ADX's contribution to the Tradability score is now gated by the current efficiency ratio, so a still-elevated ADX from a finished impulse no longer props up the score once price has gone quiet
- Added: post-breakout Balance lock ("Post-Breakout Balance Lock", default 10 bars) — a tight consolidation right after a breakout no longer immediately re-qualifies as a new Balance
- Added: dashboard "Candidate" row showing the live candidate state next to the confirmed state, to surface staleness at a glance

## v1.0.0 — 2026-07-16
- Initial release: Tradability/Balance/Compression/Direction scores, seven-state market machine (No Trade/Balance/Compression/Ready/Breakout/Trend/Exhaustion) with confirmation and minimum-duration hysteresis, balance boundary lines/midline/background, transition markers, dashboard, presets
- Pine-Log calibration logging (`MTE CONFIG` / `MTE CAL` / `MTE TRANSITION`) behind an off-by-default toggle, for offline threshold calibration from exported CSV
