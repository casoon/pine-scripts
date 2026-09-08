# CVD Bias

Estimates a price-weighted volume balance over a rolling window. This is **not** real Cumulative Volume Delta — OHLCV data carries no aggressor-side/trade classification, so "buying" and "selling" volume are inferred only from where price closed within the bar's range, never from actual trade direction. Real Delta/CVD requires `request.footprint()` (out of scope here). Within that heuristic, the indicator accumulates the per-bar signed-volume proxy as a running total rather than smoothing it into an oscillator. The distinction matters: an EMA-based indicator like CPI or WaveTrend reacts to recent bars; this proxy shows whether the price-weighted balance has been persistently skewed bullish or bearish over the window and whether that skew is accelerating or reversing. The key signal is divergence: price making a new extreme while the proxy's rate of change opposes it — indicating the price move is not backed by the same volume skew.

## Features

- **Per-bar signed-volume proxy**: `(2 × close_location − 1) × volume` — a heuristic, not real trade delta; no derived price oscillator
- **Rolling sum**: sum of the proxy over the accumulation window, normalized to −1..+1 via recent amplitude
- **Rate of change**: 1st derivative of the normalized proxy — shows acceleration/deceleration of the volume-balance skew
- **Price/proxy divergence**: fires when price prints a new N-bar high (or low) while the proxy's rate of change is falling (or rising) — suggesting the price extreme is not backed by the same volume skew
- **Dashboard**: state (Strong Bull / Bull / Neutral / Bear / Strong Bear), proxy value, rate direction, active divergence
- **Alerts**: bull/bear divergence, zero cross up/down

## Instrumente

- **Valid:** any symbol whose `syminfo.volumetype` reports `base` or `quote` — as a rule futures, exchange-listed stocks and crypto exchanges, plus broker feeds that pass real traded quantity through.
- **Proxy:** where that volume is a broker's own share of the market (a CFD feed reporting `base`), the reading describes that broker's flow, not the exchange's — an approximation, not exchange volume.
- **Invalid:** any symbol reporting `tick` (a count of price updates) or `n/a` — there is nothing to weight.

On invalid instruments the indicator shows a "benötigt echtes Handelsvolumen" (needs real trade volume) label on the last bar and plots nothing, instead of silently computing on tick volume.

A reference-market volume (e.g. `NYMEX:NG1!` for NatGas) would not fix this: the proxy is tied to the close-location of the chart's own candles — mapping another market's volume onto the CFD's price geometry would attribute trading activity that never happened on that market to bars that happened on this one. That is not "better volume for the same score," it is an unfounded link between two feeds, and per `DATA_VALIDITY.md` §4.1 it would additionally force a price comparison between the CFD and the future that the framework deliberately avoids outside a dedicated context module. Degradation (label + no output) remains the right answer here, not a reference-market request.

## Settings

| Group | Setting | Default | Purpose |
|---|---|---|---|
| CVD Settings | Accumulation Window | 50 | Bars over which the signed-volume proxy is summed |
| CVD Settings | Normalization Lookback | 200 | Lookback for recent amplitude (keeps output on −1..+1) |
| CVD Settings | Rate of Change Length | 5 | Bars used for the proxy's rate of change (derivative) |
| Divergence | Detect Divergences | On | Enable price/proxy divergence markers |
| Divergence | New Extreme Lookback | 20 | N-bar window for defining a "new high" or "new low" |
| Display | Show Dashboard | On | Toggle the info table |

## Difference from Candle Pressure Index

Both indicators use close location and volume. CPI applies body ratio and volume rank normalization, then takes an EMA — producing a smoothed oscillator. This indicator omits body ratio, uses raw volume (not rank-normalized), and sums rather than smooths — producing a running total that captures sustained accumulation or distribution over longer windows. Neither is real order flow — both are price-weighted volume heuristics.
