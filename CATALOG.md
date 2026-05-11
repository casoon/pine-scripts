# Indicator Catalog

Status values: **Draft** · **Aktiv** · **Stabil** · **Overengineered** · **Deprecated**

Quality columns (★ 1–5):
- **Konzept** — is the idea sound?
- **Code** — is the implementation clean?
- **Getestet** — validated on real data?

---

## Wyckoff / Market Structure

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [wyckoff_schematics](indicators/wyckoff_schematics/) | 4.3.1 | Aktiv | ★★★★★ | ★★★★☆ | ★★★☆☆ | Phase D/E validation still weak |
| [smc_structure_expectation](indicators/smc_structure_expectation/) | 1.0.0 | Stabil | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | |
| [sr_zones_mtf_v2](indicators/sr_zones_mtf_v2/) | 3.0.0 | Stabil | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | |
| [tweezer_kangaroo_zones](indicators/tweezer_kangaroo_zones/) | 3.0.0 | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [jma_struct](indicators/jma_struct/) | 2.3.0 | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [time_to_react_volatility_time](indicators/time_to_react_volatility_time/) | 1.0.0 | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [coilforge_zones](indicators/coilforge_zones/) | 1.1 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |

## Trend & Regime

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [chandelier_flip_radar](indicators/chandelier_flip_radar/) | 1.4 | Stabil | ★★★★☆ | ★★★★☆ | ★★★★☆ | Promising PF 1.22 |
| [smooth_trend_radar](indicators/smooth_trend_radar/) | 3.3 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [auto_trendlines](indicators/auto_trendlines/) | 1.0 | Stabil | ★★★★☆ | ★★★★☆ | ★★☆☆☆ | |
| [regime_detector](indicators/regime_detector/) | 1.0.0 | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [ma_regime_bands](indicators/ma_regime_bands/) | 1.0.0 | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [relative_leg_efficiency](indicators/relative_leg_efficiency/) | 1.0.0 | Stabil | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | |

## Momentum & Oscillators

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [wavetrend](indicators/wavetrend/) | 1.0 | Stabil | ★★★★★ | ★★★★★ | ★★★★★ | Core, best PF in repo |
| [market_pressure_scale](indicators/market_pressure_scale/) | 1.0 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [oscillator_divergence_zones](indicators/oscillator_divergence_zones/) | 1.2 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [mtf_stochrsi_pair_score](indicators/mtf_stochrsi_pair_score/) | 1.1.0 | Draft | ★★★☆☆ | ★★★★☆ | ★☆☆☆☆ | New, untested |
| [market_exhaustion](indicators/market_exhaustion/) | 1.0.0 | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [market_stress_oscillator](indicators/market_stress_oscillator/) | 1.0.0 | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |

## Reversal & Entry

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [reversal_engine_score](indicators/reversal_engine_score/) | 1.5 | Aktiv | ★★★★☆ | ★★★★☆ | ★★★☆☆ | Score logic needs rework (test131) |
| [reversal_type_classifier](indicators/reversal_type_classifier/) | 1.2 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [commodity_heat_reversal](indicators/commodity_heat_reversal/) | 1.1 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |

## Liquidity & Volume

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [volume_strata](indicators/volume_strata/) | 1.9 | Stabil | ★★★★★ | ★★★★☆ | ★★★☆☆ | |
| [money_flow_delta_profile](indicators/money_flow_delta_profile/) | 1.1 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [vwap_cross_visuals](indicators/vwap_cross_visuals/) | 2.0.0 | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |

## Pattern & Wave

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [zigzag_patterns_framework](indicators/zigzag_patterns_framework/) | 1.0.0 | Stabil | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | |
| [zigzag_fibo_pullback_map](indicators/zigzag_fibo_pullback_map/) | 1.2.0 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |

## Commodity / Multi-TF Matrix

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [commodity_pulse_matrix](indicators/commodity_pulse_matrix/) | 3.1 | Stabil | ★★★★★ | ★★★★★ | ★★★★★ | Published, v4 in progress |

## Vein Suite

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [vein_trend](indicators/vein/) | 2.0 | Stabil | ★★★★★ | ★★★★★ | ★★★★☆ | Core |
| [vein_pullback](indicators/vein/) | 2.0 | Stabil | ★★★★★ | ★★★★★ | ★★★★☆ | Core |
| [vein_exhaustion](indicators/vein/) | 2.0 | Stabil | ★★★★★ | ★★★★★ | ★★★★☆ | Core |
| [vein_accumulation_phase](indicators/vein/) | 2.0 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | NatGas focused |
| [vein_reversal_score](indicators/vein/) | 2.0 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [vein_structure_zones](indicators/vein/) | 2.0 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [vein_execution](indicators/vein/) | 2.0 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | 15m timing overlay |
| [vein_spread_context](indicators/vein/) | 2.0 | Stabil | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | Commodity spread modifier |
| [vein_feature_exporter](indicators/vein/) | 2.0 | Stabil | ★★★★★ | ★★★★☆ | ★★★★★ | Research tooling |
| [vein_reversal_labeler](indicators/vein/) | 2.0 | Stabil | ★★★★☆ | ★★★★☆ | ★★★★☆ | ML labeling only |
| [vein_reversal_zones](indicators/vein/vein_reversal_zones/) | 2.0 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |

---

## Archiv

Nicht mehr aktiv gepflegt. Dateien liegen unter `archive/` und können wiederhergestellt werden.

| Indikator / Datei | Grund |
|---|---|
| [liquidity_hunter](archive/indicators/liquidity_hunter/) | Erfordert nicht gepflegte RTA-Libraries |
| [smart_money_dashboard](archive/indicators/smart_money_dashboard/) | Erfordert nicht gepflegte RTA-Libraries |
| [mtf_trend_alignment](archive/indicators/mtf_trend_alignment/) | Erfordert nicht gepflegte RTA-Libraries |
| [pattern_recognition](archive/indicators/pattern_recognition/) | Overengineered, kaum getestet |
| [wave_navigator](archive/indicators/wave_navigator/) | Elliott-Wave-Autoerkennung konzeptionell schwach |
| [rj_wave](archive/indicators/rj_wave/) | Zu nische, kein aktiver Einsatz |
| [relative_leg_efficiency_panel_chart](archive/indicators/relative_leg_efficiency_panel_chart/) | Visualisierungs-Experiment, Basis-Version ist vollständiger |
| [flow_bias](archive/indicators/flow_bias/) | Überschneidung mit market_pressure_scale und mtf_stochrsi_pair_score |
| [candle_pressure_response_jma](archive/indicators/candle_pressure_response_jma/) | Candle-Metriken bereits in Vein suite (vein_exhaustion, vein_feature_exporter) |
| [wavetrend_strategy.pine](archive/strategies/wavetrend/) | Superseded durch v4 |
| [wavetrend_base_strategy.pine](archive/strategies/wavetrend/) | Superseded durch v4 |
| [wavetrend_v3_strategy.pine](archive/strategies/wavetrend/) | Superseded durch v4 |
