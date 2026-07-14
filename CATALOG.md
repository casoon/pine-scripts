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
| [wyckoff_schematics](indicators/market_structure/wyckoff_schematics/) | 4.8.0 | Aktiv | ★★★★★ | ★★★★☆ | ★★★☆☆ | v4.7/4.8: strengere Breakout-Bestätigung (Phase D + interne Struktur + Min-Score → Markup/Markdown), Sequenz-Validierung im Setup-Score, eigene SOSB/SOWB-Breakout-Events; Live-Validierung der Phase-D/E-Schärfung steht noch aus |
| [modern_wyckoff_state_machine_visual](indicators/market_structure/modern_wyckoff_state_machine_visual/) | 1.3 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | Lite-Wyckoff-State-Machine: Locked Range, range-begrenzte A-E Phasenzonen, Cause-Score, Spring/UTAD-Quality, echte Tests, pivot-bestätigte LPS/LPSY; ungetestet |
| [smc_structure_expectation](indicators/market_structure/smc_structure_expectation/) | 1.1.0 | Stabil | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | |
| [sr_zones_mtf_v2](indicators/market_structure/sr_zones_mtf_v2/) | 3.1.0 | Stabil | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | |
| [tweezer_kangaroo_zones](indicators/market_structure/tweezer_kangaroo_zones/) | 3.1.0 | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [jma_struct](indicators/market_structure/jma_struct/) | 2.3.1 | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [time_to_react_volatility_time](indicators/volatility/time_to_react_volatility_time/) | 1.1.0 | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [coilforge_zones](indicators/market_structure/coilforge_zones/) | 1.2.2 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [market_structure_advanced](indicators/market_structure/market_structure_advanced/) | 1.0 | Draft | ★★★★☆ | ★★★★☆ | ★☆☆☆☆ | HH/HL/LH/LL Pivot-Klassifizierung → gebundener Score-Oszillator [−100, +100]; Signal-Line, Gradient, Shadow-Fills, optionale Chart-Labels |
| [market_structure_pivot_map](indicators/market_structure/market_structure_pivot_map/) | 1.0 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | Location-Tool: HTF Pivots/CPR/Projektionen (D/W/M, Classic/Fib), Cross-TF-Confluence via Greedy-Clustering, Nearest-S/R mit ATR-Distanz; bewusst kein Signalgenerator; ungetestet |
| [structure_break_risk](indicators/market_structure/structure_break_risk/) | 2.1.0 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | RSI-Pane mit Momentum-Divergenz-Linien auf dem RSI (frühester Riss, dort sichtbar wo er lesbar ist); per force_overlay auf dem Preis-Chart: Break-Level-Linie + Risk-Zone, Trend-Kontext-EMA, Wort-Event-Labels (Watch/Break Pressure/Structure Broken/Pressure Faded), kompaktes mobilfreundliches Info-Label (Text, keine Tabelle) mit Score + Mini-Bars je Sensor; risiko-codierte Farben (neutral→orange→rot→dunkelrot), nicht richtungs-grün/rot; symmetrisch, latchender Trend-Kontext; 5 gewichtete Sensoren (Near Level, Confirmed BOS, Failed Breakout, Structure Erosion, Pivot-Divergenz); Pivots nur als Level-Referenz; Companion zu TPS; ungetestet |
| [trading_range_state_machine](indicators/market_structure/trading_range_state_machine/) | 1.1 | Draft | ★★★☆☆ | ★★★☆☆ | ☆☆☆☆☆ | Pivot-Cluster-Range-Erkennung (Fallback auf Highest/Lowest-Fenster) mit 8-Faktor-gewichtetem Range-Score (ER, Candle Overlap, Chop, Structure Chaos, Regression Flatness, Boundary Stability, ATR Compression, Mean Reversion); State Machine Inactive/Building/Confirmed/Mature/Breaking mit Richtungs-Unterscheidung (Up/Down); Position-in-Range (%+Zone); kontinuierlich skalierendes Background Heat; Range-Lines, Midline, Touch-Marker, Ribbon, Dashboard; ungetestet |

## Trend & Regime

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [chandelier_flip_radar](indicators/trend_direction/chandelier_flip_radar/) | 1.6 | Stabil | ★★★★☆ | ★★★★★ | ★★★☆☆ | PF 1.22 (pre-v1.6, vor Ratchet-Fix → Strategie neu validieren); v1.5 optionaler MTF-Confluence-Layer; v1.6 Ratchet-Fix + Conviction-Mode + K-means auf echtem Chandelier + direktionale States + Weak-Flip-Marker |
| [smooth_trend_radar](indicators/trend_direction/smooth_trend_radar/) | 3.5.0 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | v3.4.0: ATR-scaled slope-threshold trend detection + hysteresis, rejections fire in both ADX regimes, optional volume/vol-adaptive filters; v3.5.0: Trend Strength (percentile-ranked slope magnitude) |
| [auto_trendlines](indicators/market_structure/auto_trendlines/) | 1.1.1 | Stabil | ★★★★☆ | ★★★★☆ | ★★☆☆☆ | |
| [regime_detector](indicators/trend_strength/regime_detector/) | 1.1.0 | Stabil | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | v1.1: Vola-Dimension + Regime-Reife + Playbook + RS-Modifier (Aktien) |
| [ma_regime_bands](indicators/trend_direction/ma_regime_bands/) | 1.0.1 | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [relative_leg_efficiency](indicators/relative_strength/relative_leg_efficiency/) | 1.0.1 | Stabil | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | |
| [adx_advanced](indicators/trend_strength/adx_advanced/) | 1.0 | Draft | ★★★★☆ | ★★★★☆ | ★☆☆☆☆ | ADX + DI± mit pluggablem Smoothing, 4-State-Histogramm, Gradient-Linie, DI-Crossover-Signale |
| [regime_classifier](indicators/trend_strength/regime_classifier/) | 1.1 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | Reversal-Pipeline Stufe 1: FDI + Kaufman Efficiency Ratio + Choppiness → Trend/Range/Chaos mit Hysterese; symmetrische Reversal-/Trend-Permission als Quality-Output (kein Trigger); v1.1 optionale HTF-Regime-Linie (visuell, kein Veto); ungetestet |
| [trend_persistence_score](indicators/trend_strength/trend_persistence_score/) | 1.0 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | Graded-Score-Komplement zu regime_classifier: R² + Kaufman ER + ADX-Stärke/Slope + FDI → ein 0–100 Trend-Persistenz-Oszillator (Magnitude, richtungsneutral); State Strong/Healthy/Transition/Weak/Dead mit Hysterese, Kalibrier-Anker als Inputs, Richtung nur visuell; ungetestet |
| [bayesian_trend_factor](indicators/trend_strength/bayesian_trend_factor/) | 1.7 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | Bayesian-inspirierter Trend-Qualitätsfilter: Regression-Richtung + gegatete ADX/ER/R²-Stärke + korrekt gealterte Swing-Struktur + Exhaustion-Penalty → signierter −100..+100 Trend Factor mit separater Confidence, kurzer Glättung und State-Hysterese; Volatilität nur als Quality-Multiplier; PB/CONT-Labels mit Hover-Erklärungen und HAMA-artige Trend Candles; ungetestet |
| [markov_state_engine](indicators/trend_strength/markov_state_engine/) | 1.5.0 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | Regime-Resolution-Map (keine Prognose): Sechs-State-Klassifikator (Up/Down Trend, Up/Down Weak, Compression, Expansion/Chaos) — Extremzustände zuerst, State debounced gegen Flicker; EXIT-konditionierter Markov (Self-Transitions als Persistence separat); zwei getrennte Achsen: TIMING (Maturity = aktueller/typischer Dwell aus Persistence, robust) vs RICHTUNG (Exit-Verteilung, meist dünn → `dir thin`-Flag); Reliability = Sample-Adäquanz × Richtungs-Predictability (norm. Entropie); Netto-Resolution-Linie (Fill = Reliability); Hysterese-Bias, Edge mit Reversal/Breakout/Continuation-Typing; ehrliche Readout-Farbe (grün/rot reliable · amber coiled · grau sonst); Extended-State-Alert; ADX nur Stärke, kein Trigger; v1.5.0: EMA-Slope ATR-normalisiert, Compression braucht zusätzlich BB-Width-Rank, Context-konditioniertes Markov-Matching (Compression bull/bear/neutral), Readout in Timing/Richtung/Quality-Zeilen; ungetestet |
| [market_memory_decay_oscillator](indicators/trend_strength/market_memory_decay_oscillator/) | 1.0 | Draft | ★★★☆☆ | ★★★☆☆ | ☆☆☆☆☆ | Signiertes Carry/Decay-Oszillator: Autokorrelations-Half-Life + Hurst-Approximation + Path Efficiency + Range-Expansion/-Decay → ein Score, wie lange der aktuelle Impuls statistisch trägt bevor er in Richtung Rauschen zerfällt; Bullish/Bearish Carry & Decay States, Impulse-Marker, Dashboard; ungetestet |
| [regime_transition_engine](indicators/trend_strength/regime_transition_engine/) | 1.0 | Draft | ★★★☆☆ | ★★★☆☆ | ☆☆☆☆☆ | Sieben-State-Regime-Klassifikator (Noise/Compression/Expansion/Trend Up/Down/Exhaustion/Reversion) aus geteiltem Feature-Set (VolPct, Efficiency, Chop, Slope, Return-Z, Variance Ratio, Autokorrelation); Dwell+Hysterese-Debouncing gegen State-Flicker; gerichteter Transition-Pressure-Oszillator je Nachfolge-State; State-Change-Events + Dashboard; ungetestet |
| [predictability_regime_index](indicators/trend_strength/predictability_regime_index/) | 1.0 | Draft | ★★★☆☆ | ★★★☆☆ | ☆☆☆☆☆ | Signierter −100..+100 Index aus Variance Ratio, Return-Autokorrelation, Hurst-Approximation und Fractal Efficiency → Momentum/Reversion/Noise/Mixed-Regime-Klassifikation mit Confidence (Stärke × Sensor-Übereinstimmung); ungetestet |
| [adaptive_arithmetic_candles](indicators/trend_direction/adaptive_arithmetic_candles/) | 1.2 | Draft | ★★★☆☆ | ★★★☆☆ | ☆☆☆☆☆ | Efficiency-adaptiver Candle-Transform (Kaufman ER + Regression-Anker) + regressions-gestützter Body-Boost; 0-100 Trend Quality Score (Efficiency/Slope/Body-Ratio/Follow-Through); Flip = Vorwarnung, Long/Short-Signal = Setup (strongBull/Bear) + Breakout-Trigger statt Flip-als-Trade; ungetestet |
| [modern_trend_regime](indicators/trend_direction/modern_trend_regime/) | 1.3.1 | Draft | ★★★☆☆ | ★★★☆☆ | ☆☆☆☆☆ | Trend/Range/Übergang-Regime — beide Seiten als Faktor-Score statt AND-Kette (Trend: ADX+ER+DI+Stack+Preis, 4/5 bzw. 5/5 bei Range Trading; Range: 4 Faktoren, 3/4 bzw. 4/4), sofortiger Übergang bei Strukturverlust, nur Neueinstieg bestätigungsgefiltert; echte Range-Struktur mit eingefrorenen Swing-Grenzen statt ATR-Band, einmalig scharfgeschaltete Breakouts, entprellte Reaktionen; Trendbestätigung an Regime-Wechsel gekoppelt, kleiner Dreieck-Marker mit Hover-Tooltip statt Textlabel; sechs Presets + Benutzerdefiniert; ungetestet |

## Volatility

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [atr_advanced](indicators/volatility/atr_advanced/) | 1.0 | Draft | ★★★★☆ | ★★★★☆ | ★☆☆☆☆ | ATR in 4 Anzeigemodi (Raw, ATR%, Normalized, Percentile Rank), pluggables Smoothing, Gradient, Expansion/Contraction-Signale |
| [williams_vix_fix_advanced](indicators/volatility/williams_vix_fix_advanced/) | 1.9 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | Synthetischer Fear-Gauge (Williams VIX Fix): Bull-WVF + Bear-WVF-Spiegel, StdDev/Percentile-Bänder, Stall/Absorption (pro Seite unabhängig), Context-EMA, Divergenz-Wedge, Gradient-Coloring; Spike Quality (0–100), Reclaim-Signal (Long/Short) mit Quality-Gate, Sentiment Bar (±100 Bull/Bear-Dominanz) statt Pfeil-Marker, View Mode Clean/Balanced/Full; ungetestet |
| [compression_fractal_release](indicators/volatility/compression_fractal_release/) | 1.0 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | Coil→Release-Detektor: Symbol-Entropie-Komplexität + Box-Counting-FDI + Efficiency erkennen eine komprimierte Korrektur im HTF-Trend; Band-Break = einziger Trigger, Setup-Score multiplikativ (Coil-Ceiling × Release-Dynamik → hoher Coil allein feuert nicht), Chop-Veto, Per-Direction-Cooldown; HTF-Regime klassifiziert Release (Continuation) vs Base Break (Counter-Trend); Watch→Setup→Trigger-Staging, Debug-Log; ungetestet |

## Momentum & Oscillators

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [cci_advanced](indicators/momentum/cci_advanced/) | 1.4.1 | Draft | ★★★★☆ | ★★★★☆ | ★☆☆☆☆ | CCI mit pluggablem Smoothing, 3 Scale-Modes, OB/OS-Zone-Filter, Gradient + Shadow-Fills |
| [fisher_transform_advanced](indicators/momentum/fisher_transform_advanced/) | 1.3 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | Fisher Transform mit Trend-Kontext, Stall/Absorption, Cross-Conviction, Divergenz-Wedge und reversal-lastiger Extremwert-Lesart; ungetestet |
| [roc_advanced](indicators/momentum/roc_advanced/) | 1.4 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | Prozentuale ROC mit Momentum-Stretch-Zonen, Trend-Kontext, Stall/Absorption, Cross-Conviction, Divergenz-Wedge und Long/Short-Farbsprache; ungetestet |
| [rsi_advanced](indicators/momentum/rsi_advanced/) | 1.3 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | RSI mit Signal-Line, Trend-Kontext, Stall/Absorption, Cross-Conviction, Divergenz-Wedge und Long/Short-Farbsprache; ungetestet |
| [stoch_rsi_advanced](indicators/momentum/stoch_rsi_advanced/) | 1.2 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | Stoch RSI K/D mit Trend-Kontext, Stall/Absorption, Cross-Conviction, Divergenz-Wedge und Long/Short-Farbsprache; ungetestet |
| [tsi_advanced](indicators/momentum/tsi_advanced/) | 1.2 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | True Strength Index mit sauberer Signal-Line, Trend-Kontext, Stall/Absorption, Cross-Conviction, Divergenz-Wedge und Long/Short-Farbsprache; ungetestet |
| [wavetrend](indicators/momentum/wavetrend/) | 1.1 | Stabil | ★★★★★ | ★★★★★ | ★★★★★ | Core, best PF in repo |
| [wavetrend_advanced_smoothing](indicators/momentum/wavetrend_advanced_smoothing/) | 1.1.1 | Draft | ★★★★☆ | ★★★★☆ | ★☆☆☆☆ | WaveTrend mit 8 Smoothing-Kernels + reichhaltige Visualisierung (Gradient, Shadow-Fill, 4-State-Histogramm) |
| [williams_r_advanced](indicators/momentum/williams_r_advanced/) | 1.3 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | Williams %R auf 0-100 normalisiert, mit Trend-Kontext, Stall/Absorption, Cross-Conviction, Divergenz-Wedge und schneller Extremwert-Lesart; ungetestet |
| [mtf_wavetrend_opportunity_hunter](indicators/momentum/mtf_wavetrend_opportunity_hunter/) | 2.6 | Draft | ★★★★☆ | ★★★★☆ | ★☆☆☆☆ | Konfluenz-Pane + Heat-Ribbons; v2.1: RRG-Rotation-Map (Polyline), Ehlers Ultimate Smoother Core (TASC 2024), Entropie-Noise-Floor; ungetestet |
| [mtf_wavetrend_confluence](indicators/momentum/mtf_wavetrend_confluence/) | 0.7 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | Tide/Wave/Ripple — WT über drei feste Horizonte; Ripple-Cross auf Chart-TF IST das Signal, GRADED 0–5 (kein Gate), Reversal/Continuation-Read; v0.7: Two-Tier-Alerts (Watch→Signal), Deep-Tier von Exhaustion entkoppelt, Divergenz +1, Horizon Fixed/Relative, MTF Auto-Off >4h; ungetestet |
| [commodity_flow_trend](indicators/money_flow/commodity_flow_trend/) | 1.0 | Draft | ★★★★☆ | ★★★★☆ | ★☆☆☆☆ | MFI + CCI Composite für Rohstoffe; 4-State-Flow-Background, Extreme-Zone-Signale, CCI-Gate |
| [market_pressure_scale](indicators/momentum/market_pressure_scale/) | 2.4.0 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | Zwei-Komponenten-Oszillator: Setup Pressure (Coiling) vs. Impulse Pressure (Expansion), Range-Chop-Filter mit Priorität, Move-Strength-Spalten (erwartete Move-Magnitude, 5 Opazitäts-Bänder), DMI-freies Reversal-Signal (Exhaustion+Wick+Setup-Score), Dashboard mit Action-Zeile; v2.0–2.4: Regime Map/Market Character/StochRSI/MFI/WT-Overlays entfernt (rein dekorativ), Failed-Coil/Naked-Impulse/Reversal geschärft |
| [oscillator_divergence_zones](indicators/momentum/oscillator_divergence_zones/) | 1.5.0 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | v1.5: Zone-Break-Logik-Fix (Boundary statt Pivot-Level), Touch-Debounce, Quality Score 0–100, Dashboard, optionaler Trendfilter für Hidden Div; v1.4: STC + DPO + Ehlers Roofing + Cyber Cycle als zusätzliche Divergenz-Quellen (Tier-3-Bewertung) — Reversal-Pipeline Stufe 2 |
| [mtf_stochrsi_pair_score](indicators/momentum/mtf_stochrsi_pair_score/) | 2.0.0 | Draft | ★★★☆☆ | ★★★★☆ | ★☆☆☆☆ | MTF-StochRSI-Konfluenz-Scorer: Per-TF-Score (±100) über 6 TFs, gewichtete Paare (Sync-Bonus/Konflikt-Penalty), TF Agreement Index, geglätteter Total-Score; v2.0.0: Bias/Quality/Timing-State-Engine (z.B. "LONG CONFIRMED · CLEAN · FRESH") als reines Readout, Debug-Tabelle (per-TF/per-Pair) hinter Toggle; v1.8.0: auf Kern zurückgestutzt (Squeeze-Momentum-Subsystem entfernt) |
| [market_exhaustion](indicators/momentum/market_exhaustion/) | 1.1.0 | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |
| [market_stress_oscillator](indicators/momentum/market_stress_oscillator/) | 1.0.2 | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | |

## Reversal & Entry

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [reversal_engine_score](indicators/momentum/reversal_engine_score/) | 1.6 | Aktiv | ★★★★☆ | ★★★★☆ | ★★★☆☆ | Score logic needs rework (test131) |
| [reversal_type_classifier](indicators/market_structure/reversal_type_classifier/) | 1.2 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [commodity_heat_reversal](indicators/composite/commodity_heat_reversal/) | 1.4.3 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [exhaustion_scanner](indicators/momentum/exhaustion_scanner/) | 2.2 | Draft | ★★★★☆ | ★★★★☆ | ★☆☆☆☆ | Rollen-getrennt: Stretch/Exhaustion/Reaction-Scores, Vola als Multiplikator, Regime-Klassifikator (Continuation Risk / Trend Exhaustion / Range Fade); Exhaustion-Zonen (Box) + fette Labels mit Hover-Breakdown; ein Score für Dashboard+Label; ungetestet |

## Liquidity & Volume

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [volume_strata](indicators/money_flow/volume_strata/) | 1.9 | Stabil | ★★★★★ | ★★★★☆ | ★★★☆☆ | |
| [money_flow_delta_profile](indicators/money_flow/money_flow_delta_profile/) | 2.0 | Aktiv | ★★★★★ | ★★★★☆ | ★★★☆☆ | HVN/LVN/AVN + LVN-Zonen; v2.0: Intrabar-Delta (LTF) + Absorption-Profil/-Zonen — neue Features ungetestet |
| [mfi_advanced](indicators/money_flow/mfi_advanced/) | 1.3 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | MFI mit Signal-Line, No-Volume-Fallback, Trend-Kontext, Stall/Absorption, Cross-Conviction, Divergenz-Wedge und Long/Short-Farbsprache; ungetestet |
| [vwap_cross_visuals](indicators/mean_reversion/vwap_cross_visuals/) | 2.1.0 | Stabil | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | v2.1: auf VWAP-Cross-Kernsignal fokussiert (Signal Scope default), Cross-Marker als Hover-Labels; Runtime-/Limit-Fixes |
| [midas_curves](indicators/mean_reversion/midas_curves/) | 2.3 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | MIDAS S/R-Kurve (launch-anchored VWAP) + echter Topfinder/Bottomfinder mit Closed-Form-Auto-Fit; Location (Distanz/Band) + Exhaustion 4-stufig (no fit/running/late/expired); Auto-Last-Swing-Anker, Hybrid-Bänder, Reclaim nur nach Stretch, entdirektionalisierte Alerts, TBF-Linienbruch bei Re-Anker; v2.3: Element\|Wert\|Deutung-Dashboard mit TF-abhängiger Read-Zeile; Kontext-Marker statt Trigger; TBF auf Daily-Legs Log-validiert, intraday ungetestet |
| [anchored_vwap](indicators/mean_reversion/anchored_vwap/) | 1.0 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | Reversal-Pipeline Stufe 4 (Location): AVWAP ankerbar an Swing-Pivot/Session/Periode/Datum, volumengewichtete σ-Bänder, Distanz-zu-Value in σ als symmetrischer Location-Output (kein Trigger); ungetestet |
| [liquidity_hunter](indicators/market_structure/liquidity_hunter/) | 3.4.0 | Stabil | ★★★★☆ | ★★★★☆ | ★★☆☆☆ | BSL/SSL scoring + FVGs + Stop Hunts + Exhaustion Events; v3.3: Sweep/Breakout-Trennung, Wick-Quality Hunts, Struktur-/optionaler Regime-Bonus im Reclaim-Score, optionaler Level-Flip; v3.3.1: Hunt/Reclaim/Exhaustion als Wort-Label mit Hover-Tooltip statt Kreuz/Kürzel-Plotshapes; v3.4.0: FVG-Fill-Bug (Gaps wurden sofort wieder gelöscht) gefixt, gesweepte Level fallen aus Active-Scoring raus, globale (statt pro-Richtung) Event-Priorität, WT-Bonus nutzt Threshold-Input, Dashboard/State-Overhaul — neue Features ungetestet |

## Pattern & Wave

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [zigzag_patterns_framework](indicators/market_structure/zigzag_patterns_framework/) | 1.0.2 | Stabil | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | |
| [zigzag_fibo_pullback_map](indicators/market_structure/zigzag_fibo_pullback_map/) | 1.2.1 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [elliott_wave_radar](indicators/market_structure/elliott_wave_radar/) | 1.2 | Draft | ★★★★☆ | ★★★★☆ | ★★☆☆☆ | Regelvalidierte EW-Zählung inkl. Zigzag/Flat-Korrekturen + C-Setup; v1.2: Wellenpunkte auf echte Extreme verankert (Praxistest-Feedback) |
| [wolfe_wave_scanner_pro](indicators/market_structure/wolfe_wave_scanner_pro/) | 4.13 | Draft | ★★★★☆ | ★★★★☆ | ★☆☆☆☆ | Dedizierter 5-Punkt-Wolfe-Wave-Scanner (Score statt Wyckoff/Elliott-Framework-Overlap), bewusst als struktureller Setup-Finder mit Qualitäts-Score positioniert statt als Signalmaschine (Wolfe ist stark interpretationsabhängig); chart-bestätigte Lücke im `boundaryHoldOk`-Veto geschlossen (prüft jetzt symmetrisch beide Grenzen 1-3/2-4); v4.13: neuer `barsInsideOk`-Hard-Veto scannt jeden Bar (nicht nur die gewählten Swings) zwischen Punkt 1 und 5 gegen beide Kanalgrenzen; v4.12: `Max. gleichzeitige Patterns` Default 5→1 (nur bestes Pattern); v4.11: Invalidierungslinie zieht nicht mehr bis zum rechten Rand, sondern konfigurierbaren Bar-Überstand; drei weitere Hard-Gate-Fixes (Boundary Hold v4.5, P5-Zone v4.6, Convergence v4.7) sowie Mehrfach-Pattern-Tracking/Overlap-Erkennung/Eviction (v4.0-v4.4) weiterhin in Kraft, Details siehe CHANGELOG.md; Best-of-Window-Suche über nicht-konsekutive Swing-Kombinationen mit Punkt-5-Anker über alle Kandidaten im Suchfenster, Produktions-Defaults (minScore 60, pivotLen 6, searchDepth 16), optionale Pine-Logs-Ausgabe; Signal-Qualität/Backtest noch nicht bewertet |
| [triangle_compression_scanner_pro](indicators/market_structure/triangle_compression_scanner_pro/) | 1.12 | Draft | ★★★★☆ | ★★★☆☆ | ☆☆☆☆☆ | Gleitendes-Fenster-Dreieck-Scanner (symmetrisch/ascending/descending): Begrenzungslinien als Best-Boundary-Fit durch echte Touch-Punkte (nicht Least-Squares) über ein gleitendes Swing-Fenster, Score aus Struktur/Kompression(≥25%+monoton)/Touch-Qualität/Linien-Qualität/Dauer, Mehrfach-Pattern-Tracking + Overlap-Ersetzung/Eviction, Live-Breakout-Tracking (beide Richtungen) + Alert; v1.4–1.12: Default nur 1 gleichzeitiges Pattern, Linie friert nach 1× Fensterbreite ein statt endlos zu driften, Alter (× Fensterbreite) statt ATR-Drift als primärer Cleanup, `barsInsideOk`-Hard-Veto prüft jeden Bar (nicht nur Swings) gegen beide Grenzen; Kandidat/Debug/Dashboard nach Wolfe-Vorbild, eigener Code (keine geteilte Lib); Schwester-Indikator zu Broadening Wedge Scanner Pro (Kompression statt Expansion); noch nicht am Chart validiert |
| [broadening_wedge_scanner_pro](indicators/market_structure/broadening_wedge_scanner_pro/) | 1.13 | Draft | ★★★★☆ | ★★★☆☆ | ☆☆☆☆☆ | Gleitendes-Fenster-Scanner für aufweitende Keile (Descending Broadening/Ascending Broadening/Symmetric Broadening): spiegelt Triangle-Scanner-Architektur, aber Expansion statt Kompression (Endbreite ≥130% Startbreite, monoton weitend) + Geschwindigkeits-Verhältnis-Check für DBW/ABW (schnellere Seite muss spürbar schneller sein); Score aus Struktur/Expansion/Touch-Qualität/Linien-Qualität/Dauer, Mehrfach-Pattern-Tracking + Overlap-Ersetzung/Eviction, Live-Breakout-Tracking + Alert; v1.4–1.13: Default nur 1 gleichzeitiges Pattern, Linie friert nach 1× Fensterbreite ein statt endlos zu driften, Alter (× Fensterbreite) statt ATR-Drift als primärer Cleanup, `barsInsideOk`-Hard-Veto prüft jeden Bar (nicht nur Swings) gegen beide Grenzen; noch nicht am Chart validiert |

## Equities & Relative Strength

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [relative_strength_line](indicators/relative_strength/relative_strength_line/) | 2.0 | Draft | ★★★★★ | ★★★★☆ | ★☆☆☆☆ | RS vs. Benchmark (SPY/QQQ); v2.0: Konfluenz-Signal (RS + Preistrend müssen übereinstimmen) statt reiner RS-Marker; erster Aktien-Indikator, ungetestet |

## Commodity / Multi-TF Matrix

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [commodity_pulse_matrix](indicators/composite/commodity_pulse_matrix/) | 3.1.2 / 4.0.1 | Stabil | ★★★★★ | ★★★★★ | ★★★★★ | v3 published; v4.0.1 in progress (separate file) |
| [signal_quality_engine](indicators/composite/signal_quality_engine/) | 3.3 | Draft | ★★★★☆ | ★★★★☆ | ☆☆☆☆☆ | Range-Fader (eine Logik): fadet Range-Ränder — Long an erschöpften Tiefs, Short an erschöpften Hochs. Exhaustion-Score (Distance+Struktur+Momentum, aus Exhaustion Scanner), Edge→Setup→Watch→Trigger, Candle-Rejection. Für Ranges; im Trend bewusst still. Pivots nur Control-Overlay; ungetestet |

## Momentum Intelligence Suite

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [momentum_profile](indicators/momentum/momentum_profile/) | 1.0 | Draft | ★★★★☆ | ★★★☆☆ | ★☆☆☆☆ | Ø-WaveTrend pro Preiszone (Oszillator-Profil, **kein** Volume Profile) — Abgrenzung zu volume_strata/money_flow_delta_profile in README |
| [momentum_trajectory](indicators/momentum/momentum_trajectory/) | 1.1 | Draft | ★★★★☆ | ★★★☆☆ | ★☆☆☆☆ | Velocity + acceleration of WT/StochRSI/MFI |
| [adaptive_cycle_detector](indicators/trend_strength/adaptive_cycle_detector/) | 1.0.1 | Draft | ★★★★☆ | ★★★☆☆ | ★☆☆☆☆ | Dominant cycle from WT zero-crossings |
| [oscillator_topology](indicators/momentum/oscillator_topology/) | 1.1 | Draft | ★★★★★ | ★★★★☆ | ★☆☆☆☆ | Curvature + shape classification of WT pivots |

## Price Structure & Conviction

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [candle_pressure_index](indicators/money_flow/candle_pressure_index/) | 1.1 | Draft | ★★★★☆ | ★★★★☆ | ★☆☆☆☆ | Raw microstructure bias — no derived oscillators |
| [mtf_structure_bias](indicators/market_structure/mtf_structure_bias/) | 1.1 | Draft | ★★★★☆ | ★★★★☆ | ★☆☆☆☆ | HH/HL/LH/LL alignment across 4 TFs |
| [swing_conviction_radar](indicators/market_structure/swing_conviction_radar/) | 1.1 | Draft | ★★★★★ | ★★★★☆ | ★☆☆☆☆ | Per-leg speed + cleanliness + vol gradient → divergence signals |
| [cvd_bias](indicators/money_flow/cvd_bias/) | 1.1 | Draft | ★★★★☆ | ★★★★☆ | ★☆☆☆☆ | Rolling cumulative volume delta, normalized; price/CVD divergence |

## Vein Suite

| Indikator | Version | Status | Konzept | Code | Getestet | Notiz |
|---|---|---|---|---|---|---|
| [vein_trend](indicators/trend_direction/vein/) | 0.1.1 | Stabil | ★★★★★ | ★★★★★ | ★★★★☆ | Core |
| [vein_pullback](indicators/trend_direction/vein/) | 0.2 | Stabil | ★★★★★ | ★★★★★ | ★★★★☆ | Core |
| [vein_exhaustion](indicators/trend_direction/vein/) | 0.2.1 | Stabil | ★★★★★ | ★★★★★ | ★★★★☆ | Core |
| [vein_accumulation_phase](indicators/trend_direction/vein/) | 0.1.1 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | NatGas focused |
| [vein_reversal_score](indicators/trend_direction/vein/) | 0.1.2 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [vein_structure_zones](indicators/trend_direction/vein/) | 0.2 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |
| [vein_execution](indicators/trend_direction/vein/) | 0.1.3 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | 15m timing overlay |
| [vein_spread_context](indicators/trend_direction/vein/) | 0.1.1 | Stabil | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | Commodity spread modifier |
| [vein_feature_exporter](indicators/trend_direction/vein/) | 0.1.1 | Stabil | ★★★★★ | ★★★★☆ | ★★★★★ | Research tooling |
| [vein_reversal_labeler](indicators/trend_direction/vein/) | 0.1.1 | Stabil | ★★★★☆ | ★★★★☆ | ★★★★☆ | ML labeling only |
| [vein_reversal_zones](indicators/trend_direction/vein/vein_reversal_zones/) | 2.0.1 | Stabil | ★★★★☆ | ★★★★☆ | ★★★☆☆ | |

---

## Strategies

Ratings: **Not ready** (PF < 1.15 or Return/DD < 1.5) · **Promising** (PF ≥ 1.15, nicht out-of-sample validiert) · **Ready** (PF ≥ 1.3, ≥ 2 Instrumente validiert)

| Strategy | Basisindikator | SL-Typ | Best TF | Best PF | Rating | Notiz |
|---|---|---|---|---|---|---|
| [wavetrend_v4_strategy](strategies/wavetrend/) | WaveTrend | Trailing | 1D | 3.07 | Promising | Bestes PF im Repo; 4H 1.49, 1H 1.37; out-of-sample ausstehend |
| [chandelier_flip_radar_strategy](strategies/chandelier_flip_radar/) | Chandelier Flip Radar | Trailing | 4H | 1.60 | Promising | Return/DD 5.87; beide Richtungen profitabel — **stale**: Werte vor v1.6-Ratchet-Fix, Strategie noch nicht regeneriert/neu validiert |
| [smooth_trend_radar_strategy](strategies/smooth_trend_radar/) | Smooth Trend Radar | Fixed TP | 4H | 1.71 (Long) | Promising (Long Only) | Short-Seite durch NatGas-Bull-Bias strukturell schwach; **stale**: resynced to indicator v3.4.0 logic, Werte noch von vor dem Resync — neu validieren |
| [oscillator_divergence_zones_strategy](strategies/oscillator_divergence_zones/) | Oscillator Divergence Zones | Pivot ATR | 4H | 1.14 | Promising | Long PF 1.32; Short Entry-Delay durch pivRight |
| [reversal_engine_score_strategy](strategies/reversal_engine_score/) | Reversal Engine Score | — | 15M | 0.95 | Not ready | Score-Logik fehlerhaft (test131); v1.2 in Arbeit |
| [commodity_pulse_matrix_v4_strategy](strategies/commodity_pulse_matrix/) | Commodity Pulse Matrix v4 | — | — | — | Not ready | Kein Backtest vorhanden |

---

## Archiv

Nicht mehr aktiv gepflegt. Dateien liegen unter `archive/` und können wiederhergestellt werden.

| Indikator / Datei | Grund |
|---|---|
| [smart_money_dashboard](archive/indicators/smart_money_dashboard/) | Erfordert nicht gepflegte RTA-Libraries → CVD-Kern reimpl. als cvd_bias |
| [mtf_trend_alignment](archive/indicators/mtf_trend_alignment/) | Erfordert nicht gepflegte RTA-Libraries → reimpl. als mtf_structure_bias |
| [pattern_recognition](archive/indicators/pattern_recognition/) | Overengineered, kaum getestet |
| [wave_navigator](archive/indicators/wave_navigator/) | Elliott-Wave-Autoerkennung konzeptionell schwach |
| [rj_wave](archive/indicators/rj_wave/) | Zu nische, State-Machine fragil |
| [fib_retracement_quality](archive/indicators/fib_retracement_quality/) | Nur sinnvoll im Elliott-Wellen-Kontext — standalone kein Mehrwert |
| [relative_leg_efficiency_panel_chart](archive/indicators/relative_leg_efficiency_panel_chart/) | Visualisierungs-Experiment → reimpl. als swing_conviction_radar |
| [flow_bias](archive/indicators/flow_bias/) | Überschneidung mit market_pressure_scale → reimpl. als candle_pressure_index |
| [candle_pressure_response_jma](archive/indicators/candle_pressure_response_jma/) | Candle-Metriken bereits in Vein suite (vein_exhaustion, vein_feature_exporter) |
| [adaptive_supertrend](archive/indicators/adaptive_supertrend/) | Ungetestet; gleiche Familie wie chandelier_flip_radar (PF 1.22) → MTF-Confluence-Layer dort absorbiert (v1.5), Rest archiviert |
| [adaptive_fair_value_cloud](archive/indicators/adaptive_fair_value_cloud/) | Regime-Cloud rein deskriptiv (kein Forecast); nachgerüsteter Watch-Layer (Build/Sqz/Div) zu verrauscht auf Chart; User sucht anderes "Kanal mit Aussagen"-Konzept |
| [wavetrend_strategy.pine](archive/strategies/wavetrend/) | Superseded durch v4 |
| [wavetrend_base_strategy.pine](archive/strategies/wavetrend/) | Superseded durch v4 |
| [wavetrend_v3_strategy.pine](archive/strategies/wavetrend/) | Superseded durch v4 |
