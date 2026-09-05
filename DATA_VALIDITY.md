# Data Validity Matrix

**Zweck:** Regelwerk, welche Daten auf welchem Instrument überhaupt eine Aussage tragen —
bevor irgendein Indikator sie verrechnet.

**Grundsatz:** Ein Indikator bekommt seine Aussagekraft nicht daher, dass seine Mathematik
sinnvoll ist, sondern nur daher, dass seine Eingangsdaten die Information enthalten, die er
messen soll. Mathematisch korrekt verarbeiteter Müll ist Müll.

**Es gibt keine Blanket-Policy.** Jedes Skript wird einzeln entschieden — siehe
[§8 Entscheidungswege](#8-entscheidungswege-pro-skript). Das Regelwerk liefert die Kriterien,
nicht das Urteil.

---

## 1. Informationsklassen

Nicht "Trend / Momentum / Volume", sondern nach **Herkunft der Information**:

| Klasse | Inhalt | Quelle |
|---|---|---|
| **A — Chart Price** | O/H/L/C, Zeit, daraus Range, Returns, Struktur, Volatilität | Chart-Symbol |
| **B — Reference Price** | OHLC des zugrunde liegenden Referenzmarktes | `request.security()` auf Future/Underlying |
| **C — Reference Volume** | echtes Handelsvolumen, VWAP, Volume Profile | Referenzmarkt, **nie** der CFD |
| **D — Positioning** | Open Interest, ΔOI, COT | Future / Derivatemarkt |
| **E — Term Structure** | Front/Next Month, Calendar Spread, Contango/Backwardation | Futures-Kurve |
| **F — Fundamentals** | Storage, Wetter, Produktion, Makro | extern, in Pine meist nicht verfügbar |

Klasse A ist auf jedem Instrument verfügbar. Alles ab B ist eine **bewusste Zusatzentscheidung**
mit eigenen Kosten (Cross-Symbol-Request, Session-Alignment, Repaint-Risiko).

---

## 2. Die zentrale Laufzeit-Prüfung

Volumen-Validität wird **nicht** aus `syminfo.type` abgeleitet, sondern aus
`syminfo.volumetype`. Genau dafür existiert die Variable.

| `syminfo.volumetype` | Bedeutung | Verwendbar als Handelsvolumen |
|---|---|---|
| `"base"` | Volumen in Basiswährung/Kontrakten | ✅ ja |
| `"quote"` | Volumen in Quote-Währung (Krypto) | ⚠️ ja, aber andere Einheit — nicht mit `base` mischen |
| `"tick"` | Anzahl Preis-Updates, **kein** Handelsvolumen | ❌ nein |
| `"n/a"` | kein Volumen | ❌ nein |

TradingView liefert Volumen genau so weiter, wie es vom Provider kommt — Trade-Volumen,
Tick-Volumen oder gar nichts. Aus der bloßen Existenz einer `volume`-Serie folgt **nie**,
dass es sich um börsengehandeltes Volumen des zugrunde liegenden Marktes handelt.
Tick-Volumen wird u.a. für Indizes, Forex und Krypto-CFDs geliefert.

`syminfo.type` (beobachtete Werte: `stock`, `futures`, `index`, `forex`, `crypto`, `fund`,
`cfd`, `dr`, `bond`, `economic`, `spread`) ist als Enum **nicht garantiert stabil**. Nur für
grobe Beschriftung verwenden, nie als alleinige Bedingung für Rechenwege — und immer mit
defensivem Default-Zweig.

---

## 3. Die Matrix

🟢 valide · 🟡 nur als Proxy, muss gekennzeichnet werden · 🔴 nicht verwenden

### Klasse A — Preis & Struktur

| Datenart | CFD Rohstoff | CFD Index | CFD Aktie | Forex | Future | Aktie | Krypto |
|---|---|---|---|---|---|---|---|
| O/H/L/C | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| Range / True Range / ATR | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| Returns / ROC / Momentum | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| Oszillatoren (RSI, Stoch, CCI, TSI, Fisher, WT) | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| MAs, MACD, ADX, Supertrend, LinReg | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| Volatilitätsregime (BB-Width, ATR-Rank, Chop, HV) | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| Swing / Pivot / BOS / Trading Range | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| S/R-Zonen, Fib-Level (Zone, nicht Tick) | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| Tick-genaue Level-Verletzung (`high > lvl` auf 1 mintick) | 🟡 | 🟡 | 🟡 | 🟡 | 🟢 | 🟢 | 🟡 |
| Candle-Body/Wick-Pattern | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| Session-Gap | 🟡 | 🟡 | 🟡 | 🟡 | 🟢 | 🟢 | 🔴 (24/7) |
| Bid/Ask-Spread als Marktzustand | 🔴 broker-spezifisch | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | 🟡 |

**Zu 🟡 bei Level/Gap:** Der CFD-Feed ist ein Broker-Preis, nicht der Börsenpreis. Highs/Lows
weichen um Spread und Feed-Latenz ab. Ein Daily-Swing ist robust; ein Intraday-Breakout, der
sich an 1 mintick entscheidet, ist es nicht. Regel: **Level-Logik mit Toleranz (ATR-Bruchteil),
nie mit exakter Gleichheit.**

### Klasse C — Volumen

| Datenart | CFD Rohstoff | CFD Index | CFD Aktie | Forex | Future | Aktie | Krypto |
|---|---|---|---|---|---|---|---|
| `volume` roh | 🔴/🟡¹ | 🔴/🟡¹ | 🔴 → Underlying | 🟡 Tick | 🟢 | 🟢 | 🟢² |
| Relative Volume / Volume Spike | 🔴/🟡¹ | 🔴/🟡¹ | 🔴 → Underlying | 🟡 | 🟢 | 🟢 | 🟢² |
| OBV / PVT / A-D / CMF / MFI / Klinger / EOM | 🔴 | 🔴 | 🔴 → Underlying | 🔴 | 🟢 | 🟢 | 🟢² |
| VWMA | 🔴 | 🔴 | 🔴 → Underlying | 🔴 | 🟢 | 🟢 | 🟢² |
| VWAP / Anchored VWAP | 🔴 | 🔴 | 🔴 → Underlying | 🔴 | 🟢 | 🟢 | 🟢² |
| Volume Profile / POC / Value Area | 🔴 | 🔴 | 🔴 → Underlying | 🔴 | 🟢 | 🟢 | 🟢² |
| Effort-vs-Result (Range ÷ Volume) | 🔴 | 🔴 | 🔴 → Underlying | 🔴 | 🟢 | 🟢 | 🟢² |
| Wyckoff-Volumentests (SC, Spring, UT mit Volumenbestätigung) | 🔴 | 🔴 | 🔴 → Underlying | 🔴 | 🟢 | 🟢 | 🟢² |

¹ Abhängig vom Provider — muss zur Laufzeit über `syminfo.volumetype` entschieden werden.
Ist es `tick`/`n/a`: 🔴. Ist es `base`: 🟡 (Broker-Volumen ≠ Börsenvolumen, aber immerhin
gehandelte Menge bei diesem Broker) — Kennzeichnung Pflicht.
² Krypto: Volumen ist echt, aber **börsenspezifisch**. Ein einzelner Exchange ist ein Ausschnitt
des Gesamtmarktes, und `base` vs. `quote` ändert die Einheit.

**Der Punkt bei Aktien-CFDs:** Es gibt ein echtes Underlying mit echtem Volumen
(`NASDAQ:AAPL`). Es gibt keinen Grund, CFD-Volumen zu analysieren, wenn das Börsenvolumen
per `request.security()` verfügbar ist. CFD = Execution, Underlying = Analyse.

### Klasse — Orderflow

| Datenart | CFD Rohstoff | CFD Index | CFD Aktie | Forex | Future | Aktie | Krypto |
|---|---|---|---|---|---|---|---|
| Delta aus OHLCV konstruiert (`close>open ? vol : -vol`) | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 |
| Buy/Sell-Pressure aus Close-Position × Volume | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 |
| Echtes Delta / Imbalance / POC intrabar (`request.footprint()`) | 🔴 | 🔴 | 🔴 | 🔴 | 🟢³ | 🟢³ | 🟢³ |
| DOM / Orderbuch | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 in Pine | 🔴 in Pine | 🔴 in Pine |
| Liquidität / Slippage-Schätzung aus OHLC | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 |

³ `request.footprint()` (Pine, seit 2026) liefert echte intrabar Volume-Rows, Delta, POC,
VAH/VAL und Imbalances — erfordert Premium/Ultimate und einen Symbolfeed mit Footprint-Daten.

**Warum das gesamte konstruierte Delta 🔴 ist, auch auf Futures:** Jeder Trade hat Käufer
*und* Verkäufer. Ohne Aggressor-Klassifikation ist "grüne Kerze × Volumen = Kaufdruck" eine
Behauptung über Preisrichtung, nicht über Orderflow. Solche Größen dürfen **nicht** als
Orderflow benannt werden. Als *preisgewichtete Volumen-Heuristik* sind sie erlaubt — dann
muss der Name das sagen (`closeLocationValue`, nicht `delta`/`buyVolume`).

### Klasse D/E — Positionierung & Terminstruktur

| Datenart | CFD Rohstoff | CFD Index | CFD Aktie | Forex | Future | Aktie | Krypto |
|---|---|---|---|---|---|---|---|
| Open Interest (`<tickerid>_OI`) | 🔴 → Future | 🔴 → Future | – | 🔴 → FX-Future | 🟢 | – | 🟢 Perps |
| ΔOI + Preis kombiniert | 🔴 → Future | 🔴 → Future | – | 🔴 → FX-Future | 🟢 | – | 🟢 |
| COT | 🔴 → extern | 🔴 → extern | – | 🔴 → extern | 🟡 extern/wöchentlich | – | 🔴 |
| Front/Next Spread, Contango/Backwardation | 🔴 → Future | 🟡 | – | 🟡 | 🟢 | – | 🟡 Funding |
| Roll-Effekte / Kurvensteigung | 🔴 → Future | 🟡 | – | 🟡 | 🟢 | – | 🟡 |
| Saisonalität (Preis-basiert) | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |

### Klasse B — Relativ & Kontext

| Datenart | CFD Rohstoff | CFD Index | CFD Aktie | Forex | Future | Aktie | Krypto |
|---|---|---|---|---|---|---|---|
| Relative Strength vs. Benchmark | 🟢⁴ | 🟢⁴ | 🟢⁴ | 🟢⁴ | 🟢 | 🟢 | 🟢 |
| Korrelation / Beta zu anderem Symbol | 🟢⁴ | 🟢⁴ | 🟢⁴ | 🟢⁴ | 🟢 | 🟢 | 🟢 |
| Breadth (Index-Constituents) | – | 🟡 Constituents nötig | – | – | 🟡 | – | – |
| Cross-Asset-Kontext (DXY, VIX, Yields) | 🟢⁴ | 🟢⁴ | 🟢⁴ | 🟢⁴ | 🟢 | 🟢 | 🟢 |
| CFD-vs-Referenzmarkt-Abweichung als Qualitätsprüfung | 🟢 | 🟢 | 🟢 | 🟢 | – | – | 🟢 |

⁴ Nur auf **normalisierten** Größen (Returns, Ratio, Z-Score, Rank) — nie auf rohen
Preisniveaus. CFD und Referenzmarkt haben unterschiedliche Skalen, Sessions und Feiertage.

---

## 4. Referenzmarkt

### 4.1 Grundsatzentscheidung: Referenzmarkt ist die Ausnahme

**Ein Referenzmarkt-Request gehört nicht in einen Einzelindikator.** Der Default bei
fehlendem echten Volumen ist Degradation (§7), nicht ein Cross-Symbol-Request.

Begründung: Der Referenzmarkt bringt sechs zusätzliche Fehlerquellen mit — Latenz (§9.3),
Settlement-/Back-Adjustment-Unklarheit (§9.1), Session- und Feiertags-Versatz (§9.2),
Request-Budget (§9.4), Repaint-Risiko (§9.5) und eine Symbol-Mapping-Tabelle, die gepflegt
werden muss und auf unbekannten Symbolen still falsch liegt. Dem steht in den meisten
Skripten ein kleiner Nutzen gegenüber: Wo Volumen nur *bestätigt* (Wyckoff-Volumentest,
MFI-Score-Anteil), ist es kein eigenständiger Informationsträger — dafür lohnen sechs
Fehlerquellen nicht.

**Der Referenzmarkt lohnt genau dann, wenn er eine Dimension liefert, die das
Chart-Instrument überhaupt nicht hat:** Open Interest und ΔOI im Verhältnis zum Preis,
Terminstruktur / Front-Next-Spread / Contango, echtes Volumen als Regime-Kontext. Das ist
kein „besseres Volumen für den bestehenden Score", sondern eine eigene Informationsklasse
(D und E aus §1).

Und diese gehört in **ein einziges Kontext-Modul**, nicht verteilt auf zwanzig Skripte.

### 4.2 Vertrauensrangfolge

| Stufe | Quelle | Vertrauen |
|---|---|---|
| 1 | Chart-Preis (Klasse A) | hoch — immer verfügbar, keine Zusatzannahme |
| 2 | Referenzmarkt auf **Daily**, nur **Nicht-Preis-Daten** (OI, Volumen, Front/Next-Spread) | brauchbar — Latenz irrelevant, kein Settlement-Problem |
| 3 | Referenzmarkt intraday | schwach — Latenz, Session-Versatz und Settlement schlagen zusammen zu |
| 4 | alles aus CFD-Volumen abgeleitete | keins |

**Der entscheidende Punkt:** Die offene Settlement-/Back-Adjustment-Frage aus §9.1 betrifft
**nur den Preisvergleich** zwischen zwei Feeds. Liefert der Referenzmarkt ausschließlich OI,
Volumen und den Front/Next-Spread — und der Spread besteht aus zwei Legs desselben Feeds,
ist also intern konsistent — dann wird nie CFD-Preis gegen Future-Preis verglichen und die
Frage ist gegenstandslos. Stufe 2 ist deshalb nicht nur bequemer, sondern belastbarer.

### 4.3 Mapping

Nur für das Kontext-Modul aus §4.1 relevant. Prior Art:
[`vein_spread_context.pine`](indicators/trend_direction/vein/vein_spread_context.pine) —
mappt bereits CFD → Front/Next-Future, allerdings automatisch per `str.contains`. Das ist die
brüchige Variante: auf einem unbekannten Symbol greift keine Regel und das Modul liefert
stillschweigend nichts. Besser ein explizites `input.symbol()` mit sinnvollem Default und
einem sichtbaren „nicht konfiguriert"-Zustand.

| Chart-Instrument | Referenzpreis | Volumen / OI | Terminstruktur |
|---|---|---|---|
| NatGas CFD (`CAPITALCOM:NATURALGAS`) | `NYMEX:NG1!` | `NYMEX:NG1!` / `NYMEX:NG1!_OI` | `NG1!` vs. `NG2!` |
| WTI CFD | `NYMEX:CL1!` | `NYMEX:CL1!` / `_OI` | `CL1!` vs. `CL2!` |
| Brent CFD | `NYMEX:BZ1!` | `NYMEX:BZ1!` / `_OI` | `BZ1!` vs. `BZ2!` |
| Gold CFD / XAUUSD | `COMEX:GC1!` | `COMEX:GC1!` / `_OI` | `GC1!` vs. `GC2!` |
| Silber CFD / XAGUSD | `COMEX:SI1!` | `COMEX:SI1!` / `_OI` | `SI1!` vs. `SI2!` |
| Kupfer CFD | `COMEX:HG1!` | `COMEX:HG1!` / `_OI` | `HG1!` vs. `HG2!` |
| NAS100 CFD | `CME_MINI:NQ1!` | `NQ1!` / `_OI` | Roll-Quartale |
| SPX500 CFD | `CME_MINI:ES1!` | `ES1!` / `_OI` | Roll-Quartale |
| GER40 CFD | `EUREX:FDAX1!` | `FDAX1!` / `_OI` | Roll-Quartale |
| Aktien-CFD | Börsen-Underlying (`NASDAQ:AAPL`) | Underlying | – |
| EURUSD | Chart (kein zentraler Markt) | `CME:6E1!` als Proxy | `6E1!` vs. `6E2!` |
| Krypto-CFD | Referenzbörse (`BINANCE:BTCUSDT`) | Referenzbörse / `.P_OI` | Funding / Perp-Basis |

**Regeln für Cross-Symbol-Requests:**

1. `request.security()` **immer unbedingt** auf Top-Level aufrufen, nie in `if`/`for`.
2. `lookahead=barmerge.lookahead_off` — sonst Lookahead-Bias.
3. Referenzmarkt hat eigene Session/Feiertage: es gibt Bars, an denen der CFD läuft und
   der Future nicht. Ergebnis kann `na` sein → **jeder Konsument braucht einen na-Zweig**,
   und dieser Zweig muss neutral sein, nicht "0" (0 ist ein Wert, kein "unbekannt").
4. Nie rohe Preise vergleichen — nur normalisiert (⁴).
5. Der `1!`-Continuous-Kontrakt enthält Roll-Sprünge. Für Returns/Volatilität akzeptabel,
   für Level-Analyse nicht.
6. Jeder zusätzliche Request kostet Ladezeit und zählt gegen das Request-Limit (§9.4).
7. Symbolzuordnung explizit als Input, nicht automatisch per `str.contains` erraten. Ein
   nicht zugeordnetes Symbol muss sichtbar „nicht konfiguriert" sein, nicht still leer.

---

## 5. Verbotene Konstruktionen

Diese Muster sind unabhängig vom Instrument falsch benannt oder falsch begründet:

| Muster | Problem | Zulässige Form |
|---|---|---|
| `close > open ? volume : -volume` als "Delta" / "CVD" | Aggressor-Seite unbekannt | umbenennen in `signedVolumeProxy`, als Heuristik kennzeichnen |
| `volume × closePosition` als `buyVolume` | dito | `closeLocationWeightedVolume` |
| "hohes Volumen + Close nahe High = institutionelle Akkumulation" | Interpretation ohne Datengrundlage | Aussage streichen |
| Volumen-Gate ohne `volumetype`-Prüfung | feuert auf Tick-Volumen mit erfundener Semantik | Gate degradiert zu neutral, wenn kein echtes Volumen |
| `nz(volume)` als einziger "Guard" | macht fehlendes Volumen zu `0`, und `0 < sma(vol)` ist dann *immer* wahr → stiller Dauer-Block oder Dauer-Pass | explizit `hasRealVolume` prüfen und Feature abschalten |
| Volumen-Score in eine AND-Kette | auf CFD blockiert er alles, ohne dass es sichtbar wird | Score-Gewicht auf 0, Gewichte renormalisieren |
| VWAP auf CFD-Feed | Ergebnis ist ein Preis-Mittel gewichtet mit Preis-Updates | Referenzmarkt-VWAP oder Feature deaktivieren |
| Performance-/Qualitätsaussage aus Volumendaten unbekannter Herkunft | doppelter Fehler | siehe CLAUDE.md "No performance claims" |

**Die `nz(volume)`-Falle ist die häufigste im Repo.** `nz()` unterdrückt nur den `na`-Wert,
es stellt keine Datenvalidität her.

---

## 6. Data Contract

Jedes `.pine`-File deklariert im Header, welche Datenklassen es braucht. Block steht direkt
nach dem `Features:`-Block, vor dem abschließenden Separator:

```pine
// Data Contract:
//   Price:     REQUIRED   chart symbol
//   Volume:    OPTIONAL   real trade volume only — degrades to neutral
//   OI:        NO
//   Reference: NO
//   Verdict:   CFD-safe
```

Felder:

- `Price` — `REQUIRED` (immer)
- `Volume` — `NO` · `OPTIONAL` (degradiert) · `REQUIRED` (Skript ist ohne echtes Volumen sinnlos)
- `OI` — `NO` · `OPTIONAL` · `REQUIRED`
- `Reference` — `NO` · Symbolquelle, wenn Klasse B–E genutzt wird
- `Verdict` — eines von:
  - `CFD-safe` — läuft überall, keine Datenannahme jenseits Klasse A
  - `CFD-degraded` — läuft überall, Volumen-/OI-Anteil schaltet sich sichtbar ab
  - `Reference-required` — braucht Referenzmarkt, auf dem CFD allein nicht gültig
  - `Exchange-only` — nur auf Future/Aktie/Krypto-Börse sinnvoll

---

## 7. Laufzeit-Muster

### Volumen-Validität

```pine
// Echtes Handelsvolumen? tick/n/a zählt nicht.
bool volumeIsReal = (syminfo.volumetype == "base" or syminfo.volumetype == "quote")
                    and not na(volume)

// Feature-Gate: neutral, nicht 0
float volScore = volumeIsReal ? f_volScore() : na
bool  volGate  = volumeIsReal ? volume > ta.sma(volume, 20) : true   // pass-through
```

Bei gewichteten Scores das Gewicht **renormalisieren**, nicht nur den Beitrag nullen —
sonst sinkt der Gesamtscore systematisch auf CFDs.

### Sichtbarkeit

Ein degradiertes Feature muss im UI erkennbar sein. Im Dashboard-Table eine Zeile, sonst
ein einmaliges Label auf dem letzten Bar:

```pine
if barstate.islast and not volumeIsReal
    label.new(bar_index, high, "Volumen: " + syminfo.volumetype + " — Volumenmodul inaktiv",
              style=label.style_label_down, color=color.new(color.orange, 20),
              textcolor=color.white, size=size.small)
```

### Referenzmarkt

```pine
string refSym = input.symbol("NYMEX:NG1!", "Reference Market")
bool   useRef = input.bool(false, "Use Reference Market Volume")

[refVol, refClose] = request.security(refSym, timeframe.period, [volume, close],
                                      lookahead=barmerge.lookahead_off)

bool refValid = useRef and not na(refVol) and refVol > 0
float vol     = refValid ? refVol : volumeIsReal ? volume : na
```

`request.security()` steht unbedingt auf Top-Level; die Bedingung wirkt erst danach.

---

## 8. Entscheidungswege pro Skript

Es gibt keine globale Policy. Pro Skript eine der vier Entscheidungen:

| Entscheidung | Wann | Was passiert |
|---|---|---|
| **OK** | nutzt nur Klasse A | Data Contract ergänzen, sonst nichts |
| **Kennzeichnen** | Volumen ist Beiwerk, das Skript funktioniert ohne | `volumeIsReal`-Guard, Feature degradiert neutral, Sichtbarkeit im UI, Contract `CFD-degraded`, README-Hinweis |
| **Überarbeiten** | Volumen ist tragend (Score-Komponente, Gate, Signal-Bedingung) | Volumen-Anteil ausbauen und Gewichte renormalisieren. **Kein** Referenzmarkt-Input im Einzelindikator (§4.1) |
| **Umwidmen** | Skript ist nur mit echtem Volumen/OI sinnvoll (Volume Profile, CVD, Klinger) | Contract `Exchange-only`, README/CATALOG-Vermerk, im CFD-Kontext nicht verwenden |

Kriterium für "tragend": Entfernt man die Volumenkomponente und das Signal ändert sich —
tragend. Ändert sich nichts — Beiwerk.

---

## 9. Weitere Bedingungen

Datenklasse und Instrumenttyp (§1–§8) sind nicht die einzigen Bedingungen. Die folgenden
gelten zusätzlich und unabhängig davon — sie machen auch eine formal zulässige Datenquelle
unbrauchbar oder nicht reproduzierbar.

### 9.1 Unsichtbare Chart-Einstellungen

Das Skript sieht diese Einstellungen nicht, sie ändern aber die Serie, auf der es rechnet.
Zwei Nutzer mit demselben Skript auf demselben Symbol bekommen unterschiedliche Ergebnisse.

| Einstellung | Wirkung | Betroffen |
|---|---|---|
| **Back-Adjustment** (`B-ADJ`-Button) | Historische Kontraktpreise werden um Roll-Gaps korrigiert — Preisniveaus und damit alle Level/Fibs verschieben sich | Continuous Futures (`NG1!`) |
| **Settlement as close** (`SET`-Button) | Daily-Close ist Settlement-Preis statt letztem Trade. **Default: an** für Futures und Continuous. Intraday unverändert | Futures, Daily und höher |
| **Extended / Regular Session** | Andere Bars, andere Highs/Lows, anderer Tagesschluss | Aktien, teils Futures |
| **Adjustment** (Splits/Dividenden) | Historische Preise werden rückwirkend skaliert | Aktien |
| **Nicht-Standard-Charttypen** | Heikin Ashi, Renko, Kagi, P&F, Line Break liefern synthetische OHLC | alle |

**Konsequenzen:**

1. Level-basierte Logik (S/R, Fibonacci, Range-Grenzen) ist auf Continuous Futures nur
   innerhalb einer Back-Adjustment-Einstellung reproduzierbar. Im README vermerken, welche
   erwartet wird.
2. Daily-Close eines Futures ist per Default der **Settlement-Preis** — der weicht vom
   letzten Trade ab. Ein CFD-Daily-Close (Broker-Schluss) und ein Future-Daily-Close
   (Settlement) sind zwei verschiedene Größen. Cross-Market-Vergleiche auf `1D` sind
   dadurch systematisch versetzt, nicht zufällig verrauscht.
3. Ob `request.security()` auf ein Fremdsymbol dessen Settlement-/Back-Adjustment-Default
   übernimmt oder die Chart-Einstellung erbt, ist **empirisch zu prüfen** — nicht annehmen.
   Unter der Regel aus §4.2 (Referenzmarkt liefert nur Nicht-Preis-Daten) ist die Frage
   gegenstandslos; sie wird erst relevant, wenn doch einmal Preise zweier Feeds verglichen
   werden sollen.
4. Heikin Ashi und Renko sind für Backtests unbrauchbar: *"They can be useful to make visual
   assessments, but are unsuited to backtesting or automated trading, as orders execute on
   market prices — not Heikin-Ashi prices."* Renko/Kagi/P&F approximieren zusätzlich nur die
   Tick-Daten. Jede Strategie sollte den Charttyp prüfen und auf synthetischen Bars warnen —
   `chart.is_standard` ist `true` auf allen Typen mit nicht-synthetischem Close (Bars,
   Candles, Hollow Candles, Columns, Line, Area, Baseline); für gezielte Meldungen gibt es
   `chart.is_heikinashi`, `chart.is_renko`, `chart.is_linebreak`, `chart.is_kagi`,
   `chart.is_pnf`, `chart.is_range`.

### 9.2 Zeit & Session

- Futures nutzen meist die **elektronische Session (ETH) als „regular"** — `session.extended`
  ist dort äquivalent zu `session.regular`. Wer „nur RTH" meint, muss die Session explizit
  angeben.
- Extended-Session-Variablen sind nur intraday belegt; auf `1D` und höher immer `false`.
- Bar-Alignment bei Cross-Symbol-Requests: CFD 24/5, Future mit Session-Pausen und
  Wartungsfenster, Krypto 24/7. Es gibt Bars ohne Gegenstück — `na` ist der Normalfall,
  nicht der Ausnahmefall.
- Feiertage und halbe Handelstage unterscheiden sich zwischen Broker und Börse.
- `syminfo.timezone` ist die Börsenzeitzone, nicht die des Charts. Tagesgrenzen für
  Session-/Saisonalitätslogik daraus ableiten, nicht aus der Anzeigezeit.

### 9.3 Datenlatenz und Verfügbarkeit

- **CME-Gruppe (NYMEX/COMEX/CBOT) ist ohne kostenpflichtiges Datenpaket ~10 Minuten
  verzögert.** Für die Referenzmarkt-Strategie aus §4 heißt das: auf `1H`/`4H` hinkt der
  Referenzwert im Realtime hinterher, Alerts feuern auf verzögerten Daten. Auf `1D`
  vernachlässigbar, intraday nicht.
- Historientiefe hängt am Plan (5.000 bis 40.000 Bars). Ein Referenzsymbol mit kürzerer
  Historie verkürzt jede daraus abgeleitete Statistik.
- `request.footprint()` erfordert Premium/Ultimate **und** einen Feed mit Footprint-Daten.
  Ein Skript, das darauf baut, ist für einen Teil der Nutzer funktionslos.

### 9.4 Harte Pine-Limits

Diese begrenzen, wie viel Referenzmarkt-Logik überhaupt in ein Skript passt:

| Limit | Wert |
|---|---|
| Unique `request.*`-Calls | **40** (64 mit Ultimate) |
| Historie abgeleiteter Serien | 5.000 Bars (eingebaute: 10.000) |
| Labels / Lines / Boxes | je 500 · Polylines 100 · Tabellen 9 |
| Plots | 64 |
| Kompilierte Tokens | 100.256 |
| Loop-Zeit | 500 ms pro Bar · Gesamtlaufzeit 20 s (Basic) / 40 s |
| Collection-Elemente | 100.000 |

Praktische Folge im Repo: `edge_atlas` hat bereits 29 `request.security`-Aufrufe. Dort ist
für zusätzliche Referenzmarkt-Requests kaum Budget — die Entscheidung „Referenzmarkt statt
Degradation" ist nicht überall frei.

### 9.5 Repainting und Realtime

Reproduzierbarkeit ist eine Datenbedingung wie jede andere. Quellen laut Pine-Doku:

- fluide Realtime-Werte (`high`/`low`/`close` der offenen Bar)
- `request.security()` liefert im Realtime unbestätigte Werte
- `varip`, `barstate.isnew`, `timenow`
- `calc_on_every_tick` in Strategien
- Zeichnen in die Vergangenheit (Signal wird rückwirkend versetzt)
- **Datenfeed-Revisionen** — Splits und Anpassungen ändern bereits abgeschlossene Bars

### 9.6 Kosten- und Instrumentmechanik (Strategie-Ebene)

Ein Backtest ist nur so gültig wie sein Kostenmodell. Für das Referenzinstrument des Repos:

- Capital.com berechnet auf Spot-Commodity-CFDs neben einer Admin-Gebühr (0,01096 % täglich)
  eine **Daily Premium Adjustment** — sie bildet die tägliche Bewegung vom Front-Month- zum
  Folgekontrakt ab. Sie ist keine Gebühr, sondern die Roll-Komponente der Futures-Kurve,
  und kann Gutschrift oder Belastung sein.
- Seit 13.03.2026 trägt bei Commodities der Freitag die Anpassung für alle drei
  Wochenendtage.
- Damit gilt: Ein Mehrtages-Hold auf dem NatGas-CFD hat eine tägliche P&L-Komponente, die im
  Chartpreis **nicht** enthalten ist. Ein Backtest mit nur `commission_value=0.02` bildet sie
  nicht ab. Bei steilem Contango ist das kein Rundungsfehler.
- Der Spread ist broker- und tageszeitabhängig, kein Marktzustand (§3).
- Futures: `syminfo.pointvalue` als Kontraktmultiplikator, Tick-Wert und Roll-Termine gehören
  ins Sizing. `1!` ist nur bei CME/EUREX handelbar, `2!` gar nicht — reines Analyse-Instrument.

### 9.7 Fremddaten

- `request.financial()` — FactSet, nur für Symbole mit Fundamentaldaten; Reporting-Lag und
  nachträgliche Restatements ändern historische Werte.
- `request.economic()` — Wirtschaftsdaten werden revidiert; der Wert zum Zeitpunkt der
  Veröffentlichung ist nicht der Wert, den ein späterer Abruf liefert.

### 9.8 Checkliste

Vor jedem Indikator/Strategie-Review zusätzlich zur Datenklassen-Prüfung:

- [ ] Hängt das Ergebnis an einer Chart-Einstellung, die das Skript nicht sieht? (9.1)
- [ ] Ist die Session-Annahme explizit oder geerbt? (9.2)
- [ ] Wird ein verzögerter Feed als Referenz benutzt? (9.3)
- [ ] Reicht das `request.*`-Budget noch? (9.4)
- [ ] Ist das Signal auf historischen und Realtime-Bars identisch? (9.5)
- [ ] Bildet das Kostenmodell die Instrumentmechanik ab? (9.6)
- [ ] Werden Fremddaten als revisionsfrei behandelt? (9.7)

## 10. Quellen

- [TradingView — The Volume indicator on my chart looks odd or displays zero (or n/a) values](https://www.tradingview.com/support/solutions/43000481397-the-volume-indicator-on-my-chart-looks-odd-or-displays-zero-or-n-a-values/)
- [Pine Script Docs — Chart information (`syminfo.volumetype`, `syminfo.type`)](https://www.tradingview.com/pine-script-docs/concepts/chart-information/)
- [Pine Script Docs — Other timeframes and data (`request.security`, `_OI`, `request.financial`)](https://www.tradingview.com/pine-script-docs/concepts/other-timeframes-and-data/)
- [TradingView Blog — Volume footprints are now available in Pine scripts](https://www.tradingview.com/blog/en/volume-footprints-in-pine-scripts-56908/)
- [TradingView — Volume profile indicators: basic concepts](https://www.tradingview.com/support/solutions/43000502040-volume-profile-indicators-basic-concepts/)
- [TradingView — Can I switch Settlement and Last prices as close for futures?](https://www.tradingview.com/support/solutions/43000685268-can-i-switch-settlement-and-last-prices-as-close-for-futures/)
- [TradingView — What are 1! and 2! continuous futures contracts?](https://www.tradingview.com/support/solutions/43000483493-what-are-1-and-2-continuous-futures-contracts/)
- [Pine Script Docs — Non-standard charts data (`ticker.heikinashi` u.a.)](https://www.tradingview.com/pine-script-docs/concepts/non-standard-charts-data/)
- [Pine Script Docs — Repainting](https://www.tradingview.com/pine-script-docs/concepts/repainting/)
- [Pine Script Docs — Limitations](https://www.tradingview.com/pine-script-docs/writing/limitations/)
- [Pine Script Docs — Sessions](https://www.tradingview.com/pine-script-docs/concepts/sessions/)
- [TradingView — How to purchase additional market data (CME-Verzögerung)](https://www.tradingview.com/support/solutions/43000471705-how-to-purchase-additional-market-data/)
- [Capital.com — Understanding overnight fees and adjustments on spot commodities (Natural Gas)](https://help.capital.com/hc/en-us/articles/13643723322770-Understanding-overnight-fees-and-adjustments-on-spot-commodities-Natural-Gas)
