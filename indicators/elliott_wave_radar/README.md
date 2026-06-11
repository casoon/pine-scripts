# Elliott Wave Radar

Rule-validated Elliott Wave counting on ZigZag pivots. The indicator labels impulses (1–5) and zigzag corrections (A–B–C) **only when the hard Elliott rules actually hold**, scores every count by Fibonacci guideline adherence (0–100), projects targets for the developing wave, and cross-checks sub-wave structure on a finer pivot degree. When no interpretation passes the rules and the score gate, the dashboard honestly reports **"No valid count"** instead of forcing labels onto the chart.

## Features

- ZigZag pivot engine with ATR noise filter, two degrees (primary + sub)
- Hard-rule validation:
  - W2 never retraces beyond the start of W1
  - W3 is never the shortest of W1/W3/W5
  - W4 never enters W1 price territory (toggle for diagonals)
  - W3 exceeds the end of W1, W5 exceeds the end of W3 (no truncation in v1)
- Fibonacci guideline scoring (0–100): W2 ≈ 0.5–0.618, W3 ≈ 1.618×W1, W4 ≈ 0.382×W3, W5 ≈ 0.618–1.0×W1, plus an alternation bonus (W2 vs. W4 depth)
- Corrective patterns:
  - **Zigzag A–B–C** (B retraces 0.236–0.886 of A, C travels beyond A)
  - **Flat** (regular/expanded: B retraces 0.90–1.38 of A) — disjoint thresholds, so zigzag and flat never compete on the same structure
- Developing counts with Fib target projections:
  - **W3 setup** after W1–W2 confirm (targets ×1.0 / ×1.618 / ×2.618 of W1)
  - **W5 setup** after W1–W4 confirm (targets ×0.618 / ×1.0 / ×1.618 of W1)
  - **C-wave setup** after a completed impulse + confirmed A–B (targets ×1.0 / ×1.618 of A; invalidated if price takes out the impulse extreme)
  - Post-impulse correction targets (38.2 / 50 / 61.8 % of the impulse)
- Invalidation level drawn and **monitored bar-by-bar** — a broken level kills the count and fires an alert
- Sub-wave labels (i)–(iv) / (a)–(b) from the finer pivot degree; the dashboard reports whether W1/W3 internally divide into 5 legs
- Alternate (runner-up) interpretation shown in the dashboard
- Alerts: impulse complete, ABC complete, W3 setup, W5 setup, count invalidated

## How counting works

1. Primary pivots come from `ta.pivothigh/pivotlow` (confirmation delay = pivot length) with an ATR minimum-swing filter against noise. Each accepted pivot is then **re-anchored to the true extreme** since the previous pivot — sharp counter-swings too short to confirm as pivots still mark the correct wave point (e.g. the strongest Wave-2 pullback, not a later weaker high).
2. On every new confirmed pivot, six interpretations **ending at that pivot** are evaluated: complete impulse (6 pivots), complete zigzag A–B–C (4), complete flat (4), post-impulse C-wave setup (3), developing W5 setup (5), developing W3 setup (3).
3. Each interpretation must pass its hard rules, then gets a Fibonacci guideline score. Candidates below the score gate (input, default 55) are discarded.
4. The best candidate wins (complete patterns get a completeness bonus over developing prefixes); the runner-up appears as "Alt count" in the dashboard.

## Honesty constraints (by design)

- Counts use **confirmed** pivots only — labels appear `Pivot Length` bars after the actual extreme. No repainting, but also no real-time pivot calls.
- Only the most recent structure is labeled. Historical counts are not preserved when a newer structure replaces them.
- One wave degree is counted; the sub-degree is used for verification and sub-labels, not for an independent second count.
- Truncated fifths, triangles and complex corrections (W-X-Y) are not modeled — such phases simply show "No valid count". Flats are supported since v1.1.

## Inputs

| Group | Input | Default | Purpose |
|---|---|---|---|
| ZigZag Engine | Pivot Length (primary) | 8 | Swing size of the counted degree |
| ZigZag Engine | Pivot Length (sub) | 3 | Finer degree for sub-wave checks |
| ZigZag Engine | Min Swing Size (ATR ×) | 0.5 | Noise filter for primary pivots |
| Wave Validation | Allow W4 into W1 (diagonal) | off | Relaxes the overlap rule |
| Wave Validation | Min count score | 55 | Quality gate — below this, no count is shown |
| Display | Projections / sub-waves / dashboard / colors | on | Visual toggles |
