# Changelog

## [Unreleased]

### Changed
- **Score (v4):** Volatility (low ATR% = +1, high ATR% = −1) no longer enters the signed directional total; it stays visible in the matrix and the Heat Score. In the signal-optimized score its 5 % move to Trend (10 % → 15 %)

### Fixed
- **HTF requests (v4):** the previous-bar indicator set takes the history of the whole object (`s[1]`) instead of indexing its fields, which Pine v6 rejects (CE10290)
- **Pine v6 (v4):** MFI, VWAP, volume SMA/StdDev, the VFI SMA and the OBV slope now run on every bar instead of only when the preceding condition in the same expression passed, so their values on historical bars are no longer skipped; only the result stays gated by real volume

## v3.7.0 / v4.5.0 — 2026-11-17
Matrix categories, aggregate and heat change on every chart; the v4 entries (event + RSI > 50 + trend) do not use them.

- **One input per category** (v3, v4, v4 strategy). Flow = MFI (VFI and OBV removed), Momentum = RSI (ROC, Stochastic RSI and CCI removed), Trend = ADX × DMI (EMA stack and VWAP removed), Volatility = ATR% (Williams VIX Fix removed), Structure = prior-range Donchian breakout (EMA position and distance removed — they are trend reads). Several inputs per category counted the same information several times. Category values, the aggregate, DECISION and the heat score shift; the trend category reads 0 while ADX ≤ 25
- **Divergence out of the heat confluence check** (v3, v4). The check now compares Flow/Trend, Momentum/Trend and Structure/Volatility; divergence stays a context row
- **Structure reads each row's own timeframe** (v3, v4). The category was computed from the chart bars for every timeframe row, so all rows showed the same value; the Donchian breakout now comes with the timeframe's other indicators (last closed bar of that timeframe)
- **Structure breakout fixed in v4 and the v4 strategy.** The Donchian reference still included the current bar there, so a breakout needed close == high; it now uses the prior 20 bars as in v3

## v3.6.1 — 2026-11-17
Bug fix and cleanup in v3; v4 is unchanged. The HTF midline now draws one HTF bar later than before and no longer moves while the HTF bar is forming.

- **HTF Midline repainted** (v3). The midline read the still-forming higher-timeframe bar, so its history differed from what was shown live. All modes (Simple, OHLC4, VWAP, Dynamic) now show the value of the last closed HTF bar
- **Legacy entry engine removed** (v3). Entry V2 is the only entry path. The legacy continuation entry dots (● shown only with the new engine switched off) were driven by pivot highs/lows and a confluence count that included divergence-zone proximity; they are removed together with the 3-factor confluence module and the chart pivot tracking that only fed them. The divergence-zone lines stay as display
- **Input removed** (v3): Enable New Entry Engine. Volatility-stop lines, the ranging background, Entry V2 labels, weakness labels and the debug output no longer depend on it
- **Marker removed** (v3): the legacy continuation entry dot (●)
- No alerts removed. The Weakness Bull/Bear alerts no longer depend on the removed input

## v3.6.0 / v4.4.0 — 2026-11-17
The remaining point and grade gates are removed. The Entry V2 trigger stays; around it only the explicit optional filters remain. Breaking: inputs are gone, and v4 entries change frequency. With the old default (2 of 3 evidence points) entries the context points used to block now fire, so expect more entries. Re-check on the chart and re-run the strategy backtest.

- **Final Signal Gate removed** (v4, v4 strategy). The evidence-point count (quality context, trend alignment, heat at or above a threshold) no longer gates entries. An entry now fires on the Entry V2 trigger when the optional Quality Gate does not veto it and the optional Trend Filter (both default off) lets it through
- **Heat out of the entry gate** (v4, v4 strategy). The heat score has no directional component (all its parts are magnitudes), so it cannot confirm a long or a short. It stays as a display in the matrix and as the threshold for the Early Reversal markers
- **Inputs removed** (v4, v4 strategy): Entry Heat Evidence (min), Final Signal Gate (strictness). The "Entry Context Gate" group is gone
- **Legacy strong/moderate signal removed** (v3). The precision-score classification (Strategy A–D thresholds, confidence downgrade, break-pullback-continuation timing, cooldown, structure and candle filters behind it) fed only the DECISION and Confidence cells; it drew no labels and had no alerts. It is removed with everything that only fed it
- **DECISION shows the consensus** (v3). It shows the direction plus the multi-timeframe consensus value ("Bull +0.62", "Bear -0.40", "Neutral" inside ±0.20) instead of STRONG BUY / Moderate Buy. Full mode shows it in the row that held Confidence; compact mode shows Heat alone instead of "Heat|Conf"
- **Timeframe rows without grade words** (v3). The TF1–TF3 action rows show direction plus value instead of STRONG BUY / BUY / SELL / STRONG SELL
- **Confidence removed** (v3). The confidence level (HIGH/MEDIUM/LOW) and the hidden "Signal Confidence" plot are gone
- **Inputs removed** (v3): the Signal Quality group (Enable Quality Gate, ATR Contract/Expand Threshold, Volume Low/High Threshold, Block Entries on Low Volume, Block Trend Signals in Range, Allow Mean-Reversion in Range). In v3 they only filtered the removed legacy signal, never Entry V2
- **Divergence out of the market bias band** (v3). The bias score reads Flow, Momentum, Trend, Volatility and Structure; its range is now -0.9 to +0.9 (not renormalised). The band switch thresholds (0.15 / 0.05) are unchanged. The Divergence row in the matrix stays as display
- No alerts removed

## v3.5.0 / v4.3.0 — 2026-11-17
Entry V2 stays the signal; the strength score and the grade/quality outputs around it are removed. Breaking: inputs and alerts are gone, and entries can come more often where the strength threshold used to block them (and less often where it used to let them through without momentum). Re-check on the chart and re-run the strategy backtest.

- **Entry V2 condition is now explicit** (v3, v4, v4 strategy). The strength score (momentum + trend alignment with a 0.3 floor + zone proximity with a 0.5 floor, against a density threshold) is replaced by a readable rule: an entry trigger (breakout, pullback, continuation) fires when momentum points in its direction (RSI above 50 for longs, below 50 for shorts) and the volatility-stop bias does not point against it. An entry against that bias counts as counter-trend and fires only when "Allow Counter-Trend Entries" is on (no longer with raised thresholds). The momentum condition now also applies near support/resistance
- **RSI and WaveTrend extreme boosts removed** (v3, v4, v4 strategy). They added strength at RSI/WT1 extremes, which pulled entries towards the opposite of the momentum condition
- **Inputs removed** (v3, v4, v4 strategy): Signal Density, the Signal Boost group (RSI/WT Extreme Boost, Boost Amounts, Strength Threshold). v4: "Use Divergence Zones" (Early Reversal). The RSI/WT1 extreme thresholds moved to the Early Reversal group (v4), where they still select extreme readings. Entry Heat Evidence and Final Signal Gate now sit in the "Entry Context Gate" group (v4)
- **Strength upgrades removed** (v3, v4, v4 strategy). A same-direction entry no longer fires because its strength rose. v4 keeps re-entries after the cooldown on a fresh trigger; v3 emits on direction changes only
- **Early "BPC" circles removed** (v3, v4, v4 strategy). They showed entries above a lower strength threshold, which no longer exists
- **Alerts removed**: Strong Buy, Strong Sell, Moderate Buy, Moderate Sell, High Quality Setup (v3); Early Reversal Long/Short Candidate, A-Setup Long/Short, High Quality Setup (v4). Entry V2, weakness, exhaustion and mean-reversion alerts stay
- **A-Setup marker removed** (v3, v4, v4 strategy). The ★ marker and the "★ A-SETUP" matrix status depended on the removed strength score. Early Reversal markers stay as display (v4)
- **Entry labels without strength** (v3). The "Strength %" tooltip line and the strength-based transparency are gone; trend and mean-reversion labels use full color
- **Divergence no longer feeds scores** (v3, v4, v4 strategy). v3: weight 0 in the 6-category aggregate (was 1.4). v3 and v4: no longer part of the heat confluence component, the "divergence confirmed" heat setup status or the diamond-zone threshold easing; v4: no longer early-reversal evidence. The Divergence row in the matrix and the divergence-zone lines stay as display
- Matrix, heat and confidence stay as display. v3: the bottom-area mode "Signal Quality" is renamed "Category Magnitude"
- v4, v4 strategy: removed an unused internal type

## v3.4.2 / v4.2.2 — 2026-11-17
Bug fixes. Signal frequency and scores change - re-check on the chart and re-run the strategy backtest.

- **Higher-timeframe scores repainted** (v3, v4, v4 strategy). The timeframe rows read the still-forming higher-timeframe bar, so scores and signals could change after the fact. They now use the last closed bar of each higher timeframe; the chart timeframe itself still uses the current bar
- **Missing volume was stretched over other categories** (v3). Without real volume the Flow weight dropped out of the category aggregate and the chart part of the precision score was divided by the remaining weight. Flow now keeps its weight with a neutral score in both places, as in v4
- **"Exhaustion Confirmed" alert repeated** (v3, v4). It fired on every bar while the confirmed state lasted; it now fires once when the state is reached. Display and scoring are unchanged
- **A blocked entry suppressed later entries** (v4, v4 strategy). The quality veto, trend filter and evidence gate ran after the entry de-duplication, so a long the gates blocked still used up the de-duplication slot and the next valid long could be dropped. The gates now run first
- **Mean-reversion exits without an entry** (v3). A mean-reversion signal opened the position state even while the trend model was active and no MR label was shown, which led to EXIT labels and alerts without a matching entry. The state now opens only on signals of the active model
- **Weakness alerts and EXIT labels could fire in the wrong direction** (v3). A confirmed bear warning also released a pending bull weakness (and vice versa); each direction now uses its own confirmation
- **Entry V2 alerts ignored the signal mode** (v3). They now follow the same Trend / ADX Auto gate as the chart labels
- **A-Setup repeated** (v3). It fired on every bar the entry condition held; it now requires the de-duplicated entry event, as the entry labels do
- **Daily+ recovery removed** (v3). On Daily and higher, moderate signals the confidence gate removed were re-added after the quality gate, bypassing it. The confidence and quality gates now apply on Daily and higher as well
- Tooltips: "Allow Counter-Trend Entries" states the actual threshold factor (1.15) (v3, v4); "Signal Density" describes the thresholds instead of a quality claim (v4)
- v3: removed an unused internal type

- `commodity_pulse_matrix_v4` and its strategy: the Divergence category no longer enters the 6-category aggregate (weight 0; it was the largest single weight). It stays as a context row in the matrix. Heat score and A-setup read the remaining five categories, so signal density changes
- `commodity_pulse_matrix_v4` and its strategy: without real volume the Flow weight no longer drops out of the 6-category aggregate (which stretched the other categories, Divergence to 28 %); the missing evidence counts as absent. Affects only symbols without real volume; the heat score there is lower than before
- `commodity_pulse_matrix_v3`, `_v4` and the v4 strategy: code comments no longer claim JMA gives "less lag / better responsiveness"; comments only, no calculation change

## Volume check — 2026-10-12
- `commodity_pulse_matrix_v3` v3.4.0→3.4.1: Volume check fixed: only `tick` volume is rejected; `n/a` counts when the feed actually delivers volume. Most non-crypto feeds report `n/a`, so the old `base`/`quote` check treated futures and stocks with real volume (e.g. EUREX:FDAX1!) as volume-less — volume-based parts are active there again, which can change scores, gates and signals on those markets
- `commodity_pulse_matrix_v4` v4.2.0→4.2.1: Volume check fixed: only `tick` volume is rejected; `n/a` counts when the feed actually delivers volume. Most non-crypto feeds report `n/a`, so the old `base`/`quote` check treated futures and stocks with real volume (e.g. EUREX:FDAX1!) as volume-less — volume-based parts are active there again, which can change scores, gates and signals on those markets
- `commodity_pulse_matrix_v4` v4.2.1: The "backtest invalid" notice on non-standard chart types (Heikin Ashi, Renko …) now sits in the bottom-right corner as a short note instead of a label on the last candle

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
