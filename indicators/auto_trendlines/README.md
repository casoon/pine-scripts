# Auto Trendlines

Detects trendlines through pivot points using a combinatorial pair scan with OLS refinement and a composite quality score. Greedy non-overlapping selection ensures clean, non-redundant output: each pivot contributes to at most one drawn line.

## Features

- **Combinatorial pair scan + OLS refinement** — every pivot pair is evaluated; the line is then refit through all inliers via ordinary least squares for a tighter fit
- **ATR-based tolerance** — adapts to market volatility, no fixed pip distance
- **Composite quality score** — touches², span, recency, fit tightness combined into a single score
- **Greedy non-overlap** — top-scoring lines are selected first; each pivot contributes to one line at most
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
5. Score the candidate:

   ```
   score = touches² · log(span + 2) · recency_bonus · 1 / (1 + avg_residual / tolerance)
   ```

   - `touches²` rewards multi-touch lines strongly
   - `log(span + 2)` rewards lines covering longer time ranges (logarithmic, not dominant)
   - `recency_bonus` linear decay from 1.0 (newest pivot at current bar) to 0.2 (newest pivot at lookback edge)
   - `1 / (1 + avg_residual / tol)` rewards tight fits

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
| Min Touches | 3 | Minimum pivots a line must connect |
| Tolerance (× ATR) | 0.3 | Vertical distance threshold for "on the line" |
| Lookback (bars) | 300 | How far back pivots are considered |
| Max Lines per Direction | 3 | Cap on drawn resistance and support lines |
| Extend lines right | on | Project the line into the future |
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
