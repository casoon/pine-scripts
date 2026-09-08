---
name: indicator-code-audit
description: >-
  Code-QA-Regelwerk für einzelne Pine-Indikatoren: technische Bugs (Repainting,
  Lookahead, request.security, Performance/Speicher, var-/Serien-Fallen), Konzeptprüfung
  (behauptet Kommentar/README etwas anderes, als der Code tatsächlich berechnet),
  Logikfehler (tote Variablen, unbegrenzte Scores, ungenutzte Parameter) sowie
  Paket-/Doku-Struktur-Konformität nach CLAUDE.md (Verzeichnisstruktur, README/
  CHANGELOG/DESCRIPTION_TV.bbcode, .pine-Header-Format inkl. Trennzeilen und
  Data-Contract-Platzierung, CATALOG.md-/root-README-Eintrag, Dashboard-Tabellenstil,
  Performance-Claims-Guard, Standalone- vs. generierte Strategie-Zuordnung). Benutzen
  bei "Code-Review", "QA", "auditiere diesen Indikator", "prüfe den Code auf Bugs",
  "macht der Code was der Kommentar behauptet", "finde Auffälligkeiten in diesem
  Pine-Skript", "folgt der Header dem Vorgabeformat", "fehlt der CATALOG-Eintrag",
  "ist die README-/CHANGELOG-Struktur vollständig", "ist das eine standalone
  Strategie". Output ist immer eine Fundliste ("N Auffälligkeiten"), nie ein
  Gesamturteil ("der Indikator ist gut"). Nicht für Trading-Logik-Diagnose (Rollen-
  Architektur, Gate-Wirkung, verpasste Pivots/Signale) — dafür indicator-review;
  nicht für Neu-/Umbau der Signal-Logik — dafür indicator-design.
---

# Indicator Code Audit — Pine-Code-QA

Rolle: QA-Engineer, nicht Gutachter. Ergebnis ist immer eine **Fundliste**
("17 Auffälligkeiten gefunden"), niemals ein Urteil ("der Indikator ist gut"). Die
Objektivität kommt aus der Liste, nicht aus einer Note. Wenn ein Abschnitt sauber ist,
wird das nicht lobend erwähnt — nur Auffälligkeiten zählen.

## 0. Abgrenzung — welcher Skill für welche Frage

| Frage | Skill |
|---|---|
| Ist der Pine-Code technisch korrekt (Repainting, Performance, Bugs)? | **dieser Skill** |
| Behauptet der Kommentar/README etwas, das der Code nicht tut? | **dieser Skill** |
| Gibt es tote Variablen, unbegrenzte Werte, ungenutzte Inputs? | **dieser Skill** |
| Ist die Trading-Logik/Architektur sauber (Rollen, Gates, AND-Ketten)? | `indicator-review` |
| Warum wurde ein Pivot/Signal verpasst? | `indicator-review` |
| Wie sollte die Signal-/Score-Logik neu gebaut werden? | `indicator-design` |
| Trägt die Datenquelle auf diesem Instrument überhaupt eine Aussage (Volumen/VWAP/OI/Orderflow)? | `instrument-data-validity` |
| Folgt das Verzeichnis der vorgeschriebenen Datei-/Doku-Struktur (README/CHANGELOG/DESCRIPTION_TV/Header/CATALOG)? | **dieser Skill** |

Dieser Skill prüft die **Code- und Konzept-Ebene**, unabhängig davon, ob die
zugrundeliegende Trading-Idee gut ist. Ein Indikator kann hier sauber durchgehen und
trotzdem in `indicator-review` an der Architektur scheitern — beide Ebenen sind
getrennt zu bewerten, nicht vermischen.

## 1. Code-Audit — technische Fehlerklassen

Jede Kategorie einzeln durchgehen, nicht nur "wirkt beim Überfliegen ok":

| Kategorie | Worauf prüfen |
|---|---|
| **Repainting/Lookahead** | `request.security` mit `barmerge.lookahead_on` **ohne** `[1]`-Offset auf dem Expression-Argument (liest die laufende, unbestätigte HTF-Bar) — das ist der eigentliche Alarmfall, nicht das bloße Fehlen von `lookahead_off`. Beide dokumentierten TradingView-Muster gegen Repainting sind zulässig: `expression` mit `lookahead_off` ohne Offset, **oder** `expression[1]` mit `lookahead_on` (Offset gleicht das Lookahead aus) — Letzteres nicht fälschlich als Bug markieren. Zusätzlich prüfen: Zugriff auf `close`/High-TF-Werte außerhalb dieser beiden Muster; Signale, die sich nach `barstate.isconfirmed` noch ändern können |
| **request.security** | Fehlendes `gaps=barmerge.gaps_off`-Verständnis (Repaint-Risiko bei Gaps-On ohne Grund); wiederholte identische Calls statt einmal cachen |
| **Performance/Speicher** | `for`-Loops mit unnötig hoher `array.size()`-Iteration pro Bar; `label.new`/`line.new` ohne `max_labels_count`/`max_lines_count`-Bewusstsein oder ohne alte Objekte zu löschen; Tabellen-Neuerzeugung in `barstate.islast` ohne `na()`-Guard (Ressourcen-Leak, siehe Memory `reference_pine_v6_pitfalls`) |
| **var-Verwendung** | `var`-Variable, die eigentlich pro Bar neu berechnet werden sollte (bleibt sonst "eingefroren"); nicht-`var`-Akkumulator, der pro Bar zurückgesetzt wird obwohl State über Bars nötig wäre |
| **Off-by-one** | `[1]` vs. `[0]` bei Pivot-/Cross-Bestätigung; `ta.barssince()`-Vergleiche mit falschem Bar-Offset; Array-Indizierung bei `array.size()-1` ohne Empty-Guard |
| **Barstate-Fehler** | Logik, die auf `barstate.isrealtime` unterschiedlich läuft als auf historischen Bars, ohne dass das beabsichtigt ist; Alerts/Labels die auf jedem Realtime-Tick statt nur bei Bestätigung feuern |
| **Session-Probleme** | `session.ismarket`/Zeitzone-Annahmen, die auf dem Symbol/TF des Charts nicht gelten; ungetestete Verhalten auf 24h-Märkten (Crypto, CFD) vs. Session-Märkten (Aktien) |
| **UDT/Serien-Fallen** | In-Place-Mutation von UDT-Feldern statt echter historischer Serie (`obj[1].field` liefert wegen Referenzsemantik den aktuellen, nicht den historischen Wert) |
| **na-Propagation** | Division ohne Neutral-Fallback bei Feeds ohne verwertbares Volumen (`volume` 0 oder `na`) oder frühen Bars vor Warmup — ein einzelner `na`-Wert darf nicht das gesamte Ergebnis auf `na` ziehen |
| **Datenherkunft** | `volume`/`ta.vwap`/`ta.obv`/`ta.mfi`/`ta.vwma` ohne `syminfo.volumetype`-Guard; `nz(volume)` als vermeintlicher Guard (macht fehlendes Volumen zu `0` → Gate blockiert oder passiert still dauerhaft); stille Degradation ohne UI-Hinweis; Cross-Symbol-`request.security` ohne `na`-Zweig. Bewertung nach Skill `instrument-data-validity` + `DATA_VALIDITY.md` |

Bekannte, laufend gepflegte Pine-v6-Syntaxfallen (kein Duplikat hier — Quelle bleibt
aktuell): Memory `reference_pine_v6_pitfalls` und Skill `pine-script-v6-language` vor
dem Audit konsultieren, besonders bei ungewöhnlichen Compile-Fehlern.

## 2. Konzeptprüfung — Kommentar/Doku vs. Code-Realität

Frage: **Was behauptet der Code zu messen — und tut er das wirklich?**

Vorgehen:
1. Behauptung sammeln: Docstring-Kommentar über der Variable/Funktion, `## Features`-
   Bullet im README, Input-Tooltip, Plot-Titel.
2. Zur tatsächlichen Formel zurückverfolgen.
3. Prüfen, ob die Formel die Behauptung trägt — nicht nur plausibel klingt.

Beispiel für einen validen Fund:

> Kommentar: "Misst Trendstärke."
> Code: `strength = close > ema ? 1 : 0`
> Befund: Das misst nur die *Position relativ zum EMA* (binär), keine *Stärke*
> (keine Steigung, keine Distanz, keine Dauer). Die Behauptung "Stärke" ist durch die
> Formel nicht gedeckt.

Weitere typische Mismatch-Muster:
- Name/Kommentar verspricht eine Rate/Geschwindigkeit, Formel liefert nur einen
  Snapshot-Wert ohne Zeitbezug.
- "Normalisiert auf 0–100" behauptet, aber die Formel hat keine Clamp/Rescale-Stufe.
- "Gewichtet nach Volumen" behauptet, aber Volumen fließt nirgends in die Formel ein.
- Parameter-Tooltip beschreibt einen Effekt, den die Formel mit diesem Parameter gar
  nicht erzeugen kann (z. B. Tooltip verspricht Glättung, Parameter steuert aber nur
  die Farbe).

## 3. Logikfehler — unabhängig vom Trading-Konzept

- **Tote Variablen/Berechnungen**: berechnet, aber nie geplottet, nie in einen Score
  eingespeist, nie in einer Bedingung gelesen.
- **Ungenutzte Inputs**: `input.*` deklariert, aber die Variable taucht in keiner
  Formel wieder auf.
- **Unbegrenzte Normalisierung**: ein Wert wird als "normalisiert"/"Score 0–100"
  behandelt (z. B. in Farbskala, Schwellenvergleich), aber es fehlt die
  `math.min`/`math.max`/Clamp-Stufe, die das tatsächlich garantiert.
- **Unreachable/immer-wahr Branches**: `if`-Bedingung, die durch eine vorherige
  Bedingung im selben Scope bereits ausgeschlossen oder garantiert ist.
- **Doppelte Berechnung derselben Serie**: identischer `ta.*`-Ausdruck mehrfach mit
  denselben Parametern aufgerufen statt einmal berechnet und wiederverwendet.
- **Fehlende EMA/Input-Nutzung in einem Vergleich**: z. B. drei EMAs (50/100/200)
  deklariert, aber der Bullisch/Bärisch-Vergleich nutzt nur zwei davon — die dritte
  ist entweder tot (siehe oben) oder der Vergleich ist unvollständig.

## 4. Paket-/Doku-Struktur-Audit — Konformität zu CLAUDE.md

Frage: **Ist die Datei- und Doku-Struktur dieses Indikator-Verzeichnisses vollständig und
formal korrekt** — unabhängig davon, ob Code oder Trading-Logik stimmen. Die exakte
Spezifikation steht in `CLAUDE.md` (Repo-Root); dort nachlesen statt aus dem Gedächtnis zu
urteilen — Details wie Separator-Länge, erlaubte BBCode-Tags oder Farbwerte ändern sich dort,
nicht hier.

### 4.1 Verzeichnis & Pflichtdateien
- [ ] Liegt der Indikator unter `indicators/<category>/<name>/` mit einer der neun erlaubten Kategorien?
- [ ] `README.md` vorhanden, Struktur: Title → TradingView-Link (falls publiziert) → Beschreibung → `## Features` → weitere Abschnitte
- [ ] `CHANGELOG.md` vorhanden, Format `## vX.Y.Z — YYYY-MM-DD` mit Bullet-Liste
- [ ] `DESCRIPTION_TV.bbcode` vorhanden, wenn das Skript zur TV-Publikation gedacht ist; nur erlaubte BBCode-Tags (CLAUDE.md-Tabelle), Disclaimer-Absatz am Ende
- [ ] `screenshots/` (optional) folgt Namenskonvention `<indicatorname>_<context>_<optional-version>.png`

### 4.2 `.pine`-Header
- [ ] `//@version=6` ist die erste Zeile; Kommentarblock kommt vor `indicator()`/`strategy()`
- [ ] Trennzeilen exakt `// ` + 76 `=` (79 Zeichen), je einmal vor/nach Version-Block und einmal nach `Features:`
- [ ] Skriptname endet auf `[WavesUnchained]` (Kommentar UND `indicator()`-Titel), niemals mit „Waves" davor
- [ ] `Version:` / `Author: WavesUnchained` / `Build: YYYY-MM-DD[ HH:MM:SS]` in genau dieser Reihenfolge; Build-Datum nur bei tatsächlicher Änderung hochgezogen
- [ ] Beschreibung direkt nach der oberen Trennzeile, keine Leerzeile davor
- [ ] `// Features:` wörtlich als Heading, Bullets mit `✓`; genau eine leere `//`-Zeile davor und eine danach
- [ ] `Data Contract`-Block direkt nach `Features:`, vor der schließenden Trennzeile, mit gültigem `Verdict` (`CFD-safe`/`CFD-degraded`/`Reference-required`/`Exchange-only`) — Inhalt sachlich gegen `instrument-data-validity` prüfen, nicht nur Vorhandensein
- [ ] Keine `@description`/`@author`/`@version`-JSDoc-Tags

### 4.3 Repo-weite Registrierung
- [ ] Eintrag in root `README.md` (passende Sektion, ein Einzeiler)
- [ ] Eintrag in `CATALOG.md` mit Status/Qualitäts-Bewertung
- [ ] Bei Alerts: Kürzel in `indicators/ALERT_KUERZEL.md` registriert (Detail: `indicator-alerts`)

### 4.4 Dashboard-Tabellen-Stil (falls der Indikator ein Dashboard zeichnet)
- [ ] `table.new(...)` mit den vorgeschriebenen Farbkonstanten (CLAUDE.md „Dashboard table style"), kein Dark-Theme-Hintergrund
- [ ] Header-/Daten-/Status-/Separatorzeilen nutzen die vorgeschriebene `text_color`/`bgcolor`/`text_size`-Kombination — Referenz bei Zweifel: `indicators/trend_direction/vein/vein_trend.pine`
- [ ] Kein `size.tiny` für persistente Dashboard-/Tabellentexte

### 4.5 Performance-Claims-Guard
- [ ] Keine Backtest-Zahlen/Qualitäts-Superlative in `README.md`, `DESCRIPTION_TV.bbcode`, `CHANGELOG.md`, Input-Tooltips, `indicator()`/`strategy()`-Titel, Chart-Labels, Dashboard-Zellen oder Alert-Messages (CLAUDE.md „No performance claims in user-facing text")

### 4.6 Strategy-Infrastruktur (nur falls `@strategy-config`-Block oder zugehörige Strategie existiert)
- [ ] Bei vorhandenem `@strategy-config`-Block: ist die generierte Strategie unter `strategies/` aktuell (kein manueller Drift ggü. `build_strategies.py`-Output)?
- [ ] Ohne `@strategy-config`-Block, aber mit zugehöriger Strategie in `strategies/`: diese ist **standalone** und darf nie durch `build_strategies.py` überschrieben werden, auch nicht bei „rebuild all" — ohne explizite Rückfrage beim User

## 5. Ablauf

1. Vollständige `.pine`-Datei(en) lesen (nicht nur einen Ausschnitt) — bei mehreren
   Dateien im Indikator-Verzeichnis (z. B. Suite mit mehreren Modulen) jede einzeln.
2. Modul 1 (Code-Audit) durchgehen.
3. Modul 2 (Konzeptprüfung): Behauptungen aus README.md und Inline-Kommentaren gegen
   die Formeln abgleichen.
4. Modul 3 (Logikfehler) durchgehen.
5. Modul 4 (Paket-/Doku-Struktur-Audit) durchgehen — bei eigenständig katalogisierten
   Indikatoren; bei einem Sub-Modul einer Suite ohne eigenes README auf die
   Suite-Ebene beziehen.
6. Ergebnis als Fundliste ausgeben — jeder Fund mit Datei:Zeile, kurzer Behauptung
   ("was ist kaputt") und konkretem Szenario ("bei welchem Input/Zustand zeigt sich
   das"). Kein zusammenfassendes Qualitätsurteil am Ende, nur die Zahl der Funde.

Wenn im aktuellen Kontext das `ReportFindings`-Tool verfügbar ist, den Audit-Output
darüber ausgeben (ein Eintrag pro Fund, schwerwiegendste zuerst) statt als Freitext-
Liste — das erzwingt genau das geforderte Format (Fund statt Fazit) strukturell.
