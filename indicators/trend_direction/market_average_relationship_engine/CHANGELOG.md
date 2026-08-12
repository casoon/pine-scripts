# Changelog

## v1.2.0 — 2026-08-01
- Removed the `text`/`textcolor` labels ("PB", "M", "!", "BR", "D", "T") from every event marker — the hover tooltip already carries the full detail, so markers are now plain colored shapes
- Changed the Divergence marker from `shape.flag` to `shape.circle` (green bullish / red bearish); stays distinguishable from the always-orange Do Not Chase circle
- Added `@strategy-config` (Strategy Hooks section) so `scripts/build_strategies.py` can generate `strategies/market_average_relationship_engine_strategy.pine`: entries are Pullback + Momentum Release only (continuation setups already gated on an established trend); Divergence and Turn From Extreme are deliberately excluded from entries to avoid mixing trend-following and reversal logic in one signal; trailing stop is the reference MA ∓ a new `stopAtrMultInput` (ATR×, default 2.5)

## v1.1.0 — 2026-08-01
- Added regular price/relationship divergence (bullish: price lower low vs. relationship higher low; bearish: price higher high vs. relationship lower high) as its own event with pane + price-chart markers, hover tooltip, and alerts — price pivots are used only to detect the divergence itself and never gate the existing Pullback/Momentum/Do Not Chase/Exhaustion events
- Added Turn From Extreme: fires when the relationship line has recently touched a deep low/high and is now confirmed rising/falling off it — a pivot-free read on a trend starting or an already-extended trend recognizably losing steam
- Fixed oversized event markers: the hover-tooltip labels were drawn as visible, near-opaque shapes stacked on top of the actual (small) event marker, rendering as much larger blobs than intended — tooltip labels are now fully transparent (hover still works, marker size is unaffected)
- Removed the redundant oscillator-pane pullback triangle markers (bullish + bearish) — the price-chart pullback marker already carries this information
- Shrunk the remaining oversized markers (price-chart pullback triangles, price-chart/pane relationship-broken and exhaustion crosses) from `size.small` to `size.tiny` for visual consistency
- Fix: `range` is a reserved Pine v6 identifier — renamed the local candle-range variable to `candleRange`
- Fix: `ta.sum` is not a Pine v6 builtin — replaced with the `ta.sma(x, n) * n` idiom
- Fix: multiple multi-line ternary chains over `series` types (`stateName`, `trendDirection`, `directionalAgreement`, `opposingWickRatio`, `relationshipColor`, `stateBackground`, `barRelationshipColor`) threw `CE10156` — converted to `if/else if` expressions, logic unchanged

## v1.0.0 — 2026-08-01
- Initial version: single-MA relationship engine (EMA/SMA/WMA/HMA/VWMA/RMA/DEMA/TEMA/ALMA) with six diagnostic scores (Trend, Respect, Extension, Compression, Acceleration, Exhaustion)
- Relationship oscillator (−100..+100) with a twelve-state classification
- Event engine: confirmed Pullback, Momentum Release, Do Not Chase, Exhaustion, and Relationship Broken signals with per-family cooldown
- Optional price-chart overlay of the MA and event markers, hover tooltips with full diagnostics, Data Window export
- Alerts for each event direction plus a combined "any MARE event" alert
