# Williams VIX Fix Advanced

Synthetic fear gauge (Williams VIX Fix) with dual-direction signals, StdDev and percentile spike bands, stall/absorption context, slow-WVF trend context, divergence wedge, and gradient coloring on a 0–100 bounded panel.

## Features

- **Bullish WVF core** — `(Highest(Close, N) − Low) / Highest(Close, N) × 100`: measures how far below the recent high the current low is — high values = fear / potential bottom
- **Bearish WVF** — `(High − Lowest(Close, N)) / Lowest(Close, N) × 100`: mirror for top detection (complacency spike)
- **Dual spike bands** — StdDev upper band and percentile threshold; spike detected when WVF crosses either (both toggleable)
- **Stall/absorption** — when WVF surges but price barely moves (thin wick, not genuine fear), the signal is marked as absorbed/weak; computed independently for the bullish and bearish side
- **Spike Quality (0–100)** — how far a spike pushed past its own StdDev band and context EMA, penalized when stall/absorption is active
- **Reclaim** — marks the bar where price reclaims the recent range within N bars of a non-absorbed spike; the actionable signal, versus the spike itself which only flags an extreme
- **Context line (D-line)** — EMA of the fast WVF; acts as a signal line showing the smoothed fear baseline
- **Divergence wedge** — fills the gap between fast WVF and the context EMA when they move in opposite directions
- **View Mode** — Clean / Balanced / Full controls how many layers show at once (Clean: core lines + Reclaim + Sentiment Bar; Balanced: + Context/Bands; Full: + Percentile/Fills/Divergence)
- **Gradient coloring** — calm (cyan) → fear (pink) between configurable Normal Fear and Elevated Fear levels
- **Shadow fills** — fear shadow above midline, calm shadow below
- **Pluggable smoothing** — EMA, SMA, RMA, WMA, SuperSmoother, T3, KAMA, JMA Approx (optional, default off)
- **Sentiment bar** — live ±100 bull/bear dominance score with a mini bar on the right edge of the panel: `(WVF ÷ its StdDev band − Bear-WVF ÷ its StdDev band) × 100`. A graded readout, not a fixed Bullish/Bearish claim
- **Alerts** — Bull Spike, Bear Spike, absorbed variants, and Reclaim Long/Short, all bar-close gated

## Scoring

This indicator has no score — it is a pure volatility/fear gauge. Spikes indicate potential exhaustion (fear extremes); they are context signals, not directional triggers.

## Bands

| Band | Purpose |
|---|---|
| StdDev Upper Band | `SMA(WVF, bbl) + mult × StdDev(WVF, bbl)` — dynamic spike threshold |
| Percentile Level | `lowest + rangeHigh% × (highest − lowest)` over `rangeLen` bars — percentile baseline |

A spike fires when WVF crosses either band (individual toggles, OR logic). Default: StdDev band only (2σ) — this is the more selective threshold and works across all timeframes. The percentile threshold adapts to the distribution but can fire too often on sub-daily or low-volatility instruments where all WVF values are inherently small.

## Stall / Absorption

When `WVF − WVF[N] > stallWVFMin` AND `|price change over N bars| < stallFlatATR × ATR`, the spike is marked as absorbed. This catches thin wicks that trigger the fear gauge mechanically without genuine price pressure behind them. The bearish side uses its own `Bear-WVF − Bear-WVF[N]` change against the same price-flatness check, so a bull-side stall never suppresses a bear spike or vice versa.

## Spike Quality

`quality = min(100, spikeExcess × 50 + ctxExcess × 25 + (stall ? 0 : 25))`, where `spikeExcess = max(0, WVF / band − 1)` and `ctxExcess = max(0, WVF / contextEMA − 1)` (mirrored for the bearish side). The quality of the most recent spike is captured and carried into the Reclaim label.

## Reclaim

Within `Spike Recency Window` bars of a non-absorbed spike (`spikeStrong`/`bSpikeStrong`), a Reclaim fires the first bar close breaks back above the prior `Reclaim Confirmation Length`-bar high (long) or below the prior low (short). `Min Spike Quality for Reclaim` (default 0 = disabled) can require the originating spike to have scored above a threshold before the reclaim is marked.
