# Changelog

## v1.1.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.1.1 — 2026-06-29
- Alerts: messages standardized to `OTOP · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.1 — 2026-06-11
- 2 alert conditions added: V-Spike Peak, V-Spike Trough
- Docs corrected: curvature is normalized by the recent WT range, not ATR
- Internal: shape-color and dashboard ternaries rewritten as if/else for Pine v6 compatibility; dead pivBar variable removed

## v1.0 — 2026-05-15
- Initial release
- Curvature measurement at WT pivot extremes (2nd derivative normalized by ATR)
- Width tracking: bars spent near extreme for each peak/trough
- Asymmetry index: rise speed vs. fall speed at each pivot
- Shape classification per pivot: V-Spike / Round / Flat / Asymmetric
- Curvature plot and shape label drawn at each classified pivot
- Dashboard with current dominant shape and topology summary
