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
| [smc_structure_expectation](indicators/smc_structure_expectation/) | — | Stabil | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | |
| [sr_zones_mtf_v2](indicators/sr_zones_mtf_v2/) | — | Stabil | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | |
| [tweezer_kangaroo_zones](indicators/tweezer_kangaroo_zones/) | — | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [jma_struct](indicators/jma_struct/) | — | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [time_to_react_volatility_time](indicators/time_to_react_volatility_time/) | — | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [coilforge_zones](indicators/coilforge_zones/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |

## Trend & Regime

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [chandelier_flip_radar](indicators/chandelier_flip_radar/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★★★☆ | Promising PF 1.22 |
| [smooth_trend_radar](indicators/smooth_trend_radar/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [auto_trendlines](indicators/auto_trendlines/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★☆☆☆ | |
| [regime_detector](indicators/regime_detector/) | — | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [ma_regime_bands](indicators/ma_regime_bands/) | — | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [mtf_trend_alignment](indicators/mtf_trend_alignment/) | — | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | Requires RTA libs |
| [relative_leg_efficiency](indicators/relative_leg_efficiency/) | — | Stabil | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | |

## Momentum & Oscillators

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [wavetrend](indicators/wavetrend/) | — | Stabil | ★★★★★ | ★★★★★ | ★★★★★ | Core, best PF in repo |
| [market_pressure_scale](indicators/market_pressure_scale/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [oscillator_divergence_zones](indicators/oscillator_divergence_zones/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [mtf_stochrsi_pair_score](indicators/mtf_stochrsi_pair_score/) | 1.1.0 | Draft | ★★★☆☆ | ★★★★☆ | ★☆☆☆☆ | New, untested |
| [flow_bias](indicators/flow_bias/) | — | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [market_exhaustion](indicators/market_exhaustion/) | — | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [market_stress_oscillator](indicators/market_stress_oscillator/) | — | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [candle_pressure_response_jma](indicators/candle_pressure_response_jma/) | — | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |

## Reversal & Entry

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [reversal_engine_score](indicators/reversal_engine_score/) | — | Aktiv | ★★★★☆ | ★★★★☆ | ★★★☆☆ | Score logic needs rework (test131) |
| [reversal_type_classifier](indicators/reversal_type_classifier/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [commodity_heat_reversal](indicators/commodity_heat_reversal/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |

## Liquidity & Volume

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [volume_strata](indicators/volume_strata/) | — | Stabil | ★★★★★ | ★★★★☆ | ★★★☆☆ | |
| [money_flow_delta_profile](indicators/money_flow_delta_profile/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [vwap_cross_visuals](indicators/vwap_cross_visuals/) | — | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |

## Pattern & Wave

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [zigzag_patterns_framework](indicators/zigzag_patterns_framework/) | — | Stabil | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | |
| [zigzag_fibo_pullback_map](indicators/zigzag_fibo_pullback_map/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |

## Commodity / Multi-TF Matrix

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [commodity_pulse_matrix](indicators/commodity_pulse_matrix/) | v3 | Stabil | ★★★★★ | ★★★★★ | ★★★★★ | Published, v4 in progress |

## Vein Suite

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [vein_trend](indicators/vein/) | — | Stabil | ★★★★★ | ★★★★★ | ★★★★☆ | Core |
| [vein_pullback](indicators/vein/) | — | Stabil | ★★★★★ | ★★★★★ | ★★★★☆ | Core |
| [vein_exhaustion](indicators/vein/) | — | Stabil | ★★★★★ | ★★★★★ | ★★★★☆ | Core |
| [vein_accumulation_phase](indicators/vein/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | NatGas focused |
| [vein_reversal_score](indicators/vein/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [vein_structure_zones](indicators/vein/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [vein_execution](indicators/vein/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | 15m timing overlay |
| [vein_spread_context](indicators/vein/) | — | Stabil | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | Commodity spread modifier |
| [vein_feature_exporter](indicators/vein/) | — | Stabil | ★★★★★ | ★★★★☆ | ★★★★★ | Research tooling |
| [vein_reversal_labeler](indicators/vein/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★★★☆ | ML labeling only |
| [vein_reversal_zones](indicators/vein/vein_reversal_zones/) | — | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |

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
| [wavetrend_strategy.pine](archive/strategies/wavetrend/) | Superseded durch v4 |
| [wavetrend_base_strategy.pine](archive/strategies/wavetrend/) | Superseded durch v4 |
| [wavetrend_v3_strategy.pine](archive/strategies/wavetrend/) | Superseded durch v4 |
