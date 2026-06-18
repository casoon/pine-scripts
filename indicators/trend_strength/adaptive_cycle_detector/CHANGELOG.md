# Changelog

## v1.0.1 — 2026-06-11
- Performance: zero-crossing count switched from a per-bar loop over the lookback window to a rolling sum
- Removed dead interval-tracking code (lastInterval was never updated due to an off-by-one and never read)
- Internal: cycle-period color ternary rewritten as if/else for Pine v6 compatibility

## v1.0 — 2026-05-15
- Initial release
- Dominant cycle estimation via WT zero-crossing period (bars between crossings)
- ATR regime detection: rising / falling / flat volatility
- Trend clarity measurement via ADX (trend vs. chop mode)
- Adaptive length recommendations for WT, StochRSI, and MFI
- Smoothed cycle period plot with configurable min/max bounds
- Dashboard with current period estimate and adaptive length recommendations
