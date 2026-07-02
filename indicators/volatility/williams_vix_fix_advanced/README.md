# Williams VIX Fix Advanced

Synthetic fear gauge (Williams VIX Fix) with dual-direction signals, StdDev and percentile spike bands, stall/absorption context, slow-WVF trend context, divergence wedge, and gradient coloring on a 0–100 bounded panel.

## Features

- **Bullish WVF core** — `(Highest(Close, N) − Low) / Highest(Close, N) × 100`: measures how far below the recent high the current low is — high values = fear / potential bottom
- **Bearish WVF** — `(High − Lowest(Close, N)) / Lowest(Close, N) × 100`: mirror for top detection (complacency spike)
- **Dual spike bands** — StdDev upper band and percentile threshold; spike detected when WVF crosses either (both toggleable)
- **Stall/absorption** — when WVF surges but price barely moves (thin wick, not genuine fear), the signal is marked as absorbed/weak
- **Context line (D-line)** — EMA of the fast WVF; acts as a signal line showing the smoothed fear baseline
- **Divergence wedge** — fills the gap between fast WVF and the context EMA when they move in opposite directions
- **Histogram** — WVF − context EMA; positive on fear spikes, returns to zero as fear fades
- **Gradient coloring** — calm (cyan) → fear (pink) between configurable Normal Fear and Elevated Fear levels
- **Shadow fills** — fear shadow above midline, calm shadow below
- **Pluggable smoothing** — EMA, SMA, RMA, WMA, SuperSmoother, T3, KAMA, JMA Approx (optional, default off)
- **Alerts** — Bull Spike, Bear Spike, and absorbed variants, all bar-close gated

## Scoring

This indicator has no score — it is a pure volatility/fear gauge. Spikes indicate potential exhaustion (fear extremes); they are context signals, not directional triggers.

## Bands

| Band | Purpose |
|---|---|
| StdDev Upper Band | `SMA(WVF, bbl) + mult × StdDev(WVF, bbl)` — dynamic spike threshold |
| Percentile Level | `lowest + rangeHigh% × (highest − lowest)` over `rangeLen` bars — percentile baseline |

A spike fires when WVF crosses either band (individual toggles, OR logic). Default: StdDev band only (2σ) — this is the more selective threshold and works across all timeframes. The percentile threshold adapts to the distribution but can fire too often on sub-daily or low-volatility instruments where all WVF values are inherently small.

## Stall / Absorption

When `WVF − WVF[N] > stallWVFMin` AND `|price change over N bars| < stallFlatATR × ATR`, the spike is marked as absorbed. This catches thin wicks that trigger the fear gauge mechanically without genuine price pressure behind them.
