---
name: instrument-data-validity
description: >-
  Regelwerk, welche Daten auf welchem Instrument überhaupt eine Aussage tragen — bevor ein
  Indikator sie verrechnet. Benutzen, sobald Volumen, VWAP, Volume Profile, OBV/MFI/CMF/
  Klinger, CVD/Delta, Orderflow, Open Interest, COT, Terminstruktur/Contango, Breadth oder
  ein Cross-Symbol-`request.security()` im Spiel sind — und immer, wenn ein Skript auf einem
  CFD laufen soll (Capital.com NatGas, Indizes, Aktien-CFDs, Forex). Triggert bei: "hat das
  Symbol überhaupt Volumen", "ist das CFD-Volumen echt", "tick volume", "syminfo.volumetype",
  "welchen Referenzmarkt nehme ich", "NG1! statt CFD", "darf ich hier VWAP verwenden",
  "Delta aus OHLCV", "buying pressure", "Open Interest in Pine", "_OI", "request.footprint",
  "Data Contract", "läuft der Indikator auf jedem Instrument" — und für die
  Rahmenbedingungen jenseits der Datenklasse: Back-Adjustment, Settlement-as-Close, Extended
  Session, Heikin-Ashi/Renko im Backtest, verzögerte CME-Daten, `request.*`-Limit,
  Repainting-Reproduzierbarkeit, Overnight-Funding/Roll-Kosten im Kostenmodell.
  Liefert die Entscheidung
  OK / Kennzeichnen / Überarbeiten / Umwidmen pro Skript — nie eine pauschale Policy.
  Nicht für Trading-Logik-Architektur (→ indicator-design), nicht für Pine-Bugs allgemein
  (→ indicator-code-audit) — hier geht es ausschließlich um Datenherkunft und Datengültigkeit.
---

# Instrument Data Validity — Datenherkunft vor Mathematik

Ein Indikator bekommt seine Aussagekraft nicht daher, dass seine Formel sinnvoll ist,
sondern nur daher, dass seine Eingangsdaten die Information enthalten, die er messen soll.
Mathematisch korrekt verarbeiteter Müll ist Müll.

**Die vollständige Matrix (Datenart × Instrumenttyp → 🟢/🟡/🔴), das Referenzmarkt-Mapping
und die Quellen stehen in [`DATA_VALIDITY.md`](../../../DATA_VALIDITY.md) im Repo-Root.**
Dieser Skill ist das Verfahren; dort steht das Nachschlagewerk. Bei konkreten Datenarten
dort nachsehen, nicht aus dem Gedächtnis urteilen.

## 0. Abgrenzung

| Frage | Skill |
|---|---|
| Trägt diese Datenquelle auf diesem Instrument überhaupt eine Aussage? | **dieser Skill** |
| Darf ich hier Volumen/VWAP/OI/Orderflow verwenden? | **dieser Skill** |
| Welchen Referenzmarkt nehme ich, und wie hole ich ihn sauber? | **dieser Skill** |
| Ist der Pine-Code technisch korrekt (Repaint, Performance, tote Variablen)? | `indicator-code-audit` |
| Ist die Signal-Architektur sauber (Rollen, Gates, AND-Ketten)? | `indicator-review` |
| Wie baue ich die Signal-/Score-Logik? | `indicator-design` |

## 1. Es gibt keine Blanket-Policy

Volumen wird **nicht** pauschal entfernt und **nicht** pauschal degradiert. Jedes Skript
bekommt eine eigene Entscheidung, weil die richtige Antwort vom Instrument abhängt, auf dem
es laufen soll. Wer "Volumen raus" oder "immer Referenzmarkt" als Regel anwendet, hat die
Einzelfallprüfung übersprungen.

## 2. Prüfkette

Für jede Datenquelle in einem Skript in dieser Reihenfolge:

1. **Welche Informationsklasse?** A Chart-Preis · B Referenzpreis · C Referenzvolumen ·
   D Positionierung (OI/COT) · E Terminstruktur · F Fundamentals.
   Klasse A ist überall verfügbar. Alles ab B ist eine bewusste Zusatzentscheidung mit Kosten.
2. **Auf welchem Instrument soll das Skript laufen?** Steht es nicht im README/CATALOG:
   nachfragen, nicht annehmen. Die Repo-Referenz ist `CAPITALCOM:NATURALGAS` — ein CFD.
3. **Was sagt die Matrix** in `DATA_VALIDITY.md` für Datenart × Instrumenttyp?
4. **Ist die Quelle tragend oder Beiwerk?** Test: Komponente gedanklich entfernen —
   ändert sich das Signal? Tragend. Ändert sich nichts? Beiwerk.
5. **Entscheidung** (§6).

## 3. Die Laufzeit-Prüfung

Volumen-Validität kommt aus `syminfo.volumetype`, nicht aus `syminfo.type` und erst recht
nicht aus der bloßen Existenz einer `volume`-Serie:

| Wert | Bedeutung | Handelsvolumen? |
|---|---|---|
| `"base"` | Menge in Basiseinheit/Kontrakten | ja |
| `"quote"` | Menge in Quote-Währung | ja, andere Einheit — nicht mischen |
| `"tick"` | Anzahl Preis-Updates | **nein** |
| `"n/a"` | keins | **nein** |

```pine
bool volumeIsReal = (syminfo.volumetype == "base" or syminfo.volumetype == "quote")
                    and not na(volume)
```

`syminfo.type` ist als Enum nicht stabil garantiert — nur zur Beschriftung, nie als alleinige
Rechenweg-Bedingung, und immer mit defensivem Default-Zweig.

### Die `nz(volume)`-Falle

`nz(volume)` ist **kein** Guard. Es macht fehlendes Volumen zu `0`, und `0 > sma(vol)` ist
dann dauerhaft `false` → das Gate blockiert still alles. Umgekehrt wird `range / nz(volume)`
zur Division durch Null. Im Repo ist das das häufigste Muster. Ein Guard prüft Validität und
schaltet das Feature ab; er ersetzt keinen Wert.

## 4. Data Contract im Header

Jedes `.pine`-File deklariert seine Datenannahmen — Block nach `Features:`, vor dem
abschließenden Separator:

```pine
// Data Contract:
//   Price:     REQUIRED   chart symbol
//   Volume:    OPTIONAL   real trade volume only — degrades to neutral
//   OI:        NO
//   Reference: NO
//   Verdict:   CFD-degraded
```

`Verdict` ∈ `CFD-safe` · `CFD-degraded` · `Reference-required` · `Exchange-only`.
Feldbedeutungen in `DATA_VALIDITY.md` §6.

## 5. Umsetzungsmuster

**Degradation (Feature neutral, nicht 0):**

```pine
float volScore = volumeIsReal ? f_volScore() : na       // nicht 0.0
bool  volGate  = volumeIsReal ? volume > volMa : true   // pass-through, nicht false
```

Bei gewichteten Scores das **Gewicht renormalisieren**, nicht nur den Beitrag nullen —
sonst sinkt der Gesamtscore auf CFDs systematisch und alle Schwellen verschieben sich.

**Sichtbarkeit:** Ein abgeschaltetes Feature muss im UI erkennbar sein — Dashboard-Zeile
("Volumen: tick — inaktiv") oder einmaliges Label auf `barstate.islast`. Stille Degradation
ist ein eigener Fund.

**Referenzmarkt — der Default ist: nicht.** Ein Cross-Symbol-Request gehört nicht in einen
Einzelindikator. Bei fehlendem echten Volumen wird degradiert, nicht requestet. Der
Referenzmarkt bringt sechs Fehlerquellen mit (Latenz, Settlement-Unklarheit, Session-Versatz,
Request-Budget, Repaint-Risiko, Symbol-Mapping) und lohnt nur, wenn er eine Dimension
liefert, die das Chart-Instrument **überhaupt nicht hat**: OI/ΔOI, Terminstruktur, echtes
Volumen als Regime-Kontext. Diese gehören in ein einziges Kontext-Modul, nicht verteilt.

Vertrauensrangfolge (`DATA_VALIDITY.md` §4.2):

| Stufe | Quelle | Vertrauen |
|---|---|---|
| 1 | Chart-Preis | hoch |
| 2 | Referenzmarkt auf **Daily**, nur Nicht-Preis-Daten (OI, Volumen, Front/Next-Spread) | brauchbar |
| 3 | Referenzmarkt intraday | schwach |
| 4 | aus CFD-Volumen abgeleitetes | keins |

Stufe 2 umgeht die Settlement-/Back-Adjustment-Frage komplett, weil nie Preise zweier Feeds
verglichen werden. Wenn doch requestet wird: `request.security()` unbedingt auf Top-Level,
`lookahead=barmerge.lookahead_off`, `na`-Zweig neutral (nicht 0), Symbolzuordnung als
expliziter Input mit sichtbarem „nicht konfiguriert"-Zustand — nicht per `str.contains`
erraten.

## 6. Die vier Entscheidungen

| Entscheidung | Wann | Umsetzung |
|---|---|---|
| **OK** | nur Klasse A | Data Contract ergänzen, sonst nichts |
| **Kennzeichnen** | Volumen/OI ist Beiwerk | Guard + neutrale Degradation + UI-Sichtbarkeit + `CFD-degraded` + README-Hinweis |
| **Überarbeiten** | Quelle ist tragend (Score-Komponente, Gate, Signalbedingung) | Komponente ausbauen, Gewichte renormalisieren. **Kein** Referenzmarkt-Input hier |
| **Umwidmen** | nur mit echtem Volumen/OI sinnvoll (Volume Profile, CVD, Klinger, VWAP) | `Exchange-only`, Vermerk in README + CATALOG, im CFD-Kontext nicht verwenden |

## 7. Benennungsregel für Orderflow-Nahes

Aus OHLCV lässt sich kein Orderflow rekonstruieren — jeder Trade hat Käufer *und* Verkäufer.
`close > open ? volume : -volume` ist eine preisgewichtete Volumen-Heuristik, kein Delta.
Solche Größen dürfen so nicht heißen:

| verboten | zulässig |
|---|---|
| `delta`, `cvd`, `buyVolume`, `sellVolume` | `signedVolumeProxy`, `closeLocationWeightedVolume` |
| "institutionelle Akkumulation" | Aussage streichen |

Echtes Delta/Imbalance/POC gibt es nur über `request.footprint()` (Pine seit 2026,
Premium/Ultimate, nur Feeds mit Footprint-Daten) — nicht mit selbstgebautem Delta gleichsetzen.

## 8. Weitere Bedingungen jenseits der Datenklasse

Eine formal zulässige Datenquelle kann trotzdem unbrauchbar sein. Details und Zahlen in
`DATA_VALIDITY.md` §9 — hier die Prüffragen:

| # | Frage | Typischer Fehler |
|---|---|---|
| 1 | Hängt das Ergebnis an einer Chart-Einstellung, die das Skript nicht sieht? | Level/Fib-Logik auf Continuous Futures ohne Vermerk, welche Back-Adjustment-Einstellung gilt; Daily-Close eines Futures ist per Default **Settlement**, nicht der letzte Trade |
| 2 | Ist die Session-Annahme explizit? | Futures nutzen ETH als „regular" — `session.extended` ist dort gleich `session.regular`; Extended-Variablen sind auf `1D` immer `false` |
| 3 | Läuft ein Charttyp-abhängiges Skript auf synthetischen Bars? | Heikin Ashi/Renko sind laut Pine-Doku für Backtest und Automatisierung ungeeignet — Orders füllen zu Marktpreisen, nicht zu HA-Preisen |
| 4 | Ist der Referenz-Feed verzögert? | CME/NYMEX/COMEX ohne Datenpaket ~10 min — intraday hinkt jeder Referenzmarkt-Request hinterher, Alerts feuern auf verzögerten Daten |
| 5 | Reicht das Budget? | 40 unique `request.*`-Calls (64 Ultimate). Wer bei 29 steht, kann nicht beliebig Referenzmärkte nachrüsten |
| 6 | Historisch = Realtime? | fluide Bar-Werte, unbestätigte `request.security`-Werte, `varip`, `barstate.isnew`, `timenow`, `calc_on_every_tick`, Zeichnen in die Vergangenheit, Feed-Revisionen |
| 7 | Bildet das Kostenmodell die Instrumentmechanik ab? | Spot-Commodity-CFDs tragen eine tägliche Roll-Komponente (Daily Premium Adjustment) plus Admin-Gebühr, die im Chartpreis nicht steckt — `commission_value` allein bildet Mehrtages-Holds nicht ab |
| 8 | Werden Fremddaten als revisionsfrei behandelt? | `request.financial` (Reporting-Lag, Restatements), `request.economic` (Revisionen) |

Diese Fragen gehören in jedes Review — auch in eines, bei dem gar kein Volumen vorkommt.

## 9. Ablauf beim Prüfen eines bestehenden Skripts

1. `.pine` vollständig lesen; alle Stellen sammeln, die `volume`, `ta.vwap`, `ta.obv`,
   `ta.mfi`, `ta.vwma`, `request.security` mit Fremdsymbol oder `_OI` verwenden.
2. Pro Stelle: Klasse bestimmen, Matrix konsultieren, tragend-vs-Beiwerk testen.
3. Prüfen, ob bereits ein echter Guard existiert (`volumetype`) oder nur `nz()`/`na()`.
4. Prüfen, ob eine Degradation still passiert (kein UI-Hinweis) — eigener Fund.
5. Prüfen, ob Score-Gewichte bei Degradation renormalisiert werden.
6. Entscheidung nach §6 vorschlagen, mit Begründung aus §2 Schritt 4.
7. Ausgabe als **Fundliste** mit Datei:Zeile — nicht als Gesamturteil. Steht
   `ReportFindings` zur Verfügung, darüber ausgeben.
