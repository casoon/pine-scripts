# Elliott Wave Radar

Rule-validated Elliott Wave counting on ZigZag pivots. The indicator labels impulses (1–5) and zigzag corrections (A–B–C) **only when the hard Elliott rules actually hold**, shows the raw Fibonacci ratios of the count, draws ratio projections for the developing wave, and checks the sub-structure of each wave on a finer pivot degree. When no interpretation passes the rules, the dashboard reports **"No valid count"** instead of forcing labels onto the chart. It is a display of the current structure: there is no setup call and no entry signal — alerts describe count events.

## Features

- ZigZag pivot engine with ATR noise filter, two degrees (primary + sub)
- Hard rules (a count that breaks one is rejected):
  - W2 never retraces beyond the start of W1
  - W3 is never the shortest of W1/W3/W5
  - W4 never enters W1 price territory (overlapping structures are left to the diagonal fallback)
  - W3 exceeds the end of W1, W5 exceeds the end of W3 (no truncation in v1)
  - When W3 is shorter than W1, a W1–W4 count draws the W5 limit ("W5 max" = W4 end + length of W3, beyond it W3 would be the shortest) and breaks when price runs beyond it
  - Sub-structure (impulse 5-3-5-3-5, zigzag 5-3-5, flat 3-3-5) on the finer pivot degree, rejecting only on clear results — see below
  - Zigzag: B retraces less than 90 % of A; flat: B retraces at least 90 % of A; in both, C travels beyond the A end
- Guidelines (shape the Fibonacci fit, never reject on their own):
  - Fib ratios: W2 38.2–78.6 % of W1, W3 1.618–4.236 × W1, W4 ≈ 38.2 % of W3, W5 ≈ W1 or 0.618 × W1, alternation of W2/W4 depth; zigzag B 38.2–78.6 %, C 0.618–1.618 × A; flat B 0.90–1.382, C 1.0–1.618 × A
  - One extension: after an extended W3 (≥ 1.618 × W1), a W5 longer than W3 costs 30 fit points
  - Origin: a wave starts after a move against it — a move into the origin smaller than 38.2 % of the wave costs up to 20 fit points
  - Degree: a counter-swing inside a wave should be smaller than the count's own corrective waves (inside W1/W3/W5 the larger of W2 and W4, inside A and C the B wave); a larger one costs 20–40 fit points
- Raw wave ratios in the dashboard: W2/W1, W3/W1, W4/W3, W5/W1 for impulses, B/A and C/A for corrections
- Corrective patterns:
  - **Zigzag A–B–C** (B retraces less than 90 % of A, C travels beyond A)
  - **Flat** (regular/expanded: B retraces 90 % of A or more) — the 90 % split keeps zigzag and flat apart on the same structure
- Partial counts with Fib ratio projections:
  - **1–2 / A–B**: a first wave and its pullback can start an impulse or a correction, so both labels are shown ("1/A", "2/B") until the next waves decide — after the move beyond the W1 / A end, a pullback that stays out of W1 territory (with W1 and W3 not corrective) makes it W1–W4, otherwise a valid zigzag or flat makes it A–B–C. W2/B levels 38.2 / 50 / 61.8 / 78.6 % and W3/C projections ×1.0 / ×1.618 (W3 ×2.618) of W1 from the W2 end; invalidated if W2 / B breaks the W1 start. W1 can start at any pivot more extreme than all later ones, back to a pivot beyond the W1 end; the complete count decides (see origin guideline)
  - **W1–W4** (projections ×0.618 / ×1.0 / ×1.618 of W1 from the W4 end)
  - **A–B after impulse** (projections ×1.0 / ×1.618 of A from B; invalidated if price takes out the impulse extreme). When A is not a clear five on the sub degree, the same two waves run as alt count **"W1-W2 (leading diagonal?)"** — the start of a new trend with a leading diagonal, whose waves may be threes. It takes over (provisional, labeled (1)-(2)) when the A–B breaks without a valid A–B–C; a leading diagonal is only confirmed by the diagonal fallback once it is complete
  - Post-impulse retracement levels (38.2 / 50 / 61.8 % of the impulse)
- Provisional fallbacks, only when no ordinary count is found (see below): contracting / expanding diagonals and W–X–Y
- Invalidation level drawn and **monitored bar-by-bar** — a broken level kills the count and fires an alert
- Sub-wave labels (i)–(iv) / (a)–(b) from the finer pivot degree, and the sub-structure result per wave in the dashboard
- The last completed impulse stays on the chart (faded) while the next structure develops, until price trades beyond its W5 end. If it is still the active count at that moment, W5 is extending: the count returns to W1–W4 and the next pivot sets the new W5 end
- Dashboard "Checks" row: how many interpretations passed the hard rules at the last pivot, and how many of those fell below the Fib fit threshold
- Alternate count in the dashboard: the other reading (W1–W4 or A–B–C) of the same 1–2 / A–B while both hold ("running"), otherwise the best fresh interpretation of another type
- Alerts (events, optionally on bar close): impulse / zigzag / flat count complete, A–B after impulse / 1–2 or A–B ("W1-W2 count active") / W1–W4 count active, close beyond W1 end (once per 1–2 / A–B count), count invalidated

## Sub-structure check

A motive wave subdivides into five waves, a zigzag is 5-3-5, a flat 3-3-5. For each wave of a count, the sub pivots inside it (pivot length `Pivot Length (sub)`) are reduced to alternating swings of at least `Min sub-wave swing` × the wave and then searched for a 5-wave impulse that passes the same hard rules as a primary impulse. The result per wave, shown in the dashboard sub-structure row:

| Result | Meaning | Effect |
|---|---|---|
| 5 | a rule-valid 5-wave subdivision fits | rules out a B wave and the A of a flat (both 3-wave moves) |
| LD / ED | no 5-wave fit, but a diagonal (W4 overlapping W1, contracting or expanding): leading in W1 / A, ending in W5 / C | confirms W1 / A or W5 / C like a five; rules out W3 (never a diagonal), a B wave, the A of a flat |
| 3 | three swings in A-B-C shape (B 0.236–1.382 of A, C beyond A) — corrective | rules out W1/W3/W5 of an impulse / W1–W4, the A and C of a zigzag, the C of a flat |
| unclear | other swings without a 5-wave fit — the sub degree may not resolve all sub-waves | open, neither confirmed nor rejected |
| 1 | a single leg on the sub degree | open |
| ? | sub pivots do not reach back to the wave start | open |

Missing evidence is never read as proof: only the clear results 3, 5 and LD / ED reject. The check is one level deep: the sub-waves themselves are not checked again.

## Fallback patterns

When neither a running count nor a fresh ordinary interpretation exists, two rarer patterns are tried. They are shown as **provisional** ("Leading diagonal?", "W-X-Y … provisional") and never replace an ordinary count; if they also fit, they appear as the alt count.

- **Diagonal** (searched over all stored pivots like the impulse). A leading diagonal only opens a structure (W1 or A), an ending diagonal only closes one (W5 or C). Inside a running count the sub-structure check places them by position (see above); as a fallback, a diagonal starting at the last impulse end is leading: W4 overlaps W1 but stays short of the W2 end, W3 and W5 progress beyond W1 and W3, W3 is not the shortest. Contracting (W3 < W1, W4 < W2, W5 < W3, the 2–4 line converging with the 1–3 line) or expanding (all reversed, diverging). W2 and W4 must not be 5-wave moves on the sub degree, and W1/W3/W5 must not mix fives and threes. Elsewhere two 5-wave action waves suggest a leading (5-3-5-3-5), two 3-wave ones an ending diagonal (3-3-3-3-3) — without the parent wave's position this stays a guess, hence the "?". Fit: half wedge proportion (W4/W2), half sub-structure evidence; it must reach `Fallback plausibility threshold`.
- **W–X–Y** (searched over all stored pivots; the W start, W end and Y start are picked like wave origins): W, X and Y are each a zigzag or flat (with the sub-structure checks of those patterns), X stays short of the W start and is smaller than W. Fit: the mean of the three component fits, minus points for components without sub-structure evidence and for a Y that ends short of W.

Fallbacks are not continued or invalidated bar by bar; the next pivot searches again. Triangles and nested combinations are not modeled.

## How counting works

1. Primary pivots come from `ta.pivothigh/pivotlow` (confirmation delay = pivot length) with an ATR minimum-swing filter against noise. Each accepted pivot is then **re-anchored to the true extreme** since the previous pivot — sharp counter-swings too short to confirm as pivots still mark the correct wave point (e.g. the strongest Wave-2 pullback, not a later weaker high).
2. On every new confirmed pivot, six interpretations **ending at that pivot** are evaluated: complete impulse, complete zigzag A–B–C, complete flat, A–B after impulse, W1–W4, 1–2 / A–B. All counts pick their wave points from all stored pivots, each point being the extreme of its segment. Impulse / W1–W4 / 1–2: for every possible W1 end, W3 is the extreme after it, W2 the extreme between W1 and W3, W4 the extreme after W3, and W1 starts at each possible origin (every pivot more extreme than all later ones; of more than eight, the nearest one and the seven with the largest move into them relative to the wave). Zigzag / flat: for every possible A end, B is the extreme after A, C must be the extreme after B, and A starts at each possible origin. A–B after impulse: A is the extreme after the impulse end, B the extreme after A. A wave can therefore contain smaller swings of its own — e.g. a long W3 with several internal pullbacks, or a W2 that is itself an A-B-C. The candidate with the best Fibonacci fit wins.
3. **Running count first.** When a count is active, it is continued with the new pivot before anything else: W2 / B extends, W3 / C develops (count kept, dashboard "W3/C developing"), a W4 turns W1–W2 into W1–W4, the first pivot beyond the W3 end completes the impulse, then A–B after the impulse and A–B–C follow. A continued count only has to pass the hard rules (including the sub-structure check); completing an impulse also needs `Min Fibonacci fit`. When a 1–2 / A–B can be read as both W1–W4 and A–B–C, both are kept: the better fit (plus completeness bonus) is the main count, the other runs alongside as the alternate. A count is replaced only when it breaks (invalidation level, "W5 max", a pullback after W3 beyond the W2 end, W3 becoming the shortest, C of an A–B after impulse running beyond A without a valid A–B–C, a 1–2 / A–B with a corrective W1 / A that is neither W1–W4 nor A–B–C after the next pullback, its points dropping out of the stored pivots) or when a correction completes — then the running alternate takes over if it still holds, otherwise the fresh search decides. A new local pattern with a better Fib fit cannot displace a running count.
4. Without an active count, the fresh search decides: each interpretation must pass its hard rules and then gets a Fibonacci fit (0–100) — how close its ratios are to the guideline values, minus the degree penalty. Interpretations below `Min Fibonacci fit` (default 55) are not shown: a plausibility filter for typical waves, separate from the rules. The fit is not a probability that the count is correct, and it is not shown on the chart. The rest is ranked by fit plus a small bonus for more complete structures (impulse > W1–W4 > A–B after impulse > zigzag/flat > 1–2 / A–B); the top one is shown, the best interpretation of another type appears as "Alt count".

## Honesty constraints (by design)

- Counts use **confirmed** pivots only — labels appear `Pivot Length` bars after the actual extreme. No repainting, but also no real-time pivot calls.
- Only the most recent structure is the active count. The last completed impulse is kept as a faded reference; older counts are not preserved.
- A 1–2 / A–B count whose W1 ends at the last impulse end is not counted — that move is W5, not a new W1. A W1 may start at the impulse end.
- One wave degree is counted; the sub-degree is used for the one-level sub-structure check and sub-labels, not for an independent second count.
- Diagonals and W–X–Y are provisional fallbacks.
- Counts are searched on the last `Count on last N bars` bars (default 5000) and from the stored pivots (default 200); a wave start older than that cannot be found.
- A count whose waves do not show the sub-structure their type requires on the finer degree is marked "unconfirmed" in the dashboard.
- Truncated fifths, triangles and nested combinations are not modeled — such phases show "No valid count" or a provisional fallback.

## Inputs

| Group | Input | Default | Purpose |
|---|---|---|---|
| ZigZag Engine | Pivot Length (primary) | 8 | Swing size of the counted degree |
| ZigZag Engine | Pivot Length (sub) | 3 | Finer degree for sub-wave checks |
| ZigZag Engine | Min Swing Size (ATR ×) | 0.5 | Noise filter for primary pivots |
| ZigZag Engine | Max pivots stored | 200 | Primary pivots kept for counting (sub degree: 5×) |
| ZigZag Engine | Count on last N bars | 5000 | Counts are searched only on the last N bars (run-time limit) |
| Wave Validation | Min Fibonacci fit (0-100) | 55 | Plausibility filter for fresh counts: hides rule-valid counts whose ratios fit the guidelines poorly |
| Wave Validation | Min sub-wave swing (× wave) | 0.08 | Smallest sub-degree swing used in the sub-structure check |
| Wave Validation | Detect diagonal fallback | on | Diagonal fallback when no ordinary count fits |
| Wave Validation | Detect W-X-Y fallback | on | W–X–Y fallback when no ordinary count fits |
| Wave Validation | Fallback plausibility threshold | 55 | Minimum fit for a diagonal or W–X–Y fallback |
| Display | Projections / sub-waves / dashboard / colors | on | Visual toggles |
