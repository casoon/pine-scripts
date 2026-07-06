# Wolfe Wave Scanner Pro

Searches a depth window of confirmed swings for the best-scoring 5-point Wolfe Wave wedge: a contracting, alternating channel where point 5 tests the 1-3 trendline. The winning candidate projects an EPA (Estimated Price at Arrival) target from line 1-4 at the time lines 1-3 and 2-4 converge, and is tracked live until price confirms or invalidates it.

## Features

- Alternating swing engine (`ta.pivothigh`/`ta.pivotlow`) with bounded history
- Best-of-window search: every valid point-5 anchor within `Suchbereich letzte Swings` is tried (a Wolfe wave is often already several swings old by the time it completes), and for each, points 1-4 are chosen combinatorially from all valid non-consecutive swings — a wave spanning e.g. swings 1,3,5,7,9 is evaluated too, not just the literal last 5 swings
- Weighted 0-100 score across eight criteria: structure, contraction + slope consistency, point-4 channel containment, apex convergence, point-5 trendline test, reward (capped to a sane ATR distance), timing, and leg-time symmetry
- EPA target is the price on line 1-4 at the apex time (where lines 1-3 and 2-4 converge, both drawn bold and stopping exactly there — no dangling infinite extension). The 1-4 line itself is drawn visibly through points 1 and 4 up to that same apex bar, and the vertical apex marker drops from that exact point to point 5 — one shared point everywhere, label/dashboard/drawing included
- Live invalidation tracking: once a pattern fires, a close beyond the point-5 ± 0.5 ATR level marks it invalidated and fires an alert
- Near-miss candidate marker (`Watch` signal, visual only, requires a real bull/bear structure) plus a dashed candidate wedge and a score-breakdown debug table for tuning thresholds
- Light-theme dashboard (status, best score, bias, EPA, invalidation level)

## Scoring

| Criterion | Points | What it checks |
|---|---|---|
| Structure | 30 | Core, non-negotiable shape: sequence alternates high/low and point 3 undercuts/exceeds point 1, point 5 extends beyond point 3 (lows declining for a bull setup, highs rising for bear) |
| Contraction + slope | 12 | Channel (line 2-4 vs. points 1/5) narrows by at least 30% end-to-start *and* narrows monotonically through the midpoint (no bulging outward around points 2-4); the 1-3 and 2-4 boundaries trend the same direction *and* their slope magnitudes are within a 3x ratio of each other (rules out a near-flat line paired with a near-vertical one) |
| Channel containment | 8 | Point 4 sits between points 1 and 2 — a shape nicety, scored separately so it can't zero out `Structure` on its own |
| Convergence (apex) | 15 | Lines 1-3 and 2-4 converge ahead of point 5, within `2×` the pattern's own width |
| Point-5 zone | 15 | Point 5 sits within `p5TolAtr` ATR of the 1-3 trendline (symmetric distance, either side) |
| Reward | 10 | Line 1-4 evaluated at point 5's own bar (not the EPA/apex time) lies beyond point 5 in the expected direction, and isn't further away than `Max. Zielentfernung ATR-Multiple` — an internal-only check on point 5's overshoot, distinct from the EPA target itself |
| Timing | 5 | Legs are monotonically spaced and the final leg isn't disproportionately long |
| Symmetry | 5 | Corresponding legs (1-2 vs. 3-4, 2-3 vs. 4-5) don't diverge too far in duration |

A pattern only fires when its swing chain actually forms the required bull/bear structure (the 30-point `Structure` criterion) *and* the weighted score clears `Mindestqualität` — `valid` requires both explicitly, so the other criteria reaching the score threshold on their own (they can, structure-agnostic points alone can add up past a low `Mindestqualität`) still can't unlock a signal for a chain that isn't a real Wolfe sequence.

## Invalidation

Once a pattern fires, its point-5 level (± 0.5 ATR, in the direction against the trade) is tracked every bar. A confirmed close beyond it marks the pattern invalidated, draws a label, and fires the `WWSP · INVALIDATED` alert — independent of whether a new pattern has since formed.

## Debug

Enabling `Score-Breakdown Debug-Tabelle` shows a table with the current best-in-depth candidate's pass/fail state per criterion and its running score against `Mindestqualität` — useful for tuning thresholds without guessing why a candidate didn't fire. `Kandidat-Mindestscore (Watch)` controls the near-miss marker's lower bound.

Enabling `Pine-Logs aktivieren (Fehlersuche)` (off by default) emits `WWSP SWING`/`WWSP SEARCH`/`WWSP PATTERN FIRED`/`WWSP INVALIDATED` lines to the Pine Logs pane, including how many 5-point combinations were evaluated per search and the full per-criterion breakdown of the winning candidate — useful when a symbol/timeframe combination seems to produce no signals at all.
