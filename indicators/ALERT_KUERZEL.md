# Alert-Kürzel-Registry

Stabile, kollisionsfreie Kurz-Codes pro Indikator für Alert-Messages. Siehe Skill
`indicator-alerts` §4 für das Message-Format. **Kürzel sind über Versionen stabil** — bei neuem
Indikator hier einen eindeutigen Code eintragen, bestehende nie umbenennen (sonst brechen die
Alert-Regeln der User).

Message-Kanon: `<Kürzel> · <EVENT> · {{ticker}} {{interval}}` (optionaler State angehängt, z. B.
` · Score={{plot("Consensus Score")}}`). Der `alertcondition()`-**Titel** bleibt unverändert
(TradingView bindet bestehende User-Alerts an den Titel) — nur die Message folgt dem Kanon.

| Indikator | Kürzel |
|---|---|
| commodity_pulse_matrix_v3 | CPM3 |
| commodity_pulse_matrix_v4 | CPM4 |
| signal_quality_engine | SQE |
| coilforge_zones | CFZ |
| elliott_wave_radar | EWR |
| jma_struct | JMAS |
| liquidity_hunter | LQH |
| market_structure_advanced | MSA |
| market_structure_pivot_map | MSPM |
| modern_wyckoff_state_machine_visual | MWSM |
| smc_structure_expectation | SMCE |
| sr_zones_mtf_v2 | SRZ |
| structure_break_risk | SBR |
| swing_conviction_radar | SCR |
| tweezer_kangaroo_zones | TKZ |
| wyckoff_schematics | WYS |
| zigzag_patterns_framework | ZPF |
| anchored_vwap | AVWAP |
| midas_curves | MIDAS |
| cci_advanced | CCIA |
| market_pressure_scale | MPS |
| market_stress_oscillator | MSO |
| momentum_trajectory | MTJ |
| mtf_stochrsi_pair_score | MSRP |
| oscillator_topology | OTOP |
| wavetrend_advanced_smoothing | WTAS |
| williams_vix_fix_advanced | WVFA |
| candle_pressure_index | CPI |
| commodity_flow_trend | CFT |
| cvd_bias | CVDB |
| volume_strata | VST |
| relative_leg_efficiency | RLE |
| vein_accumulation_phase | VEIN-ACC |
| vein_execution | VEIN-EXE |
| vein_exhaustion | VEIN-EXH |
| vein_feature_exporter | VEIN-FX |
| vein_pullback | VEIN-PB |
| vein_reversal_score | VEIN-RS |
| vein_spread_context | VEIN-SPC |
| vein_structure_zones | VEIN-SZ |
| vein_trend | VEIN-TR |
| adx_advanced | ADXA |
| bayesian_trend_factor | BTF |
| markov_state_engine | MSE |
| regime_classifier | RGC |
| regime_detector | RDP |
| trend_persistence_score | TPS |
| atr_advanced | ATRA |
| compression_fractal_release | CFR |
| smooth_trend_radar | STR |
| ma_regime_bands | MRB |
| wavetrend | WT |
| wavetrend_v2 | WT2 |
| wavetrend_v3 | WT3 |
| chandelier_flip_radar | CHFR |
| oscillator_divergence_zones | ODZ |
| market_exhaustion | MEX |
| mtf_wavetrend_opportunity_hunter | WTOH |
| reversal_engine_score | RES |
| exhaustion_scanner | EXS |
| mtf_wavetrend_confluence | TWR |
| commodity_heat_reversal | CHR |
| relative_strength_line | RSL |
| mtf_structure_bias | MSB |
| vwap_cross_visuals | VXV |

**Kollisions-Hinweis `CFR` / `CHFR`:** `CFR` gehört `compression_fractal_release` (exaktes Akronym,
tief verankert: Indicator-Shorttitle, Log-Rows `CFR BREAK`/`CFR BAR`, Tabelle). `chandelier_flip_radar`
benutzt historisch ebenfalls `CFR` in seinen Alert-**Titeln** (z. B. „CFR Buy Signal") — diese Titel
bleiben aus Kompatibilität unverändert, die **Messages** nutzen aber `CHFR`.
