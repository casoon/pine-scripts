# Changelog

## v1.1.1 — 2026-10-02
- Oscillator scale no longer inherits the chart symbol's price precision (values like 80,0000 on 4-decimal symbols such as NATGAS) — shows 2 decimals

## v1.1 — 2026-10-02
- Fixed: the Hurst sensor measured range/stdev of price levels instead of the rescaled range of returns — it could never exceed ~0.5, so clean trends read as anti-persistent and the Hurst score pulled PRI toward reversion. It now uses a proper rescaled-range estimate on log returns; PRI, Confidence and the dashboard Hurst value shift toward momentum in persistent markets
- Note: a single-window R/S estimate reads slightly above 0.5 on a pure random walk (small-sample bias), so the Hurst score carries a small positive tilt in noise
## v1.0 — 2026-07-04
- Initial release: Variance Ratio, return autocorrelation, Hurst exponent approximation and fractal efficiency fused into one −100..+100 Predictability Regime Index
- Confidence read (distance from random walk × sensor agreement)
- Momentum / Reversion / Noise / Mixed regime classification with background zones and hysteresis-free thresholds
- Regime-shift markers, alerts, and light-theme dashboard
