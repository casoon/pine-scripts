# Pine Scripts by WavesUnchained

**Pine Version:** v6 &nbsp;·&nbsp; **License:** [MIT](LICENSE) &nbsp;·&nbsp; **Author:** [WavesUnchained](https://www.tradingview.com/u/WavesUnchained/)

> A collection of custom TradingView indicators built around composable analysis — market structure, trend, momentum, and confluence scoring. See [about.md](about.md) for background.

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
| [`vein_trend.pine`](indicators/vein/vein_trend.pine) | Trend phase scoring — EMA structure, ADX, regime, composite score |
| [`vein_pullback.pine`](indicators/vein/vein_pullback.pine) | Pullback quality — Fibonacci depth, volume, EMA proximity, micro BOS |
| [`vein_exhaustion.pine`](indicators/vein/vein_exhaustion.pine) | Exhaustion detection — candle pressure, volume absorption, momentum streaks |

**Commodity / NatGas focused**

| Script | Focus |
|--------|-------|
| [`vein_accumulation_phase.pine`](indicators/vein/vein_accumulation_phase.pine) | 4H bottom formation and accumulation phase detection — 5-component process state |
| [`vein_reversal_score.pine`](indicators/vein/vein_reversal_score.pine) | Two-layer reversal scoring (setup conditions + structural confirmation) |
| [`vein_structure_zones.pine`](indicators/vein/vein_structure_zones.pine) | Swing detection, BOS, spring/upthrust, auto S/R zones with lifecycle tracking |
| [`vein_execution.pine`](indicators/vein/vein_execution.pine) | 15m entry timing overlay — micro BOS, sweeps, rejection candles, follow-through |
| [`vein_spread_context.pine`](indicators/vein/vein_spread_context.pine) | Commodity futures calendar spread context — bias and momentum modifier, not a signal |

**Research / utility**

| Script | Focus |
|--------|-------|
| [`vein_feature_exporter.pine`](indicators/vein/vein_feature_exporter.pine) | Bar-level feature calculation for reversal research — trend, momentum, volume, candle structure |
| [`vein_reversal_labeler.pine`](indicators/vein/vein_reversal_labeler.pine) | Historical reversal labeling with forward-looking ATR rules — research and ML labeling only |

→ [`indicators/vein/README.md`](indicators/vein/README.md) — full documentation and layered reading guide

---

### Market Structure

| Script | What it does |
|--------|--------------|
| [`smc_structure_expectation.pine`](indicators/structure/smc_structure_expectation.pine) | BOS, CHoCH, order blocks, fair value gaps |
| [`wyckoff_schematics.pine`](indicators/structure/wyckoff_schematics.pine) | Wyckoff phases and events — accumulation, distribution, spring, UTAD |
| [`sr_zones_mtf_v2.pine`](indicators/structure/sr_zones_mtf_v2.pine) | Multi-timeframe support and resistance zones |
| [`tweezer_kangaroo_zones.pine`](indicators/structure/tweezer_kangaroo_zones.pine) | Tweezer tops/bottoms and kangaroo tails mapped to supply/demand zones |
| [`jma_struct.pine`](indicators/structure/jma_struct.pine) | JMA entry clusters with Wyckoff and SMC structure context |
| [`time_to_react_volatility_time.pine`](indicators/structure/time_to_react_volatility_time.pine) | BOS and sweep timing with volatility-adjusted candle coloring |

### Trend & Regime

| Script | What it does |
|--------|--------------|
| [`commodity_pulse_matrix_v3.pine`](indicators/commodity_pulse_matrix/commodity_pulse_matrix_v3.pine) | Multi-timeframe confluence scoring matrix across instruments — [published on TradingView](https://de.tradingview.com/script/aJmdpe8H/) |
| [`regime_detector.pine`](indicators/trend/regime_detector.pine) | MA-zone based trend regime overlay |
| [`ma_regime_bands.pine`](indicators/trend/ma_regime_bands.pine) | Moving average regime classification bands |
| [`relative_leg_efficiency.pine`](indicators/trend/relative_leg_efficiency.pine) | Efficiency ratio per price leg — how directional each move is |
| [`relative_leg_efficiency_panel_chart.pine`](indicators/trend/relative_leg_efficiency_panel_chart.pine) | RLE in combined panel and chart overlay view |
| [`mtf_trend_alignment.pine`](indicators/trend/mtf_trend_alignment.pine) | 4-timeframe Supertrend consensus dashboard `[RTA]` |
| [`chandelier_flip_radar.pine`](indicators/chandelier_flip_radar/chandelier_flip_radar.pine) | ATR trailing stop with five-level trend state — progressive bar coloring, trap markers, body-filtered flips |
| [`smooth_trend_radar.pine`](indicators/smooth_trend_radar/smooth_trend_radar.pine) | Double-smoothed Supertrend baseline — slope-based trend direction, rejection signals, automatic SL/TP levels on flips |

### Momentum & Oscillators

| Script | What it does |
|--------|--------------|
| [`flow_bias.pine`](indicators/momentum/flow_bias.pine) | Directional flow bias from CMF, volume delta, Stochastic, Ultimate Oscillator |
| [`market_stress_oscillator.pine`](indicators/momentum/market_stress_oscillator.pine) | Composite stress index — WVF with JMA and ADX filters |
| [`market_exhaustion.pine`](indicators/momentum/market_exhaustion.pine) | Exhaustion signals via MFI and StochRSI with divergence detection |
| [`candle_pressure_response_jma.pine`](indicators/momentum/candle_pressure_response_jma.pine) | JMA-smoothed candle pressure and response scoring |
| [`oscillator_divergence_zones.pine`](indicators/oscillator_divergence_zones/oscillator_divergence_zones.pine) | Oscillator divergence zones — RSI, CCI, MFI; regular + hidden; ATR-wide zones with retest counter |

### Liquidity & Order Flow

| Script | What it does |
|--------|--------------|
| [`vwap_cross_visuals.pine`](indicators/liquidity/vwap_cross_visuals.pine) | VWAP with multi-band deviation analysis |
| [`liquidity_hunter.pine`](indicators/liquidity/liquidity_hunter.pine) | Institutional liquidity zone mapping `[RTA]` |
| [`smart_money_dashboard.pine`](indicators/liquidity/smart_money_dashboard.pine) | Order flow, SMC, and liquidity dashboard |

### Pattern & Wave Analysis

| Script | What it does |
|--------|--------------|
| [`zigzag_patterns_framework.pine`](indicators/patterns/zigzag_patterns_framework.pine) | ZigZag-based pattern detection — ABC, triangles, Wolfe waves |
| [`wave_navigator.pine`](indicators/patterns/wave_navigator.pine) | Elliott Wave recognition and labeling |
| [`pattern_recognition.pine`](indicators/patterns/pattern_recognition.pine) | Geometric chart pattern detection with divergence analysis |
| [`rj_wave.pine`](indicators/patterns/rj_wave.pine) | Fibonacci structure validator for RJ-Wave patterns |

---

## Strategies

The goal is to eventually build properly backtested, executable strategies from these indicator signals. The two scripts here are early attempts — useful as a starting point, not a finished product.

| Script | What it does |
|--------|--------------|
| [`flowzone_strategy.pine`](strategies/flowzone_strategy.pine) | Entry execution based on FlowZone confluence signals |
| [`zigzag_corridors_strategy.pine`](strategies/zigzag_corridors_strategy.pine) | ZigZag corridor breakouts with Bollinger/Keltner squeeze |

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
