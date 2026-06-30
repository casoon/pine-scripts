# Changelog

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
