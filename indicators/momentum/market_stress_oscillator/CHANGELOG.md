# Changelog

## v1.0.4 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.0.3 — 2026-06-29
- Alerts: messages standardized to `MSO · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.0.2 — 2026-06-27
- ADX demoted to a quality/strength grade only — it never suppresses a WVF stress/reversal event. Added a continuous `adxGrade` (0..1) surfaced on peak-label tooltips; the reversal stress trigger now fires regardless of ADX, including in strong-trend phases
- JMA trend alignment is no longer a hard requirement on the trigger. New "Require trend alignment for trigger" input (default off): by default a stress extreme triggers on its own (a trend filter must not block the reversal); turn on for with-trend pullback mode

## v1.0.1 — 2026-06-11
- Fix: bias line color rewritten from a multi-line ternary to a single line (Pine v6 compile error CE10156)
- Preset summary table restyled to the standard light theme; cleared via table.clear when hidden instead of writing empty cells
- Removed duplicated calculateJMA_wind helper — HTF wind bias now uses the shared calculateJMA (identical math, separate call-site state)

## v1.0.0
- Initial release
