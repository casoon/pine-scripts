# Market Tradability Engine

Market Tradability Engine is a market-quality and no-trade filter. Instead of generating directional entries, it classifies the current market into one of eight states — from an inefficient, noisy `NO TRADE` phase through `BALANCE` and `COMPRESSION`, into `READY`, `BREAKOUT`, `TREND`, a post-impulse `AFTERMATH` pause, and finally `EXHAUSTION` — so that other signal-generating indicators or strategies can be gated by whether the market is actually worth trading right now.

This directory holds two parallel builds:

- **`market_tradability_engine.pine`** (v1, documented below) — the stable build, drives its state machine from four scores (Tradability, Balance, Compression, Direction).
- **`market_tradability_engine_v2.pine`** (v2, [documented at the end](#v2-beta--structure--energy--acceptance)) — a Beta research build that reduces those four scores to three fundamental properties (Structure, Energy, Acceptance) and derives every state from combinations of them. Not calibrated yet; meant to run side by side with v1 for comparison, not to replace it.

## Features

- Four weighted 0–100 scores: **Tradability** (efficiency, ADX, slope, consistency, baseline cleanliness, candle quality, volatility expansion, participation), **Balance**, **Compression**, and a −100..+100 **Direction** score
- Eight-state market machine (`NO TRADE` → `BALANCE` → `COMPRESSION` → `READY` → `BREAKOUT` → `TREND` → `AFTERMATH` → `EXHAUSTION`) with disagreement-streak confirmation and minimum-state-duration hysteresis to avoid flicker
- ADX's contribution to Tradability is gated by the current efficiency ratio, so a still-elevated ADX from a finished impulse can't prop up the score once price has gone quiet
- Dual-window efficiency ratio (fast/slow) distinguishes a genuine range from a pause right after a directional impulse
- Post-breakout Balance lock: a tight consolidation right after a breakout doesn't immediately re-qualify as a new Balance
- Breakout acceptance: price must hold beyond the boundary for several consecutive bars (configurable) before Breakout confirms, instead of a single spike candle
- Ready requires volatility ticking up off a recent trough ("energy building"), not just directional pressure at a boundary
- Compression score includes a coiling-energy component (shrinking candle bodies, growing wicks) alongside ATR/bandwidth contraction
- Ratio-based scores (ATR, bandwidth, efficiency, ADX, candle shape, volume) are ranked against their own recent history instead of fixed constants, so the same defaults generalize across timeframes and instruments
- Balance-boundary lines, midline, and continuous state-colored background
- Transition markers: Ready (directional pressure near a boundary), Breakout, No-Trade entry, Aftermath, Exhaustion
- Dashboard with score breakdown, live candidate state, and a plain-language action hint per state
- Presets (Very Fast / Fast / Balanced / Calm / Position) resolving all lookback lengths at once, or fully custom parameters
- Pine-Log calibration logging (config snapshot, per-bar raw scores/inputs, state-transition context) for offline threshold tuning

## States

- **NO TRADE** — none of the other states' criteria are met (including a Balance/Compression score that doesn't actually clear its own threshold); the market is inefficient, directionless, or simply doesn't fit a recognizable regime right now
- **BALANCE** — an established sideways auction: balance score above threshold, range width within the maximum ATR multiple
- **COMPRESSION** — balance plus a contracting ATR/Bollinger bandwidth and compact range
- **READY** — compression plus directional pressure (direction score beyond the ready threshold) near a range boundary, and volatility ticking up off its recent trough (energy building) rather than still flat
- **BREAKOUT** — confirmed departure from the balance range: close beyond the boundary plus an ATR buffer, held for several consecutive bars (acceptance, not a single spike), with direction, tradability, volatility expansion, body-ratio and (optionally) volume confirmation all aligned
- **TREND** — efficient directional expansion: high tradability, strong direction score, high efficiency ratio, price on the correct side of the baseline
- **AFTERMATH** — a directional impulse (high |direction| and tradability) occurred recently within the impulse lookback window, but the fast efficiency ratio has since collapsed while ADX is still elevated and volatility isn't expanding again. Covers the "just went quiet after a strong move" phase that would otherwise get mislabeled as a fresh Balance/Compression or a generic No Trade
- **EXHAUSTION** — an extended trend (large baseline extension in ATR) showing declining quality: momentum decay, rising wick ratio, or a volatility spike

State transitions require `confirmationBars` consecutive bars where the live candidate disagrees with the confirmed state (longer for leaving `NO TRADE`) — the disagreement streak accumulates regardless of which specific alternate candidate shows up bar to bar, so a confirmed state can't get stuck once the underlying scores have consistently moved past it. Outside of breakout handling, a minimum number of bars in the current state is also required before a new state can take over. `BREAKOUT` is held for a configurable number of bars unless exhaustion conditions fire early, and re-entering `BALANCE` is locked out for a configurable number of bars right after a breakout.

## Dual-Window Efficiency & Aftermath Detection

The core efficiency ratio (net movement / total movement over the Quality Window) is a comparatively slow reading. `AFTERMATH` detection instead uses a second, faster efficiency ratio (`Fast Efficiency Length`, default 8 bars) alongside it — a fast window that has already collapsed while ADX and the impulse lookback still show a recent strong directional move is the signature of "the impulse just went quiet", not a genuine new range. The rest of the score stack (Tradability, Balance, Compression) intentionally still uses the original single-window efficiency ratio to avoid re-calibrating already-validated behavior; the fast window is scoped to the Aftermath detector and the calibration log/data window for now.

## Timeframe-Adaptive Scoring

Several score components (ATR/bandwidth contraction and expansion, range compactness, efficiency, ADX, baseline cleanliness, candle body/wick shape, participation) don't compare their underlying ratio against a fixed constant anymore. Fixed bounds like "atrRatio between 0.72 and 1.08" are tuned by eye on one chart and can misclassify on a different timeframe or instrument where that ratio naturally swings wider or narrower. Instead, these components rank the current value against its own trailing history via `ta.percentrank(value, Rank Window)` (`Rank Window`, preset-scaled, default 150 bars on Balanced) — the same self-normalizing pattern already used for ATR Rank in `strategies/wavetrend/wavetrend_v4_strategy.pine`. Bar offsets that were hardcoded to a flat 3 or 5 bars (energy-building trough, momentum/energy decay comparisons) now scale with the Quality Window instead, so they represent a comparable amount of real time regardless of timeframe.

Left unranked, deliberately: gates built directly around a user-configured absolute parameter (`Max Range Width (ATR)`'s own gate, `balanceWidthComponent`'s band around it, `Volume Factor`'s breakout gate) — those are intentional user dials, not guessed constants, so relativizing them away would remove control the input is there to provide. `extensionFromBaseline`'s exhaustion threshold is left as a fixed ATR multiple too, since it's already volatility-normalized in a way that's reasonably comparable across timeframes (similar to a fixed "2 standard deviations" Bollinger threshold).

## Calibration Logging

The `Enable Calibration Log` toggle (off by default) writes structured lines to Pine Logs, in the same `KEY value` pipe-delimited format used by this repo's other calibration workflows (see `strategies/wavetrend/wavetrend_v4_strategy.pine`):

- `MTE CONFIG` — written once, snapshotting the resolved lengths and thresholds (including `rankLen`) plus symbol/timeframe, so an exported log is self-contained
- `MTE CAL` — one line per confirmed bar with the active/candidate state and every raw score and input metric behind the state machine (tradability, balance, compression, direction, atrRatio, bandWidthRatio, rangeWidthAtr, efficiencyRatio, fastEfficiencyRatio, adx, boundaryStability, rangePosition, volumeRatio, bodyRatio, wickRatio, compressionEnergy)
- `MTE TRANSITION` — one line per confirmed state change with the from/to state, how long the previous state held, and the scores at the moment of transition

Export the Pine Logs panel to CSV to build score distributions per state and sweep threshold candidates offline, rather than hand-tuning against a single chart view. This produces a large number of log lines over long ranges — keep it disabled for normal chart use and enable it only for a bounded calibration run.

## Scope

Market Tradability Engine intentionally does not generate unconditional buy/sell signals. The Ready and Breakout markers identify a market-state transition, not a complete trade setup — they are meant to gate or contextualize signals from a separate entry indicator, not to be traded directly.

---

## v2 (Beta) — Structure / Energy / Acceptance

`market_tradability_engine_v2.pine` is a parallel research build, not a replacement for v1. It keeps the same eight states and reuses v1's raw sensors (ATR, efficiency ratio, ADX/DI, candle/range/volume metrics) and several of v1's mechanics (minimum-duration hysteresis, breakout hold, post-breakout Balance lock, breakout acceptance bars, Ready energy-building check) — what changes is how the sensors are combined and interpreted, and, since v2.5.0, the state-confirmation mechanics themselves (see [State Confirmation](#state-confirmation-v250) below).

Instead of v1's four scores (Tradability, Balance, Compression, Direction), v2 derives everything from three:

- **Structure** (0–100) — is there a coherent framework right now, either a respected range or a clean trend? Computed as `max(range quality, trend quality)` rather than an average, so a market that's clearly one or the other isn't understated by blending in the other framework's (irrelevant) reading. Range quality is the geometric mean of Quality-Window-smoothed boundary persistence and compactness inside `Max Range Width`; this requires both a stable and reasonably tight auction. Trend quality is a composite of baseline-cross rarity (25%), efficiency-ratio rank (25%), ADX rank (20%), normalized-slope rank (20%) and directional-consistency rank (10%). All five trend components are ranked against their own recent history (`Rank Window`), with inverse cross quality ranked from the negated cross rate so tied zero-cross observations retain high cleanliness quality.
- **Energy** (0–100) — is movement intensity building or fading? Blends volatility expansion, how efficiently movement converts into net progress (the efficiency ratio, reframed as an energy-conversion measure rather than a Balance/Tradability input), acceleration of directional conviction, and candle commitment (body size).
- **Acceptance** (−100 to +100) — are new prices being validated or rejected, and which way? Reuses v1's Direction Score ingredients (slope, baseline displacement, DI dominance, directional consistency, range position) plus a new sensor v1 didn't have: whether bars close near their favorable extreme (held) or get wicked back toward the opposite extreme (rejected).

States fall out of threshold combinations of the three, e.g.: `Structure` above threshold + range-flavored + `Energy` low + `Acceptance` neutral → `BALANCE`; add tighter `Energy` → `COMPRESSION`; `Structure` trend-flavored + `Energy` high + `Acceptance` strong → `TREND`; a recent `Energy`+`Acceptance` impulse that's since collapsed → `AFTERMATH`; no coherent `Structure` at all → `NO TRADE`.

`READY` and `BREAKOUT` work off an *armed* balance rather than the live readings, because both would otherwise be self-contradictory: Ready can't demand neutral acceptance (compression) and directional pressure on the same bar, and a rolling range boundary starts chasing the breakout bars one bar after the break. An established compression arms a memory state and freezes the balance boundaries; `READY` fires when energy builds off its trough and acceptance pressure appears near a boundary while that armed compression is still valid, and `BREAKOUT` is measured against the frozen boundaries (which are also what the balance plot draws while armed). Arming expires when no balance has re-confirmed within one Range Window, on structure flipping trend-flavored, or after the breakout itself.

### Boundary Quality & Failed Breakouts (v2.5.0)

While a balance is armed, v2 additionally tracks how each frozen boundary is actually being tested: consecutive touches within `Boundary Touch Distance (ATR)` count as one test sequence, deduplicated via `Boundary Test Cooldown` (auto-derived from the Quality Window when left at 0 — a stable boundary shouldn't get credit for a dozen tests just because price sat against it for a dozen bars). Each test's rejection quality measures how far price rotated back toward the range midpoint versus stalling near the edge. A boundary tested at least `Stressed Boundary: Minimum Tests` times with average rejection below `Weak Rejection Threshold` — or matching directional acceptance pressure — counts as under boundary stress; a boundary tested no more than `Fresh Boundary: Maximum Tests` times counts as fresh. `Require Boundary Stress for Ready` (off by default) makes `READY` additionally require that the pressured boundary is under stress, not just that acceptance pressure and energy building line up on their own.

Independently, `Detect Failed Breakouts` (on by default) flags a wick sweep beyond an armed boundary that closes back inside the range by at least `Failed Breakout Re-entry (ATR)`, with opposing bar acceptance. A failed breakout resets that side's breakout-acceptance streak but does not clear the armed range — the frozen boundaries stay valid. It surfaces as a `noTradeReason` (`FAILED_BREAKOUT_UP`/`FAILED_BREAKOUT_DOWN`), a dedicated `FAIL` marker and alert, and a Balance-state dashboard action — a context signal, not an unconditional counter-trade trigger.

### State Confirmation (v2.5.0)

v1's disagreement-streak confirmation counts any bar where the live candidate disagrees with the confirmed state toward confirmation, regardless of which specific alternate candidate is live that bar — alternating candidates that individually never held long enough could combine into a false confirmation for whatever happened to be live on the deciding bar. v2 instead tracks one specific pending target state (`pendingState`) with its own consecutive-bar counter (`pendingStateBars`): a candidate must hold as that exact target for `Confirmation Bars` before it can take over, and switching to a different alternate candidate resets the count. Leaving the current confirmed state is gated by a separate validity check (`currentStateStillValid`, one condition per state — e.g. `BALANCE` requires `establishedBalance` to still hold) instead of piggybacking on that same counter; once that condition has been false for `Confirmation Bars`, the current state is invalidated and can be left even while candidates keep churning between different alternates, so a stale confirmed state can't get stuck indefinitely.

The dashboard is leaner as a result — six rows (Market State, Candidate, Structure, Energy, Acceptance, Action) versus v1's nine, since Structure/Energy/Acceptance are meant to replace the four v1 scores rather than sit alongside them.

Calibration logging uses the same mechanism as v1 but with an `MTE2` event prefix (`MTE2 CONFIG` / `MTE2 CAL` / `MTE2 TRANSITION`). The intended workflow is to run v1 and v2 on the same chart, export each script's separate Pine Log history, and compare state assignments and transition quality by timestamp before deciding whether v2's model earns its way into becoming the new baseline.

Since v2.4.0, `MTE2 CAL` also includes timestamp/symbol, OHLC/ATR, the Range/Trend Structure components, state gates, confirmation/state-duration context, and a dominant `noTradeReason`. This makes the log suitable for outcome analysis instead of only explaining the model to itself. Export the v2 Pine Logs to a CSV file or directory and run:

```bash
python3 scripts/analyze_mte2.py <log-file-or-directory> --out mte2_report.md
```

The report shows state/candidate occupancy, NO_TRADE blocker distribution, gate activation and ATR-normalized forward outcomes over 5/10/20 bars. For the decisive filter test, pass a realized strategy-signal CSV containing `bar` (or timestamp) and `R`:

```bash
python3 scripts/analyze_mte2.py <logs> --signals-csv signals.csv --out mte2_report.md
```

That comparison measures whether allowing only `READY,BREAKOUT,TREND` improves realized expectancy and profit factor versus the unfiltered signals. Override the allowed set with `--allowed-states` when testing a strategy that also trades Balance edges. TradingView maintains a separate Pine Log history per script, so export v1 and v2 separately and join/compare them by timestamp rather than expecting one combined log stream.

A matching Trend Persistence Score transition export can be carried forward and cross-checked at every MTE bar with `--tps-csv <TPS-log.csv>`. Use this only when symbol, timeframe and settings are known to match; TPS transition rows do not contain their own config metadata.

### Reactivity

A second preset, independent of `Preset` (which only resolves lookback lengths): `Reactivity` (`Early` / `Balanced` / `Conservative` / `Custom`) resolves every threshold that decides how readily a state change triggers — `Structure Threshold`, the three `Energy` thresholds, all four `Acceptance` thresholds, and the confirmation/duration bar counts (`Confirmation Bars`, `Minimum State Duration`, `Breakout Acceptance Bars`). `Early` loosens every threshold and shortens every bar count so states change sooner off softer evidence, at the cost of more false starts; `Conservative` does the opposite. `Custom` falls through to the individual `(Custom)`-labeled inputs in their respective groups, exactly like `Preset`'s `Custom` option falls through to the individual length inputs. `Breakout Hold Bars`, `Post-Breakout Balance Lock`, and the `Impulse Aftermath` group are left out of this dial deliberately — they aren't part of "how readily does a state trigger," they're about how long a state is held or how a distinct sub-detector fires.

### Smoothing

`Baseline Type` (`EMA` / `SMA` / `RMA` / `WMA` / `SuperSmoother` / `T3` / `KAMA` / `JMA Approx`) selects the moving-average behind the Quality Baseline — the 8-kernel "Advanced family" pattern used across this repo's `*_advanced` indicators (`rsi_advanced.pine`, `wavetrend_advanced_smoothing.pine`, `cci_advanced.pine`, and others), not the smaller 6-option EMA/RMA/SMA/WMA/HMA/JMA set found in `market_pressure_scale.pine`. SuperSmoother (Ehlers 2-pole filter), T3 (Tillson's triple-smoothed EMA), and KAMA (Kaufman's volatility-adaptive MA) behave meaningfully differently from the plain MA family — not just a different weighting shape, but adaptive lag/noise tradeoffs — which is the point of offering them here. The baseline feeds Structure's trend-cleanliness reading, Acceptance's baseline-displacement component, and the Trend state's close-vs-baseline check, so this one choice ripples through all three scores. `JMA Phase`/`JMA Power` only apply when `Baseline Type = JMA Approx`. Scoped to the baseline only — the internal reference EMAs (ATR, bandwidth, volume, candle averages) stay fixed EMA, matching how the `*_advanced` indicators apply the type selector to the primary/visible calculation rather than every internal helper average.

Thresholds are carried over analogously from v1 where a direct mapping exists (e.g. Structure Threshold ≈ v1's Balance Threshold, Energy High ≈ v1's Trend-quality gates) but are **not yet calibrated** against real data.

Like v1, v2's ratio-based sub-scores (volatility expansion, trend-cleanliness, efficiency, candle commitment, the Exhaustion wick/ATR-spike gates) are ranked against their own recent history (`Rank Window`, same preset-scaled default) rather than fixed constants — see [Timeframe-Adaptive Scoring](#timeframe-adaptive-scoring) above for why. `energyMomentumAccel` is the one exception: it measures a delta of Acceptance, which is already homogenized into a fixed −100..100 range by construction, so only its bar offset (not its scale) needed to become timeframe-relative. Since v2.5.0 it also only rewards *positive* acceleration — flat or declining acceptance magnitude contributes zero instead of the neutral 50 a symmetric ±20 scale previously produced. This pulled the average Energy score down, so the Reactivity-preset Energy thresholds (Low/Very Low/High) were lowered as provisional starting points pending recalibration against the log.
