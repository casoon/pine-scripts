# Chandelier Exit

ATR-based trailing stop with five-level trend state classification. Instead of a binary long/short flip indicator, trend weakening becomes visible before the actual direction change through progressive bar coloring and configurable warning zones.

## Features

- **Ratchet trailing stop**: long stop ratchets up only, short stop ratchets down only — never pulls back against the trend
- **Five-state classification**: strong → pullback/warning → danger → flip, each with distinct color
- **Progressive bar coloring**: full color (strong) → faded (pullback) → yellow (warning zone) → orange (danger zone near trigger)
- **Inactive stop**: opposing stop visible as gray line — see where the flip trigger is without guessing
- **Failed flip marker**: wick crossed the trigger intrabar but close held — often a stop hunt or liquidity grab
- **Body filter**: flip signals require a minimum candle body relative to ATR, reducing noise from doji and inside-bar crossings
- **Adaptive ATR multiplier**: optional scaling based on volatility regime (ATR vs. 100-bar average) — keeps stop proportional in both calm and volatile phases
- **Alert conditions** and `alert()` calls for flips and failed flips

## State System

| State | Condition | Bar color |
|---|---|---|
| +2 Strong long | dir=1, far from trigger, no pullback | Full bullish |
| +1 Long softening | dir=1, pullback or in warning zone | Faded bullish |
| 0 Danger | Distance to trigger < Danger threshold | Orange |
| −1 Short softening | dir=−1, pullback or in warning zone | Faded bearish |
| −2 Strong short | dir=−1, far from trigger, no pullback | Full bearish |

Warning zone (yellow bar color) applies when distance to trigger is between the Danger and Warning thresholds.

## Calculation

```
longStop  = highest(close | high, period) − ATR × mult   [ratchets up only]
shortStop = lowest(close  | low,  period) + ATR × mult   [ratchets down only]

dir = 1  when close > shortStop[1]
dir = -1 when close < longStop[1]

distAtr = |close − triggerStop| / ATR
```

## Failed Flip

A failed flip occurs when price crosses the opposing stop intrabar (wick) but the close stays on the current side. These are marked with small triangles and often indicate:

- Liquidity grab / stop hunt
- Failed breakout with continuation
- Institutional absorption at the trigger level
