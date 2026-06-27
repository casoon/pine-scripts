# Indikator-Audit gegen das Rollen-Regelwerk

**Datum:** 2026-06-27
**Maßstab:** Die lokalen Skills `indicator-design` und `indicator-review` (`.claude/skills/`) — Rollen-Modell (Trend/Location/Momentum/Trigger/Quality), keine harten AND-Ketten, Pivot nur Control-Overlay, Regime-Trennung, Rollen-Ebenen-Gewichtung, Debug-Pflicht.
**Umfang:** Alle 65 `.pine`-Dateien unter `indicators/`.
**Methode:** Evidenzbasiertes Audit pro Datei (Datei:Zeile + Zitat) gegen die §6-Architektur-Checkliste.

## Bearbeitungsstand

**Stand:** 2026-06-27

**Erledigt / gepatcht:**
- Kritische Defekte: `commodity_flow_trend`, `jma_struct`, `wavetrend_v3`, `tweezer_kangaroo_zones`.
- Pivot-im-Signalpfad: `jma_struct`, `vein_trend`, `vein_reversal_score`, `exhaustion_scanner`, `smooth_trend_radar`, `time_to_react_volatility_time`.
- Kleine Rollen-/Gate-Fixes: `coilforge_zones`, `market_stress_oscillator`, `candle_pressure_index`, `oscillator_divergence_zones`, `reversal_engine_score`.
- Weitere scoped Refactors: `liquidity_hunter`, `zigzag_patterns_framework`, `vein_reversal_zones`, `commodity_heat_reversal`, `regime_detector`, `vwap_cross_visuals`, `mtf_stochrsi_pair_score`, `market_pressure_scale`, `vein_execution`, `wavetrend` v1, `commodity_pulse_matrix_v3`, `commodity_pulse_matrix_v4`.

**Noch offen:**
- Keine offenen Auditpunkte im Sinne der Arbeitsliste.
- Hinweis: Bei den großen Composite-Dateien (`commodity_pulse_matrix_v3/v4`) wurde der Default-Signalpfad entschärft, nicht die Datei in mehrere Single-Purpose-Module zerlegt.

**Hinweis:** Die erledigten Punkte wurden als gezielte Defekt-/Signalpfad-Patches umgesetzt. Die offenen Punkte brauchen jeweils stärkere Architekturentscheidungen und werden separat abgearbeitet.

## Verdict-Klassen

- **Fehlerhaft** — echter Defekt: Pivot im Signalpfad, kaputte/tote Logik, Rollenfehler oder harte AND-Kette, die den eigentlichen Trigger erwürgt.
- **Ungenügend** — verstößt gegen die Rollen-Regeln (does-too-much, Indikator-Level-Gewichtung, Regime nicht getrennt, Veto-Überschuss), ohne harten Defekt.
- **OK** — regelkonform; bei reinen Single-Purpose-/Visual-/Kontext-Indikatoren gelten die sechs Signal-Fragen bewusst nicht.

## Zusammenfassung

| Verdict | Anzahl | Anteil |
|---|---|---|
| Fehlerhaft | 4 | 6 % |
| Ungenügend | 22 | 34 % |
| OK | 39 | 60 % |

Die OK-Mehrheit besteht überwiegend aus disziplinierten Single-Purpose-Indikatoren (Oszillatoren, Struktur-/Zonen-Tools, Volumenprofile, reine Vola-/RS-Indikatoren). Die Probleme konzentrieren sich auf die **Composite-/Signal-/Hunter-Varianten**, die ein vollständiges Setup liefern wollen — dort tauchen dieselben sechs Muster immer wieder auf (siehe unten).

---

## 1. Kritische Defekte (Fehlerhaft)

### commodity_flow_trend — Money-Flow als Richtung
`indicators/money_flow/commodity_flow_trend/commodity_flow_trend.pine`
Kern-Rollenverstoß des Regelwerks: MFI (Money-Flow) wird direkt als Trend-/Regime-**Richtung** verdrahtet (`:185` `regimeBull = … mfi > mfiTrend`, default an), und der CCI-Nulldurchgang ist der primäre Long/Short-**Trigger** (`:193` `cciCrossUp = ta.crossover(cci, 0.0)`). MFI/CCI sind Momentum-/Quality-Evidenz, keine Richtungs- oder Trigger-Quelle. Zusätzlich vierfache AND-Kette mit drei default-aktiven Gates.

### jma_struct — toter Regime-Schalter + Pivot im Signalpfad
`indicators/market_structure/jma_struct/jma_struct.pine`
Die beworbenen Modi „Trend/Reversion" (`:84`) sind **tot** — `trendLong/revLong` werden nie in `entryLong/entryShort` konsumiert (`:2434`), der Modus ändert nur ein Log-Label. Das Entry-Modell läuft modus-unabhängig identisch (Regime nicht getrennt). Zusätzlich: bestätigter **Pivot setzt den Entry-Cooldown zurück und erlaubt sofortigen Entry** (`:834-865`) — ein lagging `pivothigh/low` steuert das Entry-Timing, exakt die verbotene Pivot-als-Trigger-Nutzung. Plus: RSI/WaveTrend entscheiden über Pivot-Gültigkeit (`:154`).

### wavetrend_v3 — Hard-Gate-AND-Kette erwürgt den Trigger
`indicators/momentum/wavetrend/wavetrend_v3.pine`
Der WT-Reversal-Trigger läuft durch eine mehrfache harte Veto-Kette aus Setup-Gate + MTF-Gate + Score-Schwelle + **Vola-Regime-Hard-Gate** (`:732`, `:640` `volRegimeOk = … != 'Hard Gate' or _inRegimeBand`). Das ist das dokumentierte 94 %-Block-Versagensmuster der Familie — und der Vola-Regime-Gate ist im Repo bereits als wertlos belegt (`.claude/CLAUDE.md`, verworfenes Gate B, `atrRank<30`). Der Score selbst ist korrekt rollenbasiert; das Problem sind die vier Vetos *daneben*.

### tweezer_kangaroo_zones — versteckte Eval-Engine + dreifache Trend-Zählung
`indicators/market_structure/tweezer_kangaroo_zones/tweezer_kangaroo_zones.pine`
Location-Indikator mit eingebauter TP/SL-Backtest-Engine (`:1215-1308`), Confluence-Score auf roher Indikator-Ebene, und **dreifacher Trend-Zählung** (Supertrend + MOST + EMA-Gate erfüllen alle die Trend-Rolle, werden aber separat gewichtet, `:1196-1200`) plus harter Trend-AND-Kette (`:1145`). Klassische eierlegende Wollmilchsau.

---

## 2. Sonderbefund: Pivot im Signalpfad

Dein wiederkehrendes Kernprinzip (Memory `feedback_pivot_is_control_not_signal`): Pivots dürfen **nie** Trigger/Grade/Dedup speisen. Über die Verdict-Grenzen hinweg verletzen das folgende Indikatoren — diese verdienen Priorität, weil sie genau den Punkt treffen, den du dir mehrfach abgewöhnt hast:

| Indikator | Wie der Pivot in den Signalpfad leckt | Verdict |
|---|---|---|
| `jma_struct` | Pivot-Confirmation resettet Cooldown → sofortiger Entry (`:834-865`) | **Fehlerhaft** |
| `vein_trend` | Pivot-Proximity `bullAtLevel += 1.0` direkt im Setup-Score → Trigger (`:209,439`) | Ungenügend |
| `vein_reversal_score` | Pivot-Proximity als Score-Punkt (`:413`) + Premium/Discount-Location im Conf-Score | Ungenügend |
| `exhaustion_scanner` | Modus „Pivot Confirmed": `not na(ph)` ist Pflicht-Triggerbedingung (`:309-316`) | Ungenügend |
| `smooth_trend_radar` | `rejSignalBull = not na(_pivLow) and …` ist publiziertes Signal + Strategy-Long (`:163-185`) | Ungenügend |
| `time_to_react_volatility_time` | Swing-Pivot speist `eventDir` (Richtung) statt Control-Overlay (`:248-252`) | Ungenügend |

> Hinweis: `vein_trend` ist nominell „Ungenügend", trägt aber per Regelwerk-Definition einen echten Defekt (Pivot im Signalpfad). Bei einer strikten Auslegung gehören `vein_trend` und `vein_reversal_score` in die Fehlerhaft-Klasse.

Legitim (kein Defekt) ist Pivot dagegen überall, wo er **Struktur/Location** ist (ZigZag, HH/HL/LH/LL, S/R-Zonen, Divergenz-Anker, Stops) — das wird im Audit konsequent so behandelt und betrifft u. a. alle OK-bewerteten Struktur-Indikatoren.

---

## 3. Ungenügend — nach Hauptmuster gruppiert

**A — Eierlegende Wollmilchsau (mehrere konkurrierende Modelle/Outputs in einem Skript):**
- `commodity_pulse_matrix_v3` — Trend- und Reversal-Engine laufen ungetrennt parallel, willkürlicher „MR bevorzugen"-Tiebreak (`:6817-6825`); asymmetrische Hart-Vetos (Shorts im Bull-Trend geblockt, kein Long-Pendant).
- `commodity_pulse_matrix_v4` — finale Mehrfach-Veto-AND-Kette (`:5141`), Breakout/Pullback/Continuation per OR gemischt; Rollen-Scoring aber sauber, Pivot isoliert.
- `regime_detector` — als Regime-Klassifikator deklariert, enthält aber komplette Entry/Exit/TP/SL/Trailing-Trade-Engine (`:979`, `:660-684`) + In-Chart-Performance-Statistik; mischt Regime-Output als Signal-Veto.
- `vwap_cross_visuals` — Name „Visuals", emittiert aber aggregierte Long/Short-Signale (`:3130`) inkl. Volume-Profile-Event direkt als Trade-Marker (`:2733`).
- `mtf_stochrsi_pair_score` — StochRSI-Scorer trägt zusätzlich WVF, Squeeze, QQE, Fractal, Compression + 2 Divergenz-Systeme (`:18-26`); `f_score` ist roh-additiv (`:206-223`).
- `market_pressure_scale` — Setup/Impulse-Kern überfrachtet mit StochRSI/WT/MFI/Regime-Map/Character-Score; Volumen mit 35 % als Impuls-/Richtungstreiber (`:223`).
- `vein_execution` — repliziert intern ein zweites komplettes Multi-Rollen-Score-System (`:62-94`) + harte Entry-AND-Kette (`:334`).

**B — Rollenfehler (Sensor in fremder Rolle):**
- `coilforge_zones` — ADX/DI als **Richtung** (`:243` `… plusDI > minusDI → bias := Up`) + harte AND-Gate-Kette (`:181`).
- `liquidity_hunter` — WaveTrend-Exhaustion in den Sweep-Signalpfad eingebaut (`:328`) + eigenständiger Bias-Aggregator (`:401`).
- `zigzag_patterns_framework` — RSI-Divergenz (Momentum) ins Struktur-Pivot-Label gemischt (`:220-250`).
- `market_stress_oscillator` — ADX als Pflicht-Veto auf WVF-Stress-Events (`:222,372`) → Trend-Regime in Reversal-Erkennung gemischt.
- `candle_pressure_index` — Volumen×Pressure-Zero-Cross direkt als Long/Short ohne Trend-/Location-Träger (`:66`).
- `vein_reversal_zones` — sauberer Zonen-Kern, aber 5 heterogene Sensoren (WT/RSI/Supertrend/Sweep/EMA) roh „je +1" addiert (`:300-303`).

**C — Asymmetrie / Regime nicht getrennt:**
- `oscillator_divergence_zones` — `@strategy-config` verdrahtet `long: bullDiv` (Reversal) vs. `short: bearHidDiv` (Continuation) — Long/Short messen verschiedene Regimes (`:376-378`).
- `commodity_heat_reversal` — Reversal- und Continuation-Modell parallel (`:192,228`), roher Indikator-Level-Punkte-Score (`:130-134`), harte AND-Kette.

**D — Veto-Überschuss / harte AND-Kette (sonst gesund):**
- `wavetrend` (v1) — 9-fach-AND-Veto-Kette (`:642`), aber alle Gates default-off.
- `reversal_engine_score` — starre 6-fach-AND-Pflichtkette (`:183`); `rsiValue > 50` zählt für Long **und** Short als +1 (Etikettenschwindel).

---

## 4. Wiederkehrende Muster (über das ganze Repo)

1. **Pivot im Signalpfad** — 6 Fälle (Abschnitt 2). Dein meistwiederholtes Anti-Pattern.
2. **Eierlegende Wollmilchsau** — Signal-Indikatoren akkumulieren parallele Modelle (Trend+Reversal+MR+Divergenz+MTF), bis nicht mehr ableitbar ist, *warum* ein Signal feuert.
3. **Harte AND-/Veto-Ketten statt Evidenz-Scoring** — der eigentliche Trigger wird durch mehrere unabhängige Hard-Gates erwürgt (`wavetrend_v3`, `commodity_pulse_matrix_v4`, `commodity_flow_trend`, `vein_trend`).
4. **Rollenfehler** — ADX/MFI/CCI/Volumen als Richtung oder Trigger statt als Stärke-/Quality-Evidenz.
5. **Regime nicht getrennt** — Continuation- und Reversal-Logik laufen mehrdeutig parallel oder ein Regime-Schalter ist tot (`jma_struct`).
6. **Gewichtung auf Indikator- statt Rollen-Ebene** — `score = summe(roher Oszillatoren)` statt erst je Rolle bewerten, dann zusammenführen.

---

## 5. Vorbildlich (OK-Referenzen)

Diese erfüllen die Regeln exemplarisch und taugen als Muster für Refactors:

- `mtf_wavetrend_opportunity_hunter` — **Gate-frei** (alles graded statt geblockt), Pivot strikt Control-Overlay (`g_piv` „Never a Gate"), Entry rein WT-Cross; löst das 94 %-Block-Problem der Familie.
- `mtf_wavetrend_confluence` — **Grade-statt-Gate**-Architektur (Wave/Tide graden den Cross 0–4 statt zu blocken); beantwortet alle sechs Fragen.
- `signal_quality_engine` — vorbildlicher Single-Purpose-Range-Fader, Rollen-Score, Trigger statt Veto, Pivot „NOT used in any signal/grade/gate".
- `mtf_structure_bias` — Rollen-/TF-Ebenen-Gewichtung (höhere TF höher gewichtet), Referenzqualität.
- `adx_advanced` — Lehrbuch: ADX = Stärke, DI± = Richtung, sauber getrennt.
- `relative_strength_line` — RS = Quality, Preis-EMA = Richtung; Confluence verhindert RS-als-Trend.

---

## 6. Vollständige Tabelle (alle 65)

| Indikator | Kategorie | Verdict | Hauptbefund |
|---|---|---|---|
| commodity_flow_trend | money_flow | **Fehlerhaft** | MFI als Regime-Richtung + CCI-Cross als Trigger |
| jma_struct | market_structure | **Fehlerhaft** | Toter Regime-Schalter + Pivot resettet Cooldown (Trigger) |
| wavetrend_v3 | momentum | **Fehlerhaft** | Mehrfache Hard-Gate-AND-Kette inkl. widerlegtem Vola-Gate |
| tweezer_kangaroo_zones | market_structure | **Fehlerhaft** | Versteckte Eval-Engine + 3-fach Trend-Zählung + Trend-AND |
| commodity_pulse_matrix_v3 | composite | Ungenügend | Trend/Reversal parallel, asym. Hart-Vetos, roh-Scoring |
| commodity_pulse_matrix_v4 | composite | Ungenügend | Finale Mehrfach-Veto-AND-Kette, Entry-Typen gemischt |
| commodity_heat_reversal | composite | Ungenügend | Reversal+Continuation parallel, roher Punkte-Score |
| regime_detector | trend_strength | Ungenügend | Komplette Trade-Engine in einem Regime-Klassifikator |
| vwap_cross_visuals | mean_reversion | Ungenügend | „Visuals" emittiert Multi-Engine-Signale, Volumen als Trigger |
| mtf_stochrsi_pair_score | momentum | Ungenügend | 6 Subsysteme aufgesattelt, roh-additiver Score |
| market_pressure_scale | momentum | Ungenügend | Überfrachtet, Volumen als Impuls-/Richtungstreiber |
| market_stress_oscillator | momentum | Ungenügend | ADX-Pflicht-Veto auf Stress-Events (Regime-Mix) |
| liquidity_hunter | market_structure | Ungenügend | WT-Exhaustion im Signalpfad + Bias-Aggregator |
| zigzag_patterns_framework | market_structure | Ungenügend | RSI-Divergenz ins Struktur-Label gemischt |
| coilforge_zones | market_structure | Ungenügend | ADX/DI als Richtung + harte AND-Gate-Kette |
| oscillator_divergence_zones | momentum | Ungenügend | Strategy-Config Long=Reversal / Short=Continuation |
| reversal_engine_score | momentum | Ungenügend | Starre AND-Pflichtkette, rsi>50 doppelt gezählt |
| wavetrend (v1) | momentum | Ungenügend | 9-fach-AND-Veto-Kette (default-off) |
| candle_pressure_index | money_flow | Ungenügend | Volumen-Pressure-Zero-Cross direkt als Long/Short |
| smooth_trend_radar | trend_direction | Ungenügend | Pivot im Rejection-Trigger + Continuation/Reversal parallel |
| time_to_react_volatility_time | volatility | Ungenügend | Swing-Pivot speist Richtung (`eventDir`) |
| vein_trend | trend_direction | Ungenügend | Pivot-Proximity im Score + 8-fach-AND (de facto Defekt) |
| vein_reversal_score | trend_direction | Ungenügend | Pivot-Proximity + Location im Score, eigene Regime-Klass. |
| vein_execution | trend_direction | Ungenügend | Internes zweites Multi-Rollen-Score-System + AND-Kette |
| vein_reversal_zones | trend_direction | Ungenügend | 5-Sensor-Trigger roh „je +1" gemischt |
| signal_quality_engine | composite | OK | Vorbildlicher Single-Purpose-Range-Fader |
| commodity_pulse_matrix_v4 ⟂ | — | — | (siehe oben) |
| smc_structure_expectation | market_structure | OK | Sauberes Struktur-Tool, vorbildliches why-not-Debug |
| wyckoff_schematics | market_structure | OK | Additives Evidenz-Scoring, Pivot als Struktur |
| reversal_type_classifier | market_structure | OK | Ex-post-Diagnose-Tool, zweckkonform |
| zigzag_fibo_pullback_map | market_structure | OK | Reiner Struktur-/Visual-Indikator |
| elliott_wave_radar | market_structure | OK | Struktur-Location, ehrlicher „no count"-Zustand |
| sr_zones_mtf_v2 | market_structure | OK | Scoring bleibt auf Zonen-Rolle |
| swing_conviction_radar | market_structure | OK | Fokussierter Conviction/Quality-Oszillator |
| market_structure_advanced | market_structure | OK | Klarer Struktur-Bias-Oszillator |
| mtf_structure_bias | market_structure | OK | Referenz für Rollen-/TF-Gewichtung |
| auto_trendlines | market_structure | OK | Trendlinien-Location, Veto bewusst weichgemacht |
| mtf_wavetrend_opportunity_hunter | momentum | OK | Gate-frei, Pivot strikt Overlay — Referenz |
| mtf_wavetrend_confluence | momentum | OK | Grade-statt-Gate — Referenz |
| market_exhaustion | momentum | OK | Rollen getrennt, normiertes Evidenz-Scoring |
| wavetrend_v2 | momentum | OK | Minimaler reiner Oszillator |
| wavetrend_advanced_smoothing | momentum | OK | Single-Purpose-Momentum, Signal/Darstellung getrennt |
| momentum_profile | momentum | OK | Reiner Visualisierungs-Indikator |
| cci_advanced | momentum | OK | Fokussierter CCI-Oszillator |
| oscillator_topology | momentum | OK | Deskriptiver Topologie-Klassifikator |
| momentum_trajectory | momentum | OK | Symmetrischer Ableitungs-Indikator |
| oscillator_footprint | momentum | OK | Reiner Visualisierungs-Indikator |
| money_flow_delta_profile | money_flow | OK | Reines Volumen-/Delta-Profil (Location) |
| volume_strata | money_flow | OK | Sauberes Volumenprofil, Bias nur deskriptiv |
| cvd_bias | money_flow | OK | CVD als Bias/Divergenz-Layer, nicht Trigger |
| relative_leg_efficiency | relative_strength | OK | Leg-Quality-Score, Pivot als Mess-Boundary |
| relative_strength_line | relative_strength | OK | RS+Preis-Confluence — Referenz |
| chandelier_flip_radar | trend_direction | OK | Sauberer Trendstop, Body-Filter als Quality |
| adaptive_supertrend | trend_direction | OK | Conviction wirkt auf Bandbreite, nicht als Veto |
| ma_regime_bands | trend_direction | OK | Regime-Definition, AND ist definitorisch |
| vein_structure_zones | trend_direction | OK | Single-Role-Location, RSI/MFI nur Zonen-Quality |
| vein_feature_exporter | trend_direction | OK | Sauberes Export/Research-Modul |
| vein_accumulation_phase | trend_direction | OK | Single-Role-Prozesszustand |
| vein_reversal_labeler | trend_direction | OK | Research/Labeling, forward-looking deklariert |
| vein_exhaustion | trend_direction | OK | Richtungssymmetrisches Exhaustion-Modul |
| vein_pullback | trend_direction | OK | Continuation mit korrekter Regime-Trennung |
| vein_spread_context | trend_direction | OK | Reiner Kontext-Modifier, Rolle deklariert |
| adx_advanced | trend_strength | OK | ADX=Stärke, DI±=Richtung — Referenz |
| adaptive_cycle_detector | trend_strength | OK | Adaptions-/Längentool |
| atr_advanced | volatility | OK | Eindimensionaler Vola-Indikator |

> Hinweis zur Tabelle: `commodity_pulse_matrix_v3/v4` und die `wavetrend`-Versionen sind getrennt gelistet; bei den WaveTrend-Versionen ist v3 die umfangreichste/aktuellste (Fehlerhaft), v2 der bewusste reine-Oszillator-Gegenpol (OK), v1 die mildere AND-Ketten-Variante (Ungenügend).

---

## 7. Methodik & Grenzen

- Audit durch 12 parallele Subagenten, je mit dem vollständigen Regelwerk (da Subagenten die Skills nicht geladen haben). Jeder Befund ist mit `Datei:Zeile` + Zitat belegt.
- Die Verdicts spiegeln **architektonische Regelkonformität**, nicht die Trading-Performance. Ein „Fehlerhaft" heißt „verstößt gegen die Design-Regeln", nicht „verliert Geld" — und ein „OK" heißt nicht „profitabel".
- Default-Zustand zählt: mehrere „Ungenügend"-Fälle verhalten sich im Default sauber und brechen erst beim Zuschalten optionaler Engines (`vwap_cross_visuals`, `wavetrend` v1) — im Report vermerkt.
- Wo ein Subagent „Ungenügend" vergab, der Befund per Regelwerk aber ein harter Defekt ist (Pivot im Signalpfad), ist das in Abschnitt 2 explizit eskaliert.
