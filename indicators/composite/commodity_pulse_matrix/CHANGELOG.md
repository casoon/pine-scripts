# Changelog

## v3.4.0 — 2026-10-02
Follow-up to v3.3.0 from the same review. Signal frequency changes on trending charts and on Daily and higher - re-check on the chart.

- **Structure-flip escape never fired.** The counter-trend trap guard let a short through a bull trend only when the bear JMA stack was also in place, which cannot happen while the bull trend holds. A short is now allowed in a bull trend when the bar makes a lower high and lower low (vs. 2 bars back); longs in a bear trend mirror this with a higher high and higher low
- **Daily+ recovery overrode every filter.** On Daily and higher a moderate signal was injected whenever the chart score leaned ≥ 0.02 one way, with a 1-bar cooldown. Recovery now only restores a moderate signal the base strategy produced and the confidence gate removed (confidence still ≥ 0.35, chart score agreeing); the Daily+ cooldown is 2 bars
- **Volatility-spike warning could not fire.** It required a body > 1.5 ATR and, for "no progress", a body < 0.3 ATR or an against-direction close. It now reads a wide bar (range > 1.5 ATR, rising ATR) that closes near its open (body < 0.3 ATR); the direction comes from the other warning criteria
- **Signal confidence's MTF alignment was a constant 1/1.** The chart-only score set passed into signal generation now carries the real aligned/total timeframe count, as v4 does
- Removed inputs that were never read: the Take-Profit group, Stop-Loss ATR ×, Show Stop-Loss/Take-Profit Lines, Use Confirmed HTF Bars Only, Chart TF Priority Weight, the Signal Quality ATR/Volume lengths, Show Category Details, Show Signal Shapes, Show Signal Age, Show MR Signal Labels and the Colors group. Removed the uncalled risk-management module (position sizing, SL/TP levels, risk quality). v3 draws no stop-loss or take-profit levels; the header, README and TradingView description no longer claim it does

## v3.3.0 — 2026-10-02
Signal-logic fixes to the published v3 from the same bug-class review as v4.2.0. Signal frequency, heat and the matrix display change - re-check on the chart.

- **Zone threshold easing was direction-blind.** The diamond-zone boost lowered buy *and* sell thresholds by its magnitude, so a resistance zone made buys easier and a support zone made sells easier. Support now eases only buys, resistance only sells
- **Diamond-zone confluence** received the exhaustion flag as its divergence argument (exhaustion counted twice); it now gets the RSI divergence zones
- **Heat setup status was frozen.** The setup-status component (20% of heat) always read "BUILDING SETUP". It now follows the actual context: exhaustion confirmed, divergence zone, ranging or trending regime
- **Divergences compared the wrong bars.** The Divergence category and the RSI divergence zones compared the pivot-confirmation bar's low/high/oscillator instead of the pivot values. Both now compare pivot values
- **Volatility category had a permanent bearish bias.** Squeeze and WVF components were scaled by their weight twice and the squeeze is switched off in the scoring, so the category ranged from −1 to about +0.08. Components are now 0-1 and the weights renormalize when the squeeze is off
- **Structure category breakout never fired.** The Donchian reference included the current bar, so a breakout needed close == high. It now uses the prior 20 bars
- **Near-S/R context** used 20-bar highs/lows that included the current bar, so every new high/low counted as "near resistance/support". Now uses the prior 20 bars
- **Exhaustion watch fired both directions on the same bar.** Range, volume and small body are shared criteria; a watch now also needs a directional criterion (RSI extreme or rejection wick)
- **Mean-reversion exit alert repeated.** After a Long/Short exit the position was never cleared, so every later zero-line cross fired the exit again. The exit now closes the position; the WaveTrend crosses are also evaluated on every bar
- **Market structure stayed "transitioning" in trends.** A break of structure reset the bars-in-structure counter on every bar beyond the swing level, so the CHoCH flag never expired. The counter now resets only when the structure actually changes
- **Strong signals on instruments without real volume.** The neutral Flow score still carried 50% of the chart part of the precision score, capping it below the strong threshold. Flow's weight is now excluded and the rest renormalized, as in the category aggregate
- Matrix colors/symbols used ±0.5/1.5/2.5 tiers and the TF action column ±0.5/1.5 on scores clamped to ±1, so Strong/Very strong never showed - tiers are now 0.25/0.5/0.8 (actions 0.2/0.5). The heat signal-strength component (÷2.5) and the confidence score-magnitude (÷2) were capped the same way and are now 0-1

## v4.2.0 — 2026-10-02
Signal-logic fixes from a bug-class review. Signal frequency and scores change - re-check on the chart and re-run the strategy backtest.

- **Final Signal Gate now works.** Its three evidence points used to be the trigger itself, the trend filter (always true while switched off) and heat ≥ 0 (always true), so evidence was always 3/3 and the gate setting had no effect. Evidence is now real context: quality context (volume + ATR regime, or mean reversion at S/R), trend alignment (trending regime + close vs JMA50) and heat ≥ Entry Heat Evidence (new default 0.40, provisional). The default gate (4) requires 2 of 3. Quality Gate and Trend Filter, when switched on, are hard filters
- **Same-direction re-entries.** After a signal, a further signal in the same direction needed to be 0.35 stronger - even after the cooldown, until an opposite signal came. Now a fresh trigger after the cooldown fires as a re-entry; the strength-upgrade rule only applies inside the cooldown
- **Divergences compared the wrong bars.** The Divergence category and the RSI divergence zones compared the pivot-confirmation bar's low/high/oscillator instead of the pivot values, missing real divergences and producing false ones. Both now compare pivot values
- **Volatility category had a permanent bearish bias.** Squeeze and WVF components were scaled by their weight twice, so the category ranged from −1 to about +0.08. Components are now 0-1 and the weights renormalize when the squeeze is off
- **Exhaustion watch fired both directions on the same bar.** Range, volume and small body are shared criteria, so one wide doji could set Bull and Bear Watch together. A watch now also needs a directional criterion (RSI extreme or rejection wick)
- Near-S/R context used 20-bar highs/lows that included the current bar, so every new high/low counted as "at resistance/support" (disabling the momentum gate and lowering thresholds on breakout bars). Now uses the prior 20 bars
- Diamond-zone confluence received the exhaustion flag as its divergence argument (exhaustion counted twice); it now gets the RSI divergence zones
- Diamond-zone strength decay compounded every bar (≈0.01 after 30 bars) instead of flooring at 0.5
- Confirmed swing markers: the post-pivot swing-magnitude filter included the pivot bar's own range
- Heat signal-strength component divided ±1 scores by 2.5 (capped at 0.4); matrix colors/symbols and the TF action column used ±0.5/1.5/2.5 tiers on ±1 scores, so "Strong"/"Very strong" could never show - tiers are now 0.25/0.5/0.8 (actions 0.2/0.5); the legacy confidence used a hard-coded 1/1 TF alignment and a /2 magnitude cap

## v4.1.0 — 2026-09-05
- Data validity: MFI, OBV, VFI (Flow category), the VWAP component of the Trend
  category, and MV Confluence now check `syminfo.volumetype` before using
  volume — on tick/n/a volume they degrade to neutral instead of
  scoring on fake data. Flow carries weight 1.2 of 6.2 (~19%) in the default
  Swing weight profile; on degraded instruments its weight is now excluded and the other 5
  categories are renormalized to fill the full 100%, instead of silently
  dragging the total score toward zero.
- Exhaustion detection's volume criterion (1 of 5) is excluded the same way,
  with the watch threshold rescaled (3-of-5 → 2-of-4) to keep selectivity.
- Signal Quality Gate's low-volume block (Rule 1) no longer fires on tick
  volume — it passes through instead of vetoing every entry.
- Renamed the internal `vcp` variable to `volumeConfirmedPriceChange` — it is
  a price-weighted volume heuristic, not orderflow/delta.
- Added a "Volume" row to the matrix table dashboard (Real — Active / degraded
  with the detected `syminfo.volumetype`).
- Added `Data Contract` header block (`Verdict: CFD-degraded`).

## v3.2.0 — 2026-09-05
- Data validity: MFI, OBV, VFI (Flow category), the VWAP component of the Trend
  category, the HTF Midline VWAP mode, entry-timing's volume confirmation, and
  MV Confluence now check `syminfo.volumetype` before using volume — on
  tick/n/a volume they degrade to neutral instead of scoring or
  gating on fake data. Flow carries weight 1.2 of 6.2 (~19%) in the default
  Swing weight profile; on degraded instruments its weight is now excluded and the other 5
  categories are renormalized to fill the full 100%, instead of silently
  dragging the total score toward zero.
- Exhaustion detection's volume criterion (1 of 5) is excluded the same way,
  with the watch threshold rescaled (3-of-5 → 2-of-4) to keep selectivity.
- Signal Quality Gate's low-volume block (Rule 1) and the Entry Timing
  filter's volume-confirmation requirement no longer fire on tick volume —
  both pass through instead of vetoing every entry.
- HTF Midline "VWAP" / "Dynamic + VWAP" modes fall back to OHLC4 on tick/n/a
  volume instead of plotting a meaningless line.
- Renamed the internal `vcp` variable to `volumeConfirmedPriceChange` — it is
  a price-weighted volume heuristic, not orderflow/delta.
- Added a "Volume" row to the matrix table dashboard (Real — Active / degraded
  with the detected `syminfo.volumetype`), in both Compact and Full mode.
- Added `Data Contract` header block (`Verdict: CFD-degraded`).

## v4.0.4 — 2026-09-05
- Added chart-type guard: visible warning label when loaded on a non-standard chart (Heikin Ashi, Renko, Kagi, Line Break, P&F, Range) since the underlying strategy's backtest results are invalid there

## v4.0.3 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v3.1.4 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v4.0.2 — 2026-06-29
- Alerts: messages standardized to `CPM4 · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v3.1.3 — 2026-06-29
- Alerts: messages standardized to `CPM3 · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v4.0.1 — 2026-06-27
- Final signal gate: the timing trigger (Emit Entry + Entry Direction) is now always required and can no longer be out-voted by context; supporting evidence (Quality Gate / Trend Alignment / Heat) became a graded confidence score with a clamped threshold, and dead-volatility / low-volume remains the only hard structural veto. Replaces the previous 5-point AND-style confluence gate.

## v3.1.2 — 2026-06-27
- Signal model selection (ADX Auto): trend vs reversal model is now chosen by the market-structure regime classifier (trending → trend model, ranging/transitioning → reversal model), making the two mutually exclusive per bar; removed the arbitrary "prefer Mean Reversion" tiebreak.
- Structure filter is now symmetric: longs are vetoed in a confirmed bear trend just as shorts are vetoed in a confirmed bull trend, with the asymmetry driven by the regime rather than hardcoded per direction.

## v4.0
- v4 experimental build

## v3.1.1 — 2026-06-11
- Fix: alert messages referenced plots by index ({{plot_0}}, {{plot_1}}, {{plot_2}}), which pointed at the wrong plots — now referenced by name ({{plot("Consensus Score")}}, {{plot("Signal Confidence")}}, {{plot("Heat Score")}})

## v3.1
- Published release
