# Changelog

## v2.3.0 — 2026-10-02
- Cluster: the session-VWAP alignment check had no effect (any existing session VWAP satisfied it). A cluster now forms from the two anchored VWAPs plus price as before, and gets +10 strength (capped at 100) when the session VWAP sits inside it too (provisional default)
- VWAP bias: price position alone (±30) cleared the ±20 bias threshold on any tick above or below VWAP. Price position now counts ±10, plus 10 points per ATR of distance from VWAP (capped at 2 ATR, provisional), replacing the percent-based distance bonus — so price position alone turns the bias only beyond 1 ATR; crosses still count as before. Threshold stays ±20
- Volume Profile regime: the Supertrend filter confirmed a trend on every bar (its direction is never 0). It now confirms only when its direction agrees with the EMA 21/50 direction
- HTF Stack: the default Stack Alignment Threshold is lowered from 0.7 to 0.5 (provisional) — 0.7 was practically out of reach on intraday charts, so stack signals did not fire
- Removed the "Trend Detection Method" input: the HTF stack always used the EMA detector; the unused Supertrend/MOST detectors (the Supertrend one also had its direction inverted) are removed
- Removed dead code: the HTF stack's auto-tuning outputs (never read) and the VWAP-zone confluence added to the zone bias score (never read)

## v2.2.0 — 2026-10-02
- Fix: cross strength (which gates the price-cross marker) and structure strength used an ATR that only updated on the bars where it was needed, so it drifted far from the real ATR. Both now use an ATR calculated on every bar — cross markers can appear more or less often than before
- Fix: cluster strength measured the cluster's tightness as the distance of price from its 10-bar close midrange (which could even go negative). It now measures the spread between the two clustered anchored VWAPs
- Fix: pivot-based and VWAP-cluster zones were marked "touched" on the bar they were created, because the creation bar's close lies inside them by construction. Touch tracking now starts on the following bar
- Fix: the Volume Profile short signals (LVN break & retest short, VAH re-entry short) required a bullish trend filter, so they only fired in uptrends. They now require the mirrored bearish filter (EMA 50 < 200, Supertrend down, MOST down — each only when enabled)
- Cross label tooltip: "Confluence" no longer counts the cross itself (now shows the other two systems, n/2), and cross strength shows as 0–100 % instead of being multiplied by 100 a second time
- Dashboard: Volume Score shows its real maximum (/7 instead of /10)

## v2.1.3 — 2026-09-05
- **Exchange-only data contract**: added a hard `syminfo.volumetype`-based guard (`volumeIsReal`). Session VWAP, both anchored VWAPs, the Zone Management bias/target/confluence layer, and the Volume Profile module now all null out / stop processing on instruments without real trade volume — no VWAP lines, bias bands, zone boxes, target lines, or volume-profile output on those symbols.
- A warning label ("benötigt echtes Handelsvolumen — aktuell: ...") now appears on the last bar when volume isn't real.
- Added the `Data Contract` header block (`Verdict: Exchange-only`).

## v2.1.2 — 2026-06-30
- Alerts: added VWAP cross alerts (price cross up/down, structure cross up/down) with a bar-close confirmation toggle — `VXV · EVENT · {{ticker}} {{interval}}`

## v2.1.1 — 2026-06-27
- **Aggregated Long/Short signals isolated behind a toggle**: new "Emit aggregated Long/Short signals" input (Visual Settings, default OFF). When off, the module is pure VWAP cross visuals — only the core Price×VWAP cross markers render. Turning it on (with Signal Scope = "All signals") re-enables the aggregated structure-cross, cluster, entry, zone, volume-profile and HTF-stack trade markers, including the volume-profile event that previously rendered as a trade marker.

## v2.1.0 — 2026-06-11
- Focused on the core signal: new "Signal Scope" input defaults to **VWAP Cross only** — out of the box the chart shows just the Price×VWAP cross markers. "All signals" brings back structure-cross, cluster, entry and (if their modules are enabled) zone/volume/HTF markers.
- Price×VWAP cross markers are now **labels with hover tooltips** (price, VWAP, bias, confluence, cross strength) instead of plain triangles — cleaner and informative on hover. Frees two plot outputs (now ~27).

## v2.0.3 — 2026-06-11
- Cleaner default look: Zone Management, Volume Profile and HTF Stack now default to OFF. Out of the box the indicator shows only the VWAP lines and cross signals (matching its name); the box-heavy layers are opt-in. Previously all three were on at once, which over-painted the chart.

## v2.0.2 — 2026-06-11
- Fix: indicator exceeded TradingView's 64 plot-output limit (87 outputs) and would not load. Removed 34 of the 38 hidden data-window export plots (granular zone/volume/HTF detail) — kept the four core exports (Long/Short signal, bias score, confluence count). The detail values remain visible in the dashboard and panels. Total plot-like outputs now ~29.
- Fix (runtime): selection sort in `sortAndTrimZones` ran its outer loop to `size-1`; on the last pass the inner range `i+1 to size-1` became `size to size-1`, which Pine iterates descending starting at `j=size` → `array.get` out of bounds ("Index 2, array size 2"). Outer loop now stops at `size-2`.

## v2.0.1 — 2026-06-11
- Fix (compile): `plot()`, `bgcolor()` and `alertcondition()` calls were inside `if` blocks (local scope) — moved to global scope with gated series/conditions.
- Fix (compile): `var htfStackStatePrev = na` had no type annotation; the legend row cursor (`nextRow`) and `vwapZoneConfluence` were declared inside one branch but used in sibling scopes.
- Fix: HTF stack signals never fired — the "previous state" was the same mutated object, so the edge detection always compared current vs. current. Previous confluence is now tracked as plain float series.
- Fix: anchored VWAPs were anchored at the pivot *confirmation* bar instead of the pivot bar — history-referencing the in-place-mutated anchors object returned current cumulative values; anchors now subtract the window sums.
- Fix: Supertrend trend filter compared `close` against the supertrend *direction* (±1) instead of using the direction — the filter was effectively always bullish.
- Fix: market-regime trend strength used integer division (always 0 or 1).
- Fix: guarded all `for 0 to array.size()-1` loops — empty zone/node/signal arrays caused out-of-bounds runtime errors (Pine loops run descending for `0 to -1`).
- Fix: LVN break/retest cross detection and zone-target ATR/VWAP are now computed unconditionally (consistent ta history); signal buffer in `generateVwapSignals` no longer grows without bound (`var` removed).
- HTF stack panel is only rebuilt on the last bar (was re-created on every bar).
- Legend table and HTF stack panel restyled to the light-theme dashboard convention.
- Fix: display-mode tooltip showed literal `\n`.

## v2.0.0
- Initial release
