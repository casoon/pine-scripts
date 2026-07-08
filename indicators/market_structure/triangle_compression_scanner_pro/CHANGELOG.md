# Changelog

## v1.12 — 2026-07-06
- Idea evaluated from a reference indicator (Wedge and Flag Finder by Trendoscope, MPL/CC BY-NC-SA — analyzed for technique only, no code adopted per license and repo convention): its validity check tests every single bar's high/low against the channel, not just the chosen swing points. Our `insideOk` only ever checked the sampled swing highs/lows — a bar between two swings could poke through the channel without ever registering as a swing itself, so a "triangle" could hold only at the sampled points, not for real across the whole window
- Added `barsInsideOk` as a new hard veto (like `structureOk`): loops every bar from `windowStartX` to `windowEndX` and rejects the pattern if any bar's high/low breaches either boundary beyond `touchTolAtr`. Added `max_bars_back(high, 2000)`/`max_bars_back(low, 2000)` since the check can index a few hundred bars back with a variable (non-constant) offset
- New "Bars Inside (Veto)" row in the debug table

## v1.11 — 2026-07-06
- Proactive review (not log-triggered): the dashboard's "Best Score"/"Type"/"Window" showed the raw best-scoring window-end candidate regardless of whether it could ever actually be tracked — a stillborn or already-aged candidate could show a high score while nothing was ever drawn, since neither `stillOpen` nor `alreadyAged` gate `best`
- Added `bestTrackable`, tracked alongside `best` but only updated from candidates that pass both gates; the dashboard now shows the actually tracked pattern when one exists (`f_find_best_active_index`, same fix as Wolfe Wave Scanner Pro), falling back to `bestTrackable` instead of the raw `best`. The debug table still shows raw `best`, since explaining why the overall best-scoring shape isn't firing is exactly its job
- `keptPatterns` (bookkeeping for `Aufgelöste Patterns behalten`, on by default) grew unbounded across the entire chart history with no cleanup — every resolved pattern piled up forever, growing the linear `f_find_overlap_index(c, keptPatterns)` scan cost on every search event, year after year. Now trimmed on the same age basis as live patterns: an entry old enough that even a live tracked pattern of the same age would have expired can never usefully be compared against again, since no future search window reaches that far back

## v1.10 — 2026-07-06
- Same fix as Broadening Wedge Scanner Pro v1.11, log-confirmed there: the ATR-drift safety net was still firing on 92% of expirations, with 67% of fired patterns dying on the exact same bar — a candidate aged between 1.0×-1.5× its own window width has a boundary already frozen at the cap by fire time, and that frozen value is very often more than 20× ATR from current price simply because ATR measures bar-to-bar noise, not the honest cumulative price range a pattern's own real slope implies over dozens-to-hundreds of bars
- Removed `Max. Linien-Drift` entirely — `Max. Pattern-Alter` (scaled to each pattern's own window width, not a flat ATR distance) is now the sole cleanup mechanism

## v1.9 — 2026-07-06
- Same fix as Broadening Wedge Scanner Pro v1.10, log-confirmed there: a candidate fired and then expired on the exact same bar (`age=220` against an 81-bar window, 1.5×=121.5) — `Suchbereich letzte Swings` can resurface a window-end that's already past its own age-expiry threshold by the time it's found, wasting a cycle firing something that was never going to live
- Now gated before firing (`PATTERN SKIPPED (already aged)`) instead of firing and immediately expiring it, so a genuinely fresher (even if lower-scoring) candidate gets a chance at the one tracking slot instead of it being burned on a dead-on-arrival re-discovery

## v1.8 — 2026-07-06
- Same fix as Broadening Wedge Scanner Pro v1.9, log-confirmed there across 4 exports (10800+ FIRED events, ~100% ending via ATR-drift, essentially never a real breakout): the drift check was reactively killing almost everything, because extending a fitted slope forever every bar guarantees it eventually drifts far from price
- Fixed at the root instead: a tracked triangle's boundary now extends at most one more window-width past its own formation (`f_line_cap_x`), then FREEZES — both the drawn line and the level used for breakout/expiration checks stop moving forward once that fixed budget is used up. The "still open" check at discovery time uses the same frozen evaluation, so an old-but-plausible window-end candidate isn't rejected as stillborn for a reason unrelated to an actual breakout
- `Max. Pattern-Alter` default lowered 3.0× → 1.5× (now the primary cleanup mechanism); `Max. Linien-Drift` default raised 5.0× → 20.0× ATR and relabeled as a safety net, since the line can no longer drift unboundedly by construction

## v1.7 — 2026-07-06
- The v1.5 age-based expiration only counted bars, which doesn't catch every runaway line: a steep boundary can drift into implausible territory well before the age cap trips, while a flat one could stay sane far past it
- Added `Max. Linien-Drift (ATR-Multiple)` (default 5.0×): a tracked triangle now also expires if either boundary's live projected level has drifted more than that many ATRs from the current close, regardless of bar-count age — checks the actual symptom (drifted price) instead of a proxy (elapsed bars)

## v1.6 — 2026-07-06
- Chart-confirmed: the v1.3 least-squares fit still didn't visually hug the actual touches — regression minimizes error across every point at once, pulling the line through the middle of the point cloud instead of tracing the real boundary, so several highs/lows sat clearly inside the drawn lines instead of near them
- Replaced the least-squares fit with `f_best_boundary`: searches all pairs of real touch points and picks the one with the fewest violations (points poking through the wrong side beyond tolerance) and the most touches — the classic way a chartist actually draws a trendline, through real highs/lows that define the edge, not a computed average

## v1.5 — 2026-07-06
- Chart-confirmed on Broadening Wedge Scanner Pro (same architecture, same bug — NATGAS 4h): a pattern's boundary line is a straight fit on a fixed window, extrapolated further every bar it stays open (`lineAheadBars`). Left unresolved for long enough, that extrapolation drifts to nonsensical prices far outside anything the symbol has ever traded at
- Added `Max. Pattern-Alter (× Fensterbreite)` (default 3.0×): a tracked pattern that hasn't broken out within that multiple of its own formation length now expires automatically (logged as `PATTERN EXPIRED`) instead of drifting indefinitely — matches the classic TA convention that an unresolved pattern past a reasonable timeframe is stale, not live

## v1.4 — 2026-07-06
- Chart-confirmed clutter: several fanning-out triangles from largely the same early swings were tracked and drawn at once. `Max. gleichzeitige Patterns` now defaults to 1 — the eviction logic added in v1.1 means a new, better-scoring candidate still replaces the current one automatically, so only the single highest-scoring triangle is shown at a time. Raise the input if multiple genuinely separate triangles at once is wanted

## v1.3 — 2026-07-06
- Chart-confirmed: boundary lines were anchored on only their first and last touch in the window, so a single early or late outlier swing could drag the whole line away from every touch in between — a triangle could score well on the ratio-based `touchOk` while visually missing most of its own touches. Boundaries are now a least-squares fit through every high/low in the window instead of just its two endpoint touches

## v1.2 — 2026-07-06
- Boundary lines no longer use `extend.right` (drawn all the way to the chart's right edge) — they now end a configurable `Linien-Überstand (Bars)` (default 10) past the current bar and advance bar by bar while the triangle stays open, so they keep pace with the chart without spanning it

## v1.1 — 2026-07-06
- Fixed: once `maxConcurrentPatterns` tracked triangles were all still open, every new non-overlapping candidate was silently discarded forever, even if it clearly outscored the weakest tracked one — the cap is now backfilled by evicting the weakest tracked triangle when a better candidate is found (ported from the same fix in Wolfe Wave Scanner Pro)
- Fixed: 2-3 same-direction triangles could end up tracked at once in overlap chains the pairwise insertion check missed (A overlaps B, B overlaps C, but A and C don't overlap directly) — added a dedupe pass that keeps only the higher-scoring pattern of each overlapping pair
- Refactored the duplicated "finalize lines to a bounded segment + move to keptPatterns" logic (previously copy-pasted at pattern replacement and breakout resolution) into one shared helper, now also reused by the new eviction and dedupe paths

## v1.0 — 2026-07-06
- Initial release: sliding-window triangle scanner (symmetric/ascending/descending) with weighted 0-100 score (structure, compression, touch quality, line quality, duration)
- Tracks multiple simultaneously valid, non-overlapping triangles at once, each with independent drawings and breakout state, built on the same multi-pattern architecture as Wolfe Wave Scanner Pro v4.0
- Live breakout tracking (either boundary resolves the pattern) with dedicated bull/bear alerts
- Score-breakdown debug table, optional Pine Logs output
- Compression check uses signed (not absolute) width so a triangle whose lines have already crossed inside the window isn't scored as compressing
- A pattern only starts tracking if price is still between its own boundaries at detection time — pivot-confirmation lag otherwise means most patterns would already be broken the instant they're found
- Breakout detection has a one-bar grace period on a pattern's own creation bar (avoids an instant breakout label on the same bar a triangle is drawn) without letting an already-broken pattern get stuck in tracking forever
- Kept (resolved but retained) triangles are scored against later overlapping candidates — a new pattern only replaces a kept one at the same spot if it scores higher; otherwise it's skipped
- Resolved triangles that are kept on the chart (`Aufgelöste Patterns behalten`, on by default) are finalized into bounded segments ending at the breakout bar, instead of extending indefinitely to nonsensical extrapolated prices
- Added an inside-containment check (every swing must sit within its boundary line's tolerance) to line quality
- Dropped the near-miss candidate marker — it re-displayed the same stale evaluation across every bar between swing confirmations instead of a discrete signal, and it never changed a trading decision
