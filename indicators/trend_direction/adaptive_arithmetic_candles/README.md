# Adaptive Arithmetic Candles + Quality Score

Renders an adaptive, efficiency-smoothed candle overlay in place of raw price action, paired with a 0-100 Trend Quality Score that grades how trustworthy the current candle's direction is.

## Features

- Kaufman-efficiency-adaptive smoothing of a weighted close/typical/regression price blend — reacts fast in efficient moves, damps in noisy ones
- Regression-anchored close with a trend-pressure body boost (slope + body strength via `tanh`)
- Synthetic wicks derived from real wick proportions, scaled up when the market is noisy (low efficiency)
- Trend Quality Score (0-100): efficiency (35%), regression slope (30%), body-to-range ratio (20%), follow-through vs. prior close (15%)
- Strong/weak bull/bear candle coloring — "strong" requires quality ≥ `Minimum Signal Quality` input and regression slope agreement
- Optional quality score line and high-quality dot markers (quality ≥ 70) plotted below bars
- Bullish/Bearish flip signals when direction changes with quality ≥ 55 and regression-slope confirmation (early warning, not a trade signal on its own)
- Long/Short breakout signals — the actual entry trigger: a strong bull/bear state confirmed by a close breaking the prior `Signal Breakout Length` bars' high/low

## Scoring

`quality = effScore * 0.35 + slopeScore * 0.30 + bodyScore * 0.20 + followScore * 0.15`, clamped to 0-100.

- `effScore` — Kaufman Efficiency Ratio over `lenER` bars, scaled to 0-100
- `slopeScore` — normalized regression slope (`ta.linreg` delta / ATR), scaled to 0-100
- `bodyScore` — adaptive candle body size relative to its full range, scaled to 0-100
- `followScore` — 100 if the real close continued in the candle's direction, else 35

`dirQuality = quality * direction` gives a signed -100..+100 read used for score-line coloring.

## Signal Logic

Candle color is state, not a trade signal — a flip only means the state changed. The Long/Short signals are the actual entries, built as Setup + Trigger rather than a flip alone:

- **Setup** — `strongBull` / `strongBear` (candle direction + quality ≥ `minQuality` + regression-slope agreement, already fused into one state)
- **Trigger** — `breakHigh` / `breakLow`, a close beyond the prior `signalLen` bars' high/low

```
longSignal  = strongBull and breakHigh
shortSignal = strongBear and breakLow
```

Efficiency and slope are deliberately not re-checked as separate raw thresholds on top of `strongBull`/`strongBear` — `quality` already weights both, and gating on them a second time would double-count the same evidence without improving selectivity.

## Modes

- **Real Close Dots** — overlays the actual close price as reference dots
- **Subtle Trend Background** — faint green/red background tied to regression slope sign
- **Quality Score Line / Dots** — visual-only quality overlay, no bearing on candle logic
- **Flip Labels** — annotates flip signals with the numeric quality score
