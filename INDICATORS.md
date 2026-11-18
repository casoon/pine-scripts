# Indicators

Full index of active indicators in this repo, grouped by focus. For status, quality ratings and
version history see [`CATALOG.md`](CATALOG.md). For archived scripts and reasons see
[`archive/README.md`](archive/README.md). For which data sources are safe to use on
which instrument see [`DATA_VALIDITY.md`](DATA_VALIDITY.md).

## Vein Adaptive Suite

Three focused signal modules from the Vein suite (display-only und offline utility scripts were moved to [`archive/indicators/vein/`](archive/README.md)):

| Script | Focus |
|--------|-------|
| [`vein_pullback.pine`](indicators/trend_direction/vein/vein_pullback.pine) | Pullback quality — Fibonacci depth, volume, EMA proximity, micro BOS |
| [`vein_reversal_score.pine`](indicators/trend_direction/vein/vein_reversal_score.pine) | Two-layer reversal scoring (setup conditions + structural confirmation) |
| [`vein_execution.pine`](indicators/trend_direction/vein/vein_execution.pine) | 15m entry timing overlay — micro BOS, sweeps, rejection candles, follow-through |

→ [`indicators/trend_direction/vein/README.md`](indicators/trend_direction/vein/README.md) — full documentation and layered reading guide

---

## Market Structure

| Script | What it does |
|--------|--------------|
| [`market_structure_advanced.pine`](indicators/market_structure/market_structure_advanced/market_structure_advanced.pine) | Swing pivot classification (HH/HL/LH/LL) mapped to a bounded score oscillator — continuous structural bias reading without chart labels |
| [`smc_structure_expectation.pine`](indicators/market_structure/smc_structure_expectation/smc_structure_expectation.pine) | BOS, CHoCH, order blocks, fair value gaps |
| [`modern_wyckoff_state_machine_visual.pine`](indicators/market_structure/modern_wyckoff_state_machine_visual/modern_wyckoff_state_machine_visual.pine) | Modern Wyckoff State Machine Lite — locked range, range-bounded A-E phase zones, cause score, quality-graded events and dashboard |
| [`market_structure_pivot_map.pine`](indicators/market_structure/market_structure_pivot_map/market_structure_pivot_map.pine) | HTF pivot/CPR/projection map with cross-timeframe confluence zones and nearest-S/R readout — a location tool, not a signal generator |
| [`mtf_structure_bias.pine`](indicators/market_structure/mtf_structure_bias/mtf_structure_bias.pine) | HH/HL/LH/LL structure alignment across four timeframes into one bias read |
| [`tweezer_kangaroo_zones.pine`](indicators/market_structure/tweezer_kangaroo_zones/tweezer_kangaroo_zones.pine) | Tweezer tops/bottoms and kangaroo tails mapped to supply/demand zones |
| [`coilforge_zones_v1.pine`](indicators/market_structure/coilforge_zones/coilforge_zones_v1.pine) | Compression zone detection with multi-module scoring and post-zone breakout watch |
| [`edge_atlas.pine`](indicators/market_structure/edge_atlas/edge_atlas.pine) | Right-edge price-level atlas — period/session/pivot/swing-Fib/S/R/round-number levels, filtered and ranked into a shared registry, docked to the visible right edge of the chart |
| [`fib_reaction_memory.pine`](indicators/market_structure/fib_reaction_memory/fib_reaction_memory.pine) | Fibonacci retracement levels scored by confirmed local price reactions that occurred inside the frozen A→B reference leg (reaction-first, not geometric-proximity-first) — 0–100 Memory Score per level, APPROACHING/TESTING/REJECTED/ACCEPTED/RECLAIMED state machine, score-based NEXT level highlight, no table |
| [`market_scenario_projector.pine`](indicators/market_structure/market_scenario_projector/market_scenario_projector.pine) | Three weighted forward scenarios (Direct Continuation / Pullback Continuation / Failure) drawn as a dominance-ranked scenario tree from current impulse strength, efficiency, acceleration, swing structure bias, clustered support/resistance zones, candle-based rejection/exhaustion evidence and a converging pullback zone; optional outcome recorder tracks each setup to resolution for offline calibration — percentages are heuristic evidence weights, not calibrated probabilities (see indicator's todo.md) |
| [`support_resistance_zones.pine`](indicators/market_structure/support_resistance_zones/support_resistance_zones.pine) | Detector-driven support/resistance zone engine — pivot cluster, multiple-test, base/supply-demand, order block, fair value gap, price gap and equal-high/low liquidity detectors feed candidates into a central registry that merges, scores (confluence: EMA/VWAP/Fib/psychological/volume), lifecycle-tracks (touch/reaction/break/flip) and renders only the nearest score-filtered zones per side; 0.1.0 engine-foundation build, not yet compiler-tested (see indicator's todo.md) |
| [`reversal_engine_score_v1.pine`](indicators/momentum/reversal_engine_score/reversal_engine_score_v1.pine) | Liquidity sweep reversal signals with HTF trend filter and optional RSI direction filter |
| [`structure_break_risk.pine`](indicators/market_structure/structure_break_risk/structure_break_risk.pine) | How close the prevailing trend's structure is to breaking, and against which level — an RSI pane with momentum-divergence lines drawn on the RSI (the earliest crack, shown where it is readable), plus a break-level line, a shaded risk zone, a trend-context EMA and word event labels on the price chart, with the 0–100 risk magnitude in a compact, mobile-friendly info label; symmetric top-/bottom-break scoring from five weighted sensors (near level, confirmed BOS, failed breakout, structure erosion, pivot divergence); companion to Trend Persistence Score |
| [`trading_range_state_machine.pine`](indicators/market_structure/trading_range_state_machine/trading_range_state_machine.pine) | Pivot-cluster range detection with an 8-factor weighted range score, driving an Inactive/Building/Confirmed/Mature/Breaking state machine — range lines, midline, touch markers, background heat, ribbon and dashboard |
| [`market_tradability_engine_v2.pine`](indicators/market_structure/market_tradability_engine/market_tradability_engine_v2.pine) | Market-quality/no-trade filter (v2) — Structure/Energy/Acceptance model with armed balance boundaries, failed-breakout detection, transition state machine, and diagnostic `NO_TRADE` reasons |
| [`exhaustion_scanner.pine`](indicators/momentum/exhaustion_scanner/exhaustion_scanner.pine) | Role-separated overextension context (0–100): Stretch + Exhaustion + Reaction scores, volatility as multiplier, regime classifier framing each signal as Continuation Risk / Trend Exhaustion / Range Fade; per-market presets |

## Trend & Regime

| Script | What it does |
|--------|--------------|
| [`adx_advanced.pine`](indicators/trend_strength/adx_advanced/adx_advanced.pine) | ADX with DI± display, pluggable signal smoothing, 4-state histogram, gradient line, and DI crossover / threshold alerts |
| [`regime_classifier.pine`](indicators/trend_strength/regime_classifier/regime_classifier.pine) | Stage-1 reversal-pipeline filter — fuses Fractal Dimension, Kaufman Efficiency Ratio and Choppiness into a Trend / Range / Chaos classification with hysteresis, symmetric reversal/trend permission outputs (no triggers) and an optional HTF regime line |
| [`trend_persistence_score.pine`](indicators/trend_strength/trend_persistence_score/trend_persistence_score.pine) | Graded 0–100 trend-strength oscillator — fuses Regression R², Kaufman Efficiency Ratio, ADX strength+slope and Fractal Dimension into one persistence axis with a Strong/Healthy/Transition/Weak/Dead state, hysteresis, calibration-anchor inputs and visual-only directional context |
| [`bayesian_trend_factor.pine`](indicators/trend_strength/bayesian_trend_factor/bayesian_trend_factor.pine) | Bayesian-inspired trend filter — fuses regression direction, gated ADX/ER/R² strength and exhaustion risk into a signed −100..+100 Trend Factor plus separate Confidence; volatility only damps the factor; trend-state hysteresis, PB and continuation (RECLAIM/BOS/REJECT) labels with hover explanations and HAMA-style smoothed Trend Candles |
| [`markov_state_engine.pine`](indicators/trend_strength/markov_state_engine/markov_state_engine.pine) | Six-state regime resolution map with an exit-conditional Markov model ("when this regime breaks, where did similar states resolve?") — extremes-first debounced classification, a robust Timing axis (Persistence + coiled-spring Maturity) split from the thin Direction axis, a net resolution line (grey while the exit sample is thin); display only, alerts on state changes |
| [`commodity_pulse_matrix_v4.pine`](indicators/composite/commodity_pulse_matrix/commodity_pulse_matrix_v4.pine) | Multi-timeframe confluence scoring matrix (v4) — 6 categories (one input per family), Heat Score, Chart-TF Entry Engine V2, Diamond Zones, and ATR risk levels |
| [`signal_quality_engine.pine`](indicators/composite/signal_quality_engine/signal_quality_engine.pine) | Range-fade signal engine — fades exhausted range edges (long the lows, short the highs) via a Distance+Structure+Momentum exhaustion score, with an Edge → Setup → Watch → Trigger read and candle-rejection confirmation |
| [`trade_permission_engine_v1.pine`](indicators/composite/trade_permission_engine/trade_permission_engine_v1.pine) | Does the market currently permit trading Long or Short — unified Continuation/Reversal Maturity on one retracement ratio against an alternating confirmed reference leg, with a live (not just frozen-at-formation) trend-quality read and permission decay when the move goes quiet; plus a decoupled Position Health score (HOLD/PROTECT/REDUCE/EXIT) for an already-open position |
| [`ma_regime_bands.pine`](indicators/trend_direction/ma_regime_bands/ma_regime_bands.pine) | Moving average regime classification bands |
| [`relative_leg_efficiency.pine`](indicators/relative_strength/relative_leg_efficiency/relative_leg_efficiency.pine) | Efficiency ratio per price leg — how directional each move is |
| [`auto_trendlines.pine`](indicators/market_structure/auto_trendlines/auto_trendlines.pine) | Combinatorial trendline detection with OLS refinement, quality scoring, and greedy selection |
| [`chandelier_flip_radar.pine`](indicators/trend_direction/chandelier_flip_radar/chandelier_flip_radar.pine) | ATR trailing stop with five-level trend state — progressive bar coloring, trap markers, body-filtered flips, optional MTF confluence |
| [`smooth_trend_radar.pine`](indicators/trend_direction/smooth_trend_radar/smooth_trend_radar.pine) | Double-smoothed Supertrend baseline — auto-scaled per timeframe, ATR-scaled slope trend detection with hysteresis, live baseline rejections in both regimes, statistical overextension via candle coloring, automatic SL/TP setup on flips |
| [`adaptive_arithmetic_candles.pine`](indicators/trend_direction/adaptive_arithmetic_candles/adaptive_arithmetic_candles.pine) | Efficiency-adaptive candle transform with a regression-anchored body boost; strong state = direction plus matching regression slope, flips are early warnings, Long/Short signals require a strong-state breakout of the prior N bars' high/low |
| [`modern_trend_regime.pine`](indicators/trend_direction/modern_trend_regime/modern_trend_regime.pine) | Trend / Range / Transition regime — both sides scored via factors (not AND-chains) from ADX, efficiency ratio, DI, line stack, price and structure compression, with immediate transition on structure loss; trend confirmation fires on the regime change itself (not the raw crossover), plus a frozen swing-based range structure (one-shot breakouts, debounced reactions) and a time-aligned "price vs. structure preview" breakout marker; six tuned presets plus manual mode |
| [`market_average_relationship_engine.pine`](indicators/trend_direction/market_average_relationship_engine/market_average_relationship_engine.pine) | Single-MA relationship engine (EMA/SMA/WMA/HMA/VWMA/RMA/DEMA/TEMA/ALMA) — six diagnostic scores (Trend, Respect, Extension, Compression, Acceleration, Exhaustion) feed a signed −100..+100 relationship oscillator and a twelve-state classification; confirmed Pullback/Momentum Release/Do Not Chase/Exhaustion/Relationship Broken events, extension/exhaustion degrade quality without flipping direction; v1.1.0 adds price/relationship Divergence (pivots stay diagnostic-only) and a pivot-free Turn From Extreme event for trend start / trend weakening |
| [`futures_context_module.pine`](indicators/composite/futures_context_module/futures_context_module.pine) | Daily-only, non-price futures context — Open Interest, ΔOI vs. the front contract's own price change, and front/next term structure (Contango/Backwardation, curve trend) for an explicitly configured futures pair; never compares chart price against futures price; pure context, no signals |

## Volatility

| Script | What it does |
|--------|--------------|
| [`atr_advanced.pine`](indicators/volatility/atr_advanced/atr_advanced.pine) | ATR in four display modes (Raw, ATR%, Normalized, Percentile Rank) with pluggable smoothing, gradient visualization, and expansion/contraction signals |
| [`compression_fractal_release.pine`](indicators/volatility/compression_fractal_release/compression_fractal_release.pine) | Detects a compressed corrective coil inside an HTF trend and trades its release; band break is the trigger, coil strength + release dynamics are scored, choppiness vetoes low-quality breaks; classifies Release (with trend) vs Base Break (against trend) |
| [`williams_vix_fix_advanced.pine`](indicators/volatility/williams_vix_fix_advanced/williams_vix_fix_advanced.pine) | Synthetic fear gauge (Williams VIX Fix) — mirrored Bull/Bear WVF, StdDev/percentile spike bands, per-side stall/absorption, Reclaim signal, Sentiment Bar dominance score, gradient coloring |

## Momentum & Oscillators

- [Kestrel Opportunity Lens](indicators/composite/kestrel_opportunity_lens/kestrel_opportunity_lens.pine) — Long and short opportunity windows with recovery from the window extreme, trend context and confirmed-bar alerts (rule prototype).

| Script | What it does |
|--------|--------------|
| [`cci_advanced.pine`](indicators/momentum/cci_advanced/cci_advanced.pine) | CCI with pluggable smoothing, three scale modes, OB/OS extreme-zone filter, gradient line, shadow fills, and Sentiment Bar |
| [`fisher_transform_advanced.pine`](indicators/momentum/fisher_transform_advanced/fisher_transform_advanced.pine) | Fisher Transform with reversal-heavy extreme reads, trend context, stall/absorption markers, cross conviction, divergence wedge, and Sentiment Bar |
| [`roc_advanced.pine`](indicators/momentum/roc_advanced/roc_advanced.pine) | Percentage Rate of Change with momentum-stretch zones, trend context, stall/absorption markers, cross conviction, divergence wedge, and Sentiment Bar |
| [`rsi_advanced.pine`](indicators/momentum/rsi_advanced/rsi_advanced.pine) | RSI with smoothed signal, trend context, stall/absorption markers, cross conviction, divergence wedge, long/short directional coloring, and Sentiment Bar |
| [`stoch_rsi_advanced.pine`](indicators/momentum/stoch_rsi_advanced/stoch_rsi_advanced.pine) | Stoch RSI K/D with trend context, stall/absorption markers, cross conviction, divergence wedge, long/short directional coloring, and Sentiment Bar |
| [`tsi_advanced.pine`](indicators/momentum/tsi_advanced/tsi_advanced.pine) | True Strength Index with clean signal crosses, trend context, stall/absorption markers, cross conviction, divergence wedge, and Sentiment Bar |
| [`wavetrend.pine`](indicators/momentum/wavetrend/wavetrend.pine) | WaveTrend oscillator — cross signals, divergence, overextension duration, slope quality filter, zone persistence |
| [`williams_r_advanced.pine`](indicators/momentum/williams_r_advanced/williams_r_advanced.pine) | Williams %R normalized to 0-100 with fast extreme reads, trend context, stall/absorption markers, cross conviction, divergence wedge, and Sentiment Bar |
| [`commodity_flow_trend.pine`](indicators/money_flow/commodity_flow_trend/commodity_flow_trend.pine) | MFI + CCI composite oscillator for commodities — 4-state flow background, extreme-zone reversal signals, optional CCI gate, normalized CCI overlay |
| [`mtf_wavetrend_confluence.pine`](indicators/momentum/mtf_wavetrend_confluence/mtf_wavetrend_confluence.pine) | Tide / Wave / Ripple — WaveTrend across three fixed horizons; the Ripple cross on your chart TF is the signal, graded 0–4 by extreme depth + Wave/Tide agreement (minGrade = 2), two-tier Watch→Signal alerts |
| [`oscillator_divergence_zones.pine`](indicators/momentum/oscillator_divergence_zones/oscillator_divergence_zones.pine) | Oscillator divergence zones — RSI, CCI, MFI, Fisher, TSI, STC, DPO, Roofing, Cyber Cycle; regular + hidden; ATR-wide zones with retest counter |
| [`market_pressure_scale.pine`](indicators/momentum/market_pressure_scale/market_pressure_scale.pine) | Dual-component oscillator — Setup Pressure (coiling) vs Impulse Pressure (expansion), Range Chop Filter, Move Strength gauge, DMI-free Reversal signal (exhaustion plus rejection candle), phase labels and Action-readout dashboard |
| [`oscillator_cycle_statistics.pine`](indicators/mean_reversion/oscillator_cycle_statistics/oscillator_cycle_statistics.pine) | Statistics engine, not a signal — OB→OS/OS→OB cycle state machine, time-consistent progress-/age-conditioning, reliability/Brier evaluation, directional base rates, and origin-based MFE/MAE with explicit trade-evidence limits |
| [`elder_ray_pressure_engine.pine`](indicators/momentum/elder_ray_pressure_engine/elder_ray_pressure_engine.pine) | Elder Ray research framework — four pressure engines (Classic/Directional/True Range/Close-Weighted), selectable consensus and normalization, dominance, exhaustion (separated from raw extremes), pivot divergence, no composite score |

## Liquidity & Order Flow

| Script | What it does |
|--------|--------------|
| [`money_flow_delta_profile.pine`](indicators/money_flow/money_flow_delta_profile/money_flow_delta_profile.pine) | Center-out diverging profile — green (right) = net buying, red (left) = net selling at each price level; POC, Value Area, optional recency weighting |
| [`mfi_advanced.pine`](indicators/money_flow/mfi_advanced/mfi_advanced.pine) | MFI with smoothed signal, no-volume fallback, trend context, stall/absorption markers, divergence wedge, long/short directional coloring, and Sentiment Bar |
| [`anchored_vwap.pine`](indicators/mean_reversion/anchored_vwap/anchored_vwap.pine) | Stage-4 fair-value location sensor — VWAP anchored to swing pivot / session / period / manual date, volume-weighted σ bands, distance-from-value in σ as a symmetric Location output (no triggers) |
| [`midas_curves.pine`](indicators/mean_reversion/midas_curves/midas_curves.pine) | MIDAS 2.0 — anchored MIDAS support/resistance curve (launch-anchored VWAP) plus a true topfinder/bottomfinder accelerated curve with closed-form auto-fit that forecasts trend exhaustion (d/D progress); Location + Exhaustion sensor, context markers not entries |
| [`liquidity_hunter.pine`](indicators/market_structure/liquidity_hunter/liquidity_hunter.pine) | Ranked equal highs/lows — scored BSL/SSL levels, sweep markers, reclaim detection |
| [`candle_pressure_index.pine`](indicators/money_flow/candle_pressure_index/candle_pressure_index.pine) | Raw microstructure buy/sell pressure bias from candle geometry and volume — no derived oscillators; Exchange-only, requires real trade volume |
| [`cvd_bias.pine`](indicators/money_flow/cvd_bias/cvd_bias.pine) | Rolling signed-volume proxy (price-weighted heuristic, not real CVD/Delta), normalized, with price divergence; Exchange-only, requires real trade volume |
| [`klinger_volume_force_map.pine`](indicators/money_flow/klinger_volume_force_map/klinger_volume_force_map_v1_0_0.pine) | Klinger Volume Force (3 formula variants in parallel), regime engine, divergence, flow rejection/confirmed events; Exchange-only, requires real trade volume |

## Pattern & Wave Analysis

| Script | What it does |
|--------|--------------|
| [`zigzag_core.pine`](indicators/market_structure/zigzag_core/zigzag_core.pine) | Configurable ZigZag engine — separated Depth/Backstep/Deviation/Alternation filters, Percent/ATR/Hybrid reversal modes, true higher-timeframe pivot projection, non-repainting-distinct developing last leg |
| [`zigzag_patterns_framework.pine`](indicators/market_structure/zigzag_patterns_framework/zigzag_patterns_framework.pine) | ZigZag-based pattern detection — ABC, triangles, Wolfe waves, 1-2-3 reversal (Sperandeo) |
| [`elliott_wave_radar.pine`](indicators/market_structure/elliott_wave_radar/elliott_wave_radar.pine) | Rule-validated Elliott Wave counting — labels impulses/ABC only when hard EW rules hold, internal Fib-fit candidate ranking + raw Fib ratios, with target projections and invalidation watch |
| [`wolfe_wave_scanner_pro.pine`](indicators/market_structure/wolfe_wave_scanner_pro/wolfe_wave_scanner_pro.pine) | Dedicated 5-point Wolfe Wave scanner — best-of-window swing search, hard-rule validation with internal ranking, EPA target from the true 1-3/2-4 apex, multi-pattern tracking, live invalidation tracking, rule-breakdown debug table |
| [`triangle_compression_scanner_pro.pine`](indicators/market_structure/triangle_compression_scanner_pro/triangle_compression_scanner_pro.pine) | Sliding-window triangle scanner (symmetric/ascending/descending) — boundary lines fit to a swing window, weighted 0-100 score, multi-pattern tracking, live breakout resolution |
| [`broadening_wedge_scanner_pro.pine`](indicators/market_structure/broadening_wedge_scanner_pro/broadening_wedge_scanner_pro.pine) | Sliding-window broadening wedge scanner (descending/ascending/symmetric broadening) — expansion-based sibling to the triangle scanner, weighted 0-100 score, multi-pattern tracking, live breakout resolution |
| [`candle_story_engine.pine`](indicators/market_structure/candle_story_engine/candle_story_engine.pine) | Multi-candle candle-story engine — recency-weighted sequence pressure, dominance, close persistence, compression and trend exhaustion (decoupled from BUY/SELL), follow-through/failure detection; classic candlestick patterns as supporting evidence only |

## Equities & Relative Strength

| Script | What it does |
|--------|--------------|
| [`relative_strength_line.pine`](indicators/relative_strength/relative_strength_line/relative_strength_line.pine) | RS vs. a benchmark (SPY/QQQ) — Mansfield RS oscillator or raw RS line, with the IBD leadership signal (RS new high before price). See [MOMENTUM_EQUITIES.md](MOMENTUM_EQUITIES.md) for the equities roadmap |
