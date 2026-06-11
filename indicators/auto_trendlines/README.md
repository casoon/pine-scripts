# Auto Trendlines

Detects trendlines through pivot points using a Directional or Combinatorial pair scan with optional OLS/Outer refinement and a composite quality score. Greedy non-overlapping selection ensures clean, non-redundant output: each pivot contributes to at most one drawn line.

## Features

- **Directional or Combinatorial pair scan** — Directional only keeps falling resistance / rising support anchors; Combinatorial evaluates every pivot pair and refits the line through all inliers via OLS (optionally shifted outward to the outermost inlier in "Outer" fit mode)
- **ATR-based tolerance** — adapts to market volatility, no fixed pip distance
- **Composite quality score** — touches, span, extreme-anchor bonus, recency, fit tightness and violation penalty combined into a single score
- **Violation & relevance filters** — candidates with too many close/wick violations between anchors, or too far from current price, are dropped
- **Greedy non-overlap** — top-scoring lines are selected first; each pivot contributes to one line at most
- **Retest highlighting** — lines within a configurable ATR distance of price are emphasized, with optional distance label
- **Touch-count labels** — small label at the right end of each line shows the number of pivots it connects
- **Optional convex hull** — Andrew's monotone-chain envelope (strictest descending / ascending boundary), drawn dotted in a separate color

## Algorithm

For each direction (highs → resistance, lows → support):

### 1. Candidate generation — O(N²)

For each pair `(i, j)` of pivots:
1. Compute the anchor line `y = slope·x + intercept` from `(xi, yi)` and `(xj, yj)`
2. Find inliers — pivots with `|y_actual − y_line| ≤ tolerance × ATR`
3. If at least `minTouches` inliers, refit the line via OLS through them:

   ```
   slope     = (n·Σxy − Σx·Σy) / (n·Σx² − (Σx)²)
   intercept = (Σy − slope·Σx) / n
   ```

4. Re-evaluate inliers on the refined line — final touch count and residual sum
5. Filter: drop candidates with too many violations between anchors (unless anchored at an extreme), too far from current price, or outside the Sloped/Near-horizontal display mode
6. Score the candidate:

   ```
   score = touches · span · extreme_bonus · recency_bonus · fit_factor · violation_penalty
   ```

   - `touches · span` rewards multi-touch lines covering longer time ranges
   - `extreme_bonus` rewards lines anchored at the most extreme pivots (0.5 if none, up to 3.0)
   - `recency_bonus` linear decay from 1.0 (newest pivot at current bar) to 0.2 (newest pivot at lookback edge)
   - `fit_factor = 1 / (1 + avg_residual / tol)` rewards tight fits
   - `violation_penalty = 1 / (1 + violation% / 5)` punishes lines price crossed often

### 2. Sorting & greedy selection

Candidates are sorted by score descending (selection sort on indices). Iterating in score order:
- Compute the current candidate's still-unused inliers
- If at least `minTouches` are still unused, draw the line and mark its inliers as used
- Stop after `maxLines` per direction

This way the strongest line wins, and weaker overlapping candidates are skipped.

### 3. Convex hull (optional)

For pivot highs → upper hull (resistance envelope); for pivot lows → lower hull (support envelope). Andrew's monotone-chain algorithm:

```
for each pivot p in chronological order:
    while last two hull points + p form a "wrong-way" turn:
        pop last hull point
    push p onto hull
```

Wrong-way turn for the upper hull = cross product ≥ 0 (the second-to-last point lies below the line connecting its neighbors). The hull is drawn as a dotted polyline — every drawn segment lies above (resistance) or below (support) all original pivots in its span.

## Inputs

| Input | Default | Description |
|-------|---------|-------------|
| Left Bars / Right Bars | 5 / 5 | Pivot confirmation window |
| Line Fit | Outer | OLS or Outer (OLS shifted to outermost inlier) |
| Detection Method | Directional | Directional or Combinatorial pair scan |
| Min Touches | 3 | Minimum pivots a line must connect |
| Tolerance (× ATR) | 1.0 | Vertical distance threshold for "on the line" |
| Lookback (bars) | 200 | How far back pivots are considered |
| Max Lines per Direction | 3 | Cap on drawn resistance and support lines |
| Min Line Span (bars) | 15 | Minimum distance between oldest and newest touch |
| Max Violation % | 20 | Max share of bars crossing the line between anchors |
| Bars past last touch | 30 | Projection length beyond the newest touch |
| Show | Both | Sloped / Near-horizontal / Both |
| Max current distance (× ATR) | 5.0 | Relevance filter vs. current price |
| Highlight active retest | on | Emphasize lines within retest distance, optional label |
| Show touch-count label | on | Label at the right end with the touch count |
| Show convex-hull envelope | off | Draw the hull as a dotted reference |
| Colors / width / style | red / green / 2 / Solid | Visual settings |

## Notes

- Pivots are confirmed `pivRight` bars after the actual extreme — non-repainting once locked in. Lines update on each new confirmed pivot.
- The OLS refinement is the key reason an OLS-based line generally fits closer to the data than a naive 2-point line. The slope is the slope that minimizes the sum of squared vertical residuals across the inliers.
- The greedy non-overlap step prevents near-duplicate lines when two pivot pairs produce the same trend.
- If lines are too sparse or too dense, the main knobs to tune are: `pivLeft / pivRight` (more pivots), `tolMult` (stricter / looser fit), `minTouches` (clean / busy), `lookback` (history depth).
- Convex hull is opt-in. The hull's segments are mathematically the strictest possible boundary lines but may fragment into many short edges in choppy markets. Useful as a "primary envelope" in clean trends.

## Mathematical references

- **Ordinary least squares (OLS)**: minimizes `Σ(yᵢ − (m·xᵢ + b))²` over all inlier points; closed-form solution as above.
- **Convex hull (upper/lower)**: Andrew's monotone-chain algorithm — `O(n log n)` general, `O(n)` when input is already sorted by x (as pivots are, by `bar_index`).
- **RANSAC analogy**: the combinatorial pair scan is a deterministic version of RANSAC where every pair (instead of random samples) is tested. Suitable for the small N typical of pivot sets (≤ 50).
