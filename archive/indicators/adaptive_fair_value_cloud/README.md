# Adaptive Fair Value Cloud

Adaptive Fair Value Cloud plots a volatility-adaptive channel around a configurable centerline (EMA, KAMA, Regression, or VWMA). Band width blends ATR and mean absolute deviation, then scales with a regime-aware multiplier that widens in expansion, narrows in compression, and adjusts for trend/range conditions — so the cloud stays proportionate to current market behavior instead of using a fixed multiplier.

## Features

- Selectable Centerline (EMA, KAMA, Regression, VWMA)
- ATR + Mean-Deviation Blended Band Width
- Regime-Adaptive Width Multiplier (Compression / Expansion / Range / Trend)
- Trend Sensors (Slope, ADX, Efficiency Ratio, R²)
- Cloud Break and Fair Value Reclaim/Reject Signals
- Watch Layer: Regime-Acceleration, Squeeze-Release, and Divergence-at-Edge early warnings
- Regime Dashboard

## Regimes

The width multiplier and cloud color are driven by a regime classification built from four sensors:

- **Slope** — direction of the regression centerline, normalized by ATR
- **ADX** — trend strength
- **Efficiency Ratio** — how directional recent price movement is versus noise
- **R²** — how well price fits the regression line

These combine into five regimes: **Compression** (low volatility percentile, high choppiness), **Expansion** (high volatility percentile, high efficiency), **Range** (high choppiness, low ADX), **Trend Up/Down** (aligned slope, ADX, efficiency, and R²), and **Neutral** otherwise.

## Signals

- **Cloud Break** — close crosses the outer band while trending or expanding
- **Fair Value Reclaim/Reject** — close crosses the centerline while trending, without breaching the opposite outer band

Both are coincident confirmations: they fire once the move has already happened.

## Watch Layer (leading, unconfirmed)

Three early-warning signals that fire *before* the confirmed triggers above. None of them predict direction with certainty — they flag a rising probability of a move, not a guaranteed one:

- **Regime Building** (↑/↓) — Efficiency Ratio and R² are accelerating while the trend gate (ADX/Efficiency/R² thresholds) hasn't tripped yet. Fires ahead of a Trend Up/Down regime flip.
- **Squeeze Releasing** — Band width was near a multi-bar low and is now widening. Flags that a volatility expansion is starting; direction is not implied.
- **Divergence at Edge** (↑/↓) — Price sets a new pivot extreme at the outer band that RSI does not confirm (classic divergence), checked specifically where price touches the band.

The dashboard's **Watch** row shows which of these is currently active.
