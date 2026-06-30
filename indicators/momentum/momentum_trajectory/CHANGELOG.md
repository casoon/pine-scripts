# Changelog

## v1.1.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.1.1 — 2026-06-29
- Alerts: messages standardized to `MTJ · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.1 — 2026-06-11
- WT acceleration line recolored: orange when positive instead of white — was invisible on light chart themes and in the light dashboard table
- Internal: state/color/background ternaries rewritten as if/else for Pine v6 compatibility

## v1.0 — 2026-05-15
- Initial release
- WaveTrend, StochRSI, and MFI velocity (1st derivative) and acceleration (2nd derivative) plots
- Smoothed velocity lines to reduce tick noise
- State classification: Building / Peaking / Collapsing / Recovering
- Background highlight on acceleration zero-cross (early exhaustion/reversal warning)
- Dashboard showing current state per oscillator
