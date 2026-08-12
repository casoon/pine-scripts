# Changelog

## v2.2.1 — 2026-08-12
- Fixed poor label contrast (Retracement %, HH/HL/LH/LL pivot labels, rejected-pivot diagnostics): all three paired a highly transparent tinted background (e.g. 75-85% transparency) with fully-opaque colored text, so readability depended on whatever was behind the label — the Retracement % label was the worst case, since its default `color.new(color.gray, 35)` "Developing Color" made even the text itself partially transparent. All three now use a fully opaque background in the relevant color plus a new `f_contrastText()` helper that auto-picks black or white text from the background's actual luminance, so labels stay readable regardless of which Up/Down/Developing color the user configures. Pivot dot markers (the "•" style, no background) are unaffected — different case, not a background/text contrast pair

## v2.2.0 — 2026-08-11
- Added an independent Secondary ZigZag ("Show Secondary ZigZag", Dual ZigZag): a second, fully independent pivot configuration (own Pivot Depth, Minimum Pivot Spacing, Deviation Multiplier on top of the primary Reversal Mode) on the same Calculation Timeframe as the primary ZigZag — e.g. a coarser "Structural" primary alongside a finer "Internal" secondary. Confirmed-only like Level 2 (no live/developing leg, retracement, or diagnostics). Reuses the primary engine's already-buffered lower-timeframe bar data with its own scan window in LTF mode, so no second `request.security_lower_tf()` call is needed — only the higher/chart-timeframe path needs its own `request.security()` calls, since `ta.pivothigh`/`ta.pivotlow` are depth-specific
- This closes out the original TODO backlog — no open items remain in the script

## v2.1.0 — 2026-08-11
- Added an optional recursive Level-2 ZigZag ("Show Recursive (Level 2) ZigZag"): a second, coarser ZigZag built from the CONFIRMED Level-1 pivot stream instead of raw price. No Depth scan or live/developing tracking needed — L1 already guarantees each fed-in point is a genuine local extremum and the stream already strictly alternates, so L2 only needs its own Alternation/Backstep(in L1-pivot-count)/Deviation(reusing L1's Reversal Mode, scaled by a new multiplier) pass, run at the top level to work around Pine's function-can't-reassign-script-vars limitation, same as the Level-1 event handlers

## v2.0.0 — 2026-08-10
- Added a true Lower-Timeframe Engine: choosing a Calculation Timeframe lower than the chart no longer falls back to the chart timeframe with a warning — `request.security_lower_tf()` buffers every lower-timeframe bar and a manual scanner finds local extrema over it (`ta.pivothigh`/`ta.pivotlow` can't be driven through `request.security()` for a lower timeframe, since that only returns one value per chart bar). All downstream logic (alternation, backstep, deviation, activePivot, developing leg, drawing) is unchanged — only the pivot source is swapped in
- Known simplification: at most one new high pivot and one new low pivot surface per chart bar, matching the higher-timeframe path's own grain; an extreme LTF ratio confirming more than one same-type pivot within a single chart bar only surfaces the most recent
- Removed the "Show Invalid-Timeframe Warning" toggle and its fallback — a lower timeframe is no longer invalid
- Live extension/reversal tracking now bypasses `request.security()` for BOTH "same as chart" and a genuine lower timeframe (previously only "same as chart"), using plain `high`/`low`/`time` in both cases; only a genuine higher timeframe still goes through `request.security()`

## v1.2.1 — 2026-08-10
- Fixed the developing/reversal-candidate line (and its Retracement % label) freezing mid-chart during a recovery that hasn't yet set a new extreme: its endpoint was anchored to `developingExtremeTime` (the bar the extreme actually occurred on), which only advances on a new extreme, instead of the current bar — so once price stopped setting new extremes but also hadn't reversed enough to confirm, the line's right edge stayed pinned in place while price and bars kept moving, leaving a visible gap of undrawn candles. Both now track the current bar's time every bar; only the price stays pinned to the extreme until it's actually exceeded

## v1.2.0 — 2026-08-10
- Added a live Retracement % label on the reversal-candidate leg, showing how deep the current pullback is relative to the leg that preceded it (toggle: "Show Retracement %")
- Added optional Pivot Confirmation Diagnostics ("Show Rejected Pivot Diagnostics", off by default): marks a confirmed pivot candidate that got rejected by Minimum Pivot Spacing or the Reversal Filter, and which one blocked it
- Fixed a same-bar ambiguity: a large outside bar confirming both a pivot high and low on the same bar is now resolved with an explicit tie-break (the one continuing the current alternation is processed; the other defers to its own event) instead of an arbitrary high-before-low ordering
- ATR-based deviation checks now consistently reference the ATR at the swing point's own pivot bar (`ta.atr(atrLength)[pivotDepth]`) instead of the later confirmation bar, for both the seed and the active/last pivot
- pivotLabels/pivotDots trimming now shares one combined budget (plus a small fixed budget for the new diagnostics) so the two pools stay safely under Pine's 500-label cap instead of being trimmed independently

## v1.1.0 — 2026-08-10
- Fixed a state/drawing desync: `lastPivotPrice`/`lastPivotTime` (the backend gating reference) and the live-drawn endpoint could diverge once price extended past a confirmed pivot, so a subsequent reversal leg would start drawing from the stale confirmed price/time instead of where the chart last visually ended, producing a disconnected/jumping segment. Introduced a dedicated `activePivotPrice`/`activePivotTime` that is the single source of truth for the drawn endpoint — updated monotonically by live extension, same-side confirmed replacement, and reversal confirmation alike — while `lastPivotPrice`/`lastPivotTime` stay untouched as the backend deviation/backstep reference

## v1.0.3 — 2026-08-10
- The live extension/reversal tracking no longer routes through `request.security()` when Calculation Timeframe is the chart's own timeframe — that call still synchronizes like a higher-timeframe merge internally and could lag the bar-by-bar highs/lows the live line-growing depends on. Plain `high`/`low`/`time` is used directly in that (default) case; a genuine higher timeframe still goes through `request.security()` as before

## v1.0.2 — 2026-08-10
- Extension state no longer draws a separate gray line: the last confirmed leg (line + label/dot) now grows live to follow price while it keeps pushing past the last confirmed pivot. The gray dashed line is now reserved exclusively for a genuine reversal candidate once that extension stops

## v1.0.1 — 2026-08-10
- Fixed the developing leg freezing whenever price kept pushing past the last confirmed pivot in the same direction (expected with a large Pivot Depth): it now tracks a live "anchor" that extends with price, drawn as its own dashed segment, and only starts the opposite-direction reversal-candidate leg once the anchor stops extending

## v1.0.0 — 2026-08-10
- Initial release: depth/backstep/deviation/alternation ZigZag engine with Percent, ATR, and Hybrid reversal modes
- True higher-timeframe calculation with pivot-time projection onto the chart; lower-timeframe requests are rejected with a fallback warning
- Confirmed ZigZag structure plus a separately styled, non-repainting-distinct "Developing Leg" for the unconfirmed final segment
- HH/HL/LH/LL structure labels, pivot price, and swing-change % labels; optional pivot dot markers
