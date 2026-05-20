# WaveTrend v4 — Ziel und Herangehensweise

Stand: 2026-05-20 | Datenbasis: test151–166 | Symbol: CAPITALCOM:NATURALGAS | test167 pending

---

## Ziel

Die Strategie hat einen nachweisbaren Edge (Pivot-to-Pivot avgR +2.7R über alle TFs).
Das Problem ist nicht der Core-Mechanismus, sondern dass zu viele Signale in Regimes
gehandelt werden, in denen WT-Reversals systematisch scheitern.

**Ziel:** Diesen Regime-Filter datengetrieben und TF/Dir-spezifisch kalibrieren —
ohne neue Mechanismen einzuführen. PF ≥ 1.5 über alle aktiven TFs, MaxDD < 5%.

---

## Kerndiagnose

Die bisherige Gate-Kalibrierung basierte auf Aggregat-Statistiken und Intuition.
Test151–154 hat gezeigt: GateA war für 1H **invertiert** — sie blockierte die
produktiven atrRank-Zonen und ließ die schlechten durch. Nach datenbasierter
Korrektur: PF 0.73 → 1.53, MaxDD 7.8% → 1.6%.

Das ist kein Tuning-Erfolg. Es ist ein **Methodik-Erfolg**: sobald man die
Entry-Bedingungen direkt mit dem Trade-Outcome verbindet, wird sichtbar was
wirklich funktioniert — und was bisher nur vermutet wurde.

---

## Die Methode

Für jeden TF und jede Richtung getrennt:

1. **Entry-Logs + Exit-Logs joinen**
   - `WT4 ENTRY` (bar, dir, tf) → alle Einstiegsbedingungen
   - `WT4 ENTRY FILL` (tradeId) → Verbindungsglied
   - `WT4 REAL EXIT` (tradeId) → R-Outcome
   - Join-Key: `(tf, tradeId)` — tradeIds sind pro TF-Datei eindeutig, nicht global
   - Signal-Bar-Matching: fill_bar − 1 = signal_bar (entry am nächsten Open)
   - Achtung: Zahlen im deutschen Locale haben Tausendertrennzeichen (z.B. `11,069` = 11069)

2. **Pro Feld bucketed segmentieren**
   - Für jedes Feld (atrRank, chop, bbWidthRank, wt1, srsiK, lowPivBars, …)
   - n, WR%, avgR pro Bucket
   - Klar schlechte Zonen (avgR deutlich negativ, n ≥ 10) identifizieren

3. **Gate-Zonen korrigieren, nicht erweitern**
   - Schlechte Buckets blocken, gute freigeben
   - Keine neuen Gates erfinden — bestehende GateA/D/H-Zonen korrigieren
   - Ein Test pro Änderung

4. **Ergebnis validieren**
   - Gleiche Analyse im Folgetest — hat sich das Bucket-Bild verbessert?
   - Kein Tuning wenn n < 10 pro Bucket (zu wenig Datenbasis)

---

## Was die Methode sichtbar macht

Die atrRank-Zone pro TF/Dir ist kein ATR-Filter — sie ist ein **Regime-Indikator**:
sie beschreibt in welchem Volatilitätsregime WT-Crosses auf diesem TF tatsächlich
zu Reversals führen. Falsch gesetzte Zonen bedeuten: wir handeln im falschen Regime.

Gleiches gilt für chop, bbWidthRank, wt1 — alle diese Felder beschreiben das
Marktregime zum Zeitpunkt des Signals. Die Methode findet automatisch welche
Regime-Dimensionen für welchen TF/Dir relevant sind.

---

## Aktueller Stand der Kalibrierung

Stand test163 (v4.85), alle TFs abgeschlossen.

| TF / Dir | n | avgR | Aktive Gates | Status |
|---|---|---|---|---|
| 15M long | 60 | +0.44 | GateA [30,50) · GateL highPivBars [20,30) | ✓ kalibriert |
| 15M short | 50 | +0.44 | GateA [30,50) · GateH chop [40,50) | ✓ kalibriert |
| 1H long | 127 | +0.30 | GateA [40,65) · GateH chop [30,40) | ✓ kalibriert |
| 1H short | 116 | +0.15 | GateA [0,60) · GateM srsiK [70,80) · GateK wt1 [60,80) | ✓ kalibriert |
| 4H long | 95 | +0.54 | GateA [20,40) · GateJ srsiD [50,100) · GateH chop [30,40) | ✓ kalibriert |
| 4H short | 127 | +0.37 | GateA [30,60) · GateD bbWidthRank [60,90) · GateK wt1 [40,50) | ✓ kalibriert |
| 1D long | 12 | +0.45 | GateA [20,40) | n zu klein — kein Gate |
| 1D short | 18 | +0.45 | GateA [40,60) | n zu klein — kein Gate |

### Abgeschlossene Analyse: test166 (gescheitert, revertiert)

GateD 4H long [60,90) → [20,40): **Regression** +0.538→+0.38.
Die freigeschalteten [60,90)-Trades ergaben avgR≈−0.25R (26 Trades, −6.4R).
Befund: test116-Kalibrierung [60,90) war korrekt. [20,40) bei +0.341R ist suboptimal
aber positiv — wird akzeptiert. [60,90) bleibt geblockt.
GateD 4H long zurück auf [60,90) (v4.87, kein neuer Test nötig da Revert).

**Pending test167 (v4.88): GateH 1H short chop [50,60)**

Befund (test165-Daten, bestätigt in test166):
- 1H short chop [50,60): n=17, avgR=-0.185, SL 24%, TP 6% — Ranging-Markt tötet 1H shorts
- 1H short chop [30,40): n=29, avgR=+0.572 (bestes Bucket — low chop/trending → 1H short funktioniert)
- Inversion zu 1H long: dort ist chop<40 schlecht, chop>50 gut
- Erwartete Verbesserung: 1H short avgR +0.149 → ~+0.206 (Δ+0.057R), n 116→99
- Grenzfall: n=17 knapp, aber Befund ist stabil und inhaltlich konsistent

Backlog danach:
- 4H short bbWidthRank [20,40): n=39, avgR=+0.186 — non-contiguous zu [60,90), Ansatz unklar

### Anmerkungen

- **15M Doppelexport**: test160 hatte 15M-Charts doppelt (2 CSV-Profile = doppelte n). Echte n=77 long, n=50 short. Alle 15M Bucket-Befunde auf Basis deduplizierter Daten.
- **15M long bimodal**: atrRank hat bimodale Bad-Zonen ([30,50) + hypothetisch [65,80)). GateA [30,50) ist stabiler Zustand; zweite Zone nicht isolierbar.
- **1H short**: strukturell schwach (+0.15). Alle Felder Δ < 3 nach Kalibrierung — keine weiteren Gates sinnvoll.

---

## Priorisierung (abgeschlossen)

Alle TFs mit Entry-Outcome-Methode analysiert. Basis-Kalibrierung abgeschlossen.

Nächste Schritte (Backlog):
- WT depth Gate richtungsgetrennt (Long-Obergrenze abs(wt1) auf 1H/4H) — Δ war marginal, nach mehr Datenbasis
- StochRSI dir. < 20 blockieren — benötigt neues Log-Feld (srsiD dir.-korrigiert)
- Out-of-Sample Validierung auf zweitem Instrument

---

## Was wir nicht tun

- Keine neuen Gate-Mechanismen ohne klaren Datenbefund
- Kein Tuning wenn Unterschied Winner/Loser < 5 Punkte (Rauschen)
- Keine Änderungen wenn n < 10 pro Bucket
- Keine gleichzeitigen Änderungen an mehreren TFs — ein Test, eine Änderung
- Keine Aggregat-Analyse über alle TFs (maskiert TF-spezifische Muster)

---

## RTC-Analyse: Hintergrundbefunde (v1.2, 2026-05-06)

Separate Analyse mit dem Reversal-Typ-Klassifikator — unterschiedliche Methodik
(population-level, nicht Entry-Outcome-Join), aber als Hintergrundkontext relevant.

### Reversal-Typ-Verteilung

| TF | n | Snap% | Grind% | Bad% |
|---|---|---|---|---|
| 15M | 1190 | 73% | 11% | 17% |
| 1H | 1654 | 72% | 13% | 15% |
| 4H | 1408 | 90% | 4% | 6% |
| 1D | 270 | 87% | 3% | 10% |

4H ist der sauberste TF. 15M/1H haben deutlich mehr Grind-Anteil (noFollow-Logik dort
besonders relevant). Snap-Trades dauern im Schnitt ≤ 3 Bars auf allen TFs.

### Stärkstes Befund-Muster: StochRSI-Extremität

Über alle TFs konsistent: schlechte Reversals passieren bei zu extremem StochRSI (dir.
korrigiert). Bad-Trades haben durchschnittlich 4–5 Punkte tiefere Werte. Sweet-Spot
für gute Reversals liegt bei ~30 (dir.), nicht am Limit. Kontraintuitiv aber reproduzierbar.

Gate-Implikation: Block wenn StochRSI dir. < ~20. Noch nicht als Gate implementiert.

### WT Depth: Richtungs-Inversion auf 1H/4H/1D Long

| TF | L-Good | L-Bad | S-Good | S-Bad |
|---|---|---|---|---|
| 15M | 19.2 | 14.4 | 15.4 | −1.4 |
| 1H | 13.6 | **18.3** | 16.7 | 12.2 |
| 4H | 12.4 | **15.0** | 16.2 | 3.1 |
| 1D | 8.5 | **30.2** | 22.8 | −11.9 |

Shorts: tiefer in OB = besser (konsistent).
Longs auf 1H/4H/1D: **invertiert** — zu tief in OS = schlechter.
Gate-Implikation nur richtungsgetrennt sinnvoll. Bestehender osFloor1D=−48 deckt 1D ab.

### Was getestet und abgelehnt wurde (gate-spezifisch)

- **1H BB Width > 45 blockieren** (test145/147): NOOP — blockt mehr Winner als Loser
- **Gate B Divergenz required** (test133): −77% Trades, avgR kaum besser → false
- **Gate F noFollow OFF** (test137): 1H verschlechtert, noFollow rettet Geld → bleibt aktiv
- **Gate A StochRSI OFF** (test135): Coverage +4%, avgR −0.11 → aktiv lassen

---

## Abgeschlossene Entwicklungen

| Test | Maßnahme | Ergebnis |
|---|---|---|
| test116 | Gate D + I für 4H Loser-Cluster | 4H long +0.34, 4H short +0.28 |
| test118 | Gate G TF-spezifisches Smoothing, 15M/1H hardcoded | positiv |
| test121 | Trailing Stop (trailTriggerR=2.0) | NOOP, als Insurance behalten |
| test121 | Per-TF tpMult | 1D long +0.10, 1D short +0.20, 4H long +0.06 |
| test124–126 | Structural Exit (3 Varianten) | alle gescheitert |
| test127 | BE-Trigger | NOOP, revertiert |
| test128–132 | Gate B2 1H-Confluence für 15M (b2OsLevel=−30) | 15M avgR +0.13 |
| test133 | Gate B Divergenz required | NOOP/negativ |
| test135 | Gate A OFF | negativ, bleibt aktiv |
| test137 | Gate F noFollow OFF | negativ, bleibt aktiv |
| test145/147 | 1H BB Width Gate > 45 | NOOP/negativ |
| test152 | GateA 1H long [65,100)→[40,65) | PF 0.73→1.04 |
| test153 | GateA 1H short [65,100)→[0,40) | PF 1.04→1.32 |
| test154 | GateA 1H short [0,40)→[0,60) | PF 1.32→1.53, MaxDD 7.8%→1.6% |
| test155 | GateA 4H short [40,60)→[30,60) | 4H short avgR verbessert |
| test157–158 | GateJ 4H long srsiD [50,100) | 4H long +0.36→+0.51 |
| test159 | GateK 4H short wt1 [40,50) | 4H short +0.305→+0.37 |
| test161 | GateL 15M long highPivBars [20,30) | 15M long +0.29→+0.44 |
| test162 | GateM 1H short srsiK [70,80) | 1H short +0.065→+0.10 |
| test163 | GateK 1H short wt1 [60,80) | 1H short +0.10→+0.15 |
| test164 | GateH 1H long chop [30,40) | 1H long +0.22→+0.30, n 175→127 |
| test165 | GateH 4H long chop [30,40) | 4H long +0.484→+0.538, n 119→95 |
| test166 | GateD 4H long [60,90)→[20,40) | REGRESSION +0.538→+0.38 — [60,90) bleibt geblockt |

---

## Backlog

- WT depth Gate richtungsgetrennt (Long-Obergrenze abs(wt1) auf 1H/4H) — nach Basis-Kalibrierung
- StochRSI dir. < 20 blockieren — nach Basis-Kalibrierung, benötigt neues Log-Feld
