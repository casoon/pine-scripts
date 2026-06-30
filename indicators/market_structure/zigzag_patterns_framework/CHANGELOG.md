# Changelog

## v1.0.4 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.0.3 — 2026-06-29
- Alerts: messages standardized to `ZPF · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.0.2 — 2026-06-27
- Decoupled momentum from structure: RSI-divergence is now a separate optional annotation (input "RSI Divergence Markers (annotation only)", `showMomentumDiv`, default off) that only adds a marker — it no longer contributes to the smart-label signal count or alters the structural HH/LH/HL/LL pivot label

## v1.0.1 — 2026-06-11
- Fixed script not compiling: removed invalid `return` statements (Pine has no `return` keyword), split comma-separated variable declarations, restructured early-exit guards into if-blocks
- Fixed `f_make_smart_label()` being called before its definition — drawing and pattern scans now run in one block after all function definitions
- Guarded the previous-pivot lookup loop against a negative start index

## v1.0.0
- Initial release
