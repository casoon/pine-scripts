# Chandelier Flip Radar

ATR-based trailing stop with five-level trend state classification. Instead of a binary long/short flip, trend weakening becomes visible before the actual direction change through progressive bar coloring and configurable warning/danger zones.

## Features

- **Ratchet trailing stop**: long stop ratchets up only, short stop ratchets down only
- **Body filter**: direction only changes when the flipping candle has a minimum body relative to ATR — weak/doji flips are ignored, not just unlabeled
- **Five-level state**: strong → softening → warning (yellow) → danger (orange) → flip
- **Correct distance measurement**: warning/danger zones measure to `longStopPrev` / `shortStopPrev` — the actual flip trigger, not the current stop value
- **Inactive stop**: opposing stop shown as gray line — see where the flip trigger sits
- **Trap markers**: wick crossed the flip trigger intrabar but close held — often a stop hunt or liquidity grab
- **Adaptive ATR multiplier**: optional scaling based on volatility regime (ATR vs. 100-bar average)
- **Alert conditions** and `alert()` calls for flips and traps

## State System

| State | Condition | Bar color |
|---|---|---|
| +2 Strong long | dir=1, far from trigger, no pullback | Full bullish |
| +1 Long softening | dir=1, pullback or in warning zone | Faded bullish |
| Warning layer | distAtr < warnDist (either direction) | Yellow (overrides +1/−1) |
| 0 Danger | distAtr < dangerDist | Orange |
| −1 Short softening | dir=−1, pullback or in warning zone | Faded bearish |
| −2 Strong short | dir=−1, far from trigger, no pullback | Full bearish |

## Calculation

```
longStop  = highest(close | high, period) − ATR × mult   [ratchets up only]
shortStop = lowest(close  | low,  period) + ATR × mult   [ratchets down only]

flipLong  = close > shortStopPrev AND body ≥ ATR × bodyFilter
flipShort = close < longStopPrev  AND body ≥ ATR × bodyFilter

triggerStop = dir==1 ? longStopPrev : shortStopPrev
distAtr     = |close − triggerStop| / ATR
```

## Traps

A trap fires when price crosses the flip trigger intrabar (wick) but the close holds on the current side. These often indicate a liquidity grab, stop hunt, or failed breakout — and frequently precede continuation in the original direction.
