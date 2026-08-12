# Fib Reaction Memory

Scores Fibonacci retracement levels of an active A→B reference leg by the confirmed local price reactions that actually occurred inside that leg — not by geometric proximity. Instead of asking "was price ever at 61.8%?", it asks "did price show a confirmed local reaction near 61.8% while this leg was being built?" and projects the live pullback back into that same evidence.

## Features

- Confirmed structural A→B reference leg from alternating swing pivots, frozen while price retraces (a new impulse only replaces it when a confirmed pivot extends beyond B, or the pullback invalidates past A)
- Micro-pivot reaction detection inside the structural leg, sized in ATR units so weak stalls don't count the same as real reversals
- Reaction-first, fib-second: historical reactions are located and weighted before they're checked for Fib proximity, not the other way around
- 0–100 Fib Memory Score per level, combining reaction strength, proximity to the level, optional recency weighting, consumption decay (later tests at the same level count for less) and a broken-level penalty (a reaction whose level was later broken counts for less than one that held), run through a saturating (not linear) aggregation
- Per-level Hold Rate — % of historical reactions near this level that were never subsequently broken, shown alongside the score
- Per-level state machine: APPROACHING / TESTING / REJECTED / ACCEPTED / RECLAIMED, derived from the current retracement and the deepest retracement reached during this pullback
- Score-based NEXT level highlight — the next level ahead of price with the strongest evidence, not simply the nearest geometric Fib
- Persistent line/label objects reused every bar instead of recreated, keeping draw-object usage bounded

## Reference leg construction

The structural leg comes from alternating `ta.pivothigh()`/`ta.pivotlow()` confirmations (`Structural Pivot Length`, confirmed only after the right-side lookback bars have closed). A→B stays fixed while price pulls back inside it — a naive "last two pivots" approach would silently swap the reference range out from under an in-progress pullback the moment a smaller counter-pivot confirms. The leg only changes when either a new confirmed pivot extends past B (using the most recent opposite-type pivot after old B as the new A, if one exists), or the pullback exceeds `Reference Leg Invalidation` (retracement beyond 1.00, i.e. beyond A).

## Reaction memory

Inside the frozen A→B leg, smaller pivots (`Reaction Pivot Length`) are located and each is scored by how far price moved away from it afterward, in ATR units (`Minimum Reaction · ATR` filters out noise, `Strong Reaction · ATR` is the size that earns full weight). Each qualifying reaction is normalized onto the 0.0–1.0 A→B range and, if it falls within `Fib Reaction Radius` of a standard Fib ratio, contributes evidence to that level — weighted by reaction strength, proximity, and optionally recency (`Recency Influence`). Evidence per level is aggregated with a saturating curve (`Score Saturation`) so repeated touches don't produce an unbounded score. `Maximum Memory Scan` bounds how far back the historical scan runs, for performance.

Reactions are scanned in chronological order (oldest inside the leg first) so that `Level Consumption` can discount repeated tests of the same level: the first qualifying reaction near a level counts fully, each later one at that same level counts less (`1 / (1 + consumptionDecay × testsSoFar)`), reflecting that a level typically weakens rather than staying equally valid after repeated tests. `0` disables this (every test counts fully, matching v1.0/v1.1 behavior).

`Broken Level Penalty` discounts a reaction if the level it's near was later broken anyway. This is checked by projecting every bar's own raw high/low (not a historical live-leg series — the leg wasn't necessarily active back then) onto the *current* fixed A/B range, then taking the deepest such value reached between the reaction's bar and now. If that later exceeds the level plus tolerance, the reaction's contribution is multiplied by `1 - brokenLevelPenalty` (default halves it). A reaction near a level that was never subsequently broken always counts fully. `0` disables this.

The same held/broken check per reaction also feeds a **Hold Rate** per level: the % of qualifying reactions near that level that were never subsequently broken (`na`, hidden, until the level has at least one qualifying reaction). This is a descriptive statistic about what already happened in this leg, not a probability forecast — see "What this is not" below. `Show Hold Rate` toggles the label suffix.

## NEXT level selection

Among enabled Fib levels still ahead of the current retracement, the level with the highest Memory Score at or above `Minimum Score for NEXT` is preferred. If no ahead level clears that threshold, the nearest geometric level ahead is used instead. This means the highlighted NEXT level is not necessarily the closest one — a distant level with strong historical reaction evidence can outrank a close one with none.

## Level state machine

Each level's state is derived from two numbers: the current retracement (now) and the deepest retracement reached anywhere during this pullback (`pullbackDeepest`, which is always at least as deep as the current retracement). This keeps the states mutually exclusive and avoids storing a separate per-level history:

- **APPROACHING** — the pullback has never reached this level's tolerance band
- **TESTING** — the current retracement is inside the level's tolerance band right now
- **REJECTED** — the pullback reached the level's band at some point, then retreated shallower, without ever breaking decisively past it
- **ACCEPTED** — the pullback broke decisively past the level and is still beyond it
- **RECLAIMED** — the pullback broke past the level at some point, then retreated back shallower than it again

## Reading the chart

Each Fib line's color and width encode its Memory Score (`Strong Score` / `Medium Score` thresholds: gray/thin = little memory, orange = relevant structure, bold/lime = strong structure). The highlighted NEXT level (when `Highlight NEXT Level` is on) is drawn solid and in a distinct color regardless of score tier. Labels show the level, its score, its state (APPROACHING/TESTING/REJECTED/ACCEPTED/RECLAIMED) and, if `Show Hold Rate` is on and the level has been tested, its Hold Rate. `Show Weak Levels` can hide low-score levels below `Medium Score` to reduce clutter (the NEXT level stays visible regardless). A gray A/B leg line and optional anchor labels mark the current reference leg.

## What this is not

A high Fib Memory Score or Hold Rate means the area showed meaningful historical structure within this specific leg — neither is a probability that the level holds going forward, and neither makes a forecast. Both are descriptive statistics about reactions that already happened earlier in this same leg. The state machine is diagnostic only; it doesn't gate or weight anything. See `todo.md` for known gaps (pause/acceptance detection, reaction zones independent of Fib ratios, multi-leg history) that were deliberately left out.
