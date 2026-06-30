# Changelog

## v1.1.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.1.1 — 2026-06-29
- Alerts: messages standardized to `RGC · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.1 — 2026-06-27
- Optional higher-timeframe regime line via `request.security` — visual context only, never a veto/gate (default off)
- HTF source selectable: Auto (4× chart timeframe) or a manual timeframe
- HTF regime + trendiness added as a dashboard row when enabled
- Refactored the three sensors into one reusable regime engine (single source of truth for chart TF and HTF)

## v1.0 — 2026-06-27
- Initial release: Stage-1 regime filter fusing Fractal Dimension Index, Kaufman Efficiency Ratio and Choppiness Index onto one trendiness axis
- Trend / Range / Chaos classification with threshold hysteresis and an all-three-agree Chaos override
- Symmetric reversal-permission and trend-permission outputs (0–1)
- Per-sensor mapped lines, regime-change watch markers, alerts, light-theme dashboard, debug log