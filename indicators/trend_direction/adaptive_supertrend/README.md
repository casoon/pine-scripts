# Adaptive Supertrend

A Supertrend indicator with conviction-adaptive band width. Instead of a fixed ATR multiplier, the band narrows when the market is trending strongly and widens when conditions are choppy or volatility is contracting. This means the stop trails price more tightly during high-conviction moves and gives more room during uncertain regimes — without requiring any manual parameter adjustment per timeframe.

> **Relation to [chandelier_flip_radar](../chandelier_flip_radar/):** same family — ATR trailing-stop flip with ratchet, body filter and trap markers — but different anchor and focus. This indicator adds conviction-adaptive band width and an MTF confluence layer; Chandelier Flip Radar adds five-level early-warning states, AI factor selection and has a validated strategy behind it.

## Features

- Adaptive band width driven by a transparent conviction score (ATR rank, trend force, chop detection)
- Each conviction component can be individually enabled or disabled
- Conviction table in the chart corner showing live component values and the resulting multiplier
- Optional RSI overbought filter: blocks flip signals when RSI is already overextended in the flip direction
- Gradient trend cloud between stop line and price
- Glow effect on the stop line; triangle flip markers and trap (X) markers
- MTF confluence: higher-TF Supertrend direction, pullback zone highlighting, and diamond confluence signals

## Conviction System

Conviction is a 0–1 score that modulates how much the base multiplier expands or contracts:

```
adaptiveMult = baseMult × (1 + adaptivity × (1 − conviction))
```

At conviction = 1 (maximum), the multiplier equals `baseMult` (tightest stop).  
At conviction = 0 (minimum), the multiplier reaches `baseMult × (1 + adaptivity)` (widest stop).

**Components:**

| Component | What it measures | Effect when high |
|---|---|---|
| ATR Rank | ATR percentile over 100 bars (capped at 85%) | Raises conviction — expanding volatility suggests a real move |
| Trend Force | `\|emaFast − emaSlow\| / ATR`, normalized over 100 bars | Raises conviction — strong directional EMA separation |
| Chop Penalty | Trend force below chop cutoff | Multiplies conviction by 0.35 — forces wider bands during ranges |

When both ATR Rank and Trend Force are enabled, conviction is their simple average before the chop penalty is applied. If only one component is on, it contributes alone.

## Signal Filter

Flip signals (the triangle markers) fire on every Supertrend direction change by default. With the RSI Overbought Filter enabled, flips into already-overextended conditions are blocked:

- **Long flip**: blocked when RSI > threshold (default 70)
- **Short flip**: blocked when RSI < (100 − threshold)

A Min Body filter (off by default) additionally ignores flips whose flip-bar candle body is smaller than N × ATR.

## MTF Confluence

The MTF layer runs a fixed-multiplier Supertrend on a higher timeframe (default 4H, same ATR length and base multiplier as the LTF) and derives three display elements:

**Pullback zone** — when the LTF trend opposes the HTF trend, the background takes a subtle tint in the HTF direction. When the LTF is also overextended against the HTF (price stretched far from the LTF stop), the tint intensifies. This is the "ripe pullback" state where a reversal back into HTF direction is most likely.

**Confluence signal** — when a qualified LTF flip occurs in the HTF trend direction, a diamond marker appears instead of the usual triangle. The diamond is larger and visually distinct, indicating the flip has HTF backing. Triangles continue to appear for flips that lack HTF confluence.

**HTF stop line** — a secondary step-line at the HTF Supertrend stop level, drawn in a more transparent version of the trend color. Provides structural context for where the HTF trend is anchored.

**Table rows:**

| Row | Values | Meaning |
|---|---|---|
| HTF | ↑ Up / ↓ Down | Current HTF Supertrend direction |
| Setup | ↑ Watch / ↑ Ready / ↓ Watch / ↓ Ready / — | Pullback forming (Watch) or mature (Ready = LTF also overextended) |

The HTF stop uses `lookahead=off` — values update only on confirmed HTF bar closes, not mid-bar. No lookahead bias.

## Tuning

| Parameter | Lower | Higher |
|---|---|---|
| Base Multiplier | Tighter stop, more flips | Looser stop, fewer flips |
| Adaptivity | Less difference between regimes | Strong narrowing in trends, strong widening in chop |
| Chop Cutoff | Only flags extreme chop | Flags moderate ranges too |
| Fast/Slow EMA | Controls trend force sensitivity | Longer slow EMA = smoother trend force signal |
