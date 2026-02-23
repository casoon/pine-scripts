# Pine Scripts by WavesUnchained

**Author:** [WavesUnchained](https://www.tradingview.com/u/WavesUnchained/)
**Pine Version:** v6
**License:** [MIT](LICENSE)

---

## About This Collection

A mix of sketches and working tools — some of these scripts are just idea sketches that I never finished, others are functional and I still use them occasionally. The RTA libraries and strategies in particular are unfinished: I had a clear vision but didn't see them through to the end. Some scripts automate things I used to do manually on charts; others are purely experimental.

This collection was also my way of learning Pine Script. I appreciate the idea of having custom analysis tools right inside a chart, but I found Pine's limitations frustrating over time. I'm now moving toward building my own charting tools in Rust, where I have full control over the architecture.

**The idea behind all of this:** TradingView already has plenty of simple indicators. My goal was to build something more complex — not an all-in-one mega-indicator, but a set of composable building blocks. The approach: combine multiple analytical concepts, layer filters and logic on top, and gradually work toward statements that actually mean something. From there, derive strategy-level decisions — when does a signal apply, when doesn't it — and iteratively optimize toward better outcomes. The RTA libraries were meant to be the reusable foundation for that kind of work.

**Why publish these here?** My scripts were removed from TradingView publication twice. I can partly understand the moderation challenges when many people want to publish scripts — but there's a significant amount of thought and effort behind these (as the code hopefully reflects). Some of it was built with AI assistance, but the concepts, the ideas, and the overall design are mine. You don't put this kind of work in just for yourself. I wanted to find people to collaborate with, to get feedback — and when that's not possible through TradingView's publication system, there's no reason to stay on the platform.

So here they are — freely available. **None of these are polished, production-ready products.** But some can be useful as-is, and others might serve as inspiration or a starting point for your own work. Browse around, take what's useful, and feel free to build on it.

---

All scripts are **standalone** (self-contained, ready to use) unless marked with **[RTA]**, which means they require the RTA libraries published to your TradingView account first.

## Quick Start

1. Open any `.pine` file and copy its entire contents
2. In TradingView, open the **Pine Script Editor**
3. Paste the code and click **Add to Chart**

> Scripts marked **[RTA]** require the RTA libraries to be published first. See [Using RTA Libraries](#using-rta-libraries) below.

---

## Indicators

### Market Structure & Smart Money

| Script | Description |
|--------|-------------|
| [`jma_struct.pine`](indicators/jma_struct.pine) | JMA cluster entries with Wyckoff + SMC market structure analysis |
| [`smc_structure_expectation.pine`](indicators/smc_structure_expectation.pine) | SMC structural analysis — BOS, CHoCH, Order Blocks, FVG |
| [`wyckoff_schematics.pine`](indicators/wyckoff_schematics.pine) | Wyckoff methodology — phases, events, effort vs. result |
| [`tweezer_kangaroo_zones.pine`](indicators/tweezer_kangaroo_zones.pine) | Tweezer + kangaroo tail patterns with supply/demand zones |
| [`sr_zones_mtf_v2.pine`](indicators/sr_zones_mtf_v2.pine) | Multi-timeframe support & resistance zone detection |
| [`liquidity_hunter.pine`](indicators/liquidity_hunter.pine) | Institutional liquidity zone mapping **[RTA]** |
| [`smart_money_dashboard.pine`](indicators/smart_money_dashboard.pine) | Order flow + SMC + liquidity dashboard **[RTA]** |

### Trend & Regime Detection

| Script | Description |
|--------|-------------|
| [`commodity_pulse_matrix_v3.pine`](indicators/commodity_pulse_matrix_v3.pine) | Multi-timeframe commodity flow scoring matrix |
| [`regime_detector.pine`](indicators/regime_detector.pine) | MA-zone based trend regime overlay |
| [`ma_regime_bands.pine`](indicators/ma_regime_bands.pine) | Moving average regime classification bands |
| [`flow_bias.pine`](indicators/flow_bias.pine) | Directional flow bias oscillator (CMF + volume delta + Stoch + UO) |
| [`vwap_cross_visuals.pine`](indicators/vwap_cross_visuals.pine) | VWAP with multi-band deviation analysis |
| [`mtf_trend_alignment.pine`](indicators/mtf_trend_alignment.pine) | 4-timeframe Supertrend consensus dashboard **[RTA]** |

### Oscillators & Momentum

| Script | Description |
|--------|-------------|
| [`market_stress_oscillator.pine`](indicators/market_stress_oscillator.pine) | Composite stress index — WVF + JMA/ADX filters |
| [`market_exhaustion.pine`](indicators/market_exhaustion.pine) | Exhaustion detection via MFI + StochRSI with divergences |
| [`candle_pressure_response_jma.pine`](indicators/candle_pressure_response_jma.pine) | JMA-based candle pressure and response scoring |
| [`relative_leg_efficiency.pine`](indicators/relative_leg_efficiency.pine) | Efficiency ratio per price leg |
| [`relative_leg_efficiency_panel_chart.pine`](indicators/relative_leg_efficiency_panel_chart.pine) | RLE — combined panel + chart overlay view |
| [`time_to_react_volatility_time.pine`](indicators/time_to_react_volatility_time.pine) | BOS/sweep/OB timing with volatility-adjusted candle coloring |

### Pattern Recognition & Wave Analysis

| Script | Description |
|--------|-------------|
| [`pattern_recognition.pine`](indicators/pattern_recognition.pine) | Geometric chart pattern detection with divergence analysis |
| [`rj_wave.pine`](indicators/rj_wave.pine) | RJ-Wave Fibonacci structure validator |
| [`zigzag_patterns_framework.pine`](indicators/zigzag_patterns_framework.pine) | ZigZag-based pattern detection (ABC, triangles, Wolfe waves) |
| [`wave_navigator.pine`](indicators/wave_navigator.pine) | Elliott Wave recognition and labeling |

---

## Strategies

| Script | Description |
|--------|-------------|
| [`flowzone_strategy.pine`](strategies/flowzone_strategy.pine) | FlowZone confluence-based strategy execution |
| [`zigzag_corridors_strategy.pine`](strategies/zigzag_corridors_strategy.pine) | ZigZag corridors with Bollinger/Keltner squeeze strategy |

---

## Libraries

Pine Script libraries that power the **[RTA]**-tagged indicators above. Publish these to your TradingView account if you want to use the RTA-dependent indicators.

| Library | Description |
|---------|-------------|
| [`RTAFramework.pine`](libraries/RTAFramework.pine) | Core MTF framework, signal engine, risk management |
| [`RTAMarketStructure.pine`](libraries/RTAMarketStructure.pine) | Volume profile, VWAP, zones, SMC concepts |
| [`RTAAdvanced.pine`](libraries/RTAAdvanced.pine) | Divergence, Fibonacci, pattern geometry |
| [`RTAStrategy.pine`](libraries/RTAStrategy.pine) | Strategy execution, position sizing, analytics |
| [`RTALiquidity.pine`](libraries/RTALiquidity.pine) | Liquidity mapping, order flow, Wyckoff |
| [`RTAMonitoring.pine`](libraries/RTAMonitoring.pine) | Debug utilities, metrics, health monitoring |

### Using RTA Libraries

To use indicators marked **[RTA]**, you need to publish the required libraries to your TradingView account:

1. Open the library `.pine` file in TradingView's Pine Script Editor
2. Click **Publish Script** and select **Library**
3. Use the exact name from the `library()` declaration in the script header
4. Once published, the dependent indicators will resolve their `import` statements automatically

| Indicator | Required Library |
|-----------|-----------------|
| `liquidity_hunter.pine` | RTAMarketStructure |
| `mtf_trend_alignment.pine` | RTAFramework |
| `smart_money_dashboard.pine` | RTAMarketStructure + RTAAdvanced |

---

## Disclaimer

These scripts are provided for **educational and informational purposes only**. They do not constitute financial advice. Trading involves substantial risk of loss. Always do your own research and use proper risk management.

---

## License

[MIT License](LICENSE)
