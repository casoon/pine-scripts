# Changelog

## v2.8.0 — 2026-07-23
- Change: `f_findBestAnchor` no longer takes the first ("nearest") qualifying candidate from the same-type pivot history window — it now scores every qualifying candidate and picks the highest-scoring one. Score components: recency (40%, dominant — keeps the result close to the prior nearest-qualifying behavior as a baseline), oscillator rate-of-change per bar relative to its own rolling StDev (30%, not raw magnitude — deliberately avoids reintroducing the v2.4.0 regression where raw oscillator-difference magnitude systematically favored distant pivots), extreme-zone context of the candidate (20%), and price distinctness relative to ATR tolerance (10%, minor tie-breaker). New debug log fields `anchorScore` and `oscStDev` make the score independently verifiable.
- Add: `scripts/verify_pms_logs.py` Rule 9 now recomputes the same weighted score (mirrored in Python, including the `upperExtreme`/`lowerExtreme` lookup by oscillator type) instead of a plain nearest-qualifying scan, and additionally cross-checks the logged `anchorScore` against the recomputed one.
- Change: Status dashboard split into two blocks — "Latest Pivot" (oscillator type, pivot type, price/momentum structure, new "Pivot Age" row) always reflects the most recently confirmed pivot; "Latest Event" (status, renamed "Event Age", anchor) reflects the most recently fired divergence/alignment event. Previously these were mixed into one flat table with no indication that "Price"/"Momentum" and "Status"/"Age" could refer to different points in time — the two blocks make that legitimate mismatch (documented in README "Anchor Selection") visible instead of implicit.
- Docs: README "Anchor Selection" rewritten to describe the scoring model instead of "nearest qualifying"; feature bullets and header comment updated to match.

## v2.7.0 — 2026-07-17
- Add CMO (Chande Momentum Oscillator) as an oscillator source: `100 * (SumUp - SumDown) / (SumUp + SumDown)` over `CMO Length`, bounded ±100, OB/OS ±50, midline 0. Uses the shared `Source` input like RSI/Stochastic RSI/TSI. Configurable `CMO Signal Line` (SMA). MFI was considered and rejected — CFD/index feeds (Capital.com, FOREX.com, the exact kind used to test this indicator) report `volume=0` throughout, which would make a volume-weighted oscillator produce no real signal, not just a degraded one.

## v2.6.2 — 2026-07-17
- Verified a second, fresh 6844-row/8-file log export against `scripts/verify_pms_logs.py`'s full rule set (including the new priceStruct/anchor-search re-derivation from raw logged data): 2 discrepancies found, both traced to `priceTolerance` being logged with `format.mintick` — which rounds a continuous computed value (`pivotAtr × Min. Price Difference ATR`) to the instrument's tick size, occasionally making a genuinely-past-tolerance price difference look exactly boundary-equal in the log. Not a calculation bug (confirmed by inspecting the two flagged rows directly). Fixed the log format to 8 decimals so this can't recur; re-verify with a fresh export to confirm 0/6844.

## v2.6.1 — 2026-07-17
- Verified: exported and cross-checked 6046 `PMS PIVOT` log rows across 8 symbol/timeframe combinations against the divergence/confirmation calculation logic (mutual exclusivity of directional flags, gate implications, anchor arithmetic, anchor-history integrity) — 0 issues found. Validation tooling: `scripts/verify_pms_logs.py`.
- Extend debug log with `priceTolerance`, `prevPrice`, `prevOsc`, `allowEqual`, `minOscDiff`, `minPivotDist`, `maxPivotDist`, and the full same-type pivot history window (`histIdx`/`histPrice`/`histOsc`, `|`-separated) — enables independently recomputing the HH/HL/LH/LL price-structure classification and re-deriving the "nearest qualifying" anchor search from raw logged data, not just checking a row's internal consistency. Needs a fresh log export to use (older exports lack these fields; the validator detects and skips the extra checks for them).

## v2.6.0 — 2026-07-17
- Revert: default "Oscillator Anchor" back to "Exact Pivot Bar". Switching the default to "Local Extreme" (v2.5.1) coincided with visibly fewer divergence signals on live testing — plausibly because Local Extreme changes the *values* fed into the divergence math (not just where things are drawn), and that wasn't verified before defaulting to it. Correctness of the underlying calculation takes priority over the line always visually touching an oscillator peak; "Local Extreme" stays available as an explicit opt-in once verified.
- Add: "Enable Debug Logging" toggle (off by default, new Debug input group). When on, every confirmed pivot logs a `PMS PIVOT` line to the Pine Logs panel — price/oscillator values, structure classification, the anchor found (if any) with its distance/price/oscillator value, every raw boolean the divergence/confirmation math is built from (priceMadeHigher/Lower, oscMadeHigher/Lower, extreme-zone/trend-context gates), and the final signal flags. Exportable as CSV for offline verification — same purpose as the WT4 strategy's Pine-log-based testing workflow, adapted for this indicator.

## v2.5.1 — 2026-07-17
- Default "Oscillator Anchor" changed from "Exact Pivot Bar" to "Local Extreme". Matches the expectation set by price pivots (which are found by searching the price series for its own local extreme, so they always land exactly on one) — the oscillator side now gets the same treatment via its own local-extreme search, instead of just borrowing whatever value the oscillator happened to have on the price-pivot bar. "Exact Pivot Bar" is still available for users who want the strictest possible timing alignment with price over the always-touches-a-peak visual.

## v2.5.0 — 2026-07-17
- Fix: `Oscillator Anchor: Local Extreme` only swapped the oscillator *value* (borrowing the local high/low from a nearby bar) while keeping the label/line drawn at the price-pivot bar's x-position — so the point no longer sat on the plotted oscillator curve at all. Now tracks the actual bar the local extreme occurred on and draws oscillator-pane labels/lines (structure label, oscillator divergence line, guide line) at that bar instead, so they land exactly on a real peak/trough of the curve. Price-chart labels/lines are unaffected — they still use the true price-pivot bar, since they display price, not momentum.
- Note: in "Exact Pivot Bar" mode (the default), a divergence line's endpoint can still legitimately land mid-slope rather than at a visible peak/trough of the oscillator — that's the value read exactly on the price-pivot bar, which is the whole point of that mode's stricter timing guarantee. Switch to "Local Extreme" if the always-touches-a-peak visual is preferred over exact-bar timing.

## v2.4.0 — 2026-07-17
- Fix: `f_findBestAnchor` selected the candidate with the *largest* valid oscillator difference across the whole stored window, which systematically favored distant pivots — oscillators mechanically have more room to diverge the more bars separate two points, so "largest difference" kept reaching for the oldest pivot in range rather than the most relevant one. Observed on NATGAS 1H: a "Bullish Divergence" anchored 113 bars back, producing a divergence line stretching across nearly the whole visible chart. Now scans backward from the most recent stored pivot and takes the *first* one that clears the price- and oscillator-difference gates — matches the original intent (skip a too-similar/noisy intermediate pivot) without the distance bias.
- Docs updated throughout to describe the corrected "nearest qualifying" selection instead of "largest magnitude".

## v2.3.1 — 2026-07-17
- Default "Pivot Markers on Main Chart" and "Divergence Lines on Main Chart" to on. The oscillator-pane label/line Y-position is always the oscillator's value on the pivot bar, not a visual high/low — which reads as "wrong" at a glance (e.g. an "LL" label sitting near the top of the oscillator curve). Showing the same structure on the price chart, at actual price levels, resolves that without changing any signal logic. `Oscillator Anchor: Local Extreme` was considered as an alternative but rejected — it would trade one visual confusion for a selection-bias distortion (always picking the most favorable nearby oscillator reading inflates apparent divergence strength) and for a worse one (the label would no longer sit on the plotted oscillator curve at all).

## v2.3.0 — 2026-07-16
- Add "Anchor" dashboard row and pivot-label tooltip note showing how many bars back the divergence/alignment anchor was, and whether it differs from the immediately preceding pivot. Clarifies a real point of confusion: the Price/Momentum structure labels always reflect the immediately preceding pivot, but the fired event (e.g. "Hidden Bearish") can be anchored to an older pivot from the best-of-window search — so the two can legitimately look inconsistent at a glance (e.g. "Price: EH" next to "Status: Hidden Bearish") without this being a bug.

## v2.2.0 — 2026-07-16
- Add Divergence Quality Score (0-100, informational only, never gates a signal), matching `oscillator_divergence_zones`'s approach: averages pivot spacing (relative to Min/Max Pivot Distance), oscillator-difference magnitude (relative to the oscillator's own rolling standard deviation), extremity past the active OB/OS boundary, and trend context (overextension for regular divergence, alignment for hidden divergence, using the same Trend EMA as the Trend Context Filter). Shown as a suffix on the divergence label and dashboard status (e.g. "Bearish Divergence 78"). Toggle: "Show Divergence Quality Score" (default on).

## v2.1.1 — 2026-07-16
- Fix: dashboard table didn't follow the repo's mandated light-theme table style (project CLAUDE.md "Dashboard table style", reference `vein_trend.pine`) — `table.new()` was missing `bgcolor`/`border_color`/`frame_color`/`frame_width`, and cells used ad-hoc colors instead of the standard `tc`/`hd` constants. Header row was purple-tinted (oscillator accent color) instead of the neutral light-gray header background used across every other indicator's dashboard.

## v2.1.0 — 2026-07-16
- Add optional Trend Context Filter for hidden divergences (off by default), matching `oscillator_divergence_zones`'s approach: hidden bullish only fires when the pivot low is above a Trend EMA, hidden bearish only when the pivot high is below it. Hidden divergences are continuation signals — without this, they can fire repeatedly during chop or against the prevailing trend with no structural backing (observed on NATGAS 4H: repeated Hidden Bullish tags through a declining/ranging stretch that then broke down hard).

## v2.0.2 — 2026-07-16
- Fix: CE10271 compile error — `f_safeDivide` was defined in the Helper Functions section, which the v2.0 reorg placed after Oscillator Calculations, but the Stochastic RSI calculation already calls it there. Pine requires strict textual order for function definitions before their call site. Moved `f_safeDivide` to just before Oscillator Calculations.

## v2.0.1 — 2026-07-16
- Fix: alerts had no bar-close gate — `ta.pivothigh`/`ta.pivotlow` confirmation still depends on the currently forming bar until it closes, so a signal could fire intrabar and then flip. Added an "Alerts only on bar close (confirmed)" toggle (default on) gating every `alertcondition()`.
- Fix: alert messages were full sentences with no `{{ticker}} {{interval}}`, making them unattributable across parallel charts. Switched to the repo's message canon `PMS · EVENT · {{ticker}} {{interval}}`; registered `PMS` in `indicators/ALERT_KUERZEL.md`.
- Add: dedicated "Alerts" input group.

## v2.0.0 — 2026-07-16
- Fix: "Allow Near-Equal Price Pivots" was over-applied — a near-equal pivot could feed hidden divergence and momentum alignment too (via an in-place override of the higher/lower-price flags), not just regular divergence as intended. Near-equal pivots now only ever qualify as an additional OR-condition on the regular-divergence price check; the underlying higher/lower flags are no longer overridden, so hidden divergence and alignment naturally stay unaffected by near-equal pivots.
- Fix: the HH/HL/LH/LL structure label used an exact price comparison while the divergence logic used an ATR tolerance, so the displayed label could contradict the fired signal (e.g. label says "LH" while the divergence engine treats the same pivot as effectively unchanged). `f_structureHigh`/`f_structureLow` now take an explicit tolerance, using the same ATR-based tolerance as the divergence logic for price, and 0.0 (unchanged, exact) for the oscillator-structure label.
- Add: best-of-window anchor search — divergence/alignment comparisons now search up to the last 8 same-type pivots (within Min/Max Pivot Distance) and pick the one with the largest valid oscillator difference, instead of always comparing against only the immediately preceding pivot. The HH/HL/LH/LL structure label still always uses the immediately preceding pivot (unchanged, standard swing terminology) — only the divergence/alignment math uses the searched anchor. Divergence connector lines now draw from the actual anchor pivot to the current one.
- Add: optional "Local Extreme" oscillator anchor mode — reads the oscillator's own local high/low within a small radius of the price-pivot bar instead of its exact value on that bar, reducing false divergences from price/oscillator peak mistiming.
- Add: Structure Presets (Scalping / Intraday / Swing / Position / Major Structure / Custom) — set Pivot Left/Right, Min/Max Pivot Distance, and the ATR price filter together based on the swing size to detect. Default preset is Swing (8/8, matching the prior 1.2.1 manual default closely).
- Add: Oscillator Difference Mode — Reference Range % (renamed from the 1.2.0 percentage filter), Standard Deviation (adapts to the oscillator's own rolling volatility), or Off.
- Add: configurable signal-line length for CCI, TSI, and Williams %R (previously hardcoded to 9/7/9).
- Add: dashboard now shows the latest pivot type (High/Low) and the event's age in bars since confirmation.
- Rename: "Momentum Confirmation" → "Momentum Alignment" throughout (input, color, event text, alert titles) — the old name read too much like a trade trigger for what is structure agreement, not a signal that price will continue.
- Clarify: "Source" input tooltip now states it only applies to RSI/Stochastic RSI/TSI; "Max Drawings" renamed to "Max Drawings (per Type)" with a tooltip noting lines and labels are tracked separately (total objects can be up to double the set value).
- Cleanup: removed unused `f_isHigher`/`f_isLower` helpers and an unused `centerPlot` variable.
- Not included in this pass (tracked as known limitations, see README): divergence quality score, setup/trigger/invalidation lifecycle.

## v1.2.2 — 2026-07-16
- Fix: oscillator pane scale was inheriting the chart symbol's price precision (e.g. showing "80,0000" on a 4-decimal NATGAS feed instead of a clean "80") because `indicator()` didn't declare an explicit format. Now sets `format=format.price, precision=2`, matching `oscillator_divergence_zones`.

## v1.2.1 — 2026-07-16
- Default oscillator changed from WaveTrend to RSI, to match `oscillator_divergence_zones`'s default for a fairer side-by-side comparison
- Default Pivot Left/Right raised from 5/5 to 7/7, and Minimum Pivot Distance from 5 to 10 — reduces noisy intermediate pivots feeding the divergence comparison until the "compare against a window of prior pivots, not just the immediately preceding one" improvement lands

## v1.2.0 — 2026-07-16
- Fix: "Allow Near-Equal Price Pivots" was practically inert — the price-difference gate required `diff >= tolerance` while the equal-pivot check required `diff <= tolerance`, so the two could only both be true exactly at the boundary. The equal-pivot case is now an explicit OR-branch of the price-difference gate.
- Fix: `bullishConfirmation`/`bearishConfirmation` are shared globals written by both the high- and low-pivot blocks; on the rare bar where a candle is simultaneously a confirmed high and low pivot, the low-pivot block silently overwrote the high-pivot block's result (including its alert). Each block now sets its own local flag and OR-combines it into the global.
- Change: "Min. Oscillator Difference" is now expressed as a percentage of the active oscillator's OB-OS range instead of one flat absolute value — a fixed 2.0 was meaningless for Fisher (±1.5 range) and negligible for CCI (±100 range) once more oscillator types were added.

## v1.1.1 — 2026-07-16
- Translate all input labels, tooltips, group names, dashboard text, and alert messages from German to English (script was originally drafted with German UI strings)

## v1.1.0 — 2026-07-16
- Add CCI, Fisher Transform, TSI, and Williams %R as additional oscillator sources (ROC intentionally excluded — unbounded, no adaptive-band system to give it a meaningful extreme zone)
- Fix: divergence label no longer overlaps the structure label at the same pivot (opposite label direction instead of the same anchor point)
- Fix: momentum confirmation status color is now consistent regardless of whether it was triggered from a high or low pivot (always `confirmationColor`)
- Dashboard: smaller text size, tucks tighter into the top-right corner

## v1.0.0 — 2026-07-16
- Initial release: RSI / WaveTrend / Stochastic RSI oscillator, price-pivot-anchored HH/HL/LH/LL structure on both price and oscillator, regular + hidden divergence, momentum confirmation, quality filters, dashboard, alerts
