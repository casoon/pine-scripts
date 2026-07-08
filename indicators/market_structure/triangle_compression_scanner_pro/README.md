# Triangle Compression Scanner Pro

Slides a fixed-size window of confirmed swings across the search depth and fits two boundary lines — an upper line from the window's outer highs, a lower line from its outer lows — to find compressing triangles: symmetric, ascending, or descending. Every distinct, non-overlapping valid triangle in the window is tracked independently until a confirmed breakout resolves it.

Shares its core approach with Wolfe Wave Scanner Pro (swing engine, best-of-window search, weighted scoring, multi-pattern tracking, debug/dashboard conventions) but is a separate indicator — triangle geometry (variable-length boundary lines from a swing window) doesn't fit the same fixed 5-point model a Wolfe wave needs.

## Features

- Alternating swing engine (`ta.pivothigh`/`ta.pivotlow`) with bounded history
- Sliding-window search: for every possible window end within `Suchbereich letzte Swings`, the `Swings pro Dreieck-Fenster` most recent swings up to that point define the two boundary lines — not a fixed point count, so the window can span anywhere from a tight 6-swing triangle to a wide 20-swing one
- Tracks multiple simultaneously valid, non-overlapping triangles at once, each with its own drawings and breakout state. An overlapping candidate only replaces an already-tracked triangle if it scores higher
- A new candidate only starts tracking if price is still between its own boundary lines at the moment it's detected — otherwise it's skipped as already broken (pivot-confirmation lag means a lot of candidates are already resolved by the time they're found)
- Weighted 0-100 score across five criteria: structure, compression, touch quality, line quality, duration
- Live breakout tracking: either boundary being closed beyond resolves the pattern (removes it from tracking) and fires a directional alert
- Score-breakdown debug table for tuning thresholds

## Scoring

| Criterion | Points | What it checks |
|---|---|---|
| Structure | 30 | The upper/lower boundary slopes match one of the three valid triangle shapes: symmetric (upper falling, lower rising), ascending (upper flat, lower rising), descending (upper falling, lower flat). "Flat" is ATR-normalized against the window's own width, not an absolute slope value |
| Compression | 25 | Channel width (signed, not absolute — so a crossed-apex reads as fully compressed rather than a false bulge) narrows by at least `Max. Endbreite / Startbreite` end-to-start *and* narrows monotonically through the midpoint, with a minimum starting width (`Mindest-Startbreite ATR`) to rule out degenerate near-zero-width windows, and must not have already crossed to the other side by window's end |
| Touch quality | 20 | Fraction of the window's highs within `Touch-Toleranz ATR` of the upper line, averaged with the same for lows, must be ≥75% — rewards boundaries that more than just their two defining points actually respect |
| Line quality | 15 | For symmetric triangles, the two boundary slopes must be within a 3x magnitude ratio of each other (rules out a near-flat side paired with a near-vertical one that "converges" mathematically but never looks like a real triangle). Also requires every high/low in the window to sit inside its boundary line (plus touch tolerance) — a swing poking well through its own line makes the shape a geometric fit only, not a real chart structure |
| Duration | 10 | The window must span at least `3×` `Swing-Stärke` bars — rules out degenerate, near-instant clusters |

A pattern only fires when its boundary slopes actually match a valid triangle shape (`structureOk`) *and* the weighted score clears `Mindestqualität`.

## Breakout

Once a triangle fires, both boundary lines (extended forward) are checked every bar. A close beyond either one resolves the pattern — it's removed from tracking, a breakout label is drawn, and the corresponding `TCS · BULL BREAKOUT` / `TCS · BEAR BREAKDOWN` alert fires. There's no separate invalidation level like Wolfe Wave Scanner's point-5 break: for a triangle, a confirmed break of either boundary *is* the resolution, in whichever direction it happens. The pattern's own creation bar has a one-bar grace period (no breakout check) so an already-broken pattern doesn't get labeled as breaking out in the same instant it's drawn — every bar after that, a plain containment check applies, so a pattern that's outside its lines is always resolved by the next bar.

## Multiple patterns

`Max. gleichzeitige Patterns` (default 5) caps how many valid triangles are tracked and drawn at once. Each search pass finds the best-scoring valid triangle *per window end*, not just the single overall best, so two non-overlapping triangles elsewhere on the chart both surface. `Aufgelöste Patterns behalten` (on by default) controls whether a triangle's drawings are deleted once it breaks out, or kept as bounded, finished segments (finalized at the breakout bar, not left extending indefinitely). Kept triangles still count for overlap purposes — a later candidate at the same spot only replaces one if it scores higher; otherwise it's skipped.

## Debug

Enabling `Score-Breakdown Debug-Tabelle` shows a table with the current best-in-depth candidate's pass/fail state per criterion.

Enabling `Pine-Logs aktivieren (Fehlersuche)` (off by default) emits `TCS SWING`/`TCS SEARCH`/`TCS PATTERN FIRED`/`TCS PATTERN REPLACED`/`TCS BREAKOUT` lines to the Pine Logs pane, plus `TCS PATTERN SKIPPED (stillborn)` when a valid candidate is discarded because price already broke it by detection time, and `TCS PATTERN SKIPPED (kept overlap scores higher)` when a kept triangle at the same spot outscores it — useful when a symbol/timeframe combination seems to produce no signals at all, or to check why a candidate wasn't tracked.
