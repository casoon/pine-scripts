# Changelog

## v1.0.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.0.1 — 2026-06-29
- Alerts: messages standardized to `CFT · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.0 — 2026-06-18
- Initial release
- Manual MFI with pluggable smoothing (EMA, SMA, RMA, WMA)
- CCI confirmation layer normalized to MFI scale for visual alignment
- 4-state flow background: bull/bear expansion vs. accumulation/distribution
- 4-state color-coded MFI histogram
- Extreme-zone reversal signals with optional CCI gate
- Midline confirmation dots (MFI crosses 50 with aligned CCI)
- Gradient MFI line color (bull at OS, bear at OB)
- Fill between MFI and signal line
- Alert conditions for all signal types