# Klinger Volume Force Map

Volume-force analysis based on Stephen J. Klinger's original 1997 concept. It accumulates volume force while the H+L+C trend direction persists (resetting on each trend flip), takes the spread between a fast and a slow EMA of that force against its own EMA-based signal line, and normalizes the result so it stays comparable across instruments. On top of the raw oscillator it runs a hysteretic Bull/Neutral/Bear regime engine, confirmed-pivot divergence detection, and continuation/structure-break event detection.

## Features

- Original 1997 Volume Force formula as default, with alternative formula variants (TradingView documentation formula, simplified signed-volume baseline) for research/comparison
- Raw KVO remains the source of all zero/signal-cross logic regardless of display normalization
- Zero-preserving normalization (`KVO / EMA(abs(KVO), N)` by default, or StdDev scale, or raw) for readable cross-market visualization
- Momentum histogram (KVO − Signal) with acceleration/deceleration coloring
- Hysteretic Bull / Neutral / Bear regime engine, with Strong Bull / Strong Bear expansion states
- Confirmed regular + hidden divergence detection on confirmed PRICE pivots
- Divergence quality filter using ATR displacement, KVO displacement, and pivot separation
- Bull/Bear Flow Rejection continuation events
- Flow-confirmed structural breakouts
- Clean / Analysis / Research visual modes
- Optional price-chart divergence and event overlays
- Compact current-state dashboard plus research diagnostics (formula correlation/disagreement)

## Notes

- Divergences use confirmed price pivots — a divergence is only emitted after `Pivot right bars` have elapsed. This avoids repainting a still-forming pivot at the cost of confirmation delay.
- The default normalization divides KVO, Signal, and the histogram by the same denominator (`EMA(abs(KVO), N)`), which preserves zero crossings and KVO/Signal crossings while making the pane comparable across instruments.
- "StdDev scale" intentionally uses `KVO / stdev(KVO)`, not a mean-subtracted Z-score, so the semantic KVO zero line doesn't move.
- Needs real volume data; on zero-volume feeds the Volume Force term collapses toward zero.
