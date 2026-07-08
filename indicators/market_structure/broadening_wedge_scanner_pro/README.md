# Broadening Wedge Scanner Pro

Slides a fixed-size window of confirmed swings across the search depth and fits two boundary lines — an upper line from the window's outer highs, a lower line from its outer lows — to find *expanding* wedges: descending broadening (both lines fall, the lower one faster — bullish bias), ascending broadening (both lines rise, the upper one faster — bearish bias), or symmetric broadening (upper rising, lower falling — a direction-neutral "megaphone"). Every distinct, non-overlapping valid wedge is tracked independently until a confirmed breakout resolves it.

Shares its core approach with Wolfe Wave Scanner Pro and Triangle Compression Scanner Pro (swing engine, best-of-window search, weighted scoring, multi-pattern tracking, candidate/debug/dashboard conventions) but is a separate indicator — a broadening structure needs the *opposite* of Triangle's compression logic, not a shared one.

## Features

- Alternating swing engine (`ta.pivothigh`/`ta.pivotlow`) with bounded history
- Sliding-window search: for every possible window end within `Suchbereich letzte Swings`, the `Swings pro Keil-Fenster` most recent swings up to that point define the two boundary lines
- Tracks multiple simultaneously valid, non-overlapping wedges at once, each with its own drawings and breakout state. An overlapping candidate only replaces an already-tracked wedge if it scores higher
- Weighted 0-100 score across five criteria: structure, expansion, touch quality, line quality, duration
- Live breakout tracking: either boundary being closed beyond resolves the pattern and fires a directional alert
- Near-miss candidate marker and score-breakdown debug table for tuning thresholds

## Scoring

| Criterion | Points | What it checks |
|---|---|---|
| Structure | 30 | The upper/lower boundary slopes match one of the three valid broadening shapes: descending broadening (both falling, lower faster), ascending broadening (both rising, upper faster), symmetric broadening (upper rising, lower falling) |
| Expansion | 25 | Channel width widens by at least `Min. Endbreite / Startbreite` end-to-start *and* widens monotonically through the midpoint (no narrowing anywhere mid-window), with a minimum ending width (`Mindest-Endbreite ATR`) to rule out degenerate near-zero-width windows |
| Touch quality | 20 | Fraction of the window's highs within `Touch-Toleranz ATR` of the upper line, averaged with the same for lows |
| Line quality | 15 | For descending/ascending broadening, the faster side must be at least `Min. Geschwindigkeits-Verhältnis` times faster than the slower one (rules out a "technically faster by a hair" divergence that doesn't look real). For symmetric broadening, the two boundary slopes must be within a 3x magnitude ratio of each other |
| Duration | 10 | The window must span at least `3×` `Swing-Stärke` bars |

A pattern only fires when its boundary slopes actually match a valid broadening shape (`structureOk`) *and* the weighted score clears `Mindestqualität`.

## Breakout

Once a wedge fires, both boundary lines (extended forward) are checked every bar. A close beyond either one resolves the pattern — removed from tracking, a breakout label is drawn, and the corresponding `BWS · BULL BREAKOUT` / `BWS · BEAR BREAKDOWN` alert fires, regardless of which sub-type it was classified as (descending broadening is expected to resolve upward and ascending broadening downward, but a break the "wrong" way still ends the structure and is reported honestly).

## Multiple patterns

`Max. gleichzeitige Patterns` (default 5) caps how many valid wedges are tracked and drawn at once. Each search pass finds the best-scoring valid wedge *per window end*, not just the single overall best. `Aufgelöste Patterns behalten` controls whether a wedge's drawings are deleted once it breaks out, or kept as history.

## Debug

Enabling `Score-Breakdown Debug-Tabelle` shows a table with the current best-in-depth candidate's pass/fail state per criterion. `Kandidat-Mindestscore (Watch)` controls the near-miss marker's lower bound.

Enabling `Pine-Logs aktivieren (Fehlersuche)` (off by default) emits `BWS SWING`/`BWS SEARCH`/`BWS PATTERN FIRED`/`BWS PATTERN REPLACED`/`BWS BREAKOUT` lines to the Pine Logs pane.
