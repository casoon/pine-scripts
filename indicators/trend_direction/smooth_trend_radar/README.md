# Smooth Trend Radar

Double-smoothed Supertrend baseline for trend direction, with pivot-based rejection signals at the baseline, statistical overextension highlighting, and automatic SL/TP level visualization on each trend flip.

## Features

- **Double-smoothed baseline**: Supertrend upper and lower bands are averaged, then passed through WMA → EMA — significantly fewer whipsaws than standard Supertrend
- **Auto Timeframe Scaling**: Supertrend factor, ATR period, smoothing lengths, pivot window, and overextension threshold all auto-adjust to the chart timeframe (1m → W). Manual inputs remain as fallback when scaling is disabled
- **Slope-based trend direction**: bullish when the smoothed baseline rises, bearish when it falls — no price-to-band crossing required
- **Pivot-based rejection signals**: confirmed swing low/high at the baseline, validated by sustained baseline contact and a slope filter — one signal per actual extremum, no clustering
- **Statistical overextension**: bars where the absolute distance from baseline ranks in the top X% of the lookback window are flagged with accent candle coloring (purple = price far below baseline, orange = far above) — self-adapts to symbol/timeframe characteristics
- **SL/TP visualization**: on every trend flip (or rejection re-entry), entry, SL, and three TP levels are drawn with extended horizontal lines, labels, and risk/reward fills
- **Re-Entry on Rejection**: after an SL hit with unchanged trend, the next confirmed rejection signal rebuilds the full setup at current price
- **Trail to Break-Even**: optional — when TP1 is hit, SL moves to entry price so the trade can no longer result in a loss
- **Hover tooltips**: every flip and rejection label shows price, direction, and timestamp on hover

## Calculation

```
midline   = avg(supertrend_lower, supertrend_upper)
baseline  = EMA(WMA(midline, wmaLength), emaLength)

trend     = 1   when baseline > baseline[1]   (rising)
trend     = -1  when baseline < baseline[1]   (falling)
```

## Auto Timeframe Scaling

The smoothing parameters need to scale with timeframe to keep the baseline responsive without being noisy. Defaults per timeframe:

| Timeframe | ST Factor | ATR Period | WMA | EMA | Pivot Bars | Overext Lookback |
|-----------|-----------|------------|-----|-----|-----------|------------------|
| 1m        | 4.0       | 10         | 8   | 3   | 2         | 100              |
| 5m        | 5.0       | 14         | 10  | 4   | 2         | 100              |
| 15m       | 6.0       | 20         | 15  | 5   | 2         | 100              |
| 30m       | 7.0       | 25         | 18  | 6   | 2         | 100              |
| 1H        | 5.0       | 14         | 10  | 3   | 2         | 100              |
| 4H        | 10.0      | 50         | 30  | 10  | 3         | 100              |
| D         | 12.0      | 90         | 40  | 14  | 5         | 100              |
| W         | 14.0      | 120        | 50  | 18  | 4         | 100              |

Disable Auto Scaling to use the manual input values exclusively.

## Rejection Signal

A rejection fires when **all** of the following hold at a confirmed pivot bar (`pivBars` left and right confirmation):

1. `ta.pivotlow(low)` (or `pivothigh(high)` for bear) is non-na — a real swing point
2. The pivot value touches the baseline: `pivLow <= tL` (or `pivHigh >= tL`)
3. Trend at the pivot bar matches the signal direction (`trend == 1` for bull)
4. **Slope filter**: baseline is rising over `slopeLookback` bars (`tL > tL[N]`) — filters flat / chop zones
5. **Touch validation**: in the pivot window, at least `contFactor` bars touched the baseline — filters single-spike touches

The signal fires `pivBars` after the actual pivot (non-repainting), but the marker is displayed exactly at the pivot bar via `bar_index - pivBars` offset.

## Overextension Detection

Statistical, not threshold-based:

```
distAbs   = |close − baseline|
percRank  = ta.percentrank(distAbs, lookback)
overext   = percRank > threshold
```

When `overext` is true, the candle is colored with an accent color (configurable). The signed distance determines which side: bull-side overextension (price below baseline → potential reversal up) or bear-side (above → potential reversal down).

This approach is **self-adapting**: it doesn't matter whether the symbol is volatile or quiet, intraday or daily — the percentile rank is always relative to recent behavior. No multiplier tuning per timeframe is needed.

## SL / TP Modes

**SL Methods**:
- `Flip Candle` — low/high of the flip bar ± ATR × multiplier
- `Baseline` — smoothed baseline ± ATR × multiplier
- `Swing` — lowest low / highest high within `swingLookback` ± ATR

**TP Modes**:
- `Pivot` — daily/weekly/monthly Camarilla or Classic R/S levels (auto-fallback to ATR if levels land on the wrong side of entry)
- `R-Multiple` — multiples of SL distance (1R / 2R / 3R style)
- `Fibonacci` — 0.618 / 1.0 / 1.618 of the setup-swing range
- `ATR` — multiples of long ATR

## Visual Reference

| Element | Meaning |
|---------|---------|
| Teal/red line | Baseline — color follows trend |
| ▲ ▼ on baseline | Trend flip — direction-confirmed entry signal |
| Small ▲ ▼ at price | Rejection signal at confirmed pivot |
| Purple candle | Bull-side overextension (price far below baseline) |
| Orange candle | Bear-side overextension (price far above baseline) |
| Horizontal lines | Active setup — entry, SL, TP1, TP2, TP3 |
| Red fill | Risk zone — entry to SL |
| Green fill | Reward zone — entry to TP3 |
