# Edge Atlas

Edge Atlas is a right-edge price-level atlas. Instead of a conventional landscape of lines crossing the whole chart, it renders a compact, filtered set of the most relevant price levels placed just right of the last candle — period references, sessions, pivots, swing Fibonacci, clustered support/resistance, and round numbers, all normalized into one shared registry and ranked by priority and distance.

## Features

- ✓ Right-edge-style docking: label a fixed bar count past the last candle (right-facing pointer, price/zone detail in the hover tooltip only) with a short rail picking up just past it — keeping the current price area clear matters more than the rail reaching the actual price scale; nothing about the position depends on the current scroll/zoom, so it pans smoothly instead of jumping
- ✓ Line width and rail/label opacity scale with priority, so the most significant levels stand out at a glance
- ✓ Previous/current day, week, month, and year reference levels (High/Low/Close/Open/Midpoint)
- ✓ Asia, London, New York, and two freely nameable custom session ranges (High/Low/Midpoint), off by default — Asia/London/New York are defined in their own local time (Asia/Tokyo, Europe/London, America/New_York) and follow daylight saving time
- ✓ Traditional, Fibonacci, Camarilla, Woodie, and DeMark pivot points (Daily/Weekly/Monthly, PP/R1-3/S1-3 — DeMark only defines PP/R1/S1)
- ✓ Swing-based Fibonacci retracements and extensions from the latest confirmed pivot pair
- ✓ Pivot-cluster support/resistance zones with touch counting (reset when a close breaks the zone) and age filtering
- ✓ Automatic or manual round-number levels (Major/Half/Quarter)
- ✓ Session, weekly, and monthly VWAP, anchored via `timeframe.change` — shown only on symbols with real trade volume (hidden on tick-volume or volume-less feeds such as many CFDs)
- ✓ Up to 4 manually entered price levels with a free-text label each
- ✓ Daily, weekly, and monthly opening ranges (configurable window in minutes)
- ✓ Shared `Level` registry with distance, priority, count, and side filters
- ✓ Minimum label spacing scaled to the instrument's own ATR — labels sit in four columns (Session · Periods · Structure · Other), crowded labels are pushed apart with a leader line to their price, and the layout stays stable while scrolling or zooming
- ✓ Five presets (Clean, Intraday, Structure, Everything, Custom) plus fully granular module switches with explanatory tooltips — including a one-line interpretation note per level (how it's typically read/used, not just what the abbreviation stands for)
- ✓ Optional source zones drawn backward through the chart for S/R levels
- ✓ Trend Curves — up to three moving-average lines (Fast/Base/Anchor) with Responsive/Balanced/Structural/Custom presets, off by default

## Anchoring

Pine drawings can bind to chart time and price, but not to arbitrary screen pixels or the price scale itself. Many approaches were tried and rejected on the way to the current one — see CHANGELOG.md v1.1.1 through v1.2.1 for the full history — including several that tried to make the rail reach the chart's *true* right edge (`extend.right`, or anchoring near `chart.right_visible_bar_time`), and a percentage-of-visible-time-range offset. Three independent bugs surfaced while chasing those goals:

1. **Shared rail origin** — every level's rail was computed with the exact same starting x-coordinate. Several differently-colored horizontal lines beginning at the identical pixel column, stacked closely in price, read as a vertical bar regardless of segment length. Fixed by staggering each rail's start by render rank.
2. **Pine's bounded future-drawing distance** (roughly 500 bars) — a percentage of a wide 15m/1h visible history could exceed it, silently clamping every level to the same maximum point regardless of the stagger above.
3. **Freeze-then-jump while panning** — a percentage-of-visible-range offset recomputes on every scroll/zoom, but Pine only redraws when the script recalculates (not continuously during a drag). The label would sit frozen mid-pan, then snap to a new position on the next recalculation, instead of following the drag smoothly like a normal drawing.

Each level renders as a short rail at its true price followed by a leader line to its label. Labels anchor at a **fixed bar count past the last real bar** (`bar_index` plus "Label offset · bars", default 30, max 400) — not a percentage of anything, so the anchor's position never changes from chart navigation (fixing bug #3). Labels use `label.style_label_left`: the pointer faces price and the box extends away from it, so a label can never cover candles regardless of the offset. Labels sit in **four columns, left to right**: Session (sessions, opening ranges, VWAP) · Periods (day, week, month, year) · Structure (pivots, Fibonacci, S/R) · Other (round numbers, trend curves, manual levels). Inside a column, labels closer than "Minimum label spacing · ATR" (default 1.0) are **pushed apart vertically** — pairwise around the cluster's center, then a final pass guarantees the minimum distance — and the **leader line** from the rail to a moved label runs diagonally. Every level keeps its own label; none is hidden or merged. Rail and leader have the same fixed length and width in every column (width scales with priority), and rails stay inside their own column, so no rail runs through another label; in the first column the rail starts just past the last candle. Column distance is "Label column spacing · bars" (default 110), shrunk automatically if the columns would not fit within 480 bars. Four columns rather than one per category on purpose: Pine positions labels in bars, not pixels, and draws at most about 500 bars into the future — thirteen category columns could not fit at a readable width and overlapped on zoomed-out charts. Spacing is still a bar count, so on a chart zoomed out to well under one pixel per bar (or with "Full name" labels) neighboring columns can touch — increase it then. Widen the chart's right margin to see all columns without scrolling. Nothing in the script reads `chart.right_visible_bar_time`/`chart.left_visible_bar_time` — level selection was decoupled from the viewport in v1.1.16, positioning in v1.2.1. Positioning uses a plain `xloc.bar_index` offset (since v1.7.0), the same principle Fib Reaction Memory (`indicators/market_structure/fib_reaction_memory/`) uses for its projected Fib lines.

All rails in a column share the same start and end for a uniform look — the render-rank stagger used against bug #1 was dropped in v1.8.0 and is the known fix if stacked rails ever read as a bar again. Every label/rail endpoint is capped at 480 bars past the last bar, under Pine's ~500-bar future-drawing limit (bug #2).

Line width and rail/label opacity additionally scale with each level's priority (1-10): priority ≥8 renders one line-width step bolder and less transparent than the "Line transparency"/"Label transparency" baseline, priority ≤3 one step thinner and more transparent, everything in between uses the plain baseline — the same "visual weight tracks significance" principle Fib Reaction Memory applies to its Memory Score tiers, added in v1.7.0.

## Level registry

All calculation modules feed a single `Level` array (price, optional zone bounds, code, full name, category, priority, color, zone flag, touch count). Rendering reads only this registry: it sorts eligible levels by priority then distance, takes the top entries up to the cap, places each in its column and pushes labels closer than **Minimum label spacing · ATR** apart vertically with a leader line to their true price (so nearby levels never stack into an overlapping colored block), applies the maximum-level cap, and draws rails/labels/optional zone boxes. Calculation and display are fully decoupled.

Label text never includes the price, zone bounds, or touch count as numbers in the visible body — "Label content" is just Code or Full name (plus a `×N` touch-count suffix for S/R zones). All of that detail is always in the hover tooltip instead, keeping the label itself short.

The spacing metric has gone back and forth: ATR was tried first and rejected in v1.0.4 (a stock's hourly ATR can be tiny while its visible price range spans a huge historical rally, leaving 0.5 ATR nowhere near enough gap in screen pixels), replaced by a percentage of the visible price range. That in turn caused the *set of displayed levels* to change just from scrolling or zooming — panning to a wider or narrower visible price swing changed the spacing threshold and therefore which levels survived culling, which read as inconsistent/flickery, especially for S/R zones users expect to stay put while navigating history. v1.1.16 moved back to ATR on request, explicitly trading pixel-perfect spacing at every possible zoom level for a level selection that stays stable while scrolling — and, as expected from that trade-off, v1.3.2 raised the default multiplier 1.0 → 3.0 after a low-volatility instrument/timeframe combination (NatGas 15m, several modules active at once) still overlapped at 1.0. v1.8.0 lowered it back to 1.0 because the spacing no longer hides levels — it only sets how far crowded labels are pushed apart, and at 3.0 they spread far from their prices. ATR is not, and can't be, a perfect proxy for pixel height — if labels touch on some chart, increase "Minimum label spacing · ATR"; if they sit too far from their prices, decrease it. "Maximum rendered levels" and "Maximum distance from price · ATR" reduce how many labels compete for space in the first place.

## Level presets

- **Clean** — period references + nearest S/R
- **Intraday** — adds session ranges, daily pivots, and Session VWAP
- **Structure** — adds swing Fibonacci and S/R
- **Everything** (default) — activates every calculation module except Manual levels and Opening ranges, which are Custom-only
- **Custom** — uses only the individual module switches

Every module's own enable checkbox ("Enable day levels", "Enable session ranges", etc.) and its per-level sub-toggles only take effect on the **Custom** preset — the other four presets decide each module on/off themselves and ignore those checkboxes entirely. They gray out (`active =`) outside Custom so that's visible in the settings panel instead of silently doing nothing. The S/R pivot-clustering and swing-Fibonacci pivot-detection *calculation* parameters are the exception: those always run regardless of preset (they feed every preset that includes S/R/Fibonacci, not just Custom), so they stay editable throughout.

Year levels and VWAP follow the same rule as the other period-style modules — off by default, included under **Everything** (Year also matches Month's "Everything-only" treatment), and otherwise Custom-only. **Manual levels are Custom-only under every preset** — there's no sensible default price to show automatically, so no other preset ever turns this module on.

## Trend Curves

A separate module, independent of the level registry above: up to three moving-average lines plotted directly on the chart the normal way (`plot()`, editable per-line color in the Style tab), not right-edge rails/labels by default. Off by default.

"Also show as right-edge levels" additionally feeds each active curve's current value into the same `Level` registry as every other module — same rail/label rendering, same priority/spacing/distance filters, same hover tooltip — without turning off the always-on chart plot.

"MTF timeframe" (blank by default, no MTF, matching every version before v1.6.0) computes all three curves on a different timeframe by passing the whole `f_maValue(...)` call into `request.security()` — the value is evaluated against that timeframe's own OHLC series, not resampled from an already chart-timeframe-computed line, which is what a genuine "Daily SMA 200 on an hourly chart" requires. Like any live MTF plot in Pine, the value can repaint while the target timeframe's own current bar is still forming.

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
