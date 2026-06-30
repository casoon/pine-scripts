# Changelog

## v1.0.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.0.1 — 2026-06-29
- Alerts: messages standardized to `WTAS · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.0 — 2026-06-18
- Initial release
- 8 smoothing kernels: EMA, SMA, RMA, WMA, SuperSmoother, T3, KAMA, JMA
- Three scale modes: Classic, Clamp ±100, Adaptive ±100
- Gradient line color (bull ↔ bear based on oscillator level)
- Gradient shadow fills between WT main line and zero
- 4-state color-coded histogram
- Optional fill between WT main and signal lines
- OB/OS zone background fills
- Extreme cross signal markers + subtle dots for all crosses
- Alert conditions for all cross types
