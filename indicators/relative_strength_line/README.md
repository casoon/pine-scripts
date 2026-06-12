# Relative Strength Line

**TradingView:** _(unpublished)_

Measures how the chart symbol performs **relative to a benchmark** (SPY, QQQ, or any symbol) rather than in absolute terms — the dimension institutions actually trade: they buy what is *stronger than the market*. The indicator plots the classic RS line (price ÷ benchmark) or the normalized Mansfield RS oscillator, and turns it into an **actionable confluence signal**.

Designed for momentum equities (Tesla, Cloudflare, Microsoft, Apple, …) where relative strength vs. the index is the primary stock-selection filter.

## The key idea: confluence, not raw RS

Relative strength alone is decoupled from price — a stock can be *relatively* strong (falling less than the market) while its own chart falls. A signal on raw RS would then say "long" while price drops, which is useless. So a signal here fires **only when both agree**:

- **LONG** — the stock outperforms the benchmark (Mansfield > 0) **and** is in its own uptrend (price above its trend EMA)
- **SHORT** — it underperforms **and** is in its own downtrend

That makes a green mark a genuine *leader that is also rising*, and structurally rules out the "green while price falls" contradiction.

## Features

- **Two display modes** (one pane, no scale conflict):
  - **Mansfield RS** (default) — normalized oscillator around zero: the % distance of the RS line from its own moving average. Above 0 = outperforming the benchmark, below 0 = lagging.
  - **Raw RS Line** — the price ÷ benchmark ratio itself, with its moving average.
- **Confluence markers** — green up-triangle below the line on a long setup, red down-triangle above on a short (standard trading convention). Fires on entry into the regime, throttled by a minimum bar gap.
- **Dashboard** — relative strength (leads/lags + Mansfield %), absolute price trend, and the **Setup verdict** (LONG / SHORT / Neutral)
- **Right-edge tag** with the live setup
- **Alerts** — long/short confluence, Mansfield zero-cross up/down

## How to read it

- **Setup = LONG** → the stock beats the market *and* is trending up — a momentum-leader long candidate.
- **Mansfield > 0 but Price Trend = Down** → relatively strong but absolutely falling → **no signal** (this is the case that used to mislead). It tells you the stock is holding up better than the index, but it is not a long.
- **Mansfield crossing below 0** → the stock has started lagging the benchmark; rotate attention elsewhere even if price still rises.

## Benchmark choice

- `AMEX:SPY` (default) — broad market, S&P 500. The IBD standard.
- `NASDAQ:QQQ` — Nasdaq 100; usually the better reference for tech/momentum names.
- Any symbol works (e.g. a sector ETF) via the symbol picker.

## Settings

| Group | Input | Default | Purpose |
|---|---|---|---|
| Relative Strength | Benchmark | AMEX:SPY | Symbol to measure against |
| Relative Strength | Display | Mansfield RS | Oscillator vs. raw ratio |
| Relative Strength | Mansfield MA Length | 50 | MA the RS distance is measured from |
| Confluence Signal | Price Trend EMA | 50 | EMA of the stock's price defining its absolute trend (the long/short filter) |
| Confluence Signal | Min Bars Between Markers | 5 | De-clutter repeated markers |
| Confluence Signal | Marker Distance from Line | 0.4 | Vertical gap of the marker from the line (× stdev) |

## Notes

- The RS line uses `request.security` with `lookahead_off` — no repainting beyond the standard same-timeframe behavior.
- On a symbol where the benchmark has no data for the timeframe, RS is `na` and the dashboard shows "—".
