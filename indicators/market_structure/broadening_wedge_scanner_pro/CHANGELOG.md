# Changelog

## v1.13 — 2026-07-06
- Idea evaluated from a reference indicator (Wedge and Flag Finder by Trendoscope, MPL/CC BY-NC-SA — analyzed for technique only, no code adopted per license and repo convention): its validity check tests every single bar's high/low against the channel, not just the chosen swing points. This scanner only ever checked the sampled swing highs/lows via `touchOk` — a bar between two swings could poke through the channel without ever registering as a swing itself, so a "wedge" could hold only at the sampled points, not for real across the whole window
- Added `barsInsideOk` as a new hard veto (like `structureOk`): loops every bar from `windowStartX` to `windowEndX` and rejects the pattern if any bar's high/low breaches either boundary beyond `touchTolAtr`. Added `max_bars_back(high, 2000)`/`max_bars_back(low, 2000)` since the check can index a few hundred bars back with a variable (non-constant) offset
- New "Bars Inside (Veto)" row in the debug table

## v1.12 — 2026-07-06
- Proactive review (not log-triggered): the dashboard's "Best Score"/"Type"/"Window" showed the raw best-scoring window-end candidate regardless of whether it could ever actually be tracked — a stillborn or already-aged candidate could show e.g. "Best Score 100/60, Descending Broadening" while nothing was ever drawn, since neither `stillOpen` nor `alreadyAged` gate `best`
- Added `bestTrackable`, tracked alongside `best` but only updated from candidates that pass both gates; the dashboard now shows the actually tracked pattern when one exists (`f_find_best_active_index`, same fix as Wolfe Wave Scanner Pro), falling back to `bestTrackable` instead of the raw `best`. The debug table still shows raw `best`, since explaining why the overall best-scoring shape isn't firing is exactly its job

## v1.11 — 2026-07-06
- Log-confirmed the v1.9 ATR-drift safety net was still firing on 92% of expirations, with 406 of 609 fired patterns (67%) dying on the exact same bar they were fired: any candidate aged between 1.0×-1.5× its own window width has a boundary that's already frozen at the cap by fire time, and that frozen value is very often more than 20× ATR from current price — not because it's a runaway extrapolation (the cap already prevents that), but because ATR measures bar-to-bar noise, not the honest cumulative price range a pattern's own real slope implies over dozens-to-hundreds of bars. The drift check was never a calibrated way to judge this once the line was capped
- Removed `Max. Linien-Drift` entirely — `Max. Pattern-Alter` (scaled to each pattern's own window width, not a flat ATR distance) is now the sole cleanup mechanism

## v1.10 — 2026-07-06
- Log-confirmed: a candidate fired and then expired on the exact same bar (`age=220` against an 81-bar window, 1.5×=121.5) — `Suchbereich letzte Swings` can resurface a window-end that's already past its own age-expiry threshold by the time it's found, wasting a cycle firing something that was never going to live
- Now gated before firing (`PATTERN SKIPPED (already aged)`) instead of firing and immediately expiring it, so a genuinely fresher (even if lower-scoring) candidate gets a chance at the one tracking slot instead of it being burned on a dead-on-arrival re-discovery

## v1.9 — 2026-07-06
- Log-confirmed across 4 exports (10800+ FIRED events total): ~100% of tracked wedges ended via the v1.8 ATR-drift check, essentially never via a real breakout (as few as 3-15 breakouts per file vs 800-1080 fires) — the drift check was reactively killing almost everything, because a valid broadening wedge structurally requires a real, non-trivial slope, and extending that slope forever every bar guarantees it eventually drifts far from price
- Fixed at the root instead: a tracked wedge's boundary now extends at most one more window-width past its own formation (`f_line_cap_x`), then FREEZES — both the drawn line and the level used for breakout/expiration checks stop moving forward once that fixed budget is used up, instead of extrapolating the fit indefinitely. The "still open" check at discovery time uses the same frozen evaluation, so an old-but-plausible window-end candidate isn't rejected as stillborn for a reason unrelated to an actual breakout
- `Max. Pattern-Alter` default lowered 3.0× → 1.5× (now the primary cleanup mechanism); `Max. Linien-Drift` default raised 5.0× → 20.0× ATR and relabeled as a safety net, since the line can no longer drift unboundedly by construction

## v1.8 — 2026-07-06
- Chart-confirmed: a "Symmetric Broadening" wedge's inherently steep, diverging boundary drifted far from real price well before the v1.6 age-based expiration (bar-count only) would have caught it
- Added `Max. Linien-Drift (ATR-Multiple)` (default 5.0×): a tracked wedge now also expires if either boundary's live projected level has drifted more than that many ATRs from the current close, regardless of bar-count age — checks the actual symptom (drifted price) instead of a proxy (elapsed bars)

## v1.7 — 2026-07-06
- Chart-confirmed: the v1.3 least-squares fit still didn't visually hug the actual touches — regression minimizes error across every point at once, pulling the line through the middle of the point cloud instead of tracing the real boundary, so several highs/lows sat clearly inside the drawn lines instead of near them
- Replaced the least-squares fit with `f_best_boundary`: searches all pairs of real touch points and picks the one with the fewest violations (points poking through the wrong side beyond tolerance) and the most touches — the classic way a chartist actually draws a trendline, through real highs/lows that define the edge, not a computed average

## v1.6 — 2026-07-06
- Chart-confirmed (NATGAS 4h): a "Symmetric Broadening Score 100" wedge fitted on a 101-bar window near the start of the chart had, thousands of bars later while still "open" (never broken out), drifted to +7.27/-3 on a symbol that never left the 1-5 range. A boundary is a straight fit on a fixed window, extrapolated further every bar it stays open (`lineAheadBars`) — left unresolved long enough, that extrapolation runs away to nonsensical prices
- Added `Max. Pattern-Alter (× Fensterbreite)` (default 3.0×): a tracked wedge that hasn't broken out within that multiple of its own formation length now expires automatically (logged as `PATTERN EXPIRED`) instead of drifting indefinitely — matches the classic TA convention that an unresolved pattern past a reasonable timeframe is stale, not live

## v1.5 — 2026-07-06
- Log-confirmed (Pine Logs export, 2020-01 to 2026-07, 2907 lines): 574 of 681 (84%) `FIRED`/`REPLACED`/`EVICTED` events had a `BREAKOUT` logged on the exact same bar — most detected wedges were stillborn, resolving the instant they were found and never visible as a live shape. Same root cause and fix as Triangle Compression Scanner Pro v1.0: the newest swing needs `pivotLen` bars of opposite-direction movement to even confirm, which is often the same move that already carries price through a boundary that was tight moments earlier
- Added a "still open" check before tracking a new wedge (price must currently sit between its own boundaries) and a one-bar grace period on breakout detection (skips the check on a pattern's own creation bar) — ported directly from Triangle Compression Scanner Pro

## v1.4 — 2026-07-06
- Chart-confirmed clutter (GOLD 1h): 5 concurrently tracked wedges fanning out from largely the same early swings, all firing "Descending/Symmetric Broadening" labels on top of each other. `Max. gleichzeitige Patterns` now defaults to 1 — the eviction logic added in v1.1 means a new, better-scoring candidate still replaces the current one automatically, so only the single highest-scoring wedge is shown at a time. Raise the input if multiple genuinely separate wedges at once is wanted

## v1.3 — 2026-07-06
- Chart-confirmed: boundary lines were anchored on only their first and last touch in the window, so a single early or late outlier swing could drag the whole line away from every touch in between — a wedge could score well on the ratio-based `touchOk` while visually missing most of its own touches. Boundaries are now a least-squares fit through every high/low in the window instead of just its two endpoint touches

## v1.2 — 2026-07-06
- Boundary lines no longer use `extend.right` (drawn all the way to the chart's right edge) — they now end a configurable `Linien-Überstand (Bars)` (default 10) past the current bar and advance bar by bar while the wedge stays open, so they keep pace with the chart without spanning it

## v1.1 — 2026-07-06
- Fixed: once `maxConcurrentPatterns` tracked wedges were all still open, every new non-overlapping candidate was silently discarded forever, even if it clearly outscored the weakest tracked one — the cap is now backfilled by evicting the weakest tracked wedge when a better candidate is found (ported from the same fix in Wolfe Wave Scanner Pro)
- Fixed: 2-3 same-direction wedges could end up tracked at once in overlap chains the pairwise insertion check missed (A overlaps B, B overlaps C, but A and C don't overlap directly) — added a dedupe pass that keeps only the higher-scoring pattern of each overlapping pair
- Fixed: with `Aufgelöste Patterns behalten` on, a displaced or resolved wedge's boundary lines were left on `extend.right` forever instead of being finalized into a bounded segment — they'd silently drift into nonsensical extrapolated prices the longer the chart ran. Replaced/evicted/resolved wedges are now finalized to end at the bar they were displaced or broke out on

## v1.0 — 2026-07-06
- Initial release: sliding-window broadening wedge scanner (descending broadening/ascending broadening/symmetric broadening) with weighted 0-100 score (structure, expansion, touch quality, line quality, duration)
- Tracks multiple simultaneously valid, non-overlapping wedges at once, each with independent drawings and breakout state, built on the same multi-pattern architecture as Wolfe Wave Scanner Pro v4.0 and Triangle Compression Scanner Pro v1.0
- Live breakout tracking (either boundary resolves the pattern) with dedicated bull/bear alerts
- Near-miss candidate marker and score-breakdown debug table, optional Pine Logs output
- Untested on a live chart — first pass, expect threshold tuning
