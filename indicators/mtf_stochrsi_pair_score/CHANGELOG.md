# Changelog

## v1.6.0 — 2026-05-14
- Signal hygiene: edge-triggered Long/Short (fire on state change only, not every bar)
- Confirmed-bar gate: optional barstate.isconfirmed filter on signals (default on)
- Configurable minimum Agreement for signals (default 33 = 4:2 majority across 6 TFs)
- QQE division-by-zero fix: _den == 0 now returns ratio 0 instead of na
- Renamed "Divergences" → "Breadth Discrepancy" (honest: delta-based, not pivot-based)
- Table: disabled pairs shown as grayed out with "off" label

## v1.5.0 — 2026-05-14
- QQE Scoring: optional boost/penalty applied to per-TF StochRSI scores before pair calculation (default off)
- QQE Divergences: price vs QQE Agreement — bullish (price lower, QQE holds) / bearish (price higher, QQE fades), shown as diamonds
- Two new alert conditions: QQE Bullish/Bearish Divergence

## v1.4.0 — 2026-05-14
- QQE Agreement Layer: weighted RSI + adaptive trailing stop calculated across all 6 TFs
- QQE Agreement Index plotted as purple line alongside StochRSI Agreement (blue)
- Optional QQE gate on Strong Long/Short signals (off by default)
- f_qqe(): own implementation — momentum-weighted RSI, RMA-smoothed trailing stop distance

## v1.3.0 — 2026-05-14
- Squeeze Momentum integration: BB vs KC compression state (sqzOn/sqzOff/noSqz)
- Squeeze state dot on zero line (black = ON, gray = OFF, blue = no squeeze)
- Optional momentum histogram (LinReg of close vs KC midpoint, acceleration color-coded)
- Squeeze ON background (muted gray) — lower priority than WVF extremes

## v1.2.0 — 2026-05-14
- Smoothing default changed from EMA to JMA
- Added bidirectional Williams VIX Fix background: bull (fear spike) and bear (greed spike) extremes detected via Bollinger threshold — always on, can be disabled

## v1.1.0
- Initial release
