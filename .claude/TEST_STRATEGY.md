# Test-Strategie: Pivot-Window-basierte Gate-Auswertung

**Version 1, Stand: 2026-05-05**

## Grundkonzept

Der **ideale Trade** geht von einem Pivot zum nächsten gegenläufigen Pivot:
- Pivot Low → Pivot High = ideal long
- Pivot High → Pivot Low = ideal short

Innerhalb dieses **Pivot-Windows** [pivBar1, pivBar2] sollte unser tatsächlicher
Trade liegen und **70–80% des verfügbaren Wegs** abdecken, ohne SL auszulösen.

## Trade-Klassifikation pro Pivot-Window

Pro Window prüfen wir:

| Klassifikation | Bedingung |
|---|---|
| **Ideal** | tatsächlicher Trade existiert UND coverage ≥ 70% UND kein SL |
| **Cut-short** | Trade existiert ABER coverage < 70% ODER SL gehittet |
| **Lost** | kein Trade — aber Signals wurden im Window geblockt |
| **No-signal** | kein Signal im Window — niemand schuld |

`coverage = (exit_price − entry_price) / (pivBar2_price − pivBar1_price)` (richtungsbezogen)

## Gate-Bewertung

Ein Gate ist **nützlich** wenn es:
- In Lost-/Cut-short-Windows **selten** als blocker erscheint
- In Windows OHNE Pivot-Move (Range/Drift) **häufig** blockt

Ein Gate ist **schädlich** wenn es:
- In Lost-Windows mit ausreichend Pivot-Move **häufig** blockt → es nimmt uns echte Setups weg

## Disturbance-Rate

Pro Gate definieren wir die **Disturbance-Rate**:

```
disturbance_rate = (Blocks in Lost/Cut-short Pivot-Windows)
                 / (Gesamte Blocks dieses Gates)
```

### Aktionsschwellen

| Disturbance-Rate | Aktion |
|---|---|
| < 10% | Gate funktioniert sauber, BEHALTEN |
| 10–30% | Gate hat moderate Kollisionen, JUSTIEREN (Schwellwerte/Bands enger) |
| > 30% | Gate stört systematisch die echten Trades, ENTFERNEN falls nicht justierbar |

## Datenquellen

Aus dem Pine-Log werden folgende Events genutzt:

- **WT4 PIVOT** — bestätigte Pivots (pivBar, pivLow/pivHigh, pivAtr, tf, dir)
- **WT4 ENTRY** — generiertes Signal (vor Gate-Check) mit Kontext
- **WT4 BLOCKED** — geblockter Cross mit:
  - `reason=gateX` — der erste blockende Gate (chronologisch in f_blockReason)
  - `gates=A=T|B=T|C=F|D=T|G=F|H=T|I=T` — **alle** Quality-Gate-Decisions
    (ab v4.61). Ermöglicht offline-Simulation „was wäre wenn Gate X aus?"
- **WT4 ENTRY FILL** — tatsächlicher Fill (tradeId, dir, entryBar, tf)
- **WT4 REAL EXIT** — Exit (tradeId, R, exit_price, exitReason, ...)

### Gate-Flag-Simulation (v4.61+)

Mit dem `gates=` Feld im BLOCKED-Log können wir pro Signal sehen, welche Gates
genau pass/fail waren. Das ermöglicht eine zentrale Frage:

> Hätte Signal X passieren können, wenn Gate Y aus gewesen wäre?

Antwort: ja, wenn alle ANDEREN Gates `T` sind. Der Evaluator zählt pro Gate, in
wie vielen LOST/CUT_SHORT Opp-Windows ein Signal NUR durch dieses Gate gestoppt
wurde („einzigartiger Disturber").

Hohe Zahlen = Gate ist alleiniger Disturber → Entfernen würde viele Opps
freischalten. Niedrige Zahlen = Gate hat Schnittmengen mit anderen Gates →
Entfernen würde wenig ändern.

**Wichtig:** „Freischalten" heißt nicht „würde Gewinn werden". Die Auswertung
sagt nur, ob das Signal entered hätte — nicht ob es Gewinn gemacht hätte. Aber:
wenn ein Gate viele Signale alleine blockt, ist es ein klarer Kandidat für
Justierung.

## Auswertungs-Tool

`scripts/evaluate_pivot_coverage.py <testdir>`

Ausgabe:
1. Pro TF/dir: Klassifikation aller Pivot-Windows (Ideal / Cut-short / Lost / No-signal),
   gefiltert auf Opportunity-Windows (theoretical_R ≥ 1.5)
2. Pro Gate: Block-Volumen (gesamt + in Opp-Windows)
3. Pro Gate × TF/dir: Disturbance-Aufschlüsselung
4. Block-Position im Window (zeigt ob Gate timing-biased ist)
5. **Gate-Flag-Simulation** (v4.61+): pro Gate Anzahl Opps, die NUR an diesem Gate scheiterten

## Wann anwenden

- Nach jedem neuen Test (nach `analyze_gates.py`)
- Insbesondere nach Gate-Änderungen (neue Defaults, neue Gates)
- Vor Entscheidungen ein Gate zu behalten/justieren/entfernen

## Beispiel-Workflow

```
Neuer Test exportiert → testdata/testNNN/
├─ python3 scripts/analyze_gates.py testdata/testNNN
│  → grobe Übersicht (WR, avgR per TF/dir)
└─ python3 scripts/evaluate_pivot_coverage.py testdata/testNNN
   → Gate-Disturbance-Rates
   → Aktionsentscheidung pro Gate
```

## Lessons (laufend ergänzen)

### Gate F (No-Follow) — TF-Sensibilität

- Aktiv auf 1H: hilft (Disturbance moderat)
- Aktiv auf 4H/15M/1D: zerstört Winner (Disturbance hoch)
- → hardcoded auf 1H

### Was wir NICHT mehr tun

- A/B-Tests pro Gate (zu manuell, ignoriert Schnittmengen)
- Aggregierte Loser-Cluster ohne Pivot-Window-Kontext (siehe verworfene Gates A/B/C in CLAUDE.md)
