# Chandelier Flip Radar

ATR-based trailing stop with a directional, multi-level trend state. Instead of a binary long/short flip, trend weakening becomes visible before the actual direction change through progressive bar coloring and configurable warning/danger zones. Its role is trend leadership / exit-risk / flip early-warning — not a standalone entry trigger.

> **Family note:** the sibling indicator *Adaptive Supertrend* (hl2-anchored, conviction-adaptive bands) was archived; its MTF confluence layer was absorbed here as an optional, off-by-default overlay. Chandelier remains the maintained member of the ATR trailing-stop-flip family — it anchors at HH/LL ± k×ATR and specializes in *early-warning state classification* with a validated strategy behind it.

## Features

- **Ratchet trailing stop**: the active stop holds until an *accepted* flip and is never loosened by a body-rejected close past the trigger (ratchet keyed to the accepted direction, not raw price)
- **Body filter**: direction only changes when the flipping candle has a minimum body relative to ATR — weak/doji flips are ignored, not just unlabeled
- **Directional state**: per-side strong / soft / danger — the direction is preserved even in the danger zone
- **Correct distance measurement**: warning/danger zones measure to `longStopPrev` / `shortStopPrev` — the actual flip trigger, not the current stop value
- **Inactive stop**: opposing stop shown as gray line — see where the flip trigger sits
- **Three flip qualities**: confirmed flip (circle/label) · weak flip (×, body too weak) · trap (triangle, wick crossed but close held)
- **Four adaptive modes**: Off (fixed) / Simple (volatility-regime scaler) / K-means (best-performing Chandelier factor) / Conviction (trend-aware band)
- **K-means cluster selector**: Best / Average / Worst performance cluster as multiplier source, with a Performance AMA and optional factor label
- **Alert conditions** and `alert()` calls for flips and traps

## State System

The state carries direction at every level — danger keeps its sign, so you always know *danger in a long trend* vs *danger in a short trend*. Warning (yellow) and danger (orange) are an additional **bar-color layer** flagging an imminent flip; the stop line itself stays green/red so direction is never lost.

| State | Condition | Stop line | Bar color |
|---|---|---|---|
| +3 Strong long | dir=1, far from trigger, no pullback | Full bullish | Bullish |
| +2 Soft long | dir=1, pullback or in warning zone | Faded bullish | Yellow (warning) |
| +1 Danger long | dir=1, distAtr < dangerDist | Faded bullish | Orange (danger) |
| −1 Danger short | dir=−1, distAtr < dangerDist | Faded bearish | Orange (danger) |
| −2 Soft short | dir=−1, pullback or in warning zone | Faded bearish | Yellow (warning) |
| −3 Strong short | dir=−1, far from trigger, no pullback | Full bearish | Bearish |

## Adaptive Modes

| Mode | Multiplier source |
|---|---|
| Off | Fixed `ATR Multiplier`. |
| Simple | Volatility-regime scaler: wider in high volatility (ATR vs. 100-bar avg), tighter in low. **Not** trend strength. |
| K-means | K-means clustering over a factor range self-selects the best-performing factor. Each candidate simulates the **real Chandelier stop** (HH/LL ± k·ATR), not a Supertrend proxy. |
| Conviction | Trend-aware: ATR percentile rank + EMA-separation trend force, with a chop penalty. High conviction → multiplier below base (tighter); low → above base (wider), clamped to `[0.6×, 1.8×]`. |

## Calculation

```
longStop  = highest(close | high, period) − ATR × mult   [holds while long, re-seeds on flip]
shortStop = lowest(close  | low,  period) + ATR × mult   [holds while short, re-seeds on flip]

flipLong  = close > shortStopPrev AND body ≥ ATR × bodyFilter
flipShort = close < longStopPrev  AND body ≥ ATR × bodyFilter

triggerStop = dir==1 ? longStopPrev : shortStopPrev
distAtr     = |close − triggerStop| / ATR
```

## Flip Qualities

Three distinct events around the flip trigger:

- **Trap** (triangle) — wick crossed the trigger intrabar but the close held on the current side. Often a liquidity grab, stop hunt, or failed breakout, and frequently precedes continuation in the original direction.
- **Weak flip** (×) — the close *broke* the trigger, but the candle body was too weak to confirm (body filter rejected it). Direction holds; the stop does not loosen.
- **Confirmed flip** (circle / label, or diamond with HTF confluence) — close broke the trigger with a sufficient body. Direction changes.

## MTF Confluence (optional, off by default)

When enabled, a higher-timeframe Chandelier stop runs on `Higher Timeframe` (default 4H) as a **fixed-multiplier structural anchor** — same ATR Period, Multiplier and extremum mode as the chart, but no adaptive mode. It adds three display elements without touching the base signal path:

- **HTF stop line** — a step-line at the HTF stop level, in a transparent trend color.
- **Pullback zone** — when the chart trend opposes the HTF trend, the background takes a subtle tint in the HTF direction (the "pullback against the higher trend" state).
- **Confluence flips** — when a flip aligns with the HTF trend, a **diamond** marker replaces the plain dot. Non-aligned flips keep the normal dot/label.

The HTF reference uses `lookahead=off` — values update only on confirmed HTF bar closes, no lookahead bias. With MTF off, the chart, markers and alerts are identical to the base behavior, so the validated strategy path is unchanged.
