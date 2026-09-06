---
name: pine-script-v6-language
description: Pine-Script-v6-Sprachfeature- und Syntax-Referenz aus den offiziellen TradingView Release Notes (2022–2026) — was sich gegenüber älterem (v5-geprägtem) Trainingswissen geändert hat: bool/na, Kurzschluss-Auswertung, negative Array-Indizes, dynamische for-Loop-Grenzen, Zeilenumbruch-Regeln, Mehrzeilen-Strings, UDT-Sortierung, neue request.*/ta.*/str.*-Funktionen, Strategy-Deklaration (calc_on_every_history_tick, Leverage statt Margin, Bar detalization statt Bar Magnifier). Nutzen beim Schreiben oder Review von Pine-Script-Code, bei CE-Compile-Fehlern durch veraltete v5-Annahmen, oder wenn unklar ist ob ein Feature/eine Funktion in der aktuellen Version existiert. Nicht für indikatorspezifisches Design oder Gate-/Score-Logik (siehe die projekteigenen indicator-design/indicator-review-Skills bzw. trading-signal-filter-design) — reine Sprachmechanik.
---

# Pine Script v6 — Sprachreferenz

## Gotchas — Trainingswissen vs. v6-Realität

- `bool` ist in v6 nie mehr `na` — immer strikt `true`/`false`. `or`/`and` werten kurzschlussartig aus (zweiter Operand wird nicht ausgewertet, wenn das Ergebnis schon feststeht).
- `array.get/set/insert/remove` akzeptieren negative Indizes (von hinten zählen, `-1` = letztes Element).
- `for`-Schleifen werten `to_num` **vor jeder Iteration neu aus** (seit März 2025) — ändert sich der Ausdruck während der Schleife, ändert sich auch die Endgrenze. Vorher war die Grenze beim Loop-Start einmalig fixiert.
- Das Scope-Limit (früher max. 550 Scopes insgesamt) ist entfernt (Feb 2025) — beliebig viele lokale Scopes durch UDTs/Loops/Funktionen/Bedingungen erlaubt.
- Zeilenumbruch-Einrückung: **innerhalb von Klammern** ist seit Dez 2025 jede Einrückung erlaubt, auch Vielfache von 4 Leerzeichen. **Ohne** umschließende Klammern gilt weiter die alte Regel: Folgezeilen dürfen NICHT um ein Vielfaches von 4 einrücken, sonst Kompilierfehler. Der Editor fügt seit Juli 2026 beim manuellen Zeilenumbruch (Enter mitten im Ausdruck) automatisch die umschließenden Klammern ein.
- Strings: max. 40.960 Zeichen (nicht mehr 4096, seit Aug 2025). Mehrzeilige Strings via `"""..."""` bzw. `'''...'''` (seit April 2026) — Zeilenumbrüche sind automatisch enthalten, kein `\n`-Escape nötig; Einrückung im Code wird wörtlich Teil des Strings, unabhängig vom umschließenden Block.
- `array.sort()`/`array.sort_indices()`/`matrix.sort()` können seit April 2026 UDT-Objekt-Collections direkt sortieren via neuen `sort_field`-Parameter (Feldindex als const int oder Feldname als const string). Seit Aug 2026 unterstützen auch `array.binary_search()`/`array.binary_search_leftmost()`/`array.binary_search_rightmost()` denselben `sort_field`-Parameter für UDT-Arrays — Array muss aufsteigend nach genau diesem Feld sortiert sein, sonst falsches Ergebnis.
- `time()`/`time_close()` haben zusätzlich zu `bars_back` (Offset auf dem Hauptzeitrahmen) seit Okt 2025 `timeframe_bars_back` (Offset auf dem per `timeframe`-Argument angegebenen Zeitrahmen). Bei beiden Argumenten gleichzeitig: erst `bars_back` auflösen, dann `timeframe_bars_back` relativ dazu.
- `strategy.exit()` mit gleichzeitig gesetztem `limit`/`profit` (bzw. `stop`/`loss`) bevorzugt seit Dez 2024 nicht mehr automatisch den absoluten Parameter — es wählt das Preislevel, das der Markt erwartungsgemäß zuerst erreicht.
- "Margin for long/short positions" in der Properties-Tab ist durch "Long/Short leverage"-Inputs ersetzt (Juli 2026) — `margin_long`/`margin_short` bleiben als `strategy()`-Parameter für Rückwärtskompatibilität bestehen und werden intern in Leverage-Werte umgerechnet.
- "Bar Magnifier" (Checkbox) heißt jetzt "Bar detalization" (Dropdown-Menü, Juli 2026); `use_bar_magnifier` bleibt der Parameter für den Default-Wert.
- Strategien stoppen seit v6 nicht mehr bei 9000 Trades — älteste Orders werden verworfen, um Platz zu schaffen (nicht in der Trade-Liste sichtbar, Simulation bleibt aber korrekt). `strategy.closedtrades.first_index` liefert den Index des ältesten noch vorhandenen Trades.

## Neue Sprachfeatures (chronologisch relevant)

- **Objects/UDTs** (`type`-Keyword, Dez 2022), **Methods** (`method`-Keyword, Feb 2023), **Maps** (Aug 2023), **Polylines** (Okt 2023), **Enums** (`input.enum()`, Juni 2024) — bei einem Redesign prüfen, ob diese Typen Parallel-Arrays/Konstanten-Listen ersetzen können.
- **`once`-Struktur** (Aug 2026): Neues Keyword für eine bedingte Struktur, deren Block genau einmal ausgeführt wird — beim ersten `true` der Bedingung auf einer geschlossenen Bar. Danach feuert der Block nie wieder, unabhängig vom weiteren Bedingungsverlauf. Nützlich für einmalige Init-/Setup-Logik ohne manuelles `var`-Flag-Tracking.
- **Footprint-Daten**: `request.footprint()` plus `footprint`- und `volume_row`-Typen (Jan 2026, nur Premium/Ultimate) für Orderflow-/Volumen-Row-Analyse pro Bar.
- **Library-Konstanten**: `export const` für `int`/`float`/`bool`/`color`/`string` (Juni 2025).
- **`calc_on_every_history_tick`** (Juli 2026, Premium/Ultimate, Standardcharts): Script führt pro historischem Tick statt nur pro Bar-Close aus — feinere Order-Fills, geringeres Lookahead-Bias-Risiko in Backtests.
- **`request.currency_rate()`** (März 2023) für Tageskurs-Konvertierung zwischen zwei Währungen.
- **`str.repeat()`, `str.trim()`** (Feb 2024), **`str.format_time()`** (Okt 2022) für String-Handling ohne Zusatzlogik.
- **`ta.min()`/`ta.max()`** (Aug 2022): All-Time-Low/High seit Chart-Beginn, ohne eigene `var`-Tracking-Variable.
- **`display=`-Feinsteuerung** (`display.data_window`, `.pane`, `.price_scale`, `.status_line`, kombinierbar mit +/-, seit Juli 2022) statt nur `display.all`/`display.none`.
- **`active=`-Parameter** bei allen `input.*()`-Funktionen (Juli 2025): Input grau/nicht editierbar abhängig vom Wert eines anderen Inputs — nützlich für conditional Settings-Gruppen (z. B. Glättung an/aus schaltet abhängige Inputs).
- **`format`/`precision`** als Override pro `plot*()`-Call (Dez 2023), unabhängig vom globalen `indicator()`/`strategy()`-Default.
- **Strategy-Report-Felder**: `strategy.avg_trade[_percent]`, `avg_winning_trade[_percent]`, `avg_losing_trade[_percent]` (Mai 2024); `*_percent`-Varianten für grossprofit/grossloss/netprofit/max_runup/max_drawdown sowie pro Closed-/Open-Trade (Nov 2023).

## Wann hier nachschlagen statt aus Training raten

- CE-Fehler bei Zeilenumbrüchen mitten in einem Ausdruck ohne umschließende Klammern.
- Unerwartetes `na`-Verhalten bei `bool`-Variablen oder Verwunderung über fehlende Kurzschluss-Auswertung.
- Frage "gibt es dafür schon eine eingebaute Funktion" bei String-, Zeit-, Sortier- oder Footprint-Logik.
- Strategy-Tester-/Properties-Settings, die im UI anders heißen als erwartet (Margin, Bar Magnifier, Limit-Order-Assumption, Fill-orders-on-standard-OHLC).
