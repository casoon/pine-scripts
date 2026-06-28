# Pine Scripts by WavesUnchained

**Pine Version:** v6 &nbsp;·&nbsp; **License:** [MIT](LICENSE) &nbsp;·&nbsp; **Author:** [WavesUnchained](https://www.tradingview.com/u/WavesUnchained/)

> A collection of custom TradingView indicators built around composable analysis — market structure, trend, momentum, and confluence scoring.

---

## Getting Started

1. Open any `.pine` file and copy its contents
2. In TradingView: **Pine Script Editor → Paste → Add to Chart**

Scripts marked **`[RTA]`** require the RTA libraries to be published to your TradingView account first — see [Libraries](#libraries).

---

## Indicators

### Vein Adaptive Suite

A set of composable indicators — the core three cover trend, pullback, and exhaustion and are designed to be read together. The remaining scripts are more specialized: focused on commodity futures (primarily NatGas 4H), execution timing, and research tooling.

**Core**

| Script | Focus |
|--------|-------|
| [`vein_trend.pine`](indicators/trend_direction/vein/vein_trend.pine) | Trend phase scoring — EMA structure, ADX, regime, composite score |
| [`vein_pullback.pine`](indicators/trend_direction/vein/vein_pullback.pine) | Pullback quality — Fibonacci depth, volume, EMA proximity, micro BOS |
| [`vein_exhaustion.pine`](indicators/trend_direction/vein/vein_exhaustion.pine) | Exhaustion detection — candle pressure, volume absorption, momentum streaks |

**Commodity / NatGas focused**

| Script | Focus |
|--------|-------|
| [`vein_accumulation_phase.pine`](indicators/trend_direction/vein/vein_accumulation_phase.pine) | 4H bottom formation and accumulation phase detection — 5-component process state |
| [`vein_reversal_score.pine`](indicators/trend_direction/vein/vein_reversal_score.pine) | Two-layer reversal scoring (setup conditions + structural confirmation) |
| [`vein_structure_zones.pine`](indicators/trend_direction/vein/vein_structure_zones.pine) | Swing detection, BOS, spring/upthrust, auto S/R zones with lifecycle tracking |
| [`vein_execution.pine`](indicators/trend_direction/vein/vein_execution.pine) | 15m entry timing overlay — micro BOS, sweeps, rejection candles, follow-through |
| [`vein_spread_context.pine`](indicators/trend_direction/vein/vein_spread_context.pine) | Commodity futures calendar spread context — bias and momentum modifier, not a signal |

**Research / utility**

| Script | Focus |
|--------|-------|
| [`vein_feature_exporter.pine`](indicators/trend_direction/vein/vein_feature_exporter.pine) | Bar-level feature calculation for reversal research — trend, momentum, volume, candle structure |
| [`vein_reversal_labeler.pine`](indicators/trend_direction/vein/vein_reversal_labeler.pine) | Historical reversal labeling with forward-looking ATR rules — research and ML labeling only |

→ [`indicators/trend_direction/vein/README.md`](indicators/trend_direction/vein/README.md) — full documentation and layered reading guide

---

### Market Structure

| Script | What it does |
|--------|--------------|
| [`market_structure_advanced.pine`](indicators/market_structure/market_structure_advanced/market_structure_advanced.pine) | Swing pivot classification (HH/HL/LH/LL) mapped to a bounded score oscillator — continuous structural bias reading without chart labels |
| [`smc_structure_expectation.pine`](indicators/market_structure/smc_structure_expectation/smc_structure_expectation.pine) | BOS, CHoCH, order blocks, fair value gaps |
| [`wyckoff_schematics.pine`](indicators/market_structure/wyckoff_schematics/wyckoff_schematics.pine) | Wyckoff phases and events — accumulation, distribution, spring, UTAD |
| [`sr_zones_mtf_v2.pine`](indicators/market_structure/sr_zones_mtf_v2/sr_zones_mtf_v2.pine) | Multi-timeframe support and resistance zones |
| [`market_structure_pivot_map.pine`](indicators/market_structure/market_structure_pivot_map/market_structure_pivot_map.pine) | HTF pivot/CPR/projection map with cross-timeframe confluence zones and nearest-S/R readout — a location tool, not a signal generator |
| [`tweezer_kangaroo_zones.pine`](indicators/market_structure/tweezer_kangaroo_zones/tweezer_kangaroo_zones.pine) | Tweezer tops/bottoms and kangaroo tails mapped to supply/demand zones |
| [`jma_struct.pine`](indicators/market_structure/jma_struct/jma_struct.pine) | JMA entry clusters with Wyckoff and SMC structure context |
| [`time_to_react_volatility_time.pine`](indicators/volatility/time_to_react_volatility_time/time_to_react_volatility_time.pine) | BOS and sweep timing with volatility-adjusted candle coloring |
| [`coilforge_zones_v1.pine`](indicators/market_structure/coilforge_zones/coilforge_zones_v1.pine) | Compression zone detection with multi-module scoring and post-zone breakout watch |
| [`reversal_engine_score_v1.pine`](indicators/momentum/reversal_engine_score/reversal_engine_score_v1.pine) | Score-based liquidity sweep reversal signals with HTF trend filter and configurable evidence threshold |
| [`reversal_type_classifier_v1.pine`](indicators/market_structure/reversal_type_classifier/reversal_type_classifier_v1.pine) | Ex-post diagnostic: classifies confirmed pivot reversals as Snapback / Grind / Fake / Chop with WT context and R-outcome scoring |
| [`structure_break_risk.pine`](indicators/market_structure/structure_break_risk/structure_break_risk.pine) | Forward-looking 0–100 gauge of how close the prevailing trend's structure is to breaking — risk rises on approach to the break level, not only after it; symmetric top-/bottom-break scoring from five weighted sensors (near level, confirmed BOS, failed breakout, structure erosion, pivot divergence) with a Reason readout; companion to Trend Persistence Score |
| [`commodity_heat_reversal.pine`](indicators/composite/commodity_heat_reversal/commodity_heat_reversal.pine) | Score-based mean-reversion reversal signals for commodity futures — ATR distance, expansion, RSI extreme, wick pressure, BB breach |
| [`exhaustion_scanner.pine`](indicators/momentum/exhaustion_scanner/exhaustion_scanner.pine) | Role-separated overextension context (0–100): Stretch + Exhaustion + Reaction scores, volatility as multiplier, regime classifier framing each signal as Continuation Risk / Trend Exhaustion / Range Fade; per-market presets |

### Trend & Regime

| Script | What it does |
|--------|--------------|
| [`adx_advanced.pine`](indicators/trend_strength/adx_advanced/adx_advanced.pine) | ADX with DI± display, pluggable signal smoothing, 4-state histogram, gradient line, and DI crossover / threshold alerts |
| [`regime_classifier.pine`](indicators/trend_strength/regime_classifier/regime_classifier.pine) | Stage-1 reversal-pipeline filter — fuses Fractal Dimension, Kaufman Efficiency Ratio and Choppiness into a Trend / Range / Chaos classification with hysteresis, symmetric reversal/trend permission outputs (no triggers) and an optional HTF regime line |
| [`trend_persistence_score.pine`](indicators/trend_strength/trend_persistence_score/trend_persistence_score.pine) | Graded 0–100 trend-strength oscillator — fuses Regression R², Kaufman Efficiency Ratio, ADX strength+slope and Fractal Dimension into one persistence axis with a Strong/Healthy/Transition/Weak/Dead state, hysteresis, calibration-anchor inputs and visual-only directional context |
| [`commodity_pulse_matrix_v3.pine`](indicators/composite/commodity_pulse_matrix/commodity_pulse_matrix_v3.pine) | Multi-timeframe confluence scoring matrix across instruments — [published on TradingView](https://de.tradingview.com/script/aJmdpe8H/) |
| [`signal_quality_engine.pine`](indicators/composite/signal_quality_engine/signal_quality_engine.pine) | Range-fade signal engine — fades exhausted range edges (long the lows, short the highs) via a Distance+Structure+Momentum exhaustion score, with an Edge → Setup → Watch → Trigger read and candle-rejection confirmation |
| [`regime_detector.pine`](indicators/trend_strength/regime_detector/regime_detector.pine) | MA-zone based trend regime overlay |
| [`ma_regime_bands.pine`](indicators/trend_direction/ma_regime_bands/ma_regime_bands.pine) | Moving average regime classification bands |
| [`relative_leg_efficiency.pine`](indicators/relative_strength/relative_leg_efficiency/relative_leg_efficiency.pine) | Efficiency ratio per price leg — how directional each move is |
| [`auto_trendlines.pine`](indicators/market_structure/auto_trendlines/auto_trendlines.pine) | Combinatorial trendline detection with OLS refinement, quality scoring, and greedy selection |
| [`adaptive_supertrend_v1.pine`](indicators/trend_direction/adaptive_supertrend/adaptive_supertrend_v1.pine) | Supertrend with conviction-adaptive band width — narrows in strong trends, widens in chop |
| [`chandelier_flip_radar.pine`](indicators/trend_direction/chandelier_flip_radar/chandelier_flip_radar.pine) | ATR trailing stop with five-level trend state — progressive bar coloring, trap markers, body-filtered flips |
| [`smooth_trend_radar.pine`](indicators/trend_direction/smooth_trend_radar/smooth_trend_radar.pine) | Double-smoothed Supertrend baseline — auto-scaled per timeframe, pivot-based rejections, statistical overextension via candle coloring, automatic SL/TP setup on flips |

### Volatility

| Script | What it does |
|--------|--------------|
| [`atr_advanced.pine`](indicators/volatility/atr_advanced/atr_advanced.pine) | ATR in four display modes (Raw, ATR%, Normalized, Percentile Rank) with pluggable smoothing, gradient visualization, and expansion/contraction signals |

### Momentum & Oscillators

| Script | What it does |
|--------|--------------|
| [`cci_advanced.pine`](indicators/momentum/cci_advanced/cci_advanced.pine) | CCI with pluggable smoothing, three scale modes, OB/OS extreme-zone filter, gradient line, and shadow fills |
| [`wavetrend.pine`](indicators/momentum/wavetrend/wavetrend.pine) | WaveTrend oscillator — cross signals, divergence, overextension duration, slope quality filter, zone persistence |
| [`wavetrend_advanced_smoothing.pine`](indicators/momentum/wavetrend_advanced_smoothing/wavetrend_advanced_smoothing.pine) | WaveTrend with 8 pluggable smoothing kernels, gradient line coloring, shadow fills, 4-state histogram, and configurable scale modes |
| [`commodity_flow_trend.pine`](indicators/money_flow/commodity_flow_trend/commodity_flow_trend.pine) | MFI + CCI composite oscillator for commodities — 4-state flow background, extreme-zone reversal signals, optional CCI gate, normalized CCI overlay |
| [`mtf_wavetrend_opportunity_hunter.pine`](indicators/momentum/mtf_wavetrend_opportunity_hunter/mtf_wavetrend_opportunity_hunter.pine) | MTF confluence pane — net score histogram + heat ribbons per layer, RRG-style rotation map, Ehlers Ultimate Smoother core, entropy noise floor, persistent TP/SL zones on the price chart |
| [`market_stress_oscillator.pine`](indicators/momentum/market_stress_oscillator/market_stress_oscillator.pine) | Composite stress index — WVF with JMA and ADX filters |
| [`market_exhaustion.pine`](indicators/momentum/market_exhaustion/market_exhaustion.pine) | Exhaustion signals via MFI and StochRSI with divergence detection |
| [`oscillator_divergence_zones.pine`](indicators/momentum/oscillator_divergence_zones/oscillator_divergence_zones.pine) | Oscillator divergence zones — RSI, CCI, MFI, Fisher, TSI, STC, DPO, Roofing, Cyber Cycle; regular + hidden; ATR-wide zones with retest counter |
| [`market_pressure_scale.pine`](indicators/momentum/market_pressure_scale/market_pressure_scale.pine) | Dual-component oscillator — Setup Pressure (coiling) vs Impulse Pressure (expansion), phase labels, signal markers, POC/range context lines |
| [`mtf_stochrsi_pair_score.pine`](indicators/momentum/mtf_stochrsi_pair_score/mtf_stochrsi_pair_score.pine) | Multi-timeframe StochRSI confluence scorer — pair-weighted with sync bonus and conflict penalty, weighted total, signal markers |

### Liquidity & Order Flow

| Script | What it does |
|--------|--------------|
| [`volume_strata.pine`](indicators/money_flow/volume_strata/volume_strata.pine) | Fixed-range volume profile — right-anchored bars, POC, VAH/VAL, HVN/LVN zones, naked POC tracking |
| [`money_flow_delta_profile.pine`](indicators/money_flow/money_flow_delta_profile/money_flow_delta_profile.pine) | Center-out diverging profile — green (right) = net buying, red (left) = net selling at each price level; POC, Value Area, optional recency weighting |
| [`vwap_cross_visuals.pine`](indicators/mean_reversion/vwap_cross_visuals/vwap_cross_visuals.pine) | VWAP with multi-band deviation analysis |
| [`anchored_vwap.pine`](indicators/mean_reversion/anchored_vwap/anchored_vwap.pine) | Stage-4 fair-value location sensor — VWAP anchored to swing pivot / session / period / manual date, volume-weighted σ bands, distance-from-value in σ as a symmetric Location output (no triggers) |
| [`liquidity_hunter.pine`](indicators/market_structure/liquidity_hunter/liquidity_hunter.pine) | Ranked equal highs/lows — quality-scored BSL/SSL levels, sweep markers, reclaim detection with event scoring |

### Pattern & Wave Analysis

| Script | What it does |
|--------|--------------|
| [`zigzag_patterns_framework.pine`](indicators/market_structure/zigzag_patterns_framework/zigzag_patterns_framework.pine) | ZigZag-based pattern detection — ABC, triangles, Wolfe waves |
| [`zigzag_fibo_pullback_map.pine`](indicators/market_structure/zigzag_fibo_pullback_map/zigzag_fibo_pullback_map.pine) | Confirmed ZigZag pivots with pullback-to-Fibonacci labeling and active fib fan |
| [`elliott_wave_radar.pine`](indicators/market_structure/elliott_wave_radar/elliott_wave_radar.pine) | Rule-validated Elliott Wave counting — labels impulses/ABC only when hard EW rules hold, Fib-scored, with target projections and invalidation watch |

### Equities & Relative Strength

| Script | What it does |
|--------|--------------|
| [`relative_strength_line.pine`](indicators/relative_strength/relative_strength_line/relative_strength_line.pine) | RS vs. a benchmark (SPY/QQQ) — Mansfield RS oscillator or raw RS line, with the IBD leadership signal (RS new high before price). See [MOMENTUM_EQUITIES.md](MOMENTUM_EQUITIES.md) for the equities roadmap |

---

## Strategies

Most strategy files are **auto-generated** from indicator source files via `scripts/build_strategies.py` — do not edit those directly. The WaveTrend v4 strategy is standalone and maintained by hand. Each strategy adds a trade direction filter, confirmed-bar gate, cooldown, and optional break-even stop on top of the indicator logic.

```bash
python3 scripts/build_strategies.py          # rebuild all
python3 scripts/build_strategies.py indicators/trend_direction/chandelier_flip_radar/
```

| Strategy | Based on | SL type | Backtest rating |
|----------|----------|---------|-----------------|
| [`chandelier_flip_radar_strategy.pine`](strategies/chandelier_flip_radar/chandelier_flip_radar_strategy.pine) | Chandelier Flip Radar | Trailing | Promising (PF 1.60, NatGas 4H) |
| [`oscillator_divergence_zones_strategy.pine`](strategies/oscillator_divergence_zones/oscillator_divergence_zones_strategy.pine) | Oscillator Divergence Zones | Pivot ATR | Promising (PF 1.14, NatGas 4H) |
| [`smooth_trend_radar_strategy.pine`](strategies/smooth_trend_radar/smooth_trend_radar_strategy.pine) | Smooth Trend Radar | Fixed TP | Promising (PF 1.71 Long, NatGas 4H) |
| [`wavetrend_v4_strategy.pine`](strategies/wavetrend/wavetrend_v4_strategy.pine) | WaveTrend v4 | Trailing | Promising (PF 3.07, NatGas 1D — best in repo) |

Full backtest results and parameter notes: `strategies/<name>/<name>_strategy_assessment.md`. Schema: [`strategies/ASSESSMENT_SCHEMA.md`](strategies/ASSESSMENT_SCHEMA.md).

---

## Libraries

A serious attempt at a reusable Pine Script foundation for MTF analysis, market structure, and strategy execution. The architecture is solid but the project was not completed. Kept here for reference; not actively maintained.

To use `[RTA]`-tagged scripts, publish each library via **Pine Script Editor → Publish Script → Library** using the exact name from the `library()` declaration.

| Library | Covers |
|---------|--------|
| [`RTAFramework.pine`](libraries/RTAFramework.pine) | Core MTF framework, signal engine, risk management |
| [`RTAMarketStructure.pine`](libraries/RTAMarketStructure.pine) | Volume profile, VWAP, zones, SMC concepts |
| [`RTAAdvanced.pine`](libraries/RTAAdvanced.pine) | Divergence, Fibonacci, pattern geometry |
| [`RTAStrategy.pine`](libraries/RTAStrategy.pine) | Strategy execution, position sizing, analytics |
| [`RTALiquidity.pine`](libraries/RTALiquidity.pine) | Liquidity mapping, order flow, Wyckoff |
| [`RTAMonitoring.pine`](libraries/RTAMonitoring.pine) | Debug utilities, metrics, health monitoring |

---

*These scripts are for educational and informational purposes only. Not financial advice. Trading involves substantial risk of loss.*
