# WaveTrend v4 — Status & Schwerpunkt

Stand: 2026-05-05 | Datenbasis: test132 (v4.74) | Symbol: CAPITALCOM:NATURALGAS

---

## Aufgabe

Reversal-Strategie auf WaveTrend-Crosses. Entry bei WT-Crossover im OS/OB-Bereich,
Exit über fixen TP-Multiplikator und ATR-basiertem SL. Mehrere Gates filtern
schlechte Signale heraus (StochRSI, HTF-Exhaustion, Chop, ATR-Rank, u.a.).

**Hauptziel:** Möglichst viele Pivot-zu-Pivot-Moves handeln (Coverage ≥ 70%)
ohne SL-Hits. Aktuell: 14% Coverage, avgR +0.26 über 878 Trades.

---

## Aktueller Stand (test132)

### Pivot-to-Pivot Baseline (theoretisches Maximum)

| TF | Opportunities | Avg Pivot-Move | Caught | Coverage |
|---|---|---|---|---|
| 15M | 1115 | +2.73R | 59 | 5% |
| 1H | 1289 | +2.85R | 217 | 17% |
| 4H | 1164 | +2.66R | 191 | 16% |
| 1D | 238 | +2.63R | 55 | 23% |
| **ALL** | **3806** | **+2.74R** | **522** | **14%** |

Caught avgR = **+2.66R** — wenn wir einsteigen, treffen wir echte Moves.
Das Problem ist nicht die Entry-Qualität, sondern was danach passiert.

### Entry-Qualität pro TF/Dir

| TF | Dir | Trades | WR | avgR | SL% | TP% | noFollow/failfast% |
|---|---|---|---|---|---|---|---|
| 15M | long | 46 | 46% | +0.57 | 41% | 46% | — |
| 15M | short | 57 | 40% | +0.49 | 44% | 40% | — |
| **1H** | **long** | **207** | **37%** | **+0.14** | **21%** | **21%** | **49%** |
| **1H** | **short** | **186** | **36%** | **+0.03** | **22%** | **17%** | **55%** |
| 4H | long | 139 | 37% | +0.42 | 48% | 35% | — |
| 4H | short | 154 | 27% | +0.24 | 47% | 23% | — |
| 1D | long | 38 | 39% | +0.53 | 42% | 39% | — |
| 1D | short | 51 | 31% | +0.43 | 49% | 31% | — |

1H macht 45% aller Trades (393/878), ist aber der schwächste TF mit avgR +0.086 combined.

---

## Diagnose: Die drei Fragen

### 1. Sind die Einstiege zu weit weg von den Pivots?

Nein — 522 von 878 Entries (59%) landen in echten Pivot-Fenstern mit caught avgR +2.66R.
Die restlichen 40% Noise-Entries werden bereits durch die Gates reduziert.
Entry-Timing ist nicht das Kernproblem.

### 2. Sind viele Signale verlustbehaftet — wegen falscher Richtung oder zu engem SL?

Teils. WR = 36% overall, 64% treffen SL. **Aber:** SL-Trades zeigen positive MFE
bevor sie stoppen:

| TF | SL-Trades | avgMFE vor SL-Hit |
|---|---|---|
| 1H long | 41 | +6.7 (Preiseinheiten) |
| 1H short | 42 | +7.0 |
| 4H long | 67 | +19.0 |
| 1D short | 25 | +36.2 |

Die Entries sind also initial korrekt — der Trade geht zuerst ins Plus, dreht dann
aber um und trifft SL. Das ist normales Reversal-Verhalten, kein Entry-Fehler.
SL-Weite scheint angemessen (nicht zu eng, sonst wäre MFE ≈ 0).

### 3. Wird der TP falsch berechnet?

Nein. Die Exit-Arithmetik stimmt:

- 4H long: WR=37%, tpMult≈3 → erwartet: 0.37×3 − 0.63 = +0.48R ≈ actual +0.42R ✓
- 1H: WR=37%, tpMult≈2 → erwartet: 0.37×2 − 0.63 = +0.11R ≈ actual +0.09R ✓

TP ist korrekt kalkuliert für den WR, den die Gates ermöglichen.

---

## Hauptbefund: 1H hat zwei 1H-exklusive Exit-Mechanismen (Gate E + F)

**Gate E (Fail-Fast):** Schließt sofort wenn Trade in ersten `failFastBars` Bars
um `failFastR` adverse läuft. Nur auf 1H aktiv.

**Gate F (No-Follow):** Schließt wenn nach `nftWindow` Bars der Fortschritt unter
`nftRequiredR` liegt. Nur auf 1H aktiv.

### Wirkung in test132:

| Exit-Typ | n | avgR | Anteil 1H |
|---|---|---|---|
| sl | 83 | −0.99 | 21% |
| tp | 82 | +1.96 | 21% |
| be | 24 | ±0.00 | 6% |
| **failfast** | **52** | **−0.54** | **13%** |
| **noFollow** | **152** | **−0.11** | **39%** |

**1H ohne noFollow/failfast (sl+tp+be allein): n=189, avgR = +0.417R**
**1H aktuell mit allen Exits: n=393, avgR = +0.086R**

noFollow + failfast verursachen −44.9R Drag über 204 Trades.

noFollow hat 41% positive Exits — Trades die im Gewinn waren, aber abgeschnitten
wurden. failfast schneidet 100% der Trades ins Minus, spart aber ~0.46R vs. SL.

---

## Schwerpunkt: Gate F (noFollow) deaktivieren

Das ist der größte einzelne Hebel. Hypothese:

- noFollow blockt 152 1H-Trades mit avgR −0.11 (59% Verlierer, 41% Gewinner)
- Wenn diese Trades stattdessen zu sl/tp laufen (WR ~36%): ca. +0.07R avg
- Erwartete 1H-Verbesserung: von +0.086R auf ~+0.24R combined
- Overall-Wirkung: +0.06 avgR auf das Gesamtportfolio

**Test:** `useNoFollow = false` in TradingView Strategy-Settings aktivieren.

failfast separat testen — spart tatsächlich Geld (100% cuts, avg −0.54 statt −1.0).

---

## Coverage-Ceiling: Struktureller Befund

Mit dem WT-Cross-Einstieg sind ~27% Coverage das theoretische Maximum
(nur ~38% der WT-Crosses liegen überhaupt nahe eines echten Pivots).
70% Coverage ist mit dieser Architektur nicht erreichbar — das ist ein
Einstiegsmechanismus-Problem, kein Gate-Problem.

Realistische Obergrenze bei aktuellem Gate-Setup: **14–18%** Coverage.
Fokus bleibt auf avgR-Optimierung, nicht Coverage-Maximierung.

---

## Gate-Kosten-Übersicht (test132)

| Gate | Geblockte Signals | Near-Pivot-Blocks | Bewertung |
|---|---|---|---|
| gateA (StochRSI) | 679 (25%) | 190 | Korrekt — gateA OFF verliert avgR (test135) |
| gateG (Trend/Range) | 435 (16%) | 111 | Nicht getestet |
| gateC (HTF Exhaustion) | 333 (12%) | 108 | Etabliert, nicht anfassen |
| gateD (4H Cluster) | 146 (5%) | 24 | Etabliert |
| gateB2 (15M/1H Confluence) | 88 (3%) | 36 | Etabliert, v4.74 |
| gateB (Divergence) | — | — | Negativ getestet (test133) |
