# Kestrel — TradingView-Vergleichsskripte

Kein Indikator-Katalog wie der Rest von `pine-scripts/indicators/` — hier
liegen reine **Referenz-Generatoren** für den Kestrel-Parity-Workflow
(Kestrel-Repo: `todo.md` §9/§11/§16, `.claude/skills/pine-to-rust`).

Jedes Skript rechnet exakt das nach, was der jeweilige Kestrel-Indikator
tatsächlich portiert hat (nicht das volle Pine-Original mit allen Optionen)
und gibt die Werte auf zwei Wegen aus:

## Track A — CSV-Replay (harte Parity-Gate)

1. Skript auf den passenden Chart laden (Symbol = die Instanz, die geprüft
   werden soll), Timeframe auf **M15, H1 oder H4** stellen — das sind die
   einzigen drei, die Kestrel tatsächlich fährt (`orchestrator.rs`,
   `TARGET_TIMEFRAMES`), unabhängig davon, was `config.toml`s `enabled_tfs`
   sagt.
2. „**...**"-Menü am Chart → **Export chart data** → CSV. Die
   `display.data_window`-Plots des Skripts landen dort als eigene Spalten,
   neben `time`/OHLC.
3. CSV nach
   `kestrel/crates/core/tests/fixtures/tradingview/<indikator>_<epic>_<tf>.csv`
   legen (z. B. `cci_naturalgas_h4.csv`).
4. Kestrel-seitig liest ein Test die CSV, füttert die Bars durch den echten
   `on_bar()`-Port und vergleicht jeden Wert mit Toleranz — löst damit die in
   `todo.md` §16 offene Lücke ("kein echter TradingView-Parity-Test").

Braucht keinen Zeitversatz-Abgleich: TradingViews eigene Bars laufen offline
durch Kestrels Engine, nicht gegen Kestrels Live-Feed.

## Track B — Live-Log-Spotcheck

1. Gleiches Skript, gleicher Chart, Kestrel parallel laufen lassen.
2. Pine-Logs-Panel (unten in der Toolbar) zeigt eine Zeile pro
   abgeschlossenem Bar (`barstate.isconfirmed`), z. B.:
   ```
   KESTREL cci epic=NATURALGAS tf=240 t_close=1751558400000 cci_line=42.1 signal=38.9 ...
   ```
3. Diese Zeilen kopieren/exportieren und mir geben — ich gleiche sie gegen
   Kestrels laufende `indicator_values`-Tabelle (DuckDB) für dieselbe
   epic/tf/ts ab.

**Nur Grobcheck, bewusst kein exakter Zahlenabgleich:** Kestrels Bars kommen
vom Capital.com-**Bid**-Kurs, nicht vom Feed, den dieser Chart zeigt
(`todo.md` §9) — erwartbar sind Übereinstimmung bei Zonen/Vorzeichen und
Cross-Timing auf ±1 Bar, keine 1e-4-Parität. Das ist Track As Job.

`t_close` ist absichtlich `time_close`, nicht `time` — Kestrels `Bar.ts` ist
die **Bar-Close-Zeit** in epoch ms UTC (`capital/model.rs`), nicht die
Open-Zeit.

## Skripte

- `cci_export.pine` — Kestrels `Cci`-Port (`indicators/cci.rs`), Defaults =
  `config.toml`s NATURALGAS-Block + `registry.rs`-Fallbacks für
  `require_extreme_zone`/`ctx_length`/`div_length`/`div_min`. Spalten:
  `cci_line` (= `IndicatorOutput::value`), `signal`, `ctx` (beide aus
  `extra`), `bull_extreme`/`bear_extreme`/`bull_zero_cross`/
  `bear_zero_cross`/`bull_divergence`/`bear_divergence` (0/1, aus
  `CciAlerts`), `extreme_strength`/`divergence_strength`.

Weitere Indikatoren (RSI, MFI, Stoch RSI, Williams %R, ADX, ATR, Fisher
Transform, TSI, Money Flow Profile) folgen nach demselben Muster, sobald CCI
den Workflow einmal end-to-end bestätigt hat.

Analytics-Read-outs (Fear/Greed, Regime, Trend Persistence, Cheat Sheet)
sind hier bewusst noch nicht dabei — die werden bei Kestrel aktuell nur
in-memory berechnet, keine DuckDB-Historie zum Abgleichen. Bräuchte vorher
einen kleinen Schema-Zusatz auf Kestrel-Seite.
