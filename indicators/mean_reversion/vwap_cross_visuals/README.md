# VWAP Cross Visuals

Session VWAP and two pivot-anchored VWAPs with markers for the events between them: price crossing the session VWAP, the session VWAP crossing an anchored VWAP, and the VWAPs converging into a cluster. It is a display tool — it shows where price stands relative to VWAP and does not grade setups or emit trade signals. Optional layers (zones with VWAP bands, volume profile, HTF slope panel) are off by default.

## Features

- **Session VWAP** (resets daily) plus **anchored VWAP high/low** (anchored at the latest confirmed pivot high/low)
- **Price × VWAP cross markers** as labels; the tooltip shows close, VWAP and the distance in ATR
- **Structure crosses** — session VWAP crossing an anchored VWAP
- **Multi-VWAP cluster** — the anchored VWAPs within the cluster tolerance, with price inside
- **Session-reset filter** — the VWAP jump at the session start never counts as a cross
- **Marker throttling** — minimum bar distance between two markers of the same type (visual only)
- **Display modes** — Smart / Price Only / Cluster Only
- **Zone Management (Pro)** — orderblock/pivot, VWAP-cluster, HTF and FVG zones on the current and a higher timeframe, with touch/violation tracking, ranking for display and trimming; ATR or σ band around the session VWAP
- **Volume Profile (Pro)** — POC, VAH and VAL over a fixed, rolling or session window
- **HTF Slope Panel (Pro)** — EMA(50) change over 5 bars in % for four auto-selected higher timeframes, plus the chart's Choppiness Index in the legend
- **Alerts** — neutral event descriptions on the confirmed bar

## Cross detection

A cross is a change of the last strict side (above / below) of the two lines. At the start of each session the session VWAP resets and jumps; the side memory is cleared on that bar, so neither the jump nor the first side established afterwards counts as a cross. Structure crosses use the same rule.

## Higher timeframe values

All HTF requests read the last closed HTF bar (`expr[1]` with `lookahead_on`), so HTF values do not change while the HTF bar is forming and do not repaint after a reload. HTF zones are created only on the first chart bar of a new HTF bar — one HTF pivot yields at most one zone.

## Zones

| Source | Created when |
|---|---|
| Orderblock | last opposite candle before an impulse candle (body > 0.5 ATR) |
| Pivots | confirmed pivot whose outer edge lies within 2 ATR of the session VWAP |
| VWAP cluster | once, on the bar a cluster forms (one zone above and one below the centre) |
| HTF | new HTF bar with a confirmed HTF pivot whose edge lies within 3 HTF ATR of the HTF VWAP |
| FVG | three-bar gap (bullish: low above the high two bars back; bearish: high below the low two bars back) with the session VWAP inside the gap |

Zones are ranked (HTF, FVG overlap, freshness, distance, touched) only to decide which ones are kept and which one is highlighted per side.

## Instrumente

Jede Berechnung in diesem Skript — Session-VWAP, beide Anchored-VWAPs, das VWAP-Band der Zonen-Ebene und das Volume-Profile-Modul — ist volumengewichtet. Ob `volume` auf dem Chart-Symbol echtes gehandeltes Volumen ist, entscheidet `syminfo.volumetype` zur Laufzeit:

- **Gültig:** jedes Symbol, dessen Feed Volumen liefert und es nicht als `tick` ausweist. Die meisten Feeds außer Krypto melden `syminfo.volumetype = n/a` („nicht angegeben“), auch Futures mit echten Kontrakten — `n/a` mit vorhandenem Volumen gilt deshalb als gültig
- **Näherung:** ist dieses Volumen der Anteil eines einzelnen Brokers (ein CFD-Feed mit eigenem Volumen), liegt der VWAP dort, wo *dieser Broker* gehandelt hat — nicht zwingend dort, wo die Börse gehandelt hat. Als ungefähres Niveau lesen, nicht als das Level, auf das andere Marktteilnehmer reagieren
- **Ungültig:** jedes Symbol mit `volumetype` = `tick` (Anzahl Transaktionen, keine Menge) oder ganz ohne Volumen — dort gibt es nichts zu gewichten

Auf einem ungültigen Instrument liefert das Skript **keinen VWAP-, Zonen- oder Volume-Profile-Output** — keine Linien, keine Bänder, keine Zonen-Boxen, keine Marker. Unten rechts erscheint stattdessen kurz „VWAP Cross Visuals · not available“.

Ein Referenzmarkt-Workaround (z. B. `NYMEX:NG1!` statt der Capital.com-CFD-Notierung) wurde für dieses Skript geprüft, aber bewusst nicht implementiert: Ein Intraday-VWAP über `request.security()` auf einem anderen Symbol würde die Preisbewegung des Chart-Symbols mit dem volumengewichteten Durchschnitt eines *anderen* Marktes überlagern. Beide Feeds haben unterschiedliche Preisniveaus (Spread-/Feed-Offset), sodass ein roh übernommener Referenzmarkt-VWAP-Preis auf dem Chart irreführend wäre, wenn er nicht sorgfältig normalisiert wird. Von einer naiven Implementierung wird abgeraten. Falls ein Referenzmarkt-VWAP je verfolgt wird, gehört er gemäß der Vertrauensrangfolge in `DATA_VALIDITY.md` §4.1 in ein einziges gemeinsames Daily-Kontext-Modul, nicht in diesen Einzelindikator.

## Chart markers

| Marker | Meaning |
|---|---|
| `▲ / ▼` | Close crossed above / below the session VWAP |
| `◆ S` | Session VWAP crossed an anchored VWAP (bottom = above, top = below) |
| `● C` | Price inside a multi-VWAP cluster |

## Legend

Close vs VWAP (above / below), distance to VWAP in ATR, cluster state; with the zone layer the band position (above / inside / below band) and the zone counts; with the volume profile POC and VA range; with the HTF panel the Choppiness Index (14). The data window carries "Distance to VWAP (ATR)".

## Alerts

All alerts fire on the confirmed bar, once per cross. The marker throttle does not apply to alerts.

| Alert | Event |
|---|---|
| VXV Close Crossed Above VWAP | close crossed above the session VWAP |
| VXV Close Crossed Below VWAP | close crossed below the session VWAP |
| VXV Session VWAP Crossed Above AVWAP | session VWAP crossed above an anchored VWAP |
| VXV Session VWAP Crossed Below AVWAP | session VWAP crossed below an anchored VWAP |

## Notes

- Pro modules (zones, volume profile, HTF slope panel) can be toggled independently; the legend grows accordingly.
- The volume profile recomputes its histogram per bar over the configured window — on very long histories this is the heaviest part of the script.
