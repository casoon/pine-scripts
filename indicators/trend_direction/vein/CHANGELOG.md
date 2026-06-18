# Changelog

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
