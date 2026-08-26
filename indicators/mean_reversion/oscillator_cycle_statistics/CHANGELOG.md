# Changelog

## v1.5.2 — 2026-08-26
- Corrected Klinger Volume Force and flat-bar trend handling to match the documented formula; invalid Fast/Slow EMA ordering now stops with an explicit configuration error
- Marked MFI as volume-dependent and made zero-volume windows explicitly neutral instead of relying on an undefined money-flow ratio
- Smoothed classic Stochastic %K with the shared K smoothing input while keeping normalized Williams %R explicitly tied to raw Fast %K
- Added oscillator-specific default zones (80/20 for Stochastic-family oscillators and MFI; 70/30 for RSI, DeMarker, and reference-normalized oscillators), with optional custom levels
- Unified straight-line and failure-polyline history under one displayed-cycle cap, declared the Pine polyline limit explicitly, and made reverted failures dashed
- Reverted-failure V-shapes now use the exact bar of maximum cycle progress instead of combining an exact level with a bucket-approximated timestamp
- Added validation for inverted Opportunity zones and removed 100% from the allowed Opportunity range so completion bars cannot emit reversed-direction opportunity markers
- Made dashboard state labels respect configured OB/OS levels before the fixed neutral bands

## v1.5.1 — 2026-08-26
- Fixed RVI: the raw ratio was divided by an extra, asymmetric `* 6.0` on the denominator side only (`rviNumSmooth / (rviDenSmooth * 6.0)`). The (1,2,2,1) weights sum to 6 on both numerator and denominator identically, so that factor cancels in the ratio and dividing it in on one side only shrank the raw value to about 1/6 of its true magnitude — never close enough to the default `rviReference` (0.3) to leave the neutral zone, so RVI never crossed into overbought/oversold and never produced a cycle. Now `rviNumSmooth / rviDenSmooth`, no extra factor

## v1.5.0 — 2026-08-26
- Added four oscillator choices: DeMarker (natively 0..100, no reference input needed), RVI (Relative Vigor Index, normalized like CCI/WaveTrend via a configurable reference), EOM (Ease of Movement), and Klinger Volume Oscillator (its own Fast/Slow EMA length inputs, since a meaningful spread needs two genuinely different periods, unlike every other oscillator here)
- EOM and Klinger are volume-dependent. On zero-volume feeds (Capital.com, FOREX.com, and other CFD/index feeds commonly used for commodities — the exact instruments this indicator has been tested against) both collapse to a constant neutral 50: no crash, no na-cascade, but also no cycles ever detected on that feed. Flagged in the dropdown label and a tooltip, not silently

## v1.4.2 — 2026-08-26
- Fixed reverted-failure cycle lines rendering as invisible: a straight `line.new()` from origin back to origin has identical start/end Y, making it perfectly horizontal and camouflaged against the OB/OS gridline it sits exactly on. Reverted failures now draw a 3-point V-shape polyline (origin → deepest point the attempt actually reached, bucket-approximated → back to origin) via `f_cycleFailurePeak()`, which is both visible and more informative than a straight line ever was. Timeout failures keep the simple line — their endpoint is wherever the oscillator actually was, never forced onto the origin rail, so they were never camouflaged
- Failure V-shapes were initially created solid and, because polylines have no `set_color`/`set_width` setters, were capped by simple eviction rather than fading like the mutable success/timeout `line` objects

## v1.4.1 — 2026-08-26
- Fixed a look-ahead bug in the Brier Skill Score: the naive direction-base-rate benchmark was re-derived from today's base rate for every historical calibration record, letting the naive competitor see hindsight the live model never had. The base rate is now snapshotted at forecast-capture time (`capturedBaseRate`) alongside the forecast itself and stored per calibration record (`calibNaivePredicted`), so both sides of the comparison use the same information horizon
- Made the live label use the exact same gates as the Opportunity marker (sample size, Wilson CI width, progress zone) instead of only checking Edge — the label could previously claim OPPORTUNITY in situations (too late, too uncertain) where the marker itself would refuse to fire
- Added STALLED (age past the historical median completion duration) and UNCERTAIN (Wilson interval still too wide) to the label's state vocabulary, alongside the existing LOW DATA / LATE / OPPORTUNITY / WATCH / WAIT; the Expected Target Time projection is no longer drawn once a cycle is STALLED — it previously collapsed into a near-vertical line to the target on the current bar, which read as "arriving now" instead of "overdue"
- Cycle Start and Success/Failure markers now default off (`Show Cycle Start Markers`, `Show Success/Failure Markers`) — outcome is already encoded in the completed line's color/style, so they added no information over the zigzag itself; `Show Opportunity Markers` (default on) is the one marker meant to draw the eye

## v1.4.0 — 2026-08-26
- The statistics now drive the geometry instead of only annotating it. Five changes, no new statistical model:
- Replaced the raw `BULL 100.0% · n1`-style label with `UP/DOWN CYCLE` + `Edge` (Conditional minus the direction's plain base rate) + a WAIT/WATCH/OPPORTUNITY state word; below the sample minimum it reads only `LOW DATA` — a thin sample can no longer look like a strong signal
- Added a once-per-cycle Opportunity marker (▲/▼), evaluated at progress-bucket crossings inside a configurable zone (default 30–65%), gated on Edge ≥ threshold, sample size ≥ `Minimum Conditional Samples`, and Wilson interval width ≤ a configurable cap — a cycle that's already mostly done no longer qualifies just because its raw completion number looks good
- Added a dashed Expected Target Time projection from the live point to `bar_index + median remaining duration` at the target extreme — a time projection, explicitly not a price forecast
- Recent completed-cycle lines (`Prominent Recent Cycles`, default 25) stay full color; older ones (within `Max Displayed Cycle Lines`) fade to a much lighter shade, so the current cycle doesn't visually compete with a wall of history
- (Carried over from the color/width pass) cycle lines stay royal blue/gray by outcome, width scaled by `cycleMaxProgress`

## v1.3.0 — 2026-08-26
- Visualization rewrite. No statistical model changes — presentation only.
- Removed the second progress plot; replaced it with cycle zigzag lines drawn directly on the oscillator (origin extreme → resolution), solid for completed successes, dashed for failures/timeouts, and a live line tracking the active cycle to the current bar
- Added a target marker at the cycle's target extreme while a cycle is active, and an on-chart probability label (`XX% · nNN`) attached to the live line's current endpoint — computed independently of the dashboard table, so it works with any Dashboard Detail setting
- Reduced event markers from four (start implied, success, failure, timeout-cross) to three explicit ones: Cycle Start, Cycle Success, Cycle Failure — timeout is now visually distinguished by the dashed line landing off the extreme rail rather than by a separate marker shape
- `Shade Active Cycle` background now defaults off — the cycle line carries that information more clearly than a background tint
- Added a `Visual` dashboard mode (single confirmation-tag row) as the new default; renamed `Detailed` to `Research`; `Compact` unchanged
- Added `Max Displayed Cycle Lines` input to cap the rolling window of drawn completed-cycle lines
- Colored the cycle lines by outcome instead of gray-on-gray, so the zigzag pattern itself reads as the historical completion rate — royal blue for success, light gray for failure, deliberately not red/green since a cycle's own success/failure isn't a bullish/bearish price call; line width scales with `cycleMaxProgress` (successes are always full width, failures thin out the earlier they reverted) as a second, continuous "how far did it get" signal
- Colored the on-chart probability label by the same green/red/gray/blue tiers as the dashboard's Conditional row instead of a fixed blue, and prefixed it with BEAR/BULL (matching the existing short/long convention behind the MFE/MAE price tracking) so the label states a price direction, not just "OB -> OS"

## v1.2.0 — 2026-08-26
- Fixed the Reliability checkpoint capture: it now snapshots the forecast at the exact configured `calibCheckpoint` progress instead of the cycle's peak progress reached at capture time, so a bucket labeled "at 50%" actually contains only forecasts made at 50%, not a mix of whatever progress the cycle had jumped to intrabar
- Separated cycle-stage classification (EARLY/DEVELOPING/MATURE/LATE, and the Compact dashboard's Progress row) to use current progress instead of peak progress reached; historical-evidence conditioning (the Conditional statistic itself) continues to use peak progress, since that's the correct comparison against fully-resolved historical cycles
- Added a naive direction-base-rate Brier score and a Brier Skill Score (`1 - modelBrier/naiveBrier`) to the Reliability table, so the paired base/regime comparison has an actual floor to beat instead of only comparing against itself

## v1.1.2 — 2026-08-26
- Restored compact-dashboard and Reliability text from `size.tiny` to Retina-readable `size.small`; compact table structure remains unchanged

## v1.1.1 — 2026-08-26
- Added a compact two-column, eight-row dashboard as the default and retained the previous full table as optional `Detailed` mode
- Initially switched compact and Reliability tables to tiny text
- Disabled the Reliability table by default
- Collapsed Reliability to one collection-status row until its sample minimum is reached

## v1.1.0 — 2026-08-26
- Restricted walk-forward reliability samples to the current Medium lookback
- Replaced bucket-only calibration output with average forecast, observed rate, error in percentage points, and sample size
- Added base Brier score and a paired base/regime Brier comparison; regime improvement is withheld below the configured paired-sample minimum
- Reframed the dashboard as cycle stage and evidence rather than trade permission; fresh entries and price exits are explicitly marked as not validated
- Added failed-cycle MFE alongside failed-cycle MAE
- Added separate OB → OS and OS → OB base rates to expose directional asymmetry
- Renamed normalized Williams %R to make its equivalence to Stochastic %K explicit

## v1.0.0 — 2026-08-25
- Initial release: OB → OS / OS → OB cycle state machine (origin/armed/success/failure/timeout) with persistent per-cycle sample storage
- Progress-conditioned and regime-conditioned completion probability, Recent/Medium/Long lookback comparison
- Descriptive Wilson interval and explicit minimum-sample status
- Median time-to-target and price MFE/MAE (ATR) statistics for successful cycles, plus failed-cycle MAE
- Time-consistent age/progress conditioning in 10-percentage-point buckets: matching historical cycles must have reached the bucket by the queried age and remained unresolved beyond it
- Walk-forward calibration table: buckets the exact live Conditional prediction snapshotted mid-cycle against actual outcomes and excludes predictions below the configured sample minimum
- Initial conservative dashboard readout for overall context, entry timing, position management, and evidence risk
- Compact dashboard layout: Wilson interval merged into Conditional and Recent/Medium/Long condensed into one lookback row
- RSI, Stochastic RSI, Stochastic, Williams %R, MFI, CCI, WaveTrend oscillator selection (Stochastic RSI/Stochastic via `ta.stoch()`)
- Dashboard, cycle progress plot, event markers, alerts for success/failure/timeout
- Light-theme dashboard table per repo convention (status cells only where a discrete state exists)
