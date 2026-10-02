# Changelog

## v1.2 — 2026-10-02
- Changed: the half-life now comes from the lag-1 autocorrelation of the smoothed impulse line instead of raw returns. Raw-return autocorrelation sits near zero, so the half-life was a fraction of a bar, the decay curve was zero one bar after any impulse, and Bullish/Bearish Carry (±25) was practically unreachable. The half-life now runs from the impulse EMA's own memory (about 6 bars at the default Fast Impulse Length) upward, still clamped by Max Half-Life; MMDO, Carry states, alerts and the dashboard half-life change accordingly
## v1.1 — 2026-10-02
- Fixed: the Hurst approximation measured range/stdev of price levels instead of the rescaled range of returns — it stayed at or below 0.5, so the positive Hurst memory term in Memory Strength was effectively always zero and the negative term added a near-constant offset to Decay Pressure. It now uses a proper rescaled-range estimate on log returns; Memory Strength, Decay Pressure, MMDO and the dashboard Hurst value change accordingly
## v1.0 — 2026-07-04
- Initial release — Memory/Decay composite oscillator fusing autocorrelation half-life, Hurst exponent approximation, path efficiency and range expansion/decay
- Bullish/Bearish Carry and Decay regime states with background shading
- Impulse markers on Z-score threshold breach
- Light-theme dashboard (score, state, half-life, impulse age, Hurst, efficiency, range ratio)
- Bullish/Bearish Carry and Impulse Decay alerts
