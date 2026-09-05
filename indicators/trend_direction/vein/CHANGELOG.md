# Changelog

## Volume data validity — 2026-09-05
- `vein_trend` v0.1.3→0.2.0 (Überarbeiten): added `volumeIsReal` guard (`syminfo.volumetype`). MFI degrades to `na`; its Setup Score weight (1.0/0.5) is reassigned to RSI so the composite ceiling is unchanged on tick-volume symbols. `relVol` degrades to a neutral 1.0 (no penalty, no shock-bar contribution from the volume leg). Climax detection's volume confirmation becomes pass-through (range-only extreme bar) so the Spring/UT/CLX confirmation cascade keeps functioning without real volume. Dashboard gained a "Volume" row. Data Contract added (`CFD-degraded`).
- `vein_exhaustion` v0.2.3→0.3.0 (Überarbeiten): added `volumeIsReal` guard. MFI's Overextension weight is reassigned to RSI (0.5→1.0) so the 3.0 layer cap is unchanged. Absorption/Capitulation/Distribution (Orderflow Proxy) have no price-only equivalent and now fail closed (never fire) without real volume; the 0-10 composite is rescaled onto the reduced achievable max (8 instead of 10) so `scoreThresh` stays comparable instead of the score silently sinking. Climax-bar volume confirmation degrades to pass-through (range-only extreme bar). Dashboard gained a "Volume" row. Data Contract added (`CFD-degraded`).
- `vein_pullback` v0.2.2→0.3.0 (Überarbeiten): added `volumeIsReal` guard. The Move Weakness (Layer C) volume-spike sub-condition has no price-only equivalent and drops out without real volume; the layer is rescaled onto its reduced max (2 instead of 3) so the 0-3 practical range is unchanged. Dashboard gained a "Volume" row. Data Contract added (`CFD-degraded`).
- `vein_reversal_score` v0.1.4→0.2.0 (Überarbeiten): added `volumeIsReal` guard. MFI degrades to `na`; its Setup Score weight (1.0/0.5) is reassigned to RSI so the composite ceiling is unchanged on tick-volume symbols. `relVol` degrades to neutral 1.0. Climax detection's volume confirmation becomes pass-through (range-only extreme bar) so the Confirmation layer keeps functioning without real volume. The Quality-breakdown Absorption bonus (+15) has no price-only equivalent and fails closed without real volume. Score table gained a "Volume" row (both Light and Debug/Research modes). Data Contract added (`CFD-degraded`).
- `vein_structure_zones` v0.2.2→0.3.0 (Überarbeiten): added `volumeIsReal` guard. MFI degrades to `na`. Volume Profile / POC+Value-Area (Class C, no price-only equivalent) is skipped entirely without real volume — `pocLevel`/`vaHighLevel`/`vaLowLevel` stay `na` instead of profiling tick-count noise as size; the zone-assessment POC-proximity bonus (+7/+3) is consequently unreachable and now explicitly na-guarded (previously compared directly against a possibly-na `pocLevel`/`vaLowLevel`/`vaHighLevel`, undefined behavior even before this change). EVR absorption (`volume/range`, Class C) fails closed without real volume. Climax detection's volume confirmation becomes pass-through (range-only extreme bar). `f_approachQ`'s volume/MFI sub-conditions fail closed instead of comparing against `na`. Added a one-time chart label ("Volume: <type> — ... inactive") on `barstate.islast` when degraded. Data Contract added (`CFD-degraded`).
- `vein_feature_exporter` v0.1.3→0.1.4 (Kennzeichnen): added `volumeIsReal` guard. This module exports raw features for downstream analysis rather than scoring, so MFI/relative-volume now export `na` — never `0` — when volume is not real, so a research script can distinguish "no signal" from "no data". Interpretation text, tooltips, the Debug/Research feature table and the Volume plot-group labels all degrade to explicit "n/a" text instead of rendering `NaN` or comparing against `na`. Data Contract added (`CFD-degraded`).

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
