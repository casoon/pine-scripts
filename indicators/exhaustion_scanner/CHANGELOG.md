# Changelog

## v1.3 — 2026-06-11
- Added a dedicated trigger score for labels so strong distance/structure/divergence evidence can produce signals even when the weighted total is low
- Recalibrated signal thresholds to Early 30 / Normal 40 / Conservative 50
- Label scores now show trigger strength instead of the weighted dashboard total

## v1.2 — 2026-06-11
- Recalibrated signal thresholds to Early 45 / Normal 55 / Conservative 65 for more practical 4H commodity signals
- Changed default signal mode from Conservative to Normal
- Added divergence-assisted setup labels so visible WT divergences can produce exhaustion signals when price is stretched
- Shortened the dashboard confirmation text for better readability

## v1.1 — 2026-06-11
- Added signal confirmation modes: Score Only, Candle Reaction, Pivot Confirmed
- Added faint candidate dots so raw exhaustion zones remain visible before confirmation
- Added same-side signal spacing to reduce repeated labels in persistent trends
- Hardened Money Flow scoring for feeds with missing or unusable volume data
- Dashboard now shows confirmation mode and current extreme state

## v1.0 — 2026-06-11
- Initial release
- Weighted top/bottom exhaustion scores (0–100) from five components: Distance, Momentum, Money Flow, Volatility, Structure
- Market presets (Stocks / Commodities / Forex-CFD / Crypto / Custom weights)
- Signal modes Early / Normal / Conservative (thresholds 75 / 82 / 88)
- WT divergence detection with validity window as momentum sub-component
- Heatmap background, extreme labels, component breakdown dashboard (light theme)
- Alerts: Top Exhaustion, Bottom Exhaustion, Any
