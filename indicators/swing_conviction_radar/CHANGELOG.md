# Changelog

## v1.0 — 2026-05-16
- Initial release
- Per-leg conviction score 0–100: speed (ATR-normalized) + cleanliness (on-trend bar fraction) + volume gradient (volume rising toward pivot)
- Bearish divergence: price higher high, conviction lower → hidden weakness
- Bullish divergence: price lower low, conviction lower → exhausted sellers
- Step-line conviction history for both bull and bear legs
- Divergence labels at exact pivot bar positions
- Dashboard: last/prev leg scores for each direction, divergence state
