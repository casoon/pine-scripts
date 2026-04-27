# Smooth Trend Radar

Double-smoothed Supertrend baseline for trend direction, with rejection signals at the baseline and automatic SL/TP level visualization on trend flips.

## Features

- **Double-smoothed baseline**: Supertrend upper and lower bands are averaged, then passed through WMA → EMA — significantly fewer whipsaws vs. standard Supertrend
- **Slope-based trend direction**: bullish when the smoothed baseline rises, bearish when it falls — no price-to-band crossing required
- **Rejection counter**: counts consecutive bars where price touches the baseline; fires a signal after N bars (configurable)
- **SL/TP visualization**: on every trend flip, entry, SL, and three TP levels are drawn as horizontal lines extending 40 bars forward
- **Risk/reward fill**: semi-transparent fills between entry–SL (red) and entry–TP3 (green) for at-a-glance R:R assessment
- **Direction-aware alerts**: TP and SL hit alerts adjust for long vs. short trade direction

## Calculation

```
midline = avg(supertrend_lower, supertrend_upper)
baseline (tL) = EMA(WMA(midline, wmaLength), emaLength)

trend = 1  when tL > tL[1]  (rising)
trend = -1 when tL < tL[1]  (falling)

SL (long)  = low  − ATR × slMultiplier
SL (short) = high + ATR × slMultiplier

TP1/2/3 = entry ± |entry − SL| × tp1/2/3Multiplier
```

## Rejection Signal

A rejection fires when price crosses the baseline (`high > tL and low < tL`) for `contFactor` consecutive bars without the trend flipping. The counter resets on any non-touching bar or trend change. This identifies consolidation at the baseline before continuation.

## Notes

- The default Supertrend factor (12) and ATR period (90) are intentionally large — the double smoothing needs wide bands as input to produce a stable baseline
- Changing oscillator to shorter settings without adjusting WMA/EMA lengths will produce noisy output
- SL and TP lines show only the most recent signal; previous setups are removed on the next flip
