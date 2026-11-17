# Commodity Pulse Matrix v3

**TradingView:** https://de.tradingview.com/script/aJmdpe8H/

Commodity Pulse Matrix v3 is a comprehensive multi-timeframe confluence indicator designed for commodity trading. It aggregates signals across multiple timeframes into a single scored matrix, showing where the market stands across timeframes, the market regime, and chart-timeframe entry triggers in one view on the chart.

## Features

- 6-Category Multi-Timeframe Scoring (Flow, Momentum, Trend, Volatility, Structure, Divergence)
- Heat Score (multi-timeframe agreement display, 0-1)
- Exhaustion Detection
- MV Confluence (Momentum-Volume)
- Diamond Zones (Support/Resistance)
- Entry Engine V2 (breakout, pullback, continuation with trend and momentum in direction)
- Signal Quality Gate (ATR + Volume)
- Market Regime Detection (BOS, CHoCH)
- Matrix Table Visualization
- Mean Reversion System

## Scoring

Each bar is evaluated across six categories, each contributing to an overall confluence score:

- **Flow** — Directional bias based on price and volume flow
- **Momentum** — Short-term momentum strength and direction
- **Trend** — Medium-to-long-term trend alignment across timeframes
- **Volatility** — Market condition quality relative to ATR expansion/contraction
- **Structure** — Market structure events (Break of Structure, Change of Character)
- **Divergence** — Momentum-price divergences, shown as a context row (weight 0 in the aggregate and the heat score)

The matrix table displays these per-category scores across timeframes, along with a Heat Score (0–1) that shows how far the timeframes and categories agree. Matrix, heat and confidence are display only and have no alerts.

## Entry Engine V2

An entry fires when one of the enabled triggers occurs — a breakout of the prior 8-bar range, a pullback to the fast JMA at support/resistance, or a continuation after a mini-pullback — and two conditions hold:

- **Momentum in direction** — RSI above 50 for longs, below 50 for shorts
- **Not against the bias** — a long is counter-trend when the volatility-stop bias is short (mirrored for shorts). A counter-trend entry and fires only when "Allow Counter-Trend Entries" is on

Breakouts and continuations are off in ranging markets (ATR compression). An entry is shown when the direction changes; repeated entries in the same direction are de-duplicated.

## Modes

- **Compact Mode** (10 rows) — A condensed view suited for smaller screens or mobile use, showing the core timeframe scores without per-category detail rows.
- **Full Mode** (17/18 rows) — The default view, which includes all timeframe scores plus individual Flow, Momentum, Trend, and Divergence detail rows, and a Volume validity row, for deeper analysis.

## Data validity

The Flow category (MFI, OBV, VFI), the VWAP component of the Trend category, the
HTF Midline VWAP mode (v3), and MV Confluence all need real trade volume
(the feed delivers volume and `syminfo.volumetype` is not `tick`). On instruments that only provide tick
volume or none at all these components degrade to neutral automatically — the Flow category keeps its weight with a
neutral score, so missing evidence counts as absent instead of being stretched over the other categories.
The dashboard's "Volume" row shows whether the module is running on real
volume or is currently degraded. See `DATA_VALIDITY.md` in the repo root.
