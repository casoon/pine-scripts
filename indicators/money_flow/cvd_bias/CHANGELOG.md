# Changelog

## v1.1.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.1.1 — 2026-06-29
- Alerts: messages standardized to `CVDB · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.1 — 2026-06-11
- 4 alert conditions added: Bull/Bear Divergence, CVD zero cross up/down
- na-volume bars now count as 0 instead of breaking the rolling CVD sum for the full window
- Internal: dashboard state ternary rewritten as if/else for Pine v6 compatibility

## v1.0 — 2026-05-16
- Initial release
- Per-bar delta: (2 × close_location − 1) × volume
- Rolling CVD: sum over configurable window, normalized to −1..+1 via recent amplitude
- CVD rate of change (ROC) as acceleration line
- Price/CVD divergence: price making a new N-bar extreme while CVD rate opposes
- Dashboard: state, CVD value, rate direction, divergence
