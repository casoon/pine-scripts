# Changelog

## v3.5.0 — 2026-07-14
- Added Trend Strength: baseline-slope magnitude ranked against its own recent history (percentile-rank, same method as Overextension) flags a "strong trend" state — self-adapting, new `Trend Strength` input group (`Lookback`, `Percentile Threshold`, `Highlight Strong Trend`)
- Optional background tint marks bars where the trend is currently "strong"
- Rejection signal tooltips now note "Strong Trend" when the flag is active; added dedicated `STR Bull/Bear Rejection (Strong Trend)` alerts for rejection entries inside an already-strong trend

## v3.4.0 — 2026-07-09
- Trend direction now uses an ATR-scaled slope threshold with hysteresis (`Trend Slope Lookback` / `Trend Slope Threshold`) instead of a raw baseline crossover — fewer whipsaw flips on micro-noise
- Rejection signals now fire in both ADX regimes (trend and range), tagged in the tooltip as "Trend Pullback" or "Range Rejection" — previously restricted to sideways markets only
- Added optional Volume Filter for rejections (`Above Average` vs bar's own SMA) — off by default
- Added optional Volatility-Adaptive Band Width — scales the Supertrend factor by the instrument's own ATR percentile rank so band width normalizes across instruments — off by default
- Removed `@strategy-config` block — the matching strategy is now maintained standalone in `strategies/smooth_trend_radar/` and no longer auto-regenerated

## v3.3.2 — 2026-06-30
- Alerts: messages standardized to `<KÜRZEL> · EVENT · {{ticker}} {{interval}}` for a uniform format across the library (titles unchanged)

## v3.3.1 — 2026-06-11
- Signal tooltips: German fragments (Kurs/Tief/Hoch) translated to English (Price/Low/High) — no logic change

## v3.3 — 2026-04-28
- Initial release
