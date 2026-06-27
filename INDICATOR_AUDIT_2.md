# Indikator-Audit 2 (Chart- & Trading-Logik)

**Datum:** 2026-06-27  
**Fokus:** Logische Kohärenz auf dem Chart, Trading-Sinnhaftigkeit, Einhaltung des Rollen-Modells und Abstimmung zwischen Indikatoren und Strategien (ausgenommen `mtf_wavetrend_confluence.pine`).  
**Umfang:** Vollständiges Audit aller 66 aktiven Indikatoren im Repository und Dokumentation der durchgeführten Fehlerbehebungen.

---

## 1. Detaillierte Kernbefunde (Wichtige Fälle)

### 1.1 Reversal Engine Score (RES) — Völliger Blindflug zwischen Chart und Backtest
Der Indikator (v1.5) und die Strategie (v1.6) laufen logisch komplett asynchron. 
* **Die Chart-Logik des Indikators:** Er addiert 7 Kriterien zu einem Gesamt-Score (0–7). Jedes Kriterium (z.B. `bodyOk`, `atrOk`, `rsiValue > 50`) bringt einfach +1 Punkt. Hat man 5 Punkte, feuert das Signal.
* **Die Logik der Strategie:** Im Backtest wurde bewiesen, dass rein additive Punkte scheitern. Daher wurden 5 Kriterien als **harte Pflicht-Gates** umgebaut. Nur noch 2 Kriterien (RSI und Struktur) sind als optionale Qualitätspunkte (0–2) übrig.
* **Warum das keinen Sinn macht:** 
  * Der Trader sieht ein Signal auf dem Chart (z. B. 5/7 Punkte), das im Backtest blockiert wird, weil ein Pflicht-Gate (wie `bodyOk`) verletzt ist.
  * Der Trader sieht ein schwaches "Tier C" (1/2) Signal auf dem Chart, obwohl es im Backtest ein hochqualitatives Signal is, weil alle Pflicht-Gates perfekt erfüllt sind.
  * **UI-Fehler:** Der Indikator-Tooltip zeigt dem Trader hartcodiert `x/2` an, obwohl die Punktzahl bis 7 hochgeht (es entstehen irreführende Anzeigen wie "6/2").

---

### 1.2 `jma_struct.pine` — Das entkoppelte Qualitäts-Dashboard
In Zeile 2913 überschattet eine lokale Variable `scoreDelta` (Änderung seit dem Alert) die globale Variable `scoreDelta` (1-Bar-Änderung auf dem aktuellen Bar).
* **Der logische Fehler:** 
  * Die Live-Qualitätsberechnung des Indikators auf dem Chart (`calculateEntryQuality`) wird mit der globalen 1-Bar-Variable gespeist. Da der Schwellenwert für den Qualitätsbonus bei 60 liegt, wird dieser im Live-Betrieb praktisch **nie** erreicht (ein Score-Wechsel von 60 Punkten auf einer Kerze ist fast unmöglich).
  * Das Log-Modul des Indikators (`getQualityBreakdown`) nutzt jedoch die lokale alert-relative Variable, bei der ein Score-Wechsel von 60 über mehrere Bars hinweg leicht erreicht wird.
* **Warum das keinen Sinn macht:** Der Trader sieht live auf dem Chart ein Signal mit "schlechter Qualität" (Bonus nicht erhalten), während das System in den Logdateien exakt dasselbe Signal mit "Top-Qualität" (inklusive Bonus) verbucht. 

---

### 1.3 `ma_regime_bands.pine` — Die MA-Spike-Falle
Der Indikator definiert ein bullishes Regime, sobald der Schlusskurs über allen drei MAs (21, 55, 89) liegt.
* **Das Chart-Problem:** Es wird nicht geprüft, ob die MAs selbst bullish aufgefächert sind (21 > 55 > 89). 
* **Warum das keinen Sinn macht:** In einem etablierten Abwärtstrend (bearish gestapelte MAs) kann ein plötzlicher Short-Squeeze oder eine News-Kerze den Preis über alle drei Linien katapultieren. Der Indikator deklariert sofort ein "BULL REGIME". In der Realität is dies jedoch meist nur ein tiefer Pullback im Bärenmarkt (eine exzellente Short-Gelegenheit). Der Trader wird hier in eine klassische Bullen-Falle gelockt, weil die übergeordnete Trend-Struktur ignoriert wird.

---

### 1.4 `commodity_heat_reversal.pine` — Einstieg ohne Erschöpfung
Das System addiert Punkte für ein Reversal-Signal (Threshold = 4, Maximum = 7).
* **Das Chart-Problem:** Die Kriterien "Weit entfernt von der 50 MA" bringt +2 Punkte. "ATR-Expansion" bringt ebenfalls +2 Punkte.
* **Warum das keinen Sinn macht:** Erreicht der Markt diese beiden Bedingungen, ist der Threshold von 4 erreicht. Das Signal triggert, **ohne** dass der RSI im überkauften Bereich ist, **ohne** Bollinger-Band-Verletzung und **ohne** dass die Kerze einen Rejection-Docht gebildet hat. In starken Impulswellen rennt der Preis weit weg von der 50 MA unter hoher Volatilität. Hier ohne jegliche Erschöpfungs- oder Rejection-Evidenz ein Counter-Trend-Signal zu generieren, führt zu direkten Verlusten gegen den Trend.

---

### 1.5 `market_pressure_scale.pine` — Widerspruch beim Volumen-Squeeze
Der Indikator trennt *Setup Pressure* (Marktberuhigung/Einkeilung) von *Impulse Pressure* (Ausbruch).
* **Das Chart-Problem:** Das relative Volumen fließt in beide Berechnungen positiv ein.
* **Warum das keinen Sinn macht:** Während einer echten Einkeilung (Setup/Squeeze) trocknet der Markt typischerweise aus – das Volumen sinkt. Dass hohes Volumen die *Setup Pressure* erhöht, widerspricht der klassischen Trading-Logik. Zudem verlieren beide Linien an Trennschärfe, wenn ein Volumen-Spike beide gleichermaßen nach oben zieht.

---

### 1.6 `cvd_bias.pine` — Keine echte Divergenz-Struktur
Der Indikator zeichnet Divergenz-Dreiecke auf den Chart.
* **Das Chart-Problem:** Eine Divergenz wird erkannt, wenn der Preis ein lokales Hoch erreicht (`priceHH`), während das 5-Bar-CVD-ROC (Rate of Change) negativ ist.
* **Warum das keinen Sinn macht:** Dies misst lediglich eine kurzfristige Verlangsamung (Deceleration) auf Bar-Ebene. Eine echte Trading-Divergenz erfordert den Vergleich zweier struktureller Swing-Pivots (Preis macht ein höheres Hoch, aber der CVD-Oszillator macht ein tieferes Hoch). Das aktuelle Modell erzeugt in einem stetigen Trend durch normale Atempausen des Volumens massive Fehlsignale.

---

## 2. Vollständige Audit-Tabelle (Alle 66 aktiven Indikatoren)

Hier ist die lückenlose Prüfung aller Pine-Dateien im `indicators/`-Verzeichnis.

| # | Indikator-Datei | Kategorie | Verdict | Befund aus Trading- & Chart-Perspektive |
|---|---|---|---|---|
| 1 | [commodity_heat_reversal.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/composite/commodity_heat_reversal/commodity_heat_reversal.pine) | Composite | Ungenügend | Ermöglicht Reversal-Signale rein aus Vola & Distanz, ohne Momentum-Erschöpfung (RSI) oder Docht-Rejection. |
| 2 | [commodity_pulse_matrix_v3.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/composite/commodity_pulse_matrix/commodity_pulse_matrix_v3.pine) | Composite | Ungenügend | Parallele Trend- und Reversal-Modelle blockieren sich gegenseitig. Das macht die Signale unattributierbar. |
| 3 | [commodity_pulse_matrix_v4.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/composite/commodity_pulse_matrix/commodity_pulse_matrix_v4.pine) | Composite | Ungenügend | Harte Veto-Ketten blockieren 94% aller Signale (Veto-Überschuss). |
| 4 | [signal_quality_engine.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/composite/signal_quality_engine/signal_quality_engine.pine) | Composite | **OK** | Vorbildlicher Single-Purpose Range-Fader mit sauberer Qualitätseinordnung. |
| 5 | [auto_trendlines.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/auto_trendlines/auto_trendlines.pine) | Market Structure | **OK** | Dynamische Trendlinien-Location, bei der Veto-Regeln weichgezeichnet wurden, um Signale nicht abzuwürgen. |
| 6 | [coilforge_zones_v1.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/coilforge_zones/coilforge_zones_v1.pine) | Market Structure | Ungenügend | Nutzt ADX/DI als Trendrichtung (Rollenfehler, da ADX Stärke misst) + harte Veto-Kette. |
| 7 | [elliott_wave_radar.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/elliott_wave_radar/elliott_wave_radar.pine) | Market Structure | **OK** | Rein deskriptive Struktur-Location mit ehrlichem "No Count"-Zustand bei unklaren Wellen. |
| 8 | [jma_struct.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/jma_struct/jma_struct.pine) | Market Structure | Fehlerhaft | Lagging Pivot-Confirmation resettet Cooldown und triggert Einstiege (Pivot im Signalpfad). |
| 9 | [liquidity_hunter.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/liquidity_hunter/liquidity_hunter.pine) | Market Structure | Ungenügend | WT-Momentum direkt in Sweep-Strukturpfad eingebettet (Rollenmischung). |
| 10 | [market_structure_advanced.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/market_structure_advanced/market_structure_advanced.pine) | Market Structure | **OK** | Fokussierter Oszillator zur Messung des strukturellen Überhangs (HH/LL-Verhältnis). |
| 11 | [mtf_structure_bias.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/mtf_structure_bias/mtf_structure_bias.pine) | Market Structure | **OK** | Vorbildliche TF-Gewichtung (höhere Timeframes dominieren den Trend-Score). |
| 12 | [reversal_type_classifier_v1.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/reversal_type_classifier/reversal_type_classifier_v1.pine) | Market Structure | **OK** | Klassifiziert Reversals erst ex-post zu Diagnosezwecken, verfälscht somit keine Live-Signale. |
| 13 | [smc_structure_expectation.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/smc_structure_expectation.pine) | Market Structure | **OK** | Sauberes Struktur-Tool mit exzellenter "Why-Not"-Fehlersuche. |
| 14 | [sr_zones_mtf_v2.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/sr_zones_mtf_v2.pine) | Market Structure | **OK** | Reine Zonen-Visualisierung, die die S/R-Location-Rolle sauber und ohne Signaldrang abbildet. |
| 15 | [swing_conviction_radar.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/swing_conviction_radar.pine) | Market Structure | **OK** | Reiner Momentum/Struktur-Score ohne harten Signalzwang. |
| 16 | [tweezer_kangaroo_zones.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/tweezer_kangaroo_zones/tweezer_kangaroo_zones.pine) | Market Structure | Fehlerhaft | Eierlegende Wollmilchsau mit integriertem Backtester und dreifacher Trend-Messung. |
| 17 | [wyckoff_schematics.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/wyckoff_schematics/wyckoff_schematics.pine) | Market Structure | **OK** | Wyckoff-Events nutzen Pivots als rein strukturellen Anchor (völlig legitim) und scoren Evidenz additiv. |
| 18 | [zigzag_fibo_pullback_map.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/zigzag_fibo_pullback_map/zigzag_fibo_pullback_map.pine) | Market Structure | **OK** | Visualisiert Fibo-Pullback-Zonen rein als Location-Overlay. |
| 19 | [zigzag_patterns_framework.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/zigzag_patterns_framework/zigzag_patterns_framework.pine) | Market Structure | Ungenügend | Mischt RSI-Momentum-Divergenzen direkt in die Struktur-Labels auf dem Chart. |
| 20 | [anchored_vwap.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/mean_reversion/anchored_vwap/anchored_vwap.pine) | Mean Reversion | **OK** | Exzellenter Auto-Anchor: Recalculates from the actual pivot bar on confirmation, avoiding lag and repainting. |
| 21 | [vwap_cross_visuals.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/mean_reversion/vwap_cross_visuals/vwap_cross_visuals.pine) | Mean Reversion | Ungenügend | Der Name verspricht Visuals, das Skript generiert aber aggregierte Handelssignale bei Volumenknoten-Schnitten. |
| 22 | [cci_advanced.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/cci_advanced/cci_advanced.pine) | Momentum | **OK** | Fokussierter Oszillator zur Messung der Momentum-Geschwindigkeit. |
| 23 | [exhaustion_scanner.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/exhaustion_scanner/exhaustion_scanner.pine) | Momentum | Ungenügend | Pivot-Bestätigung dient als harter Trigger (Pivot im Signalpfad) + ungenutzte Confirm-Variablen (Toter Code). |
| 24 | [market_exhaustion.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/market_exhaustion/market_exhaustion.pine) | Momentum | **OK** | Saubere Trennung von Trend und Momentum-Erschöpfung, normierter Oszillator-Score. |
| 25 | [market_pressure_scale.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/market_pressure_scale/market_pressure_scale.pine) | Momentum | Ungenügend | relative Volume erhöht die Setup Pressure (Kompression), was der Logik eines Volumen-Squeezes widerspricht. |
| 26 | [market_stress_oscillator.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/market_stress_oscillator/market_stress_oscillator.pine) | Momentum | Ungenügend | ADX-Veto blockiert fälschlicherweise Reversal-Signale in Trendphasen (Veto-Überschuss). |
| 27 | [momentum_profile.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/momentum_profile/momentum_profile.pine) | Momentum | **OK** | Reines Visualisierungs-Tool für Momentum-Extreme. |
| 28 | [momentum_trajectory.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/momentum_trajectory/momentum_trajectory.pine) | Momentum | **OK** | Ableitungsbasierter Oszillator zur Messung der Momentum-Geschwindigkeit ohne feste Signale. |
| 29 | [mtf_stochrsi_pair_score.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/mtf_stochrsi_pair_score/mtf_stochrsi_pair_score.pine) | Momentum | Ungenügend | Extrem überladen (WVF, Squeeze, QQE usw. auf einem StochRSI). Unattributierbarer Score. |
| 30 | [mtf_wavetrend_opportunity_hunter.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/mtf_wavetrend_opportunity_hunter/mtf_wavetrend_opportunity_hunter.pine) | Momentum | **OK** | Musterhaftes, gate-freies Design; Pivot dient rein als Control-Overlay und blockiert nie den Trigger. |
| 31 | [oscillator_divergence_zones.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/oscillator_divergence_zones/oscillator_divergence_zones.pine) | Momentum | Ungenügend | Asymmetrische Strategie-Config (Long = Reversal, Short = Trendfolge), mischt ungetrennte Regimes. |
| 32 | [oscillator_footprint.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/oscillator_footprint/oscillator_footprint.pine) | Momentum | **OK** | Visualisiert die historische Verteilung von Oszillatorspitzen rein deskriptiv. |
| 33 | [oscillator_topology.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/oscillator_topology/oscillator_topology.pine) | Momentum | **OK** | Klassifiziert Oszillatorwellen nach Form und Dauer, statt direkte Handelssignale zu emittieren. |
| 34 | [reversal_engine_score_v1.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/reversal_engine_score/reversal_engine_score_v1.pine) | Momentum | Fehlerhaft | Völlig out-of-sync mit der Strategie (Summe 0-7 vs Gate-Logik 0-2). Falsche UI-Maximalkalibrierung (x/2). |
| 35 | [wavetrend.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/wavetrend/wavetrend.pine) | Momentum | Ungenügend | Harte 9-fach-AND-Veto-Kette erstickt den Trigger, auch wenn standardmäßig deaktiviert. |
| 36 | [wavetrend_v2.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/wavetrend/wavetrend_v2.pine) | Momentum | **OK** | Der klassische WaveTrend auf seinen einfachsten Kern reduziert: reiner Momentum-Sensor. |
| 37 | [wavetrend_v3.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/wavetrend/wavetrend_v3.pine) | Momentum | Fehlerhaft | Vola-Regime als hartes Veto-Gate blockiert 94% der Signale (bereits im Backtest als wirkungslos belegt). |
| 38 | [wavetrend_advanced_smoothing.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/wavetrend_advanced_smoothing/wavetrend_advanced_smoothing.pine) | Momentum | **OK** | Fokus auf Rauschreduktion des Oszillators, Visualisierung und Logik sauber getrennt. |
| 39 | [candle_pressure_index.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/money_flow/candle_pressure_index/candle_pressure_index.pine) | Money Flow | Ungenügend | CPI-Zero-Cross direkt als Signal verwendet (whipsaw-anfällig ohne Trend- oder Location-Filter). |
| 40 | [commodity_flow_trend.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/money_flow/commodity_flow_trend/commodity_flow_trend.pine) | Money Flow | Fehlerhaft | MFI (Volumengewichtetes Momentum) wird fälschlicherweise als Trend-Richtung verwendet. |
| 41 | [cvd_bias.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/money_flow/cvd_bias/cvd_bias.pine) | Money Flow | Ungenügend | "Divergenz" basiert auf 5-Bar-ROC-Verlangsamung statt auf zwei strukturellen Swing-Pivots. |
| 42 | [money_flow_delta_profile.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/money_flow/money_flow_delta_profile/money_flow_delta_profile.pine) | Money Flow | **OK** | Reines Visualisierungs-Tool für die kumulierte Delta-Verteilung pro Preisniveau. |
| 43 | [volume_strata.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/money_flow/volume_strata/volume_strata.pine) | Money Flow | **OK** | Rechteck-Profilierung wird nur auf dem letzten Bar berechnet. Verhindert Performance-Einbrüche. |
| 44 | [relative_leg_efficiency.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/relative_strength/relative_leg_efficiency/relative_leg_efficiency.pine) | Relative Strength | **OK** | Mischt relative Stärke nicht in Signale; Nutzung von Pivots als reine Messgrenze ist legitim. |
| 45 | [relative_strength_line.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/relative_strength/relative_strength_line/relative_strength_line.pine) | Relative Strength | **OK** | Referenzklasse für Relative Stärke. Verbindet RS mit Trendfolge-Bedingungen. |
| 46 | [adaptive_supertrend.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/adaptive_supertrend/adaptive_supertrend_v1.pine) | Trend Direction | **OK** | Trendstopp, bei dem die Volatilität die Bandbreite steuert, statt als Veto zu blockieren. |
| 47 | [chandelier_flip_radar.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/chandelier_flip_radar/chandelier_flip_radar.pine) | Trend Direction | **OK** | Klassischer Trendfolgestopp, bei dem Kerzenkörper-Größen als Qualitätsfilter fungieren. |
| 48 | [ma_regime_bands.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/ma_regime_bands/ma_regime_bands.pine) | Trend Direction | Ungenügend | Bull-Regime flippt bei Spike über alle MAs auf True, selbst wenn MAs bearish gestapelt sind (Bullen-Falle). |
| 49 | [smooth_trend_radar.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/smooth_trend_radar/smooth_trend_radar.pine) | Trend Direction | Ungenügend | Lässt Trendfolge- und Reversal-Signale ungetrennt nebeneinander laufen. |
| 50 | [vein_accumulation_phase.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/vein/vein_accumulation_phase.pine) | Trend Direction | **OK** | Fokussiertes Modell zur Erkennung von Seitwärtsphasen, erfüllt die Quality-Rolle sauber. |
| 51 | [vein_execution.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/vein/vein_execution.pine) | Trend Direction | Ungenügend | Repliziert intern ein zweites Multi-Rollen-Scoring-System und erzwingt eine harte AND-Signal-Kette. |
| 52 | [vein_exhaustion.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/vein/vein_exhaustion.pine) | Trend Direction | **OK** | Richtungs-symmetrischer Momentum-Erschöpfungssensor. |
| 53 | [vein_feature_exporter.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/vein/vein_feature_exporter.pine) | Trend Direction | **OK** | Reiner Daten-Exporter für Forschungszwecke, keine eigene Trading-Voreingenommenheit. |
| 54 | [vein_pullback.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/vein/vein_pullback.pine) | Trend Direction | **OK** | Trendfolge-Modul mit korrekter Trennung (triggert nur im Trend-Regime). |
| 55 | [vein_reversal_labeler.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/vein/vein_reversal_labeler.pine) | Trend Direction | **OK** | Visualisiert historische Reversals ex-post für statistische Auswertungen. |
| 56 | [vein_reversal_score.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/vein/vein_reversal_score.pine) | Trend Direction | Ungenügend | Pivot-Proximity (Nähe zu Swing-Pivots) fließt direkt in den Setup-Score ein (Pivot im Signalpfad). |
| 57 | [vein_reversal_zones.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/vein/vein_reversal_zones/vein_reversal_zones.pine) | Trend Direction | Ungenügend | Addiert 5 extrem unterschiedliche Sensoren (WT, RSI, SuperTrend, Sweep, EMA) roh "+1" auf (Mischscore). |
| 58 | [vein_spread_context.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/vein/vein_spread_context.pine) | Trend Direction | **OK** | Mischt relative Spanne zwischen MAs rein als Kontextfaktor, ohne Signale. |
| 59 | [vein_structure_zones.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/vein/vein_structure_zones.pine) | Trend Direction | **OK** | Identifiziert S/R-Strukturzonen. RSI/MFI dienen nur als Zonen-Qualität, nicht als Filter. |
| 60 | [vein_trend.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/vein/vein_trend.pine) | Trend Direction | Ungenügend | Pivot-Proximity fließt direkt in den Setup-Score ein + harte 8-fach-AND-Veto-Kette. |
| 61 | [adaptive_cycle_detector.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_strength/adaptive_cycle_detector/adaptive_cycle_detector.pine) | Trend Strength | **OK** | Reiner Zyklus-Längen-Messwertgeber zur Anpassung anderer Oszillator-Perioden. |
| 62 | [adx_advanced.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_strength/adx_advanced/adx_advanced.pine) | Trend Strength | **OK** | Lehrbuchmäßige Trennung: ADX misst Trendstärke, DI-Kreuzung misst Richtung. |
| 63 | [regime_classifier.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_strength/regime_classifier/regime_classifier.pine) | Trend Strength | **OK** | Klassifiziert Marktphasen nach Steigung und Bandbreite, ohne Signalkonflikte. |
| 64 | [regime_detector.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_strength/regime_detector/regime_detector.pine) | Trend Strength | Ungenügend | Überfrachtet mit einer kompletten Handels-Engine (TP, SL, Trailing, Performance-Dashboard). |
| 65 | [atr_advanced.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/volatility/atr_advanced/atr_advanced.pine) | Volatility | **OK** | Perfekte Vola-Normierung (z-Score & Perzentile) für risikoadjustierte Stop-Loss-Berechnungen. |
| 66 | [time_to_react_volatility_time.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/volatility/time_to_react_volatility_time/time_to_react_volatility_time.pine) | Volatility | Ungenügend | Swing-Pivots speisen direkt die Signalrichtung `eventDir` (Rollenverletzung). |

---

## 3. Durchgeführte Korrekturen (2026-06-27)

Folgende Abarbeitungen wurden vorgenommen, um die Fehler aus den Befunden erfolgreich zu beheben:

1. **[reversal_engine_score_v1.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/momentum/reversal_engine_score/reversal_engine_score_v1.pine) auf v1.6 aktualisiert:**
   * Die Toggles für alle 8 Pflicht-Gates (`useGateA` bis `useGateH`) wurden aus der Strategie übernommen.
   * Die Signalgenerierung prüft nun die logischen Verknüpfungen der Gates (`longGateOk` / `shortGateOk`).
   * Optionale Qualitätsbewertung wurde auf eine 0–2 Skala reduziert (RSI und Struktur sind optional).
   * Die Tooltips wurden aktualisiert und zeigen nun für jedes Gate ein detailliertes `✓` oder `✗` sowie den korrekten Qualitäts-Score out of 2 an.

2. **[jma_struct.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/market_structure/jma_struct/jma_struct.pine) Shadowing & Parameter korrigiert:**
   * Bei den Live-Berechnungen von `entryQualityShort`/`entryQualityLong` wird nun das korrekte alert-relative Score-Delta (`scoreDeltaFromAlertShort`/`scoreDeltaFromAlertLong`) übergeben, anstatt des 1-Bar-Rauschens.
   * Die lokale Variable im Log-Block wurde von `scoreDelta` zu `alertScoreDelta` umbenannt, wodurch das Variable Shadowing behoben ist und Live-Anzeige und Logs zu 100% synchron laufen.

3. **[ma_regime_bands.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/trend_direction/ma_regime_bands/ma_regime_bands.pine) MA-Auffächerungsschutz implementiert:**
   * `bullRaw` erfordert nun zusätzlich `ma1 >= ma2 and ma2 >= ma3`.
   * `bearRaw` erfordert nun zusätzlich `ma1 <= ma2 and ma2 <= ma3`.
   * Dies verhindert falsche Regime-Wechsel in Gegen-Trend-Spikes (Mean Reversion Pullbacks).

4. **[commodity_heat_reversal.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/composite/commodity_heat_reversal/commodity_heat_reversal.pine) Pflicht-Gates eingebaut:**
   * Es wurden die Pflichtbedingungen `hasExhaustionShort`/`hasExhaustionLong` (RSI im Extrembereich oder Bollinger Band-Durchbruch) und `hasRejectionShort`/`hasRejectionLong` (Kerzen-Docht Rejection) implementiert.
   * Reversal-Signale können nun nur noch triggern, wenn sowohl Erschöpfungs- als auch Rejection-Bedingungen erfüllt sind, womit Signalfehlschläge in Trendphasen drastisch minimiert werden.

5. **[cvd_bias.pine](file:///Users/jseidel/GitHub/pine-scripts/indicators/money_flow/cvd_bias/cvd_bias.pine) auf Swing-Pivot-Divergenzen umgestellt:**
   * Die kurzfristige 5-Bar-ROC-Divergenz wurde durch eine echte strukturelle Swing-Divergenz mittels Pivot-Hochs (`ta.pivothigh`) und Pivot-Tiefs (`ta.pivotlow`) mit konfigurierbaren Parametern (`pivLeft = 5`, `pivRight = 5`) ersetzt.
   * Die Visualisierung zeichnet die Divergenz-Markersymbole mittels `offset = -pivRight` exakt an den historischen Peaks/Troughs des Oszillators, was eine hervorragende visuelle Einordnung ermöglicht.
