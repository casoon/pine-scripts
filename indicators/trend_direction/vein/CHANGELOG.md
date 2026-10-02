# Changelog

## Scale precision — 2026-10-02
- `vein_feature_exporter` v0.1.4→0.1.5: Oscillator scale no longer inherits the chart symbol's price precision (values like 80,0000 on 4-decimal symbols such as NATGAS) — shows 2 decimals
- `vein_reversal_score` v0.2.2→0.2.3: Oscillator scale no longer inherits the chart symbol's price precision (values like 80,0000 on 4-decimal symbols such as NATGAS) — shows 2 decimals

## Design decisions — 2026-10-02
- `vein_trend` v0.2.1→0.2.2: the header, the Min Confluence Gate Score / Require Follow-Through tooltips and the README now describe the confluence gate as what it is — a weighted score (Evidence 2.0, Trigger 1.5 + 0.5 + 0.5, Trend 1.0, Quality 1.0 + 0.5) where only the cooldown is a hard veto, not a list of required guards (no gate code change). Follow-through after a Spring/Upthrust is now measured against the event bar's close instead of its wick low/high, like every other structure event.
- `vein_reversal_score` v0.2.1→0.2.2: same follow-through trigger level as `vein_trend` (event bar's close). The event bar's confirmation is latched and fades with the existing decay curve, so a structure event can still count as confirmed on its follow-through bars — CANDIDATE and the ACTION alert are reachable without a second event stacking on top. Setup + confirmation without follow-through is now always PENDING (previously CANDIDATE or EXPIRED once the follow-through window had passed); the EXPIRED status is gone.
- `vein_accumulation_phase` v0.1.4→0.1.5: Range Formation and Volatility Compression are direction-neutral and now count only for the side whose prior trend is weakening (Trend Loss > 0) instead of feeding the accumulation and the distribution score at the same time. The mature-state range check, the phase label and the table show the side's gated values.
- `vein_execution` v0.1.6→0.1.7: Entry Min Micro Score default 7.0→6.0 (provisional) so behaviour and follow-through are no longer de-facto required for an entry. When both setup sources (or both trend sources) are left on their default `close`, they are treated as not connected: the module stays inactive (trend neutral) and the table shows "4H sources not connected" instead of activating both sides on the chart close.
- `vein_exhaustion` v0.3.1→0.3.2: the time-exhaustion grace bar re-arms only after at least two directional bars since the last grace or reset, so a zig-zag no longer grows both counters. The Orderflow Proxy is now symmetric: a bull blow-off bar (bullish, very high volume, large range, close near high; 2.0, mirror of capitulation) and a bear accumulation bar (bullish close with dominant lower wick, high volume, overextended below; 1.5, mirror of distribution) were added, both only with real volume. Blow-off gets a ★ marker above the bar, a table event and an alert.

## Logic fixes — 2026-10-02
- `vein_trend` v0.2.0→0.2.1: the higher-low / lower-high check compared the last swing with itself (the previous swing was copied after the last one had already been overwritten), so it never fired — the previous swing is now shifted first. The climax sequence (CLX → Reacting → Test → Confirmed) now advances at most one stage per bar instead of running through all stages on a single bar, and it actually expires after 20 bars (the expiry check could never be true, so a confirmed climax stayed active until the next climax). A confirmed climax now registers as a new structure event only on the bar it confirms, not on every following bar, so follow-through can be evaluated.
- `vein_reversal_score` v0.2.0→0.2.1: same climax-sequence fixes as `vein_trend` (one stage per bar, working 20-bar expiry, confirmation registers once). The Invalidation alert now fires only when the failed event had reached CANDIDATE before, as documented.
- `vein_structure_zones` v0.3.0→0.3.1: touches are counted per visit (each new entry into the zone) instead of per bar inside it, and the first touch is no longer counted twice. Bounces are counted once per visit as well, so repeated reactions accumulate and the WEAKENING state can be reached. A zone is no longer tested, confirmed or broken on the bar that created it, and a broken zone flips only on a retest at a later bar, not on the break bar itself.
- `vein_accumulation_phase` v0.1.3→0.1.4: sweeps, springs, upthrusts and high sweeps are counted once per event instead of once per bar the condition persists. Accumulation and distribution alerts track their previous state separately, so the distribution alerts no longer fire repeatedly while an accumulation phase is active.
- `vein_pullback` v0.3.0→0.3.1: the structure break is now measured against the swing reference frozen at pullback start (as documented) and no longer requires the EMA trend to still be intact, so a deep pullback that flips the EMAs is still detected as a break. Structure Intact now gives the reduced 1.0 when price is within 1 ATR of that reference (previously this tier was unreachable).
- `vein_reversal_labeler` v0.1.2→0.1.3: first touch wins — once the target is hit, later adverse moves neither cancel the reversal nor count towards MAE.
- `vein_reversal_zones` v2.0.2→2.0.3: same first-touch rule as the labeler. The Trigger Requirement input now works: "2+" requires at least two directional role groups (Structure, Momentum, Trend, MA Trigger) on the same bar. Zone proximity is measured to the zone itself (0 inside it) instead of to its mid, so price at the edge of a wide zone counts as near it.

## Compile fixes — 2026-10-02
- `vein_reversal_zones` v2.0.1→2.0.2: the confluence score referenced an undeclared `relVol` (script did not compile). The Volatility role is now defined as ATR relative to its 50-bar mean (`relVol > 1.2` = expanding volatility); no volume involved.
- `vein_exhaustion` v0.3.0→0.3.1: `bullExhaustRaw`/`bearExhaustRaw` were declared twice (float score sum, then bool signal) — script did not compile. The score sums are now `bullExhaustSum`/`bearExhaustSum`; behaviour unchanged.

## Volume data validity — 2026-09-05
- `vein_trend` v0.1.3→0.2.0 (Überarbeiten): added `volumeIsReal` guard (`syminfo.volumetype`). MFI degrades to `na`; its Setup Score weight (1.0/0.5) is reassigned to RSI so the composite ceiling is unchanged on tick-volume symbols. `relVol` degrades to a neutral 1.0 (no penalty, no shock-bar contribution from the volume leg). Climax detection's volume confirmation becomes pass-through (range-only extreme bar) so the Spring/UT/CLX confirmation cascade keeps functioning without real volume. Dashboard gained a "Volume" row. Data Contract added (`CFD-degraded`).
- `vein_exhaustion` v0.2.3→0.3.0 (Überarbeiten): added `volumeIsReal` guard. MFI's Overextension weight is reassigned to RSI (0.5→1.0) so the 3.0 layer cap is unchanged. Absorption/Capitulation/Distribution (Orderflow Proxy) have no price-only equivalent and now fail closed (never fire) without real volume; the 0-10 composite is rescaled onto the reduced achievable max (8 instead of 10) so `scoreThresh` stays comparable instead of the score silently sinking. Climax-bar volume confirmation degrades to pass-through (range-only extreme bar). Dashboard gained a "Volume" row. Data Contract added (`CFD-degraded`).
- `vein_pullback` v0.2.2→0.3.0 (Überarbeiten): added `volumeIsReal` guard. The Move Weakness (Layer C) volume-spike sub-condition has no price-only equivalent and drops out without real volume; the layer is rescaled onto its reduced max (2 instead of 3) so the 0-3 practical range is unchanged. Dashboard gained a "Volume" row. Data Contract added (`CFD-degraded`).
- `vein_reversal_score` v0.1.4→0.2.0 (Überarbeiten): added `volumeIsReal` guard. MFI degrades to `na`; its Setup Score weight (1.0/0.5) is reassigned to RSI so the composite ceiling is unchanged on tick-volume symbols. `relVol` degrades to neutral 1.0. Climax detection's volume confirmation becomes pass-through (range-only extreme bar) so the Confirmation layer keeps functioning without real volume. The Quality-breakdown Absorption bonus (+15) has no price-only equivalent and fails closed without real volume. Score table gained a "Volume" row (both Light and Debug/Research modes). Data Contract added (`CFD-degraded`).
- `vein_structure_zones` v0.2.2→0.3.0 (Überarbeiten): added `volumeIsReal` guard. MFI degrades to `na`. Volume Profile / POC+Value-Area (Class C, no price-only equivalent) is skipped entirely without real volume — `pocLevel`/`vaHighLevel`/`vaLowLevel` stay `na` instead of profiling tick-count noise as size; the zone-assessment POC-proximity bonus (+7/+3) is consequently unreachable and now explicitly na-guarded (previously compared directly against a possibly-na `pocLevel`/`vaLowLevel`/`vaHighLevel`, undefined behavior even before this change). EVR absorption (`volume/range`, Class C) fails closed without real volume. Climax detection's volume confirmation becomes pass-through (range-only extreme bar). `f_approachQ`'s volume/MFI sub-conditions fail closed instead of comparing against `na`. Added a one-time chart label ("Volume: <type> — ... inactive") on `barstate.islast` when degraded. Data Contract added (`CFD-degraded`).
- `vein_feature_exporter` v0.1.3→0.1.4 (Kennzeichnen): added `volumeIsReal` guard. This module exports raw features for downstream analysis rather than scoring, so MFI/relative-volume now export `na` — never `0` — when volume is not real, so a research script can distinguish "no signal" from "no data". Interpretation text, tooltips, the Debug/Research feature table and the Volume plot-group labels all degrade to explicit "n/a" text instead of rendering `NaN` or comparing against `na`. Data Contract added (`CFD-degraded`).
- `vein_execution` v0.1.5→0.1.6 (Kennzeichnen): added `volumeIsReal` guard. `relVol` (used only as a `> 1.0` sub-condition in the Behaviour role's range-expansion check) degrades to neutral 1.0 when volume isn't real, so that leg never fires on tick-count noise. Also replaced `request.security("", ...)` with `request.security(syminfo.tickerid, ...)` for readability (no functional change — the HTF pivot/EMA/RSI request already reads the chart's own symbol). Data Contract added (`CFD-degraded`).

## Chart-type guard — 2026-09-05
- Added visible warning label when loaded on a non-standard chart (Heikin Ashi, Renko, Kagi, Line Break, P&F, Range) since the underlying strategy's backtest results are invalid there: vein_reversal_labeler v0.1.1→0.1.2

## Alerts bar-close gate — 2026-06-30
- Added a "Alerts only on bar close (confirmed)" toggle (default on) to the vein modules; all alert conditions now respect it (prevents intrabar repaint): vein_accumulation_phase v0.1.2→0.1.3, vein_execution v0.1.4→0.1.5, vein_exhaustion v0.2.2→0.2.3, vein_feature_exporter v0.1.2→0.1.3, vein_pullback v0.2.1→0.2.2, vein_reversal_score v0.1.3→0.1.4, vein_spread_context v0.1.2→0.1.3, vein_structure_zones v0.2.1→0.2.2, vein_trend v0.1.2→0.1.3.

## Alerts standardized — 2026-06-29
- Alerts across the vein modules standardized to `VEIN-* · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged): vein_accumulation_phase v0.1.1→0.1.2, vein_execution v0.1.3→0.1.4, vein_exhaustion v0.2.1→0.2.2, vein_feature_exporter v0.1.1→0.1.2, vein_pullback v0.2→0.2.1, vein_reversal_score v0.1.2→0.1.3, vein_spread_context v0.1.1→0.1.2, vein_structure_zones v0.2→0.2.1, vein_trend v0.1.1→0.1.2.

## vein_trend v0.1.1 — 2026-06-27
- Confluence gate is now role-grouped evidence scoring instead of a flat +1 per heterogeneous guard: Evidence (composite) 2.0, Trigger (structure/follow-through/persistence) 2.5, Trend 1.0, Quality (no-conflict/dominance) 1.5. Structure is weighted but no longer a hard veto. Min Confluence Gate Score input keeps its 1..7 meaning.

## vein_reversal_score v0.1.2 — 2026-06-27
- Combined score is now role-weighted (Setup = momentum/location, Confirmation = structure) via new Setup/Confirmation Role Weight inputs, instead of a flat sum of the two layers. Confirmation outweighs raw setup by default (1.3 vs 1.0).

## vein_execution v0.1.3 — 2026-06-27
- Fix: file now compiles. `htfEma20` and `htfRsi` (used in the 4H reference overlay and interpretation line) were referenced but never defined — now requested from the HTF via `request.security` (4H EMA20 / RSI14). The `htfTrendUp`/`htfTrendDown` source plugs were used directly as booleans (type error) — now compared `> 0`.

## vein_execution v0.1.2 — 2026-06-27
- Removed the duplicated internal setup score: the 4H setup is now consumed once as activation/context evidence (single score path) rather than re-derived as a parallel role. Micro score is fully role-weighted (Evidence 3 / Structure 4 / Behaviour 2 / Tempo 1).
- Entry signals converted from a hard AND chain to evidence scoring: a 15m structure trigger fires the timing, and the role-weighted micro score must clear the new Entry Min Micro Score threshold. Behaviour/follow-through contribute weight instead of vetoing.
- Distance to 4H swing levels is now a dashboard-only diagnostic and no longer feeds the score (pivot-proximity removed from the signal path).

## vein_reversal_zones v2.0.1 — 2026-06-11
- Fix: data-window plot "Reversal Label" now uses the actual evaluation offset — it was misaligned when Forward Bars > Extended Bars.

## vein_reversal_labeler v0.1.1 — 2026-06-11
- Fix: data-window plots (Reversal Label, Timing) now use the actual evaluation offset — they were misaligned when Forward Bars > Extended Bars.
- Fix: research table was re-created on every realtime update of the last bar (resource leak).
- Fix: research table showed hardcoded "v0.2" although the script header said 0.1.
- Research table restyled to the suite light-theme convention (was dark #1a1a2e with white text).

## vein_feature_exporter v0.1.1 — 2026-06-11
- Fix: research table and interpretation table were re-created on every realtime update of the last bar — now created once and reused (resource leak).

## vein_spread_context v0.1.1 — 2026-06-11
- Fix: status table was re-created on every realtime update of the last bar — now created once and reused (resource leak).

## vein_exhaustion v0.2.1 — 2026-06-11
- Fix: multi-line ternaries with series values rewritten as if/else (Pine v6 compile error CE10156) — time scores, background tint, table status labels. No behavior change.

## v0.1
- Initial release
