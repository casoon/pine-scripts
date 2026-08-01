# Edge Atlas

Edge Atlas is a right-edge price-level atlas. Instead of a conventional landscape of lines crossing the whole chart, it renders a compact, filtered set of the most relevant price levels docked to the visible right edge of the chart — period references, sessions, pivots, swing Fibonacci, clustered support/resistance, and round numbers, all normalized into one shared registry and ranked by priority and distance.

## Features

- ✓ Right-edge-style docking: label a fixed bar count past the last candle (right-facing pointer, price/zone detail in the hover tooltip only) with a short rail picking up just past it — keeping the current price area clear matters more than the rail reaching the actual price scale; nothing about the position depends on the current scroll/zoom, so it pans smoothly instead of jumping
- ✓ Previous/current day, week, and month reference levels (High/Low/Close/Open/Midpoint)
- ✓ Asia, London, and New York session ranges (High/Low/Midpoint), off by default
- ✓ Traditional and Fibonacci pivot points (Daily/Weekly/Monthly, PP/R1-3/S1-3)
- ✓ Swing-based Fibonacci retracements and extensions from the latest confirmed pivot pair
- ✓ Pivot-cluster support/resistance zones with touch counting and age filtering
- ✓ Automatic or manual round-number levels (Major/Half/Quarter)
- ✓ Shared `Level` registry with distance, priority, count, and side filters
- ✓ Minimum label spacing scaled to the instrument's own ATR — crowded levels are culled by priority instead of stacking into overlapping boxes, and the selection stays stable while scrolling or zooming
- ✓ Five presets (Clean, Intraday, Structure, Everything, Custom) plus fully granular module switches with explanatory tooltips — including a one-line interpretation note per level (how it's typically read/used, not just what the abbreviation stands for)
- ✓ Optional source zones drawn backward through the chart for S/R levels
- ✓ Trend Curves — up to three moving-average lines (Fast/Base/Anchor) with Responsive/Balanced/Structural/Custom presets, off by default

## Anchoring

Pine drawings can bind to chart time and price, but not to arbitrary screen pixels or the price scale itself. Many approaches were tried and rejected on the way to the current one — see CHANGELOG.md v1.1.1 through v1.2.1 for the full history — including several that tried to make the rail reach the chart's *true* right edge (`extend.right`, or anchoring near `chart.right_visible_bar_time`), and a percentage-of-visible-time-range offset. Three independent bugs surfaced while chasing those goals:

1. **Shared rail origin** — every level's rail was computed with the exact same starting x-coordinate. Several differently-colored horizontal lines beginning at the identical pixel column, stacked closely in price, read as a vertical bar regardless of segment length. Fixed by staggering each rail's start by render rank.
2. **Pine's bounded future-drawing distance** (roughly 500 bars) — a percentage of a wide 15m/1h visible history could exceed it, silently clamping every level to the same maximum point regardless of the stagger above.
3. **Freeze-then-jump while panning** — a percentage-of-visible-range offset recomputes on every scroll/zoom, but Pine only redraws when the script recalculates (not continuously during a drag). The label would sit frozen mid-pan, then snap to a new position on the next recalculation, instead of following the drag smoothly like a normal drawing.

The rail no longer tries to reach the true edge at all (dropped on request — keeping the current price area clear of labels matters more than the rail visually touching the price scale), which removes most of the exposure to bug #1 for the rail specifically. Labels anchor at a **fixed bar count past the last real bar** (`time` plus `labelOffsetBarsInput` bars, default 250, max 400, "Label offset · bars") — not a percentage of anything, so the anchor's calendar-time position never changes from chart navigation (fixing bug #3). Labels use `label.style_label_right` — pointer facing right, box extending back toward price; the rail is a short, fixed-length segment (`extend.none`) starting just past the label. Nothing in the script reads `chart.right_visible_bar_time`/`chart.left_visible_bar_time` anymore — level selection was decoupled from the viewport in v1.1.16, positioning in v1.2.1.

A fixed bar count has its own trade-off, symmetric to the percentage-based one: on a chart showing a lot of history, 250 bars is a smaller fraction of the visible width, so it can still look tight against the last candle at some zoom levels — there is no single value that looks identical at every zoom level, only "increase this if it looks tight" (same tension as ATR-based spacing below, just on the horizontal axis).

Every rail endpoint is separately clamped to at most 480 bars past `time`, regardless of "Label offset · bars" or "Maximum rendered levels" settings — a large offset combined with many rendered levels (each level's rail is staggered further out by its render rank, see bug #1) could otherwise push the highest-ranked rail past Pine's ~500-bar future-drawing limit and get silently clamped, recreating bug #1 via input combinations instead of chart zoom.

The *label body grows toward price* direction is inherently riskier than growing away from price — mitigated by the label no longer showing price in the body at all (see Level registry below — shorter text needs less clearance) and a generous default offset. If labels ever start touching candles again on an extremely zoomed-out chart, "Label offset · bars" is the first thing to increase.

## Level registry

All calculation modules feed a single `Level` array (price, optional zone bounds, code, full name, category, priority, color, zone flag, touch count). Rendering reads only this registry: it sorts eligible levels by priority then distance, greedily accepts them in that order while skipping any candidate within **Minimum label spacing · ATR** of an already-accepted level (so nearby levels don't stack into an overlapping colored block), applies the maximum-level cap, and draws rails/labels/optional zone boxes. Calculation and display are fully decoupled.

Label text never includes the price, zone bounds, or touch count as numbers in the visible body — "Label content" is just Code or Full name (plus a `×N` touch-count suffix for S/R zones). All of that detail is always in the hover tooltip instead, keeping the label itself short — which also keeps it well clear of price now that its body grows back toward price from a right-facing anchor (see Anchoring above).

The spacing metric has gone back and forth: ATR was tried first and rejected in v1.0.4 (a stock's hourly ATR can be tiny while its visible price range spans a huge historical rally, leaving 0.5 ATR nowhere near enough gap in screen pixels), replaced by a percentage of the visible price range. That in turn caused the *set of displayed levels* to change just from scrolling or zooming — panning to a wider or narrower visible price swing changed the spacing threshold and therefore which levels survived culling, which read as inconsistent/flickery, especially for S/R zones users expect to stay put while navigating history. v1.1.16 moved back to ATR on request, explicitly trading pixel-perfect spacing at every possible zoom level for a level selection that stays stable while scrolling — and, as expected from that trade-off, v1.3.2 raised the default multiplier 1.0 → 3.0 after a low-volatility instrument/timeframe combination (NatGas 15m, several modules active at once) still overlapped at 1.0. ATR is not, and can't be, a perfect proxy for pixel height — if labels ever overlap on some chart, "Minimum label spacing · ATR" is the first thing to increase; "Maximum rendered levels" and "Maximum distance from price · ATR" are the other two levers when a preset simply has too many modules active for the available vertical space.

## Level presets

- **Clean** — period references + nearest S/R
- **Intraday** — adds session ranges and daily pivots
- **Structure** — adds swing Fibonacci and S/R
- **Everything** — activates every calculation module
- **Custom** — uses only the individual module switches

Every module's own enable checkbox ("Enable day levels", "Enable session ranges", etc.) and its per-level sub-toggles only take effect on the **Custom** preset — the other four presets decide each module on/off themselves and ignore those checkboxes entirely. They gray out (`active =`) outside Custom so that's visible in the settings panel instead of silently doing nothing. The S/R pivot-clustering and swing-Fibonacci pivot-detection *calculation* parameters are the exception: those always run regardless of preset (they feed every preset that includes S/R/Fibonacci, not just Custom), so they stay editable throughout.

## Trend Curves

A separate module, independent of the level registry above: up to three moving-average lines plotted directly on the chart the normal way (`plot()`, editable per-line color in the Style tab), not right-edge rails/labels. Off by default.

Each of the three lines has a fixed role rather than just a different period of the same average:

- **Fast Curve** — immediate movement / momentum impulse
- **Base Curve** — the tradable trend
- **Anchor Curve** — the higher-order market direction / regime

Presets assign type and length per role:

| Preset | Fast | Base | Anchor | For |
|---|---|---|---|---|
| Responsive | JMA-style 9 | JMA-style 21 | JMA-style 50 | Intraday, fast markets (oil, indices, forex, crypto), early pullback/trend-change detection. Three fast adaptive lines react alike and can still whipsaw in choppy sideways phases — adaptive smoothing doesn't remove the whipsaw problem by itself. |
| Balanced (default) | JMA-style 21 | EMA 50 | SMA 200 | Classic day/swing trading, stocks/indices/commodities. Three different time horizons and reaction speeds instead of three measurements of the same thing. |
| Structural | EMA 20 | SMA 50 | SMA 200 | Swing/position trading, daily/weekly charts. Filters short-term noise; the 50/200 relationship reads as a regime signal (e.g. Golden/Death Cross), not a timing signal — it's late by design. |
| Custom | — | — | — | Type (JMA-style/EMA/SMA), length, and — only shown when a line's type is JMA-style — phase/power, set per line. |

Lengths are never auto-scaled by chart timeframe: a length of 20 always means 20 bars of whatever timeframe is currently open (20 bars on 5m ≠ 20 bars on 1D), matching how the rest of the indicator already treats "bars" as the unit — the timeframe itself is the horizon the user already chose.

Global controls: master toggle, source, line offset (bars), and a line-thickness-only "Visual emphasis" setting (colors are edited per line via the chart's Style tab, not through inputs).

**JMA-style, not JMA.** The Jurik Moving Average is patented and proprietary; the JMA-style lines here use the same open-source Jurik-inspired smoothing approximation already implemented elsewhere in this repo (`jma_struct.pine`, `candle_pressure_response_jma.pine`) via a shared `f_jma` helper — a phase/power-tunable adaptive filter, not Mark Jurik's original algorithm. It's labeled "JMA-style" throughout the UI to keep that honest.

See `todo.md` in this directory for the list of features from the original concept that are not yet implemented.
