# Changelog

## v1.0.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.0.1 — 2026-06-29
- Alerts: messages standardized to `MSPM · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.0 — 2026-06-27
- Initial release
- Classic / Fibonacci pivots (P, R1–R4, S1–S4) for Daily / Weekly / Monthly
- Central Pivot Range with Narrow/Normal/Wide width regime vs daily ATR
- Previous high/low, current-day open, and ADR/Range/ATR projections (0.25 / 0.50 / 1.00)
- Confluence zones via greedy cross-timeframe clustering
- Nearest support/resistance readout with ATR-normalized distance
- Free timeframe selection via input.timeframe (blank = chart timeframe, or any fixed TF) plus two optional overlay timeframes
- Role-coded palette (pivot/band/resistance/support/prev/open/projection) and labels staggered into horizontal columns so overlapping levels stay readable
- Slim light-theme status table (CPR width + nearest support/resistance with ATR distance), configurable position, and CPR-cross / context alerts