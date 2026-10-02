---
name: strategy-from-indicator
description: >-
  Bauanleitung für eine TradingView-Strategie aus einem bestehenden Pine-Indikator dieses
  Repos — Standard-Input-Gruppen (Trade Direction, Confirmed Bar, Cooldown, Break-Even,
  Filter), die fünf Exit-Muster (trailing, trailing_ratchet, fixed, fixed+TP-Level,
  directional_fixed_tp, pivot_atr), die Transformation `indicator()` → `strategy()` und
  der Charttyp-Guard. Benutzen, sobald aus einem Indikator eine Strategie werden soll, eine
  bestehende Strategie an eine geänderte Indikator-Logik nachgezogen wird, ein
  `@strategy-config`-Block gelesen oder geschrieben wird, oder gefragt wird "wie mache ich
  daraus eine Strategie / einen Backtest". Triggert auch bei: "strategy.entry",
  "strategy.exit", "Trailing Stop bauen", "Break-Even-Stop", "Cooldown nach Exit",
  "Kommission für den Backtest", "warum repaintet meine Strategie", "Strategie neu
  generieren". Nicht für die Bewertung von Backtest-Ergebnissen (→ trading-signal-filter-design)
  und nicht für die Signal-Logik selbst (→ indicator-design).
---

# Strategie aus Indikator bauen

Bis 2026-09 erzeugte `scripts/build_strategies.py` diese Dateien mechanisch. Das Skript ist
entfernt; **alle Strategien unter `strategies/` sind ab jetzt standalone und handgepflegt.**
Dieser Skill trägt das Wissen, das im Generator steckte.

## Gotchas — was beim Umbau schiefgeht

- **`alertcondition()` ist in einem `strategy()`-Skript ein Compile-Fehler.** Alle Aufrufe
  restlos entfernen, nicht auskommentieren. Das ist der häufigste Fehler beim Umbau.
- **`max_bars_back` aus dem `indicator()`-Call nicht mit übernehmen** — die Strategie setzt
  ihren eigenen Wert (`max_bars_back=500`). Ein doppelter Parameter ist ein Compile-Fehler.
- **Break-Even als *zweiter* `strategy.exit()`-Aufruf erzeugt ein Exit-Race.** Zwei Exits auf
  dieselbe Position konkurrieren; welcher zuerst greift, ist nicht deterministisch. Break-Even
  gehört als `math.max`/`math.min` in **denselben** Stop-Level (Muster unten).
- **Ohne `barstate.isconfirmed`-Gate repaintet jede Strategie im Livebetrieb.** Der
  `confirmClose`-Input gehört in jede Strategie, Default `true`.
- **Nicht-Standard-Charttypen verfälschen den Backtest.** Heikin Ashi, Renko, Kagi, Line Break,
  P&F und Range füllen Orders zu synthetischen Preisen — der Test sieht großartig aus und ist
  wertlos. Jede Strategie braucht den Charttyp-Guard (unten).
- **Ein Signal-Ausdruck aus mehreren Quellen wird ge-`or`-t, nicht ge-`and`-et.**
  `long: sig1, sig2` bedeutet `(sig1 or sig2)` — die Klammern sind Pflicht, sonst bindet
  `and _canLong` falsch.
- **Trailing-Ratchet ist nicht automatisch besser.** Ein nur-enger-werdender Stop wurde auf
  NatGas getestet und war dort schlechter als die Per-Bar-Hülle, weil Retracements die
  nachgezogenen Stops abgreifen. Instrumentabhängig — nicht als Default setzen.

## Ablauf

1. Indikator-Datei vollständig nach `strategies/<name>/<name>_strategy.pine` kopieren.
2. `indicator(...)` durch den `strategy(...)`-Call ersetzen (unten).
3. Alle `alertcondition()`-Aufrufe entfernen. `plot()`, `barcolor()`, Labels und Linien
   **bleiben** — sie sind die visuelle Kontrolle über die Trades.
4. Kopfzeile im Header auf `<Name> [WavesUnchained] — Strategy (standalone)` setzen.
5. Charttyp-Guard einfügen.
6. Standard-Input-Block anhängen.
7. Exit-Muster wählen und anhängen.
8. `@strategy-config` im **Indikator** pflegen (siehe unten) — es dokumentiert, welche
   Variablen die Entry-Signale sind, damit die Strategie später nachgezogen werden kann.

## `strategy()`-Call

`title` des Indikators übernehmen und `— Strategy` anhängen (nur falls nicht schon enthalten).
`overlay` sowie `format`, `precision`, `max_lines_count`, `max_labels_count`, `max_boxes_count`
aus dem `indicator()`-Call mitnehmen — `max_bars_back` **nicht**.

```pine
strategy("<Titel> [WavesUnchained] — Strategy", overlay=<true|false>,
     <übernommene extras>,
     default_qty_type=strategy.percent_of_equity, default_qty_value=10,
     commission_type=strategy.commission.percent, commission_value=0.02,
     slippage=1, max_bars_back=500)
```

`commission_value=0.02` (0,02 %) ist der Repo-Default — realistisch für CFD/Futures. Für
Krypto mit Maker/Taker-Gebühren höher setzen. Die Overnight-/Roll-Komponente bei CFDs ist
darin **nicht** enthalten; sie ist eine bekannte, nicht eingepreiste Verzerrung.

## Charttyp-Guard

Direkt nach dem `strategy()`-Call:

```pine
if barstate.islast and not chart.is_standard
    label.new(bar_index, high, "Backtest ungültig auf diesem Charttyp — Orders füllen zu " +
              "Marktpreisen, nicht zu synthetischen Bar-Preisen (Heikin Ashi/Renko/Kagi/etc.)",
              style=label.style_label_down, color=color.new(color.red, 10),
              textcolor=color.white, size=size.small)
```

Wortlaut nicht abwandeln — alle acht Strategien tragen exakt diesen Block.

## Standard-Input-Block

Wörtlich so, in jeder Strategie:

```pine
// ─── Strategy inputs ─────────────────────────────────────────────────────────
g_strat       = "Strategy"
tradeDirInput = input.string("Both", "Trade Direction",
     options=["Both", "Long Only", "Short Only"], group=g_strat,
     tooltip="Filter entries by direction. Useful for asymmetric instruments.")
confirmClose  = input.bool(true,  "Entries on Confirmed Bar Only", group=g_strat,
     tooltip="Only trigger entries on closed bars. Prevents repainting in live trading.")
cooldownBars  = input.int(0,     "Cooldown Bars After Exit", minval=0, group=g_strat,
     tooltip="Block new entries for N bars after a position closes. Set 0 to disable.")
enableBE      = input.bool(false, "Break-Even Stop", group=g_strat,
     tooltip="Move SL to entry price once the trade is N×ATR in profit.")
beATRInput    = input.float(1.0,  "Break-Even Trigger (ATR×)", minval=0.1, step=0.1, group=g_strat,
     tooltip="ATR distance from entry that triggers the break-even move.")

g_filters     = "Filters"
useSession    = input.bool(false, "Session Filter", group=g_filters)
sessionInput  = input.session("0000-2345", "Session", group=g_filters)
useDateRange  = input.bool(false, "Date Range", group=g_filters)
dateFrom      = input.time(timestamp("01 Jan 2020 00:00 +0000"), "From", group=g_filters)
dateTo        = input.time(timestamp("31 Dec 2030 23:59 +0000"), "To",   group=g_filters)
useMaxDD      = input.bool(false, "Max Drawdown", group=g_filters)
maxDD         = input.float(20.0, "Max Drawdown (%)", minval=1, step=1, group=g_filters)
useMaxIntraDD = input.bool(false, "Max Intraday Loss", group=g_filters)
maxIntraDD    = input.float(5.0,  "Max Intraday Loss (%)", minval=1, step=1, group=g_filters)
useLossStreak = input.bool(false, "Losing Streak Limit", group=g_filters)
maxLossStreak = input.int(5,      "Max Consecutive Losses", minval=1, group=g_filters)

strategy.risk.max_drawdown(useMaxDD ? maxDD : 100, strategy.percent_of_equity)
strategy.risk.max_intraday_loss(useMaxIntraDD ? maxIntraDD : 100, strategy.percent_of_equity)

var int _lossStreak = 0
if strategy.losstrades > strategy.losstrades[1]
    _lossStreak := _lossStreak + 1
if strategy.wintrades > strategy.wintrades[1]
    _lossStreak := 0
_filterOk = (not useSession or not na(time(timeframe.period, sessionInput))) and
     (not useDateRange or (time >= dateFrom and time <= dateTo)) and
     (not useLossStreak or _lossStreak < maxLossStreak)

var int _lastExitBar = na
_justClosed = strategy.closedtrades > 0 and strategy.closedtrades.exit_bar_index(strategy.closedtrades - 1) == bar_index
if _justClosed
    _lastExitBar := bar_index
_inCooldown = cooldownBars > 0 and not na(_lastExitBar) and (bar_index - _lastExitBar) < cooldownBars
_canEntry   = not _inCooldown and (not confirmClose or barstate.isconfirmed) and _filterOk
```

## Break-Even — das gemeinsame Fragment

Steht in **jedem** Exit-Muster direkt vor den `strategy.exit()`-Aufrufen:

```pine
_beAtr   = ta.atr(14) * beATRInput
_beLong  = enableBE and strategy.position_size > 0 and close >= strategy.position_avg_price + _beAtr
_beShort = enableBE and strategy.position_size < 0 and close <= strategy.position_avg_price - _beAtr
```

Der Stop wird dann per `math.max(<stop>, strategy.position_avg_price)` (long) bzw.
`math.min(...)` (short) auf Entry gehoben — nie als eigener Exit.

## Exit-Muster

Alle beginnen mit:

```pine
_canLong  = tradeDirInput != "Short Only"
_canShort = tradeDirInput != "Long Only"

if (<long-Ausdruck>) and _canLong and _canEntry
    strategy.entry("Long", strategy.long)
if (<short-Ausdruck>) and _canShort and _canEntry
    strategy.entry("Short", strategy.short)
```

### 1. `trailing` — Per-Bar-ATR-Hülle

Der Indikator liefert zwei laufende Stop-Serien (`longStop` / `shortStop`). Zusätzlich der
Volatilitäts-Exit auf ATR-Spike (Climax-/Erschöpfungskerzen).

Zusatz-Inputs:

```pine
g_exits       = "Strategy — Advanced Exits"
enableVolExit = input.bool(true,  "Volatility Exit (ATR spike)", group=g_exits,
     tooltip="Close the position when current ATR jumps above its baseline by the configured ratio — captures climax / exhaustion bars where the rest of the move is unlikely to continue.")
volExitRatio  = input.float(1.6, "  Volatility Spike Ratio",   minval=1.2, maxval=5.0, step=0.1, group=g_exits,
     tooltip="Exit when ta.atr(atrLen) >= ratio × ema(ta.atr(atrLen), 50). Default 1.6 = current ATR is 60% above its 50-bar average.")
```

Execution:

```pine
if enableVolExit and strategy.position_size != 0
    _atrCur  = ta.atr(atrLen)
    _atrBase = ta.ema(_atrCur, 50)
    _spike   = not na(_atrBase) and _atrCur >= _atrBase * volExitRatio
    if _spike and strategy.position_size > 0
        strategy.close("Long",  comment="Vol Exit (ATR×" + str.tostring(volExitRatio, '#.#') + ")")
    if _spike and strategy.position_size < 0
        strategy.close("Short", comment="Vol Exit (ATR×" + str.tostring(volExitRatio, '#.#') + ")")

<Break-Even-Fragment>

_finalLongStop  = _beLong  ? math.max(<sl_long>,  strategy.position_avg_price) : <sl_long>
_finalShortStop = _beShort ? math.min(<sl_short>, strategy.position_avg_price) : <sl_short>

if strategy.position_size > 0
    strategy.exit("Long Exit", "Long", stop=_finalLongStop)
if strategy.position_size < 0
    strategy.exit("Short Exit", "Short", stop=_finalShortStop)
```

### 2. `trailing_ratchet` — Stop zieht nur an

Wie `trailing`, aber der Stop wird gemerkt und lockert nie. Zusätzlich ist der Vol-Exit
**gerichtet**: er schließt nur auf einer Gegenrichtungs-Climax-Kerze, damit ein guter Trend
nicht auf einer With-Trend-Erschöpfungskerze verlassen wird.

```pine
var float _trailLong  = na
var float _trailShort = na

if strategy.position_size > 0
    _trailLong := na(_trailLong[1]) ? <sl_long> : math.max(_trailLong[1], <sl_long>)
else
    _trailLong := na

if strategy.position_size < 0
    _trailShort := na(_trailShort[1]) ? <sl_short> : math.min(_trailShort[1], <sl_short>)
else
    _trailShort := na

if enableVolExit and strategy.position_size != 0
    _atrCur    = ta.atr(atrLen)
    _atrBase   = ta.ema(_atrCur, 50)
    _spike     = not na(_atrBase) and _atrCur >= _atrBase * volExitRatio
    _vRange    = high - low
    _vClosePos = _vRange > 0 ? (close - low) / _vRange : 0.5
    if _spike and strategy.position_size > 0 and _vClosePos < 0.35
        strategy.close("Long",  comment="Vol Exit (ATR×" + str.tostring(volExitRatio, '#.#') + ", bear close)")
    if _spike and strategy.position_size < 0 and _vClosePos > 0.65
        strategy.close("Short", comment="Vol Exit (ATR×" + str.tostring(volExitRatio, '#.#') + ", bull close)")
```

Danach Break-Even + Exits wie bei `trailing`, aber gegen `_trailLong` / `_trailShort`.

### 3. `fixed` — ein Stop-Level, kein TP

```pine
<Break-Even-Fragment>

_finalLongStop  = _beLong  ? math.max(<sl>, strategy.position_avg_price) : <sl>
_finalShortStop = _beShort ? math.min(<sl>, strategy.position_avg_price) : <sl>

if strategy.position_size > 0
    strategy.exit("Long Exit", "Long", stop=_finalLongStop)
if strategy.position_size < 0
    strategy.exit("Short Exit", "Short", stop=_finalShortStop)
```

### 4. `fixed` mit TP1/TP2/TP3

Zusatz-Input (`<default>` = TP1, TP2 oder TP3):

```pine
exitLvlInput  = input.string("<default>", "Exit at TP",
     options=["TP1", "TP2", "TP3", "None (next signal)"], group=g_strat,
     tooltip="TP level for the exit limit order. 'None' holds until the next opposing signal.")
```

Das TP wird **beim Entry eingefroren** (`var float _exitTP`), damit ein später wandernder
TP-Level die offene Position nicht verschiebt:

```pine
var float _exitTP = na

_doLong  = (<long>)  and _canLong  and _canEntry
_doShort = (<short>) and _canShort and _canEntry

if _doLong
    _exitTP := exitLvlInput == "TP1" ? <tp1> :
               exitLvlInput == "TP2" ? <tp2> :
               exitLvlInput == "TP3" ? <tp3> : na
    strategy.entry("Long", strategy.long)

if _doShort
    _exitTP := exitLvlInput == "TP1" ? <tp1> :
               exitLvlInput == "TP2" ? <tp2> :
               exitLvlInput == "TP3" ? <tp3> : na
    strategy.entry("Short", strategy.short)
```

Exits wie `fixed`, zusätzlich `limit=_exitTP`.

> Der mehrzeilige Ternary oben funktioniert hier, weil `exitLvlInput` ein *simple string* ist.
> Bei **Serien**-Bedingungen wirft Pine v6 `CE10156` — dort `if / else if` verwenden.

### 5. `directional_fixed_tp` — richtungsspezifische SL/TP

SL und TP werden je Richtung beim Entry eingefroren:

```pine
var float _longSL = na, _longTP = na, _shortSL = na, _shortTP = na
```

(Deklaration in Pine v6 einzeln schreiben, nicht als Kommaliste.) Beim Long-Entry
`_longSL := <sl_long>` / `_longTP := <tp_long>`, analog short. Exits mit
`stop=_finalLongStop, limit=_longTP`.

Optional indikatorgetriebener Exit, wenn der Indikator eigene Exit-Signale liefert:

```pine
if strategy.position_size > 0 and (<long_exit>)
    strategy.close("Long",  comment="Indicator Exit")
if strategy.position_size < 0 and (<short_exit>)
    strategy.close("Short", comment="Indicator Exit")
```

### 6. `pivot_atr` — SL am Divergenz-Pivot

Zusatz-Inputs:

```pine
slBufInput = input.float(0.5, "SL ATR Buffer (×)", minval=0.1, step=0.1, group=g_strat,
     tooltip="ATR distance beyond the divergence pivot for the stop loss.")
tpRRInput  = input.float(2.0, "TP R:R Ratio",      minval=0.5, step=0.5, group=g_strat,
     tooltip="Take profit at this R:R multiple of the SL distance from entry.")
```

```pine
var float _sl = na
var float _tp = na

if (<long>) and _canLong and _canEntry
    _atr    = ta.atr(14)
    _sl    := <pivot_low> - _atr * slBufInput
    _slDist = math.max(close - _sl, syminfo.mintick)
    _tp    := close + _slDist * tpRRInput
    strategy.entry("Long", strategy.long)

if (<short>) and _canShort and _canEntry
    _atr    = ta.atr(14)
    _sl    := <pivot_high> + _atr * slBufInput
    _slDist = math.max(_sl - close, syminfo.mintick)
    _tp    := close - _slDist * tpRRInput
    strategy.entry("Short", strategy.short)
```

`math.max(..., syminfo.mintick)` verhindert eine Division-durch-Null-artige Entartung, wenn
Pivot und Close zusammenfallen. Exits mit `stop=_finalLongStop, limit=_tp`.

## `@strategy-config` im Indikator

Der Block am Dateiende des **Indikators** ist keine Build-Anweisung mehr, sondern die
**Signal-Deklaration**: er hält fest, welche Variablen die Entry-Signale und Stop-Level sind.
TradingView ignoriert die Kommentarzeilen. Er ist die Vorlage beim Nachziehen einer Strategie
nach einer Indikator-Änderung — pflegen, nicht löschen.

```pine
// @strategy-config
// long:       longSignal
// short:      shortSignal
// sl_type:    trailing          // trailing | trailing_ratchet | fixed | directional_fixed_tp | pivot_atr
// sl_long:    longStop          // trailing / trailing_ratchet / directional_fixed_tp
// sl_short:   shortStop
// sl:         SL                // fixed
// tp1:        TP1_lvl           // fixed mit TP-Leveln
// tp2:        TP2_lvl
// tp3:        TP3_lvl
// tp_default: TP1
// tp_long:    longTakeProfit    // directional_fixed_tp
// tp_short:   shortTakeProfit
// long_exit:  exitLongSignal    // optional, indikatorgetriebener Exit
// short_exit: exitShortSignal
// pivot_low:  low[pivRight]     // pivot_atr
// pivot_high: high[pivRight]
// @end-strategy-config
```

Mehrere Signale pro Richtung: kommasepariert (`long: sig1, sig2` → `(sig1 or sig2)`).

## Nach dem Bauen

- Assessment-Datei `strategies/<name>/<name>_strategy_assessment.md` anlegen, Schema in
  `strategies/ASSESSMENT_SCHEMA.md`. Auch dann, wenn noch kein Backtest existiert — dann mit
  Verdikt „Not ready — nicht getestet".
- Backtest-Zahlen gehören **ausschließlich** in diese Assessment-Datei, nie in README,
  CHANGELOG, `DESCRIPTION_TV.bbcode`, Tooltips oder den `strategy()`-Titel.
- Weicht die Strategie bewusst von der Indikator-Logik ab, das im Header vermerken — sonst
  liest sich die Kopie später wie ein Drift-Bug.
