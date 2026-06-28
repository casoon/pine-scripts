# Changelog

## v1.8.0 — 2026-06-27
- Stripped back to the core role: a multi-timeframe StochRSI pair score. The total score is now driven only by the StochRSI pair across the configured timeframes.
- Removed the Squeeze Momentum subsystem (inputs, BB/KC compression state, momentum histogram, state dot, compress-phase background) — it was a visual-only bolt-on detached from the score
- Removed stale header feature bullets advertising subsystems no longer in the file (Williams VIX Fix, QQE agreement/scoring, breadth discrepancy, fractal momentum alignment, oscillator compression detector)

## v1.7.1 — 2026-06-11
- Fix: multi-line ternaries with series types (cell background, QQE trailing stop, QQE score weighting, squeeze momentum color) rewritten to if/else (Pine v6 compile error CE10156)
- Removed unused f_state() helper
- Squeeze state dot tooltip corrected to actual colors (orange = ON, teal = OFF, gray = no squeeze)

## v1.7.0 — 2026-05-15
- Fractal Momentum Alignment: gradient consistency score (0–100) across the TF chain — 100 = all adjacent TF pairs agree in direction (ordered), 0 = every adjacent pair disagrees (chaotic); optional plot + dashboard row
- Oscillator Compression Detector: fires when the sum of absolute TF scores falls below threshold (avg |score| < 20 per TF by default), indicating all TFs near zero — potential pressure buildup; purple background + dashboard row

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
