# Changelog

## v2.0.0 — 2026-07-07
- Added Bias / Quality / Timing state engine — collapses the score/agreement/exhaustion data into a single-glance readout (e.g. "LONG CONFIRMED · CLEAN · FRESH") instead of requiring the viewer to interpret two lines and a raw table
- Bias: NO EDGE / LONG or SHORT BUILDING / LONG or SHORT CONFIRMED / CONFLICT (score vs. agreement pointing opposite ways)
- Quality: CLEAN / MIXED / WEAK, derived from the existing TF Agreement Index
- Timing: FRESH (within N bars of the confirmed cross) / ACTIVE / LATE (majority of TFs already deep in the extreme zone) — surfaces the exhaustion dampening that `f_score()` already computed internally but never exposed
- Table: now shows the Bias/Quality/Timing block by default; per-TF and per-pair breakdown moved behind a new "Show Debug Table" toggle (off by default)
- Removed the Agreement Index line from the main plot — it now lives only in the dashboard, so the pane shows one score line instead of two competing oscillators
- Pair labels renamed from raw TF strings ("P 15+30") to relative tier names (Fast / Mid / Slow / Macro / Macro+) in the debug table
- No changes to trigger/alert logic — `longTrigger`/`shortTrigger` and both alertconditions are unchanged; all of the above is a read-only layer on top of the existing scores

## v1.9.0 — 2026-07-06
- Per-TF score: added continuous K/D-distance and K-momentum terms; halved the fresh-cross weight (±30 → ±15) so a cross no longer dominates the score for a single bar and then drops out
- Signal markers: replaced edge-triggered state-change logic with direct threshold crossing (`ta.crossover`/`ta.crossunder` on the smoothed total) — fires exactly on zone entry instead of on any state flip

## v1.8.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.8.1 — 2026-06-29
- Alerts: messages standardized to `MSRP · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

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
