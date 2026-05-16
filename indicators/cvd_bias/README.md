# CVD Bias

Estimates Cumulative Volume Delta (CVD) over a rolling window — buying volume (close near the high) minus selling volume (close near the low), accumulated as a running total rather than smoothed into an oscillator. The distinction matters: an EMA-based indicator like CPI or WaveTrend reacts to recent bars; CVD shows whether the net flow has been persistently bullish or bearish over the window and whether that accumulation is accelerating or reversing. The key signal is divergence: price making a new extreme while CVD rate of change opposes it — indicating the price move is not backed by volume conviction.

## Features

- **Per-bar delta**: `(2 × close_location − 1) × volume` — no derived price oscillator
- **Rolling CVD**: sum of deltas over the accumulation window, normalized to −1..+1 via recent amplitude
- **CVD rate of change**: 1st derivative of normalized CVD — shows acceleration/deceleration of buying/selling pressure
- **Price/CVD divergence**: fires when price prints a new N-bar high (or low) while CVD rate of change is falling (or rising) — suggesting the price extreme is not volume-confirmed
- **Dashboard**: state (Strong Bull / Bull / Neutral / Bear / Strong Bear), CVD value, rate direction, active divergence

## Settings

| Group | Setting | Default | Purpose |
|---|---|---|---|
| CVD Settings | Accumulation Window | 50 | Bars over which delta is summed |
| CVD Settings | Normalization Lookback | 200 | Lookback for recent CVD amplitude (keeps output on −1..+1) |
| CVD Settings | Rate of Change Length | 5 | Bars used for CVD ROC (derivative) |
| Divergence | Detect Divergences | On | Enable price/CVD divergence markers |
| Divergence | New Extreme Lookback | 20 | N-bar window for defining a "new high" or "new low" |
| Display | Show Dashboard | On | Toggle the info table |

## Difference from Candle Pressure Index

Both indicators use close location and volume. CPI applies body ratio and volume rank normalization, then takes an EMA — producing a smoothed oscillator. CVD omits body ratio, uses raw volume (not rank-normalized), and sums rather than smooths — producing a running total that captures sustained accumulation or distribution over longer windows.
