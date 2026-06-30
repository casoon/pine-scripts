# Changelog

## v1.1.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.1.1 — 2026-06-29
- Alerts: messages standardized to `SCR · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.1 — 2026-06-11
- Fixed `ta.atr()` being called inside conditional pivot blocks (inconsistent series calculation) — ATR is now computed once per bar in global scope
- Fixed multi-line ternary with series operands in the leg-scan loop (compile error) — rewritten as if/else
- Volume sums now use `nz()` so instruments without volume data no longer produce na scores
- Added alert conditions for bearish and bullish conviction divergences

## v1.0 — 2026-05-16
- Initial release
- Per-leg conviction score 0–100: speed (ATR-normalized) + cleanliness (on-trend bar fraction) + volume gradient (volume rising toward pivot)
- Bearish divergence: price higher high, conviction lower → hidden weakness
- Bullish divergence: price lower low, conviction lower → exhausted sellers
- Step-line conviction history for both bull and bear legs
- Divergence labels at exact pivot bar positions
- Dashboard: last/prev leg scores for each direction, divergence state
