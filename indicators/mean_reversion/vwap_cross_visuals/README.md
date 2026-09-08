# VWAP Cross Visuals

VWAP cross detection at its core, with optional advanced layers. Session VWAP and two pivot-anchored VWAPs feed a cross signal engine; the **Price × VWAP cross** is the headline signal (shown as hover-tooltip labels). Optional layers — structure crosses, VWAP cluster, ranked S/R zones, rolling volume profile, HTF trend-stack — are off or hidden by default to keep the chart clean.

**Out of the box:** VWAP lines + Price×VWAP cross markers only. Set **Signal Scope → All signals** to surface the secondary systems, and enable the **Zone / Volume / HTF** modules individually when you want those layers.

## Features

- **Session VWAP** plus **anchored VWAP high/low** (anchored at the latest confirmed pivot high/low)
- **Price × VWAP cross signals** with ATR-based strength scoring and throttling
- **Structure crosses** — session VWAP crossing the anchored VWAP levels
- **Multi-VWAP cluster detection** — confluence zones when VWAPs converge within a tolerance
- **Zone Management (Pro)** — orderblock/pivot/cluster/FVG zone creation, scoring (HTF, FVG overlap, freshness, distance, touches), ranking, trimming, and break detection on current and higher timeframe
- **Bias engine** — VWAP band regime (BULL/BEAR/NEUTRAL) used as confirmation gate
- **Target levels** — ATR or sigma multiples from the nearest active zone, drawn as extendable lines
- **Entry signals** — VWAP/zone retest-and-reject logic (Conservative/Aggressive) with cooldown
- **Volume Profile (Pro)** — POC, value area, HVN/LVN nodes, LVN break-and-retest and VA re-entry signals, EMA/Supertrend/MOST trend filters, optional auto-tuning by market regime
- **HTF Stack Panel (Pro)** — weighted trend confluence across four auto-selected higher timeframes with stack alignment/break signals and choppiness index
- **Display modes** — Smart / Price Only / Cluster Only
- **Alerts** — granular `alertcondition`s plus dynamic `alert()` messages, including multi-system confluence alerts
- **Hidden export plots** — signals, VWAP levels, zone/volume/HTF metrics for use in other scripts (`display.none`)

## Instrumente

Jede Berechnung in diesem Skript — Session-VWAP, beide Anchored-VWAPs, das Zone-Management-Bias-Band, die Zone-Zielwerte und das Volume-Profile-Modul — ist volumengewichtet. Ob `volume` auf dem Chart-Symbol echtes gehandeltes Volumen ist, entscheidet `syminfo.volumetype` zur Laufzeit:

- **Gültig:** jedes Symbol, dessen `syminfo.volumetype` `base` oder `quote` meldet — in der Regel Futures, börsennotierte Aktien und Krypto-Börsen, dazu Broker-Feeds, die echte gehandelte Menge durchreichen
- **Näherung:** ist dieses Volumen der Anteil eines einzelnen Brokers (ein CFD-Feed, der `base` meldet), liegt der VWAP dort, wo *dieser Broker* gehandelt hat — nicht zwingend dort, wo die Börse gehandelt hat. Als ungefähres Niveau lesen, nicht als das Level, auf das andere Marktteilnehmer reagieren
- **Ungültig:** jedes Symbol mit `volumetype` = `tick` (reine Zahl der Preis-Updates) oder `n/a` — dort gibt es nichts zu gewichten

Auf einem ungültigen Instrument liefert das Skript **keinen VWAP-, Zonen- oder Volume-Profile-Output** — keine Linien, keine Bänder, keine Zonen-Boxen, keine Signale. Ein Warnlabel ("benötigt echtes Handelsvolumen") erscheint stattdessen auf der letzten Bar.

Ein Referenzmarkt-Workaround (z. B. `NYMEX:NG1!` statt der Capital.com-CFD-Notierung) wurde für dieses Skript geprüft, aber bewusst nicht implementiert: Ein Intraday-VWAP über `request.security()` auf einem anderen Symbol würde die Preisbewegung des Chart-Symbols mit dem volumengewichteten Durchschnitt eines *anderen* Marktes überlagern. Beide Feeds haben unterschiedliche Preisniveaus (Spread-/Feed-Offset), sodass ein roh übernommener Referenzmarkt-VWAP-Preis auf dem Chart irreführend wäre, wenn er nicht sorgfältig normalisiert wird. Von einer naiven Implementierung wird abgeraten. Falls ein Referenzmarkt-VWAP je verfolgt wird, gehört er gemäß der Vertrauensrangfolge in `DATA_VALIDITY.md` §4.1 in ein einziges gemeinsames Daily-Kontext-Modul, nicht in diesen Einzelindikator.

## Signal markers

| Marker | Meaning |
|---|---|
| `▲/▼ P` | Price crosses session VWAP |
| `◆ S` | VWAP structure cross (session vs anchored) |
| `● C` | Multi-VWAP cluster |
| `ZL / ZS` | Zone-based long/short |
| `L / S` | Entry signal (retest + reject, bias-gated) |
| `VL / VS` | Volume profile signal (LVN break & retest, VA re-entry) |
| `HTF↑ / HTF↓ / BREAK` | HTF stack alignment / break |

## Notes

- Pro modules (zones, volume profile, HTF stack) can be toggled independently; the legend table grows accordingly.
- The volume profile recomputes its histogram per bar over the configured window — on very long histories this is the heaviest part of the script.
- Target mode "LIQUIDITY" is exposed in the inputs but currently falls back to sigma targets.
