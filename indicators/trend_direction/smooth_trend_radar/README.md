# Smooth Trend Radar

Double-smoothed Supertrend baseline for trend direction, with pivot-based rejection signals at the baseline, statistical overextension highlighting, and automatic SL/TP level visualization on each trend flip.

## Features

- **Double-smoothed baseline**: Supertrend upper and lower bands are averaged, then passed through WMA → EMA — significantly fewer whipsaws than standard Supertrend
- **Auto Timeframe Scaling**: Supertrend factor, ATR period, smoothing lengths, pivot window, and overextension threshold all auto-adjust to the chart timeframe (1m → W). Manual inputs remain as fallback when scaling is disabled
- **Volatility-Adaptive Band Width** (optional): scales the Supertrend factor by the instrument's own ATR percentile rank, so the same factor produces comparable relative band width across instruments — off by default
- **Slope-based trend direction**: baseline slope over `Trend Slope Lookback` bars, scaled to ATR units. Trend flips only when the move exceeds `Trend Slope Threshold` and holds its previous value otherwise (hysteresis) — filters micro-noise flips
- **Trend strength**: baseline-slope magnitude ranked against its own recent history — self-adapting like Overextension, not a fixed threshold. Flags a "strong trend" state (optional background tint) and tags rejection signals fired during it, with a dedicated alert pair for rejection entries inside an already-strong trend
- **Live baseline rejection signals**: validated by sustained baseline contact, a slope filter, and optional bar-polarity and volume filters. Fires in both ADX regimes, tagged "Trend Pullback" (trending) or "Range Rejection" (sideways) in the tooltip
- **Statistical overextension**: bars where the absolute distance from baseline ranks in the top X% of the lookback window are flagged with accent candle coloring (purple = price far below baseline, orange = far above) — self-adapts to symbol/timeframe characteristics
- **SL/TP visualization**: on every trend flip (or rejection re-entry), entry, SL, and three TP levels are drawn with extended horizontal lines, labels, and risk/reward fills
- **Re-Entry on Rejection**: after an SL hit with unchanged trend, the next confirmed rejection signal rebuilds the full setup at current price
- **Trail to Break-Even**: optional — when TP1 is hit, SL moves to entry price so the trade can no longer result in a loss
- **Hover tooltips**: every flip and rejection label shows price, direction, and timestamp on hover

## Calculation

```
midline   = avg(supertrend_lower, supertrend_upper)
baseline  = EMA(WMA(midline, wmaLength), emaLength)

slope     = baseline - baseline[trendSlopeLookback]
trend     = 1   when slope >  atr * trendSlopeThreshold
trend     = -1  when slope < -atr * trendSlopeThreshold
trend     = trend[1]   otherwise (holds previous value — hysteresis)
```

## Trend Strength

Statistical, not threshold-based — same percentile-rank approach as Overextension, but on a
different axis (slope magnitude, not distance from baseline):

```
slopeMag   = |slope| / atr
strengthPctRank = percentrank(slopeMag, strengthLookback)
strongTrend = strengthPctRank > strengthThreshold
```

`strongTrend` marks bars where the baseline is moving faster than usual for this symbol/timeframe
— i.e. a decisive, high-conviction move rather than a bare threshold-crossing. Distance from the
baseline already has the opposite meaning (Overextension = stretched = reversal risk), so it isn't
reused here — strength reads the baseline's own rate of movement instead.

Used for: an optional background tint while active, a "Strong Trend" note in rejection tooltips,
and a dedicated `STR Bull/Bear Rejection (Strong Trend)` alert pair — for entering rejection
pullbacks specifically inside an already-strong trend rather than every rejection.

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

Disable Auto Scaling to use the manual input values exclusively. Enable **Volatility-Adaptive Band Width** to additionally scale the Supertrend factor by the instrument's own ATR percentile rank (200-bar lookback) — keeps relative band width comparable across instruments (crypto vs. forex vs. commodities) instead of relying on the fixed per-timeframe factor alone.

## Rejection Signal

Pivots are not used for signal timing — rejection is detected live, from the current bar plus recent baseline contact. A rejection fires when **all** of the following hold on the current bar:

1. Price touches the baseline this bar: `low <= tL and close > tL` for bull (or `high >= tL and close < tL` for bear)
2. Trend matches the signal direction (`trend == 1` for bull)
3. **Slope filter**: baseline is rising over `slopeLookback` bars (`tL > tL[N]`) — filters flat / chop zones
4. **Touch validation**: at least `contFactor` of the last bars touched the baseline in the trend direction — filters single-spike touches
5. **Polarity filter** (optional): pivot bar's body or close-position matches direction
6. **Volume filter** (optional): bar volume exceeds its own SMA — confirms rejections with real participation

Rejections fire in **both** ADX regimes — a pullback in an active trend is as valid a signal as one in a range. The regime is not a gate; it's carried as a tooltip tag: **Trend Pullback** when `isTrending` (ADX above threshold), **Range Rejection** when `isSideways`.

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
| Faint teal/red background | Strong Trend zone — slope percentile above threshold |
| Horizontal lines | Active setup — entry, SL, TP1, TP2, TP3 |
| Red fill | Risk zone — entry to SL |
| Green fill | Reward zone — entry to TP3 |
