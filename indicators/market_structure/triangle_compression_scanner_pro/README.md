# Triangle Compression Scanner Pro

Slides a fixed-size window of confirmed swings across the search depth and fits two boundary lines — an upper line from the window's outer highs, a lower line from its outer lows — to find compressing triangles: symmetric, ascending, or descending. Every distinct, non-overlapping valid triangle in the window is tracked independently until a confirmed breakout resolves it.

Shares its core approach with Wolfe Wave Scanner Pro (swing engine, best-of-window search, weighted scoring, multi-pattern tracking, debug/dashboard conventions) but is a separate indicator — triangle geometry (variable-length boundary lines from a swing window) doesn't fit the same fixed 5-point model a Wolfe wave needs.

## Features

- Alternating swing engine (`ta.pivothigh`/`ta.pivotlow`) with bounded history
- Sliding-window search: for every possible window end within `Suchbereich letzte Swings`, the `Swings pro Dreieck-Fenster` most recent swings up to that point define the two boundary lines — not a fixed point count, so the window can span anywhere from a tight 6-swing triangle to a wide 20-swing one
- Tracks multiple simultaneously valid, non-overlapping triangles at once, each with its own drawings and breakout state. An overlapping candidate only replaces an already-tracked triangle if it scores higher
- A new candidate only starts tracking if price is still between its own boundary lines (plus a small `Breakout-Puffer ATR` buffer) at the moment it's detected — otherwise it's skipped as already broken (pivot-confirmation lag means a lot of candidates are already resolved by the time they're found)
- Weighted 0-100 score across eight continuous criteria: swing path, traversal, realized compression, boundary proximity, line quality, boundary/apex, duration, relevance — plus a set of hard gates that must all pass before a candidate can fire
- Live breakout tracking: either boundary being closed beyond (plus `Breakout-Puffer ATR`) resolves the pattern (removes it from tracking) and fires a directional alert
- Score-breakdown debug table for tuning thresholds

## Scoring

The upper/lower boundary slopes must first match one of the three valid triangle shapes — symmetric (upper falling, lower rising), ascending (upper flat, lower rising), descending (upper falling, lower flat); "flat" is ATR-normalized against the window's own width, not an absolute slope value (`structureOk`). Everything below is then scored continuously and gated separately.

| Criterion | Points | What it checks |
|---|---|---|
| Swing path | 20 | Swings must alternate high/low without repeats, and same-side highs/lows must monotonically progress in the triangle's direction (falling highs for symmetric/descending, rising lows for symmetric/ascending). Gate `pathOk` additionally requires ≥6 path points, ≥3 highs and ≥3 lows, and a perfect progression match — a single non-progressing pair fails the gate even if the score stays high |
| Traversal | 20 | Consecutive swing-to-swing legs must actually cross the local channel width, not just sit inside a generous outer envelope. Score blends the average traversal ratio with the fraction of legs clearing `Min. Traversal pro Leg`; gate `traversalOk` requires a run of ≥3 consecutive qualifying legs |
| Realized compression | 15 | Compares actual price-leg amplitudes, not just the fitted geometry: the last two legs must be tighter than the first two (≤`Max. realisierte Leg-Kompression`), and same-direction legs must generally shrink leg-over-leg (≥60% of tested pairs). Gate `realizedCompressionOk` additionally requires the projected end/start width ratio to clear `Ziel proj. Endbreite / Startbreite` and at least 5 legs |
| Boundary proximity | 15 | Average proximity quality of every non-anchor high/low to its boundary line, in ATR terms (full credit ≤0.25 ATR, zero credit ≥0.75 ATR) — rewards boundaries the whole window actually respects, not just the two points that define them |
| Line quality | 10 | Blends boundary residual quality, bar-containment ratio, violation ratio, and contact-zone distribution — draws from the same soft ≥90% bar-containment check as `barsInsideOk` (no longer a standalone veto, see Breakout below). Gate `lineQualityOk`: for symmetric triangles, the two boundary slopes must stay within a 3x magnitude ratio of each other; ascending/descending triangles just need `structureOk` |
| Boundary / apex | 10 | 60% anchor-span quality (how much of the window each boundary's own touch points span) + 40% apex-maturity quality (how close the two lines' projected intersection lands to 65% of the way through the pattern's own duration). Gates `boundaryOk` (anchor span ≥`Min. Anker-Span / Pattern-Dauer`, mean residual ≤`Max. mittleres Boundary-Residuum ATR`, zero swing violations, contacts spread across the window's early/middle/late thirds, and — for ascending/descending — an extra touch confirming the flat side) and `apexOk` (the intersection must lie ahead of the window, within `Max. Apex-Distanz`× its width) |
| Duration | 5 | Continuous credit up to `6×` `Swing-Stärke` bars; gate `durationOk` still requires at least `3×` |
| Relevance | 5 | Decays linearly with how many bars have passed since the window's own end, relative to `Max. Pattern-Alter`× the window width — an old-but-still-technically-valid candidate scores lower than a fresh one |

A pattern only fires when every hard gate — `structureOk`, `pathOk`, `traversalOk`, `realizedCompressionOk`, `boundaryOk`, `apexOk`, `lineQualityOk`, `durationOk` — passes *and* the weighted score clears `Mindestqualität`.

## Breakout

Once a triangle fires, both boundary lines (extended forward) are checked every bar. A close beyond either one by more than `Breakout-Puffer ATR` resolves the pattern — it's removed from tracking, a breakout label is drawn, and the corresponding `TCS · BULL BREAKOUT` / `TCS · BEAR BREAKDOWN` alert fires. There's no separate invalidation level like Wolfe Wave Scanner's point-5 break: for a triangle, a confirmed break of either boundary *is* the resolution, in whichever direction it happens. The pattern's own creation bar has a one-bar grace period (no breakout check) so an already-broken pattern doesn't get labeled as breaking out in the same instant it's drawn — every bar after that, the same buffered containment check applies, so a pattern that's outside its lines (beyond the buffer) is always resolved by the next bar.

## Multiple patterns

`Max. gleichzeitige Patterns` (default 5) caps how many valid triangles are tracked and drawn at once. Each search pass finds the best-scoring valid triangle *per window end*, not just the single overall best, so two non-overlapping triangles elsewhere on the chart both surface. `Aufgelöste Patterns behalten` (on by default) controls whether a triangle's drawings are deleted once it breaks out, or kept as bounded, finished segments (finalized at the breakout bar, not left extending indefinitely). Kept triangles still count for overlap purposes — a later candidate at the same spot only replaces one if it scores higher; otherwise it's skipped.

## Debug

Enabling `Score-Breakdown Debug-Tabelle` shows a table with the current best-in-depth candidate's per-criterion points alongside each hard gate's pass/fail (`OK`/`GATE`) state, plus overall pattern validity and trackability.

Enabling `Pine-Logs aktivieren (Fehlersuche)` (off by default) emits `TCS SWING`/`TCS SEARCH`/`TCS PATTERN FIRED`/`TCS PATTERN REPLACED`/`TCS BREAKOUT` lines to the Pine Logs pane, plus `TCS PATTERN SKIPPED (stillborn)` when a valid candidate is discarded because price already broke it by detection time, and `TCS PATTERN SKIPPED (kept overlap scores higher)` when a kept triangle at the same spot outscores it — useful when a symbol/timeframe combination seems to produce no signals at all, or to check why a candidate wasn't tracked.
