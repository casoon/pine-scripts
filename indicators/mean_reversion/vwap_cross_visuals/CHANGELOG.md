# Changelog

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
