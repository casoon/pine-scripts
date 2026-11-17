# Elliott Wave Radar

Rule-validated Elliott Wave counting on ZigZag pivots. The indicator labels impulses (1–5) and zigzag corrections (A–B–C) **only when the hard Elliott rules actually hold**, shows the raw Fibonacci ratios of the count, draws ratio projections for the developing wave, and cross-checks sub-wave structure on a finer pivot degree. When no interpretation passes the rules, the dashboard reports **"No valid count"** instead of forcing labels onto the chart. It is a display of the current structure: there is no score, no setup call and no entry signal — alerts describe count events.

## Features

- ZigZag pivot engine with ATR noise filter, two degrees (primary + sub)
- Hard-rule validation:
  - W2 never retraces beyond the start of W1
  - W3 is never the shortest of W1/W3/W5
  - W4 never enters W1 price territory (toggle for diagonals)
  - W3 exceeds the end of W1, W5 exceeds the end of W3 (no truncation in v1)
- Raw wave ratios in the dashboard: W2/W1, W3/W1, W4/W3, W5/W1 for impulses, B/A and C/A for corrections
- Corrective patterns:
  - **Zigzag A–B–C** (B retraces 0.236–0.886 of A, C travels beyond A)
  - **Flat** (regular/expanded: B retraces 0.90–1.38 of A) — disjoint thresholds, so zigzag and flat never compete on the same structure
- Partial counts with Fib ratio projections:
  - **W1–W2** (projections ×1.0 / ×1.618 / ×2.618 of W1 from the W2 end)
  - **W1–W4** (projections ×0.618 / ×1.0 / ×1.618 of W1 from the W4 end)
  - **A–B after impulse** (projections ×1.0 / ×1.618 of A from B; invalidated if price takes out the impulse extreme)
  - Post-impulse retracement levels (38.2 / 50 / 61.8 % of the impulse)
- Invalidation level drawn and **monitored bar-by-bar** — a broken level kills the count and fires an alert
- Sub-wave labels (i)–(iv) / (a)–(b) from the finer pivot degree; the dashboard reports whether W1/W3 internally divide into 5 legs
- Alternate (runner-up) interpretation shown in the dashboard
- Alerts (events, optionally on bar close): impulse / zigzag / flat count complete, A–B / W1–W2 / W1–W4 count active, close beyond W1 end (once per W1–W2 count), count invalidated

## How counting works

1. Primary pivots come from `ta.pivothigh/pivotlow` (confirmation delay = pivot length) with an ATR minimum-swing filter against noise. Each accepted pivot is then **re-anchored to the true extreme** since the previous pivot — sharp counter-swings too short to confirm as pivots still mark the correct wave point (e.g. the strongest Wave-2 pullback, not a later weaker high).
2. On every new confirmed pivot, six interpretations **ending at that pivot** are evaluated: complete impulse (6 pivots), complete zigzag A–B–C (4), complete flat (4), A–B after impulse (3), W1–W4 (5), W1–W2 (3).
3. Each interpretation must pass its hard rules. There is no score and no score gate.
4. The most complete valid interpretation is shown, in a fixed order: impulse, zigzag/flat (disjoint), A–B after impulse, W1–W4, W1–W2. The next valid one appears as "Alt count" in the dashboard.

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
| Display | Projections / sub-waves / dashboard / colors | on | Visual toggles |
