# Market Structure Advanced

Converts swing pivot classifications (HH/HL/LH/LL) into a continuous bounded score oscillator. Instead of painting structure labels on the chart, this indicator gives a numerical structural bias reading that can be read like a momentum oscillator.

## Features

- **Pivot detection:** `ta.pivothigh` / `ta.pivotlow` with configurable left/right bars
- **Pivot classification:** HH (+2), HL (+1), LH (−1), LL (−2) — symmetric scoring, no directional bias in the logic
- **Windowed score:** sum of the N most recent pivot scores, normalized to [−100, +100] based on maximum possible sum
- **Signal line + fill + histogram:** same signal/hist/fill pattern as the rest of the Advanced suite
- **Gradient line:** `color.from_gradient()` from bear pink to bull teal over the −50 to +50 range
- **Shadow fills:** gradient fills between score and zero
- **Optional pivot labels on chart:** draws HH/HL/LH/LL text labels on the price pane when enabled
- **Signal markers:** score/signal crosses; zero-line crosses
- **Alert conditions:** bull/bear cross; zero-line cross up/down

## Scoring

Each confirmed swing high is classified as HH (score +2) or LH (score −1) by comparing to the previous swing high. Each confirmed swing low is classified as HL (score +1) or LL (score −2) by comparing to the previous swing low.

The window keeps only the most recent N pivot classifications. The sum is divided by `N × 2` (the maximum possible score if all pivots were HH) to normalize to [−100, +100]. A score above zero means the recent structure is dominated by higher highs and higher lows; below zero means the opposite.

Note: scores are computed on confirmed pivots only — a pivot is confirmed `pivRight` bars after it forms. This means the indicator has inherent lag relative to the candle where the pivot occurred.
