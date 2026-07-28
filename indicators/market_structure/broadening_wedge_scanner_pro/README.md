# Broadening Wedge Scanner Pro

Slides a fixed-size window of confirmed swings across the search depth and fits two boundary lines — an upper line from the window's outer highs, a lower line from its outer lows — to find *expanding* wedges: descending broadening (both lines fall, the lower one faster — bullish bias), ascending broadening (both lines rise, the upper one faster — bearish bias), or symmetric broadening (upper rising, lower falling — a direction-neutral "megaphone"). Every distinct, non-overlapping valid wedge is tracked independently until a confirmed breakout resolves it.

Shares its core approach with Wolfe Wave Scanner Pro and Triangle Compression Scanner Pro (swing engine, best-of-window search, weighted scoring, multi-pattern tracking, candidate/debug/dashboard conventions) but is a separate indicator — a broadening structure needs the *opposite* of Triangle's compression logic, not a shared one.

## Features

- Alternating swing engine (`ta.pivothigh`/`ta.pivotlow`) with bounded history
- Sliding-window search: for every possible window end within `Suchbereich letzte Swings`, the `Swings pro Keil-Fenster` most recent swings up to that point define the two boundary lines
- Tracks multiple simultaneously valid, non-overlapping wedges at once, each with its own drawings and breakout state. An overlapping candidate only replaces an already-tracked wedge if it scores higher
- Weighted 0-100 score across eight criteria: swing path, traversal, realized expansion, touch quality, line quality, anchor span, duration, relevance
- Live breakout tracking: either boundary being closed beyond resolves the pattern and fires a directional alert
- Near-miss candidate marker and score-breakdown debug table for tuning thresholds

## Scoring

Boundary slopes still classify the geometric family first (`structureOk`: descending broadening — both falling, lower faster; ascending broadening — both rising, upper faster; symmetric broadening — upper rising, lower falling), but that classification alone is no longer sufficient. The weighted score below is built from the actual alternating swing path, not just the two fitted lines.

| Criterion | Points | What it checks |
|---|---|---|
| Swing path | 20 | Every same-side swing step progresses in the direction the classified shape requires (higher highs for ascending/symmetric, lower lows for descending/symmetric). Hard-gated (`pathOk`): the path must alternate cleanly, have ≥3 highs and ≥3 lows, and every progression step must match — scored by the fraction of progression steps that match |
| Traversal | 20 | Each alternating swing leg's move across the channel width (as a fraction of the local channel width at each end), so a shape where price stays trapped near the midpoint scores poorly even if every bar is technically inside. Gated (`traversalOk`) on at least 3 consecutive legs clearing `Min. Traversal pro Leg` |
| Realized expansion | 15 | Actual swing-leg amplitude growth (last two legs vs. first two, direction-aware) plus per-leg growth consistency, blended with the projected end/start width ratio (`Ziel proj. Endbreite / Startbreite`). Gated (`realizedExpansionOk`) on ≥5 legs, a ratio ≥ `Min. realisierte Leg-Expansion`, and ≥60% of legs growing |
| Touch quality | 15 | Extra highs/lows beyond the two anchor points that land within `Touch-Toleranz ATR` of their boundary — the anchors themselves earn no points here, only independent confirmations do |
| Line quality | 10 | Blend of mean residual distance to each boundary, bar-level containment ratio, violation ratio, and mid-channel occupancy. Gated (`lineQualityOk`) on the faster-diverging side being at least `Min. Geschwindigkeits-Verhältnis` times faster (descending/ascending) or within a 3x magnitude ratio of each other (symmetric) |
| Anchor span | 10 | How much of the window each boundary's two anchor points actually spans, rewarding a wide-spaced anchor pair over a close pair that then gets extrapolated across the whole window. Gated (`boundaryOk`, together with line ordering, minimum end width, and `Max. Boundary-Drift ATR`) at ≥ `Min. Anker-Span / Pattern-Dauer` |
| Duration | 5 | Window length relative to `6×` `Swing-Stärke`. Gated (`durationOk`) at ≥ `3×` `Swing-Stärke` |
| Relevance | 5 | How recently the window ended relative to `Max. Pattern-Alter (× Fensterbreite)` — an already-stale candidate scores near zero here even if every other criterion is strong |

A pattern only fires when every hard gate (`structureOk`, `pathOk`, `traversalOk`, `realizedExpansionOk`, `boundaryOk`, `lineQualityOk`, `durationOk`) passes *and* the weighted score clears `Mindestqualität`. Bar-level containment (`barsInsideOk`, ≥90% of bars inside `Touch-Toleranz ATR`) is soft — it feeds into the line-quality score instead of vetoing the pattern outright.

## Breakout

Once a wedge fires, both boundary lines (extended forward) are checked every bar. A close beyond either one resolves the pattern — removed from tracking, a breakout label is drawn, and the corresponding `BWS · BULL BREAKOUT` / `BWS · BEAR BREAKDOWN` alert fires, regardless of which sub-type it was classified as (descending broadening is expected to resolve upward and ascending broadening downward, but a break the "wrong" way still ends the structure and is reported honestly).

## Multiple patterns

`Max. gleichzeitige Patterns` (default 5) caps how many valid wedges are tracked and drawn at once. Each search pass finds the best-scoring valid wedge *per window end*, not just the single overall best. `Aufgelöste Patterns behalten` controls whether a wedge's drawings are deleted once it breaks out, or kept as history.

## Debug

Enabling `Score-Breakdown Debug-Tabelle` shows a table with the current best-in-depth candidate's pass/fail state per criterion. `Kandidat-Mindestscore (Watch)` controls the near-miss marker's lower bound.

Enabling `Pine-Logs aktivieren (Fehlersuche)` (off by default) emits `BWS SWING`/`BWS SEARCH`/`BWS PATTERN FIRED`/`BWS PATTERN REPLACED`/`BWS BREAKOUT` lines to the Pine Logs pane.
