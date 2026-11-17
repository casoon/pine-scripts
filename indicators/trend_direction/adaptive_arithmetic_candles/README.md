# Adaptive Arithmetic Candles

Renders an adaptive, efficiency-smoothed candle overlay in place of raw price action, colored by candle direction and regression-slope agreement.

## Features

- Kaufman-efficiency-adaptive smoothing of a weighted close/typical/regression price blend — reacts fast in efficient moves, damps in noisy ones
- Regression-anchored close with a trend-pressure body boost (slope + body strength via `tanh`)
- Synthetic wicks derived from real wick proportions, scaled up when the market is noisy (low efficiency)
- Strong/weak bull/bear candle coloring — "strong" means the candle direction and the regression slope agree
- Bullish/Bearish flip signals when direction changes with regression-slope confirmation (early warning, not a trade signal on its own)
- Long/Short breakout signals — the actual entry trigger: a strong bull/bear state confirmed by a close breaking the prior `Signal Breakout Length` bars' high/low; fires once per strong bull/bear run (first break only)

## Signal Logic

Candle color is state, not a trade signal — a flip only means the state changed. The Long/Short signals are the actual entries, built as Setup + Trigger rather than a flip alone:

- **Setup** — `strongBull` / `strongBear` (adaptive candle direction + regression-slope agreement)
- **Trigger** — `breakHigh` / `breakLow`, a close beyond the prior `signalLen` bars' high/low

```
strongBull  = bull and regSlope > 0
longSignal  = strongBull and breakHigh   (first break per strongBull run)
shortSignal = strongBear and breakLow    (first break per strongBear run)
```

The Data Window shows the raw inputs behind each state: direction, ATR-normalized regression slope, efficiency ratio, strong state and break flags.

## Modes

- **Real Close Dots** — overlays the actual close price as reference dots
- **Subtle Trend Background** — faint green/red background tied to regression slope sign
