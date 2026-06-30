# Changelog

## v3.1.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v3.1.1 — 2026-06-29
- Alerts: messages standardized to `TKZ · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v3.1.0 — 2026-06-11
- HTF Stack panel and Metrics panel restyled to the light-theme table convention (readable on both TradingView themes)
- Metrics panel "Active" zone count now counts only active zones (previously showed the total number of zones ever created)
- Fixed: rolling 5-bar high/low for structure check was computed inside the zone loop, corrupting the series when multiple zones were active
- Fixed: wick-similarity score could divide by zero when "Max wick ratio" was set to 1.0 (input now has a minimum of 1.1)
- Fixed: impulse score returned na on the first bars of the chart
- Choppiness length input now has a minimum of 2 (prevented a division by zero)
