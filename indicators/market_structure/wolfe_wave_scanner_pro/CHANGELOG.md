# Changelog

## v3.3 — 2026-07-06
- The 1-4 trigger line and its vertical apex marker now use the bull/bear color (`col`, same as the wedge lines) instead of a fixed yellow `EPA-Ziel` color, and are drawn thinner (width 1 instead of 2) so they read as a secondary reference against the bolder wedge
- Removed the now-unused `EPA-Ziel` color input

## v3.2 — 2026-07-06
- The v3.1 fix closed the gap at the top (marker now reaches the red apex) but opened a new one at the bottom: the marker ran down to `y5`, while the 1-4 diagonal line actually ends at `targetETA` — which is usually much further away than y5 (the 1-4 target is typically a bigger move than the channel apex itself), leaving the diagonal's real endpoint disconnected from the marker
- The vertical marker now connects the red crossing price (`apexY13`) directly to the 1-4 line's actual endpoint (`targetETA`) — one continuous line from the red apex to where the diagonal line actually terminates, no gap on either end

## v3.1 — 2026-07-06
- Fixed a visible gap between the 1-4 line's endpoint and the red channel apex: the vertical marker started at `targetETA` (line 1-4's price at the apex time), which sits at the same bar as but a different price than where the red 1-3/2-4 lines actually cross. The vertical marker now spans from the red lines' own crossing price down to point 5, so it always visibly reaches the apex instead of stopping short of it

## v3.0 — 2026-07-06
- Simplified back to one yellow concept instead of three: dropped the separate horizontal "channel apex" EPA projection line entirely (per feedback that it "didn't belong there") and reverted `targetETA` to the classic definition — price on line 1-4 at the apex time
- The 1-4 trigger line and the vertical apex marker now both anchor on the exact same `targetETA` value, so they always visibly connect at one point instead of two lines that were close but didn't quite meet

## v2.9 — 2026-07-06
- Re-added the classic 1-4 "trigger line" (dropped entirely in v2.7 when EPA was redefined to the channel apex): it now draws again from point 1, visibly through point 4, up to the apex bar — as its own reference line alongside (not instead of) the channel-apex EPA projection

## v2.8 — 2026-07-06
- Fixed the yellow horizontal EPA line spanning the entire chart width: `extend.right` extends past the *second* point, in the direction from the first point to the second — it does not simply mean "extends towards increasing x". Since `etaBar` (the apex projection) is often further into the future than the current `bar_index`, passing `(etaBar, ...)` as the first point and `(bar_index, ...)` as the second reversed the direction whenever etaBar > bar_index, making "extend right" actually run left across the whole visible chart
- Fixed by sorting the two x-coordinates first (`math.min`/`math.max`) so the second point passed to `line.new` is always the larger one, guaranteeing the extension runs forward regardless of whether the apex projects ahead of or behind the current bar

## v2.7 — 2026-07-06
- Redefined "EPA" as a deliberate simplification: it's now literally the channel apex — the same point the 1-3/2-4 boundary lines are drawn to — instead of the theoretically-distinct price on line 1-4 at the apex time. Those two were always close but never exactly equal, which is why the yellow line/label could never be made to visually "start" at the red lines' crossing point no matter how it was anchored
- The yellow target line now starts exactly at that shared apex point and projects forward as a plain horizontal line — no separate anchoring to points 1/4 needed, since its start point is the same one the red lines already end at
- `targetNow` (used only internally for the `reward` scoring criterion) is unaffected

## v2.6 — 2026-07-06
- Reverted the v2.5 "EPA line starts at the apex" change: cutting the line off before point 1/4 made it impossible to visually verify it's actually the 1-4 line (nothing was drawn there anymore, so it looked "shifted"/arbitrary). The EPA line is back to starting at point 1, passing visibly through point 4, and now extends (`extend.right`) on past the apex instead of stopping there — anchored and verifiable, and still shows the forward projection

## v2.5 — 2026-07-06
- Channel boundaries (1-3, 2-4) no longer extend indefinitely (`extend.right`) past the apex — they now stop exactly at the apex bar (`etaBar`), since there's nothing meaningful to show once the channel has closed
- The EPA line no longer draws the full 1-4 line back to point 1 — it now starts exactly at the apex (`etaBar`/`targetETA`) and extends forward from there, showing only the forward-looking target projection

## v2.4 — 2026-07-06
- Fixed the actual complaint behind "the intersection point isn't respected": the "EPA" label (score box + dashboard) displayed `targetNow` — the price on line 1-4 *at point 5's own bar* — while the drawn yellow projection line goes to `targetETA` — the price on line 1-4 *at the computed apex/convergence bar*. Two different numbers under one "EPA" label, so the displayed value never matched what the chart actually showed converging
- Both displays now show `targetETA`, matching the classic "Estimated Price at Arrival" definition and the line that's actually drawn. `targetNow` remains an internal-only value used for the `reward` scoring criterion (grading how far point 5 overshoots line 1-4), never shown to the user

## v2.3 — 2026-07-06
- Fixed the next chart-confirmed issue: after v2.2, a real example showed 2-4 near-vertical (a short, steep leg) crossing an almost-flat 1-3 — mathematically "converging" (same sign, crosses within bounds) but nothing like a real wedge visually
- `sameDirection` was also still comparing the slope of the no-longer-drawn 1-5 line against 2-4 instead of the actually-drawn 1-3 boundary — inconsistent since the v2.2 redesign
- Fixed both: slope comparison now uses 1-3 (matching what's drawn), and `contractionOk` additionally requires the two boundary slopes to be within a 3x magnitude ratio of each other (`slopesComparable`) — a near-flat line paired with a near-vertical one no longer qualifies, even if they technically cross in the right place

## v2.2 — 2026-07-06
- Fixed the actual convergence lines: v2.1 extended 2-4 forward but left it converging against the bold, non-extended 1-5 "outline" line — which has a different slope than 1-3 and made it look like the wrong two lines were meeting (confirmed from a chart example: the two extended lines diverged sharply instead of crossing near the EPA point)
- The two real channel boundaries — 1-3 and 2-4 — are now both drawn bold and extended forward in the same style, so they visibly converge exactly at the apex bar the EPA line ends at. The old 1-5 "outline" line is dropped entirely (it isn't a real boundary and only added a third, differently-angled line into the mix)

## v2.1 — 2026-07-06
- Fixed visual feedback from a chart example: the vertical marker at the EPA apex was barely visible (thin dotted, width 1) next to the bold main EPA line — both now use the same dashed/width-2 style
- Extended the 2-4 channel line forward (`extend.right`): it now visibly converges with the already-extended 1-3 line at the true apex bar (the same bar the EPA line ends at), instead of only implying that convergence through the separate EPA projection

## v2.0 — 2026-07-06
- Fixed a visual-quality gap flagged from real chart examples: two fired "Score 100" patterns had channels that clearly didn't look like a converging wedge — the 2-4 line ran roughly parallel to / above the 1-5 line without visibly closing in
- Root cause: `contraction` only compared channel width at the two endpoints (x1 vs x5) and accepted *any* narrowing, even 1%. A channel that bulges outward around points 2/3/4 before barely re-narrowing at the very end passed just as easily as a real wedge
- Fixed: `contraction` now requires (1) a real contraction ratio — end width ≤ 70% of start width — and (2) monotonic narrowing through the midpoint (checked at x3): `widthStart >= widthMid >= widthEnd`. A channel that widens anywhere before narrowing again no longer qualifies

## v1.9 — 2026-07-06
- Fixed a runtime crash: `Bar index value of the x2 argument (...) in line.new() is too far from the current bar index` on the EPA line draw. `etaBar`/`targetETA` used the raw 1-3/2-4 intersection (`xi`) whenever it wasn't `na` — but near-parallel (not exactly parallel) lines can push that intersection absurdly far from point 5, or even negative, well outside anything `line.new()` accepts
- Fixed by always bounding the drawn/measured apex to `x5 + 2×patternWidth` when the true intersection isn't sane (`xiBounded`), independent of `etaOk` (which still grades the real intersection for scoring). The `not na(best.targetETA)` draw-guard was removed since `targetETA` is unconditionally bounded now and can no longer be `na`

## v1.8 — 2026-07-06
- Found the reason the last drawn pattern was thousands of bars behind the live edge across all 4 re-test files: `newSwing = sz != prevSwingCount` compares the swing array's *length*, not its content. Once `array.size(swings)` reaches its `Max. gespeicherte Swings` cap, every new swing is paired with an `array.shift` — the length stops changing forever, `newSwing` goes permanently `false`, and the search never runs again from that point on (confirmed in the logs: zero `WWSP SEARCH` lines after the first bar where `count` hit the cap, in all 4 files)
- Fixed by tracking the newest swing's bar index instead of the array length (`lastSwingX`) — this changes on every push *and* every in-place replace (when a same-direction swing gets superseded by a more extreme one), which a length-based check missed entirely once capped

## v1.7 — 2026-07-06
- Confirmed via Pine Logs across 4 symbols/timeframes that the v1.6 sentinel fix works: `WWSP PATTERN FIRED` now appears 12-22 times per test file (was 0 before), with both bull and bear signals and correct invalidation follow-through
- Re-tightened `bullStructure`/`bearStructure` back to the full core shape (`y5 < y3` for bull / `y5 > y3` for bear restored) now that the real blocker (the `na`-comparison dedup bug) is fixed — point 4's channel containment stays a separately-scored criterion, not re-merged into the hard gate
- Reset debug-only defaults back to production values: `Swing-Stärke` 3→6, `Suchbereich letzte Swings` 30→16, `Mindestqualität` 45→60. `Pine-Logs aktivieren` stays available (off by default) for future troubleshooting

## v1.6-debug — 2026-07-06
- Found the actual root cause, visible directly in the requested Pine Logs: across 4 test files, `valid=true` with `best.score=100` occurred 73-76 times each, yet `PATTERN FIRED` never appeared once. The search and scoring were correct all along
- The bug: `lastPatternX5`/`lastPatternDir` were initialized to `na`, and the dedup check compared directly against it (`best.x5 != lastPatternX5`) — a direct `!=`/`==` comparison against `na` is unreliable in Pine (always evaluates falsy; the documented fix is to use `na()`, never compare directly). `newPattern` was therefore always `false`, no matter how many valid patterns the search found
- Fixed by using real sentinel values instead of `na` (`-1` for x5, `0` for direction — bar indices are always ≥0 and direction is always ±1, so neither can collide with a genuine value)
- This means the v1.2-v1.5 loosening (thresholds, structure relaxation, non-consecutive search) were fixing real but secondary issues — the primary reason nothing drew was this dedup check. Worth re-testing with the debug defaults first, then re-tightening `bullStructure`/`bearStructure` (the y5-vs-y3 check) and dialing `Mindestqualität`/`Swing-Stärke`/`Suchbereich` back to sane production values once confirmed working

## v1.5-debug — 2026-07-06
- Added Pine Logs output for debugging (`Pine-Logs aktivieren (Fehlersuche)`, off by default): `WWSP SWING` on every new confirmed swing (dir/x/y/running count), `WWSP SEARCH` on every search event (how many 5-point combinations were evaluated, how many had `structureOk`, and the full per-criterion breakdown of the winning candidate), `WWSP SEARCH SKIPPED` while there aren't 5 swings yet, `WWSP PATTERN FIRED` and `WWSP INVALIDATED` on those events
- Open the Pine Logs pane (bottom toolbar, terminal icon) after enabling this to see: whether swings are forming at all, how many combinations the search actually evaluates, and which single criterion is missing from the best candidate each time

## v1.4-debug — 2026-07-06
- Fixed the remaining reason patterns went stale: `i5` was pinned to `sz - 1` (the freshest swing), so a Wolfe wave that was already 2-10 swings old the moment it completed was never checked again once one more swing formed. The search now tries every valid point-5 anchor within `Suchbereich letzte Swings`, not just the newest one
- Temporarily loosened the structure gate further for debugging: dropped the `y5 < y3` (bull) / `y5 > y3` (bear) requirement, leaving only `y3 vs y1` — `p5ZoneOk` grades point 5's actual position instead of a second hard AND
- Debug-only parameter defaults for this pass: `Mindestqualität` 45, `Kandidat-Mindestscore` 25, `Swing-Stärke` 3, `Suchbereich letzte Swings` 30 — deliberately loose to confirm the scanner can find *anything*. Re-tighten before relying on this for real signals; the wider search + smaller `Swing-Stärke` also multiply the per-search-event cost substantially (many point-5 anchors × a full combinatorial scan each), worth checking for slowdowns on long histories

## v1.3 — 2026-07-06
- Found the actual reason nothing drew even after the v1.2 relaxation: `bullStructure`/`bearStructure` required a hard AND of 4 conditions (full ordering `y5<y3<y1<y4<y2`), and this `structureOk` flag gated *everything* — the confirmed signal, the candidate marker, and the candidate wedge. One strict sub-check (point 4 must sit exactly inside the 1-2 channel) was enough to zero out the whole pattern, no matter how good the rest of the shape was
- Split that out: `bullStructure`/`bearStructure` now only require the core, non-negotiable shape (lows declining for bull / highs rising for bear across points 1-3-5); point 4's channel containment is now a separate scored criterion (`channelOk`, 8 points) instead of a hard gate
- Rebalanced score: contraction+slope 20→12, new channel-containment 8, everything else unchanged (still sums to 100)

## v1.2 — 2026-07-06
- Fixed the "best-of-window" search: v1.1 still only checked 5 *consecutive* swings. Now searches all valid non-consecutive 5-point combinations within `Suchbereich letzte Swings` (point 5 anchored to the freshest swing, points 1-4 chosen combinatorially from the alternating swing chain) — a Wolfe wave spanning e.g. swings 1,3,5,7,9 is no longer discarded
- Relaxed defaults that made the scanner "malen" almost nothing: `Mindestqualität` 72→60, `Punkt-5-Toleranz ATR` 1.0→1.5, `Max. Zielentfernung ATR-Multiple` 3.0→8.0, `Kandidat-Mindestscore` 55→45
- P5-zone check is now a symmetric distance (`|y5 - line13At5| <= atr * p5TolAtr`) instead of a one-sided inequality that accepted arbitrarily deep overshoots on one side
- Fixed candidate marker: `not best.bull` no longer implies "bearish" — both plotshape conditions now require `best.structureOk`, so an invalid candidate (neither bull nor bear) can't paint a false bear circle
- Added a lightweight candidate wedge (dashed, 2 lines) drawn for the current best-in-window pattern even when it's only a near-miss, so a sub-threshold candidate's geometry is visible instead of only the tiny plotshape marker
- Guarded the new combinatorial search loops against Pine's `for i = A to B` auto-reversing (and stepping on an out-of-bounds array index) whenever the same/opposite-direction candidate lists are too small

## v1.1 — 2026-07-06
- Replaced literal-last-5-swings scan with a consecutive-window search across `Suchbereich letzte Swings` — a strong pattern is no longer lost once one more (unrelated) swing forms
- Tightened structure rule: point 3 must undercut/exceed point 1, point 5 must extend beyond point 3, point 4 must stay contained between points 1 and 2 (replaces the looser "point 2/5 are the global extremes" check)
- Rebalanced score to 7 weighted criteria (structure 30, contraction+slope 20, apex convergence 15, P5-zone 15, reward 10, timing 5, symmetry 5); reward is now capped to `Max. Zielentfernung ATR-Multiple` so a near-parallel wedge can't claim an unrealistic target
- Added live invalidation tracking: a fired pattern's point-5 level (± 0.5 ATR) is monitored every bar; a break marks it invalidated and fires `WWSP · INVALIDATED`
- Added near-miss candidate marker (Watch signal, visual only, threshold configurable) and a light-theme dashboard (status/score/bias/EPA/invalidation)
- Replaced the point-array pattern-history dedup with simple last-fired-pattern tracking (`x5`/direction), matching the new best-of-window search
- Kept the v1.0 apex fix (EPA convergence computed from lines 1-3/2-4, not 1-5/2-4) and the structure-must-match-score-threshold guard

## v1.0 — 2026-07-06
- Initial release: 5-point Wolfe Wave scanner with weighted 0-100 score (structure, contraction/slope, convergence, P5-zone, reward, timing)
- EPA target projected from the correct 1-3/2-4 apex (line 1-4 extended to the apex time), not an approximation via line 1-5
- Overlap dedup uses true interval overlap between the candidate and stored pattern ranges
- Bull/bear signals require both the matching pivot sequence and the score threshold — sequence-agnostic criteria alone can't fire a signal
- Optional score-breakdown debug table
- Alerts standardized to `WWSP · EVENT · {{ticker}} {{interval}}` with bar-close confirmation gating
