---
name: indicator-design
description: >-
  Rollenbasiertes Design-Regelwerk für TradingView/Pine-Indikatoren in diesem Repo.
  Benutzen, sobald ein Indikator (oder Strategie-Signal) neu gebaut, umgebaut, vereinfacht
  oder dessen Signal-/Score-Logik geändert wird — auch wenn der User das Wort "Rolle" oder
  "Architektur" nicht nennt. Triggert bei: neuen Indikatoren, Score-/Gewichtungs-Design,
  "warum killt mein Filter alle Setups", AND-Ketten von Gates, Veto-Logik, Watch/Setup/Trigger-
  Signaltypen, Regime-Umschaltung (Trendfolge vs. Reversal), Multi-Timeframe-Gewichtung,
  Markt-/Profil-spezifischer Gewichtung, Hardcoding von Schwellenwerten, und der Frage, ob ein
  Indikator "zu viel auf einmal" macht (eierlegende Wollmilchsau). Für das *Prüfen/Diagnostizieren*
  eines bestehenden Indikators stattdessen indicator-review verwenden.
---

# Indicator Design — Rollenbasiertes Regelwerk

Dieses Regelwerk hält Indikatoren **prüfbar** und **attributierbar**: man muss immer
sagen können, *warum* ein Signal kam (oder nicht) und *welche Ebene* dafür zuständig war.
Es kodifiziert die teuer gelernten Lektionen dieses Repos (siehe `.claude/CLAUDE.md`:
verworfene Gates A/B/C; Memories `feedback_one_thing_done_well`,
`feedback_pivot_is_control_not_signal`, `feedback_er_gates_blocking_reversals`).

## 0. Grundregel: ein Indikator ist nicht alles gleichzeitig

Ein Modul darf **nicht** gleichzeitig Trendfilter, Momentumfilter, Locationfilter, Trigger,
Qualitätsbewertung *und* Exitlogik sein. Tut es das, kann niemand mehr sagen, warum ein
Signal feuerte — das ist genau der Zustand, den dieses Repo wiederholt als „eierlegende
Wollmilchsau" verworfen hat.

- **Eine Hauptaufgabe pro Modul.** Eine Nebenaufgabe höchstens *visuell*.
- Default ist EIN Modell mit EINER klaren Entscheidungskette. Ein zweites Paradigma nur auf
  ausdrückliche Bitte — und nie so, dass zwei Modelle auf derselben Kerze mehrdeutig feuern.
- Wenn eine Version „in die falsche Richtung gelaufen" / zu komplex ist: **auf den Kern
  zurückstrippen**, nicht den nächsten Fix obendrauf setzen.

## 1. Das Rollen-Modell

Jeder Baustein bekommt **genau eine Rolle**. Indikatoren sind nur *Sensoren innerhalb* einer
Rolle — nicht selbst die Rolle.

| Rolle | Frage | Beispiel-Sensoren | NICHT die Rolle |
|---|---|---|---|
| **Trend** | In welche Richtung arbeitet der Markt? | EMA-Stack, Slope, HTF-Bias | ADX ist *keine* Richtung (nur Stärke) |
| **Location** | Sind wir in einem interessanten Preisbereich? | S/R, VWAP-Distanz, BB-Extrem, Range-Position | WaveTrend ist *kein* Location-Sensor |
| **Momentum** | Frisch oder erschöpft? Druck? | WT, RSI, MFI, StochRSI, Divergenz | — |
| **Trigger** | Gibt es *jetzt* ein Timing-Signal? | WT-Cross, Kerzenmuster, Break | ein Pivot ist *kein* Trigger (lagging) |
| **Quality** | Wie sicher ist die Aussage? | ATR-Regime, Chop, Spread, Liquidität | ein Volumen-Spike ist *kein* Long/Short-Signal |

Wenn du einem Sensor eine fremde Rolle gibst (z. B. RSI als Trendrichtung), wird der
Indikator unprüfbar — du erwartest dann die falsche Aussage vom falschen Modul.

## 2. Keine harten AND-Ketten

`Signal = A AND B AND C AND D` killt gute Setups. Genau dieses Muster hat in diesem Repo
94 % der WT-Crosses geblockt, ohne besser zu selektieren als der Marktdurchschnitt
(`.claude/CLAUDE.md`, test92).

Stattdessen: **jeder Sensor liefert Evidenz, am Ende wird bewertet — nicht blockiert.**

```pine
// schlecht: harte Kette
signal = trendUp and locExtreme and momFresh and triggerFired

// besser: Evidenz sammeln, dann Score
locationScore = ...   // 0..1
momentumScore = ...   // 0..1
triggerScore  = ...   // 0..1
score = wLoc*locationScore + wMom*momentumScore + wTrig*triggerScore
signal = score >= threshold and triggerFired   // Trigger als Timing, Rest als Gewicht
```

Ein einzelner schwacher Sensor (z. B. ein mittelmäßiger RSI) darf ein gutes Setup **nicht
allein töten**. Vor jedem neuen Gate gilt die Repo-Regel: erwartetes Block-Volumen aus den
Daten schätzen (Gates < ~5 % sind wirkungslos, Gates die gute *und* schlechte Trades gleich
oft entfernen sind selektionsneutral).

## 3. Veto-Regel — nur wenige echte Vetos

Nur strukturelle Markt-*Zustände* dürfen ein ganzes Setup kippen, nie ein einzelner
Indikator-Wert. Sinnvolle Vetos:

- zu wenig Volatilität / illiquide / extremer Spread
- extrem schlechte Marktqualität (Chop weit oben)
- Signal exakt mitten in der Range (Location-Veto)
- HTF völlig konträr — **nur bei Trendfolge**, nicht bei Reversal-Setups

Ein schlechter RSI-Wert ist **kein** Veto. Wichtig (Repo-Memory
`feedback_er_gates_blocking_reversals`): ein Veto darf den *eigentlichen Reversal-Trigger*
nicht blockieren — Over-Filtering ist hier das wiederkehrende Versagensmuster.

## 4. Scoring & Gewichtung auf Rollen-Ebene

Erst *innerhalb* der Rolle bewerten, dann die Rollen-Scores zusammenführen — nicht Indikatoren
direkt mischen.

```text
schlecht:  Score = RSI + CCI + WT + MFI + Trend        (beliebig, unattributierbar)
besser:    LocationScore, MomentumScore, TrendScore, TriggerScore, QualityScore
           Final = wLoc·Loc + wMom·Mom + wTrend·Trend + wTrig·Trig + wQual·Qual
```

Gewichtung gehört auf die **Rollen-Ebene**, nicht auf einzelne Indikatoren
(nicht „RSI = 20 %, CCI = 20 % …"). Richtwert:

| Rolle | Default-Gewicht |
|---|---|
| Location | 35 % |
| Momentum | 25 % |
| Trend | 20 % |
| Trigger | 15 % |
| Quality | 5 % |

### Gewicht hängt vom Timeframe ab

| TF | Verschiebung |
|---|---|
| Intraday | Trigger ↑, Volumen ↑, Noise-Filter ↑, Trend weniger stabil |
| 4H | Location ↑↑, Momentum ↑, Trend ↑, Trigger mittel |
| Daily | Trend ↑, Location ↑, Trigger ↓, Momentum langsamer interpretieren |

### Gewicht hängt vom Markt-Profil ab

| Markt | Betonte Rollen |
|---|---|
| Rohstoffe (z. B. NatGas) | Volatilität/ATR-Extreme, Mean Reversion, Exhaustion, Saison/News-Risiko |
| Aktien | Trend, relative Stärke, Volumen, Gap-Verhalten, Index-Kontext |
| Indizes | Trend, Breadth, Volatilitätsregime, VWAP/Value |
| Crypto | Momentum, Liquidität, Volatilität, Breakouts, Funding/Overextension |

Profile als Inputs/Presets bauen — **nicht** je Markt hart in die Signal-Logik gießen.

## 5. Hardcoding nur auf Rollen-Ebene

Nicht „RSI muss 72, CCI muss 148, WT muss kreuzen". Sondern: *„Momentum ist erschöpft",
„Location ist extrem", „Trend ist gedehnt", „Trigger bestätigt"* — die konkreten
Schwellenwerte sind je Profil/TF anpassbare Inputs hinter dieser Rollen-Aussage.

## 6. Regime zuerst — Trendfolge und Reversal nie ungetrennt mischen

Trendfolge- und Wendepunkt-Logik widersprechen sich. Erst Regime bestimmen
(Trend / Range / Expansion / Compression / Exhaustion), **dann** die passende Logik wählen.
Nie ein Signalmodell für alles. Wenn eine Auto-Regime-Umschaltung beide Modelle in
Übergangszonen gleichzeitig laufen lässt, werden Signale unattributierbar — das hat dieses
Repo bereits als Fehler verworfen (Memory `feedback_one_thing_done_well`).

Regeln symmetrisch halten: kein hartcodiertes Long/Short. Asymmetrie kommt aus der
*Situation* (Regime/Kontext), nicht aus der Richtung (Memory
`feedback_symmetric_situation_driven`).

### 6.1 Reversal-Pipeline — die vier Stufen

Grundsatz: **Kein Indikator erkennt die Trendwende.** Er erkennt nur, dass sich *eine
Eigenschaft* des Marktes geändert hat (Momentum erschöpft, Struktur gebrochen, Volatilität
komprimiert). Robuste Wendepunkt-Erkennung kombiniert deshalb mehrere Eigenschaften in
**fester Reihenfolge** — nicht ein einzelner Oszillator, der im Trend dauernd Fehlsignale
meldet.

Die vier Stufen sind eine Konkretisierung von §6 (Regime zuerst) und mappen direkt auf das
Rollen-Modell (§1):

| Stufe | Frage | Rolle | Sensoren (Repo) |
|---|---|---|---|
| **1. Regime** | Ist hier ein Reversal überhaupt sinnvoll? | Quality / Veto | FDI, Efficiency Ratio, ADX, Chop |
| **2. Erschöpfung** | Ist die Bewegung am Ende? | Momentum | Divergenz, WaveTrend, MFI, ruhige Osz. (Fisher/TSI) |
| **3. Bestätigung** | Dreht die Struktur *jetzt*? | Trigger + Location | BOS/CHOCH, SFP, Kerzen-Rejection (Pivot nur Diagnose, §8) |
| **4. Qualität** | Wie gut ist das Setup? | Quality + Location | BB-Width-Kompression, AVWAP-Distanz, Zonennähe |

**Die Reihenfolge ist die Regel.** Stufe 1 ist ein *Filter/Veto*, kein Trigger — sie
entscheidet, ob die Erschöpfungs-Logik überhaupt scharf ist. Erschöpfungssignale **ohne**
vorgeschaltetes Regime-Gate sind genau das wiederkehrende Fehlsignal-Muster im starken Trend
(`.claude/CLAUDE.md`: Gates blockten 94 % ohne besser zu selektieren — die Ursache war, dass
gefiltert *statt* regime-gestaffelt wurde).

Aber: das Regime-Veto darf den eigentlichen Reversal-Trigger nicht abwürgen (§3, Memory
`feedback_er_gates_blocking_reversals`) — es verschiebt die *Schwelle*, killt nicht das
Signal. Ein Modul deckt **eine** Stufe sauber ab (§0); ein Reversal-Scanner führt die vier
Stufen-Scores zusammen (§4), statt alles in eine AND-Kette zu pressen (§2).

**Repo-Abdeckung (Stand 2026-06-27):** Stufe 2 (Erschöpfung) und Stufe 3 (Bestätigung) sind
breit besetzt; **Stufe 1 (Regime-Klassifikator aus FDI/ER/Chop) und Stufe 4 (Anchored VWAP)
sind die offenen Lücken** — beim Bauen dort priorisieren, bevor weitere Erschöpfungs-Sensoren
hinzukommen.

## 7. Signaltypen trennen

Nicht alles in *ein* finales Signal pressen — das macht alles zu hart. Mindestens:

`Watch` → `Setup` → `Trigger` → `Confirmation` → `Invalidation`

Punkt-genaue Trigger (true nur auf der Cross-Kerze) sind zu punktuell — ein
**Momentum-Fenster** verwenden (`ta.barssince(momTurn) <= N`). „Bias" muss ein **stabiler
Richtungszustand** sein (hält bis klarer Gegen-Trend), nicht `longScore >= shortScore`
(flippt auf Score-Rauschen).

## 8. Pivots sind Diagnose, nicht Signalpfad

Pivots (`ta.pivothigh/low`) bleiben **Control-Overlay** — Marker, Distanz, Proximity in
Labels/Dashboard zur Genauigkeits-Prüfung. Sie speisen **nie** den Signalpfad: nicht als
Trigger, nicht als Grade-Gate, nicht als Dedup-Key (Memory
`feedback_pivot_is_control_not_signal`). Der Pivot ist durch `pivRightBars` lagging und damit
untergeordnet. Bessere Timing über pivot-freie Hebel (WT-Turn aus Extrem, WT-Velocity,
Momentum/Struktur auf der Trigger-TF). Details zur Pivot-*Auswertung*: siehe `indicator-review`.

## 9. Visuelle Regel — Information ohne Logik-Last

Alles, was nicht entscheidend sein *darf*, wird nur visuell gezeigt, nicht in die Logik
verdrahtet:

- RSI extrem, aber kein Signal → kleine graue Markierung
- Location stark, aber kein Trigger → gelbe Zone
- Trigger ohne Location → schwacher Marker

So geht keine Information verloren, ohne die Entscheidungslogik zu überladen.

## 10. Debug ist Pflicht

Jeder Indikator braucht Debug-Ausgaben — nicht nur Signal ja/nein, sondern:
*Warum kam ein Signal? Warum keins? Welcher Rollen-Score fehlte? Welches Modul hat geblockt?
Welche Rolle war stark/schwach?* Ohne Debug ist keine systematische Verbesserung möglich.

In diesem Repo: `log.info(...)`-Events mit Rollen-Scores + blockendem Gate (Muster wie
`WT4 BLOCKED reason=<gate>` in `strategies/wavetrend_v4_strategy.pine`), auswertbar über
`scripts/analyze_gates.py` und die Dashboard-Tabelle (Stil siehe `CLAUDE.md`).

## Mindestanforderung — die sechs Fragen

Ein fertiger Indikator muss diese Fragen jederzeit beantworten. Fehlt eine Antwort, weißt du,
welche Rolle/Ebene noch fehlt:

1. **Wo** sind wir? (Location)
2. In welche **Richtung** arbeitet der Markt? (Trend)
3. Ist Bewegung **erschöpft oder frisch**? (Momentum)
4. Gibt es **jetzt** ein Timing-Signal? (Trigger)
5. Wie **sicher** ist die Aussage? (Quality)
6. **Warum kam kein Signal**? (Debug)

## Kernregelwerk (Kurzform)

1. Keine All-in-one-Logik ohne Rollen.
2. Keine harten AND-Ketten — Evidenz bewerten, nicht blockieren.
3. Erst Rollen bewerten, dann Gesamtwertung.
4. Pivots zur Diagnose, nicht als exaktes Signalziel.
5. Gewichtung auf Rollen-Ebene, abhängig von TF, Markt-Profil und Regime.
6. Jeder Sensor liefert Information, blockiert aber nicht automatisch.
7. Nur wenige echte Vetos.
8. Debug-Ausgabe ist Pflicht.
