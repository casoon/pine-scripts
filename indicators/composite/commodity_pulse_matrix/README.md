# Commodity Pulse Matrix v3

**TradingView:** https://de.tradingview.com/script/aJmdpe8H/

Commodity Pulse Matrix v3 is a comprehensive multi-timeframe confluence indicator designed for commodity trading. It aggregates signals across multiple timeframes into a single scored matrix, giving traders a clear read on setup quality, market regime, and entry timing from a unified view on the chart.

## Features

- 6-Category Multi-Timeframe Scoring (Flow, Momentum, Trend, Volatility, Structure, Divergence)
- Heat Score System (Setup quality 0-1)
- Exhaustion Detection
- MV Confluence (Momentum-Volume)
- Diamond Zones (Support/Resistance)
- Entry Timing (Break-Pullback-Continuation)
- Signal Quality Gate (ATR + Volume)
- Market Regime Detection (BOS, CHoCH)
- Risk Management (ATR-based SL/TP)
- Matrix Table Visualization
- Mean Reversion System

## Scoring

Each bar is evaluated across six categories, each contributing to an overall confluence score:

- **Flow** — Directional bias based on price and volume flow
- **Momentum** — Short-term momentum strength and direction
- **Trend** — Medium-to-long-term trend alignment across timeframes
- **Volatility** — Market condition quality relative to ATR expansion/contraction
- **Structure** — Market structure events (Break of Structure, Change of Character)
- **Divergence** — Momentum-price divergence signals indicating potential reversals

The matrix table displays these per-category scores across timeframes, along with a combined Heat Score (0–1) representing overall setup quality at a glance.

## Modes

- **Compact Mode** (10 rows) — A condensed view suited for smaller screens or mobile use, showing the core timeframe scores without per-category detail rows.
- **Full Mode** (17/18 rows) — The default view, which includes all timeframe scores plus individual Flow, Momentum, Trend, and Divergence detail rows, and a Volume validity row, for deeper analysis.

## Data validity

The Flow category (MFI, OBV, VFI), the VWAP component of the Trend category, the
HTF Midline VWAP mode (v3), and MV Confluence all need real trade volume
(`syminfo.volumetype` = `base`/`quote`). On instruments that only provide tick
volume or none at all (most CFDs, forex, many indices) these components degrade
to neutral automatically — the Flow category weight is excluded and the other
categories are renormalized instead of a false score dragging the total down.
The dashboard's "Volume" row shows whether the module is running on real
volume or is currently degraded. See `DATA_VALIDITY.md` in the repo root.
