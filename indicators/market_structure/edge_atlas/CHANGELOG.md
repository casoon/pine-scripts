# Changelog

## v1.7.0 — 2026-08-11
- Rebuilt right-edge label/rail positioning from an `xloc.bar_time` offset (`time` + bar count × per-bar duration) to a plain `xloc.bar_index` offset (`bar_index` + "Label offset · bars"), matching the positioning principle Fib Reaction Memory uses for its projected Fib lines. Both are fixed, viewport-independent offsets, so this carries no regression risk for the pan/zoom freeze-then-jump bug the original bar_time system was built to avoid — bar_index is simply simpler, with no per-bar duration bookkeeping needed. The `atlasBarMs` helper is gone
- Line width and rail/label opacity now scale with each level's priority (1-10): priority ≥8 renders one line-width step bolder and less transparent, priority ≤3 one step thinner and more transparent, everything in between unchanged — the same "visual weight tracks significance" principle Fib Reaction Memory applies to its Memory Score tiers, so the most significant levels (PDH/PDL-class) stand out from secondary ones at a glance instead of every level looking equally weighted

## v1.6.0 — 2026-08-01
- Added Daily/Weekly/Monthly Opening Ranges (ORH/ORL, WORH/WORL, MORH/MORL) — high/low of the first N configurable minutes after each new day/week/month starts, own module, Custom-preset-only. Unlike the existing sessions, the still-forming range is never shown as a level (na until the window closes), so there's no separate "developing vs completed" toggle to add
- Added an MTF mode to Trend Curves ("MTF timeframe", blank = chart's own timeframe, unchanged default behavior) — the whole `f_maValue(...)` call is passed into `request.security()` so it's computed against the target timeframe's own OHLC series, the standard pattern for e.g. a Daily SMA 200 on an hourly chart. Repaints on the target timeframe's still-forming bar until it closes, same as any other live MTF plot in Pine

## v1.5.2 — 2026-08-01
- Full pass over the preset/module gating logic on request. Found and fixed one real bug: the three Trend Curves `plot()` calls never checked `masterEnableInput` — turning off "Enable indicator" correctly hid every right-edge rail/label but left the Trend Curves lines drawn on the chart regardless. Now gated by the same master switch.
- Reviewed everything else without finding further bugs: Day/Week/Sessions/Pivots/Fib curate which of their secondary sub-levels show outside Custom (only the commonly-used ones force to "on"; rarer ones like PDO/PDM/PWC/PWO/PWM stay off unless the user explicitly enables them via Custom) — because those modules are themselves on by default in nearly every preset, this keeps the "always-on" baseline from getting noisy. Month/Year/Round instead show every sub-level once their own module is switched on, because that module is opt-in-only in the first place (only ever active via Custom or Everything) — the module toggle itself is already the noise control, so a second curation layer isn't needed. Two different strategies, but each internally consistent with why that module is/isn't on by default — not a bug, and Year (added in v1.4.0) correctly followed Month's existing pattern
- Also updated the "Intraday" preset's description (tooltip + README) to mention Session VWAP, which v1.4.0 added to that preset's module set without updating the preset's own description text

## v1.5.1 — 2026-08-01
- Default "Label offset · bars" halved 400 → 200 (user report: at the maximum, labels/rails now sit too far from price on their chart). The offset is measured in bars, not calendar time, so this isn't a timeframe-specific fix — a given bar count looks the same distance from price at a given zoom level (bars visible in the viewport) regardless of whether those bars are 1m or 1D. What actually varies the felt distance is the value itself and the user's current zoom, not the chart's timeframe — same conclusion as the existing "no single value works at every zoom level" tradeoff already documented for this input and for ATR-based label spacing

## v1.5.0 — 2026-08-01
- Added two freely nameable custom sessions (own name/hours/High-Low-Mid toggles per slot), alongside the existing fixed Asia/London/NY sessions — Custom-preset-only, same reasoning as manual levels: no sensible default name/hours to auto-enable on another preset
- Added Camarilla, Woodie, and DeMark pivot methods (previously Traditional/Fibonacci only) — pivot PP/R1-3/S1-3 calculation rewritten from a nested ternary to an if/else chain per method, one branch each, avoiding the multi-line-ternary-on-series-floats risk (CE10156) the ternary version would have hit with 5 methods instead of 2. DeMark only defines PP/R1/S1 — R2/R3/S2/S3 checkboxes simply have no level to register for that method, handled by the existing na-skip in `f_addLevel`
- Trend Curves can now optionally also register their current value in the right-edge Level registry ("Also show as right-edge levels", off by default) — previously only ever a full-chart plot; the always-on plot is unchanged, this is additive

## v1.4.0 — 2026-08-01
- Added Previous-Year period levels (PYH/PYL/PYC/PYO/YO/PYM), following the same pattern as the existing Day/Week/Month modules — new "Period levels · Year" group, off by default (on with Everything), fed from `request.security(..., "12M", ...)`
- Added VWAP module: Session (default on with Intraday/Everything), Weekly, and Monthly VWAP, anchored via `timeframe.change("D"/"W"/"M")` and `ta.vwap(hlc3, anchor, 1.0)` — new "VWAP" group
- Added up to 4 manually entered price levels (own group, Custom-only) — each slot has an enable checkbox, an `input.price` value, and a free-text label; a slot at its 0.0 default price is treated as unset rather than a real level at zero
- Renumbered input groups to fit the three new ones in: Year sits between Month and Sessions, VWAP and Manual levels sit between Round numbers and Trend Curves (Trend Curves is now group 13, was 10) — purely a settings-panel ordering change, no behavior change for existing inputs
- These three were picked from todo.md's "Not yet implemented" list as the items that fit the existing Level-registry architecture directly (single current-bar reference value, same as every other level module) without needing a structural change first — collision modes, price-scale docking, and persistent objects are still open

## v1.3.4 — 2026-08-01
- Default "Label offset · bars" raised 250 → 400 (the maximum) after the same NatGas 15m chart still showed labels tight against the last candle at 250 — a fixed bar count is inherently a smaller fraction of the visible width on a chart showing a lot of history, and no fixed value is guaranteed sufficient at every possible zoom level. This is a default-tuning response, not a structural fix; raising "Label offset · bars" further is no longer available since the default now equals the cap

## v1.3.3 — 2026-08-01
- Default "Label offset · bars" raised 180 → 250 (max raised 300 → 400): on a chart showing a lot of history, a fixed bar count is a smaller fraction of the visible width, so it can still look tight against the last candle — same class of issue as v1.3.2's spacing tuning, different variable
- Found and fixed a latent risk while doing this: a large offset combined with a high "Maximum rendered levels" (up to 120) pushes the highest-ranked rail's stagger far enough that it could exceed Pine's bounded future-drawing distance (roughly 500 bars) and get silently clamped — reintroducing the shared-coordinate vertical-bar bug from v1.1.13/v1.1.14, this time via input combinations rather than chart zoom. Added a hard 480-bar ceiling that every rail endpoint is now clamped to, regardless of offset/level-count settings

## v1.3.2 — 2026-08-01
- Fixed severe label overlap reported on a 15m NatGas chart with several modules enabled at once (Round/Week/Pivot/S-R/Session/Day all active): default "Minimum label spacing · ATR" raised 1.0 → 3.0 (max 20.0) — on a low-volatility instrument/timeframe, 1.0 ATR was too small in screen-pixel terms even though the underlying math was correct
- Tooltip now names the other two levers for this same crowding problem when a preset simply has too many modules active for the available vertical space: "Maximum rendered levels" and "Maximum distance from price · ATR" (both in Right-edge rendering)

## v1.3.1 — 2026-08-01
- Removed the abbreviation legend feature entirely (clarified request: "ausbauen" meant remove, not expand) — the "Show abbreviation legend" input, its now-empty "Help" input group, and the whole legend table render block are gone. Every level's own hover tooltip already carries this information (see v1.2.0), so the separate reference table was redundant

## v1.3.0 — 2026-08-01
- Expanded the abbreviation legend from 11 to 18 entries — now covers every level code the indicator can produce, including Close/Open pairs and midpoints for Day/Week/Month (previously only High/Low and a generic "current opens" row), all three session midpoints, every individual pivot level (R1-3/S1-3, not just "PP/R/S"), every swing Fibonacci ratio (previously only "F38.2" as an example), and all three round-number tiers (Major/Half/Quarter, previously only "RN")
- Documented the R1-3/S1-3 code collision directly in the table: the same codes mean different things depending on whether they came from the Pivots module or the clustered S/R module — listed as two separate rows instead of one ambiguous one
- Fixed the legend table's own styling: it used `text_color = color.white` with no background, which is very likely invisible on TradingView's default light chart theme — switched to this repo's standard light-theme dashboard table style (light background, dark gray text, light gray header)

## v1.2.1 — 2026-08-01
- Fixed labels freezing then jumping while panning the chart horizontally (user report): the label offset was a percentage of the live visible time range, recomputed on every scroll/zoom — since Pine only redraws when the script recalculates (not continuously during a drag), the label would sit still mid-pan and then snap to a new position on the next recalculation instead of following the drag smoothly
- "Label offset · % of visible range" replaced with "Label offset · bars" (fixed bar count, default 180, capped at 300) — the label now sits at a fixed calendar-time position that only changes when new price data arrives, never from chart navigation, so it pans/zooms exactly like a normal drawing with nothing left to jump
- Removed the now-fully-unused `visibleTimeSpan`/`chart.right_visible_bar_time`/`chart.left_visible_bar_time` reads — nothing in the script depends on the current viewport anymore (level selection was already decoupled in v1.1.16, positioning is decoupled as of this version)

## v1.2.0 — 2026-08-01
- Added interpretation notes to every level tooltip (period references, sessions, pivots, swing Fibonacci, S/R zones, round numbers) — a one-line note on how that specific level is typically used/read (e.g. PWL: "stops often cluster just below it, so a sweep followed by a reclaim is a common reversal pattern here"), not just what the abbreviation stands for
- Swing Fibonacci ratio checkboxes (23.6–161.8) had no tooltip at all before this — now each explains what that specific ratio is typically used for (shallow pullback vs. deep retracement vs. extension target)
- Confirmed via a full-file audit that the ATR-based spacing fix in v1.1.16 was the only place viewport/scroll state was influencing level *selection* — everything else that reads the visible viewport only affects label/rail *position*, which is correct and intentional

## v1.1.16 — 2026-08-01
- Fixed level selection changing just from scrolling/panning the chart (user report: "resistance zones sometimes show, sometimes don't"): "Minimum label spacing" was a percentage of the *visible* price range (`ta.highest`/`ta.lowest` over a viewport-tracking window) — panning to show a wider or narrower price swing changed the spacing threshold, which changed which levels survived the priority-based culling, even though nothing about the market or the settings changed
- Minimum label spacing is now based on the instrument's ATR instead ("Minimum label spacing · ATR", default 1.0) — tied to the instrument's own volatility, not the current scroll position, so the set of displayed levels stays stable while navigating history. This reintroduces the ATR-based approach rejected in v1.0.4 for a different reason (pixel-accuracy at extreme zoom on a single view) — the trade-off here is explicitly chosen: stability while scrolling over pixel-perfect spacing at every possible zoom level
- Removed the now-unused visible-range price lookup (`visibleHigh`/`visibleLow`/`visibleRangeLookback`/`visibleBarsApprox`) — nothing else in the script depended on it

## v1.1.15 — 2026-08-01
- Simplified on request: the rail no longer tries to reach the chart's true right edge — keeping the current price area clear of labels matters more than the rail visually touching the price scale. It's now a short, fixed-length segment (`extend.none` instead of `extend.right`) starting just past the label
- Default "Label offset · % of visible range" raised 45% → 65% (max 95%) — labels were still sitting too close to the current candle
- `gapTime`'s cap (protecting the label's own future anchor from Pine's bounded future-drawing distance) is kept and raised slightly to 300 bars, since dropping `extend.right` freed up some of the margin that cap used to have to share with the rail reaching the edge

## v1.1.14 — 2026-08-01
- Fixed both symptoms still present on 15m/1h after v1.1.13's stagger fix (labels back on top of candles, vertical bar unchanged): a distinct, third cause — Pine only allows drawings a bounded number of bars into the future (roughly 500), and a percentage of the *full* visible range on a 15m/1h chart showing a wide history could exceed that easily, silently clamping every level's label/rail to the same maximum allowed point regardless of the v1.1.13 per-level stagger (which only varies the *requested* position, not what Pine actually honors once clamped) — this produced the same shared-origin vertical bar via a different mechanism, and also explains labels snapping back to sit on price instead of at the configured offset
- `gapTime` is now capped at 250 bars regardless of the percentage calculation, leaving headroom under Pine's future-drawing limit for the smaller gap/seed/stagger amounts added on top

## v1.1.13 — 2026-08-01
- Fixed the vertical bar recurring yet again on 15m after v1.1.12's smaller gap (user report): the real cause was never "segment too short" specifically — every level's rail was computed with the exact same shared starting x-coordinate, and several differently-colored horizontal lines all beginning at the identical pixel column, stacked closely in price, read as a vertical bar at that column regardless of segment length. Tuning the length only ever changed the odds at whatever zoom got tested, never removed the shared origin that actually causes it
- Each rail's start (and its seed endpoint) is now staggered by its render rank — one `atlasBarMs` per level — so no two levels can ever share the same starting x-coordinate, closing this off structurally instead of via segment-size tuning

## v1.1.12 — 2026-08-01
- Shrunk the visual gap between the label and where the rail picks up (line length itself was already right, per feedback — just needed the label pulled closer to it): split what was one shared `railGap` value into a small `labelToRailGap` (label positioning, 3% of the offset gap) and a separately-sized rail seed segment (kept at 15%, unchanged) — narrowing the visible gap no longer risks shrinking the rail's own seed back toward the sub-pixel-collapse bug fixed in v1.1.10

## v1.1.11 — 2026-08-01
- Default "Label offset · % of visible range" raised 25% → 45%: labels were still sitting too close to price on the reference chart used during testing

## v1.1.10 — 2026-08-01
- Fixed the vertical colored bar through the label stack recurring on 15m/1h charts (user report): v1.1.9's rail used a fixed 1-bar seed segment (the two points defining its slope before `extend.right` takes over) — the exact same failure mode already fixed once for the price-to-label rail (now removed): on a chart with many bars visible, a 1-bar segment can round to sub-pixel width, and every level's rail shared that same near-identical starting point, visually merging into one bar
- Both the label's gap from price and the rail's seed segment are now sized as a percentage of the visible time range (`railGap`, 15% of the label offset gap, floored at 3 bars) instead of a fixed bar count — neither can collapse below a sane pixel width at any zoom level or timeframe

## v1.1.9 — 2026-08-01
- Removed the rail segment between price and the label (v1.1.8 ran it continuously from the last candle through the label's anchor to the true edge — reported as "the line goes too far"): the rail now starts just past the label's anchor and runs (`extend.right`) from there to the chart's true right edge. No line between price and the label anymore — just the label, then a short gap, then the rail to the scale
- Label anchor math is unchanged from v1.1.8 (`time + gapTime`, safe forward offset, not derived from the live visible edge)

## v1.1.8 — 2026-08-01
- Fixed labels ending up right back at the last candle with no visible rail at all (user report: exact opposite of the request): v1.1.7's `chart.right_visible_bar_time - gapTime` anchor formula subtracted from a value that can itself shift because of this script's own future-projected drawings, making the result behave unpredictably instead of landing near the true edge as intended
- Reverted to a simple forward offset from the last real bar (`time + gapTime`), which never depends on a value this script might itself be moving — predictable regardless of existing chart margin
- The rail now runs continuously (`extend.right`) from the last real bar straight through the label's anchor to the chart's true right edge, instead of trying to compute a separate stopping point short of the label — the label sits on top of the rail partway along it
- Default "Label offset · % of visible range" raised 5% → 25% (max raised to 80%) so the label sits meaningfully closer to the edge; can be pushed higher still, with a tooltip note that very high values can overshoot on charts with a lot of pre-existing right-side margin

## v1.1.7 — 2026-08-01
- Combined v1.1.5's edge-relative anchoring with v1.1.6's right-facing pointer style: the label now anchors close to the chart's true visible right edge (pulled back by a percentage of the visible time range, falling back to a guaranteed forward gap from price on charts with no right margin) instead of sitting a fixed gap forward from price — v1.1.6 put the label near price with a long rail to the scale, which the user wanted flipped: label near the scale, rail filling the gap back to price
- Since the anchor now sits far from price by construction, the label body's leftward growth (`label.style_label_right`) stays safely inside the rail's own empty space instead of relying mainly on a generous gap default — offset default lowered back 10% → 5%, since the primary risk this was guarding against no longer applies the same way
- Rail now runs `extend.none` from the last real bar to just short of the label, instead of `extend.right` — the label is already at the edge, so the rail no longer needs to reach past it

## v1.1.6 — 2026-08-01
- Reworked the right-edge layout on explicit request: v1.1.5's edge-relative anchoring left labels floating far from the actual price scale whenever the chart had a lot of right-side margin, and removing `extend.right` meant the rail no longer visually reached the scale at all
- Labels now sit a percentage-of-visible-range gap past the last real candle (pointer facing right, `label.style_label_right`), followed by a short gap, then a thin rail picks up and runs (`extend.right`) all the way to the chart's true right edge next to the price scale — label near price, line reaching the scale, as requested
- This reintroduces the label-body-grows-toward-price direction that earlier versions deliberately avoided after repeated overlap bugs. Two things keep it safe: labels no longer show price in the body at all (see next point — shorter text needs less clearance) and the default gap increased 6% → 10%. If labels start touching candles again on some chart, increasing "Label offset · % of visible range" is the first thing to try
- Labels no longer show price (or zone bounds/touch count numbers) in the visible body — only the code or full name, optionally with a touch-count suffix for S/R zones. Price, zone bounds, and touch count are still in the hover tooltip. "Label content" input simplified to Code/Full name (removed the "+ Price" variants)

## v1.1.5 — 2026-08-01
- Labels now anchor relative to the chart's true visible right edge (`chart.right_visible_bar_time` minus a percentage-of-visible-range buffer), so they sit close to the price scale whenever the chart has empty margin there — previously the anchor was computed forward from the last candle, which could leave a large, unintentional gap between the label and the actual edge on charts with a wide right margin
- Falls back to a guaranteed forward gap from the last real candle when the chart has little or no right-side margin, so price never gets crowded either way; default offset bumped 4% → 6% for more breathing room from price in that fallback case
- The rail now stops a couple of bars short of the label instead of running directly into it, leaving a small visible gap between the line and the label box; `extend.right` is no longer needed since the label itself already sits close to the true edge

## v1.1.4 — 2026-08-01
- Confirmed and fixed the real cause of the vertical colored bar through the label stack (user-verified: it goes away when both "Levels above price" and "Levels below price" are off, i.e. tied directly to level rendering): the rail's `railWidthInput` was a fixed bar count (default 5). On a tightly zoomed-in or low-timeframe chart with many bars visible, 5 bars can collapse to a near-invisible pixel width — with several price levels stacked closely (as spacing forces them to be), each rail's tiny near-zero-width "start cap", colored per level, visually merged into what looked like one solid, color-shifting vertical bar right where the labels begin
- Rails now start at `time` (the last real bar) instead of a fixed-bar-count segment before the label — always a substantial, clearly horizontal width regardless of zoom level, removing the failure mode outright. Removed the now-unnecessary "Rail width · bars" input
- Fixed a real input-wiring UX bug (reported: many toggles in Properties appeared to do nothing): module-level master switches (Enable day/week/month levels, Enable session ranges, Enable pivot points, Enable swing Fibonacci, Enable pivot-cluster S/R, Enable round numbers) were never visually grayed out outside the Custom preset, even though every non-Custom preset ignores their value entirely — clicking them looked like it should do something and silently did nothing. They (and their dependent sub-toggles) now correctly show as inactive/grayed unless the preset is Custom, with a tooltip explaining why
- Correctly left active regardless of preset: the S/R pivot-clustering calculation parameters and the swing-Fibonacci pivot-detection parameters (these always run, feeding every preset, not just Custom), and the round-number Major/Half/Quarter/step controls on the Everything preset specifically (which genuinely uses them, unlike Clean/Intraday/Structure)
- Note: TradingView's own settings-panel rendering of the "Show abbreviation legend" checkbox label (reported as white-on-white) is outside this script's control — `input.bool()` has no parameter to set its own label's text color; that's purely the platform's settings-dialog theme

## v1.1.3 — 2026-08-01
- Fixed label spacing being too tight whenever a rendered level (e.g. a prior week's high/low) sits outside the recent candles the chart is currently zoomed to: the spacing check used the visible candles' own high/low as a proxy for "visible price range," but TradingView auto-scales the y-axis to include our own rails/labels too — so on a tightly zoomed-in chart with widely spread reference levels, the true visible range was larger than what the candles alone showed, and spacing stayed too tight exactly when levels needed the most room
- Minimum label spacing now uses the combined range of the visible candles AND all eligible level prices, not candles alone

## v1.1.2 — 2026-08-01
- Fixed the vertical colored line running down through the label stack on low timeframes: the optional S/R "source zone" box (`showSourceZonesInput`) had its right edge set to `rightTime` — the same future offset point the labels anchor to — instead of `time` (the last real bar). A "historical zone" box has no business extending into the artificial future whitespace; when several S/R zones (S1/S2/R1/R2) were all shown at once, their right borders all landed at that same shared future x-coordinate, and stacked on top of each other they read as one solid, color-shifting vertical bar running straight through the label column
- The box now correctly spans from its historical start back in time up to *now*, matching what "drawn backward through the chart" in its own tooltip already promised

## v1.1.1 — 2026-08-01
- Fixed the real, structural cause of labels still overlapping the last few candles on daily/1h charts even after v1.0.2–v1.0.4: labels used `label.style_label_right`, so the label body grows *leftward* (toward price) from its anchor. Label width is a fixed pixel quantity Pine cannot query — no time-based percentage offset can guarantee it stays clear, because on a zoomed-out chart with narrow bars, the rendered text box is simply wider than the computed gap and reaches back over recent candles regardless of how that gap was computed
- Switched to `label.style_label_left`: the label's own anchor is its *left* edge, placed at the same offset point as before, but the body now grows rightward — toward the chart's true edge, away from price. This makes the overlap structurally impossible rather than merely less likely, independent of zoom level, timeframe, or label text length
- The reported vertical line on 1h charts is very likely not from Edge Atlas — nothing in this script draws a vertical line or a box tall enough to reach that far below the lowest rendered level. Toggle Edge Atlas's visibility off to confirm whether it's coming from another loaded indicator (e.g. Liquidity Hunter's event markers)

## v1.1.0 — 2026-08-01
- Added a "Trend Curves" module: up to three moving-average lines (Fast/Base/Anchor) plotted as familiar, always-on chart lines, fully separate from the right-edge level registry/rails
- Three presets, each giving the three lines a distinct role instead of measuring the same thing three ways: Responsive (JMA-style 9/21/50 — intraday/fast markets), Balanced (JMA-style 21 / EMA 50 / SMA 200 — default, movement + tradable trend + long-term anchor), Structural (EMA 20 / SMA 50 / SMA 200 — swing/position, filters short-term noise)
- Custom mode exposes type (JMA-style/EMA/SMA), length, and — only when a line's type is JMA-style — phase/power per line
- Lengths are never auto-adjusted by chart timeframe: 20 always means 20 bars of whatever timeframe is open, matching how the rest of Edge Atlas already treats "bars" as the unit
- New shared `f_jma` helper reuses the same open-source JMA approximation formula already used elsewhere in this repo (`jma_struct.pine`, `candle_pressure_response_jma.pine`); labeled "JMA-style" everywhere in the UI (not "JMA") since it's an approximation, not Mark Jurik's patented original algorithm
- Global controls: master toggle (off by default), source, line offset (bars), and a line-thickness-only "Visual emphasis" setting — colors stay editable per line via the chart's own Style tab, no color inputs added

## v1.0.4 — 2026-08-01
- Fixed labels still overlapping after v1.0.3's ATR-based spacing: ATR measures short-term volatility (e.g. a stock's typical hourly range), not the chart's visible price scale — a stock that rallied from single digits to the high $70s can have a tiny hourly ATR while the chart's visible y-axis still spans that entire multi-year range, so 0.5 ATR was far too small a gap in screen-pixel terms
- Minimum label spacing is now a percentage of the chart's actual visible price range (highest high to lowest low over the visible bars, via `ta.highest`/`ta.lowest` with a dynamic length tracking the current zoom), not ATR. New input "Minimum label spacing · % of visible price range" (default 3%) replaces "Minimum label spacing · ATR"
- The visible-viewport helper values (bar duration, visible time span, visible price range) now compute unconditionally on every bar instead of only inside the `barstate.islast` render block, since `ta.highest`/`ta.lowest` use a dynamic length and should track the window every bar rather than being called conditionally

## v1.0.3 — 2026-08-01
- Fixed nearby levels rendering as overlapping/adjacent label boxes that visually merge into a solid colored block at the right edge: levels are now greedily selected in priority order, skipping any candidate whose price is within a configurable ATR distance of an already-selected level. New input "Minimum label spacing · ATR" (default 0.5)
- On intraday charts with several close-together levels (e.g. daily/weekly reference levels bunched near current price), this is the fix for the reported "block instead of separate levels" look; it does not add positional stagger/merge (still open in `todo.md`), it selects the strongest non-crowded subset instead

## v1.0.2 — 2026-08-01
- Fixed labels still overlapping recent candles on charts zoomed out to show many bars: v1.0.1's fixed "N bars past the last candle" offset shrinks to just a few pixels once hundreds of bars are visible (e.g. years of weekly data), so the label boxes ended up back on top of price
- Replaced the fixed bar-count offset with a percentage of the chart's current visible time range (`chart.right_visible_bar_time - chart.left_visible_bar_time`), so the gap stays visually consistent regardless of zoom level; new input "Label offset · % of visible range" (default 4%) replaces "Label offset · bars"
- Rail width is now clamped against the resulting time gap instead of the raw bar offset, so it still can't reach back into the last real candle at any zoom level

## v1.0.1 — 2026-08-01
- Fixed "text" cannot be used as a variable or function name (CE10150) — renamed the reserved `text` local to `labelText`
- Fixed labels overlapping the last few visible candles: the default "Visible Right Edge" anchor placed the label anchor at `chart.right_visible_bar_time`, which equals the last real candle's time on any chart without manually scrolled-in whitespace — since labels are right-anchored, their body then painted backward over the price bars
- Replaced the two-mode anchor (Visible Right Edge / Last Bar + Offset) with a single fixed "Label offset · bars" input; labels now always sit a fixed number of bars past the last real candle, in the empty right margin, regardless of zoom or scroll state
- Rail lines now use `extend.right` so they continue visually to the chart's true right edge next to the price scale, while the label itself stays clear of price
- Rail width is now clamped below the label offset so a misconfigured rail can never reach back into the last real candle

## v1.0.0 — 2026-08-01
- Initial release: right-edge price-level atlas
- Previous/current day, week, and month reference levels
- Asia/London/New York session ranges
- Traditional and Fibonacci pivot points
- Swing-based Fibonacci retracements and extensions
- Pivot-cluster support/resistance zones
- Automatic or manual round-number levels
- Shared level registry with distance/priority/count/side filters
- Clean/Intraday/Structure/Everything/Custom presets
- Not yet verified against the TradingView Pine compiler — see `todo.md`
