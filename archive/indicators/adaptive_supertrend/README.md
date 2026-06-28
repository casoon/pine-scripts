# Adaptive Supertrend

A Supertrend indicator with conviction-adaptive band width. Instead of a fixed ATR multiplier, the band narrows when the market is trending strongly and widens when conditions are choppy or volatility is contracting. This means the stop trails price more tightly during high-conviction moves and gives more room during uncertain regimes — without requiring any manual parameter adjustment per timeframe.

> **Archived.** Superseded by [chandelier_flip_radar](../../../indicators/trend_direction/chandelier_flip_radar/) — same family (ATR trailing-stop flip with ratchet, body filter, trap markers). The MTF confluence layer from this indicator was absorbed into Chandelier Flip Radar (v1.5) as an optional overlay; this conviction-adaptive / hl2-anchored variant remained untested and is kept here for reference only.

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
rawMult = baseMult × (1 + adaptivity × (0.5 − conviction))
adaptiveMult = clamp(rawMult, baseMult × 0.60, baseMult × 1.80)
```

The formula is symmetric around `baseMult` at conviction = 0.5:

- conviction = 1 (maximum) → multiplier tightens **below** `baseMult` (tightest stop, floored at `baseMult × 0.60`)
- conviction = 0.5 (neutral) → multiplier equals `baseMult`
- conviction = 0 (minimum) → multiplier widens **above** `baseMult` (widest stop, capped at `baseMult × 1.80`)

**Components:**

| Component | What it measures | Effect when high |
|---|---|---|
| ATR Rank | ATR percentile over 100 bars (capped at 85%) | Raises conviction — but only when trend force confirms a real move; otherwise it contributes a neutral value (`ATR Conviction in Chop`, default 0.50) so volatility spikes (panic, news, blow-off) don't count as conviction |
| Trend Force | `\|emaFast − emaSlow\| / ATR`, mapped to 0–1 against an absolute cap (`Trend Force Full Conviction`, default 2.0) | Raises conviction — strong directional EMA separation |
| Chop Penalty | Trend force below chop cutoff | Multiplies conviction by 0.50 — widens bands during ranges |

When both ATR Rank and Trend Force are enabled, conviction is their simple average before the chop penalty is applied. If only one component is on, it contributes alone.

## Signal Filter

Flip signals (the triangle markers) fire on every Supertrend direction change by default. With the RSI Overbought Filter enabled, flips into already-overextended conditions are blocked:

- **Long flip**: blocked when RSI > threshold (default 70)
- **Short flip**: blocked when RSI < (100 − threshold)

A Min Body filter (off by default) additionally ignores flips whose flip-bar candle body is smaller than N × ATR.

## MTF Confluence

The MTF layer runs a plain **fixed-multiplier reference Supertrend** on a higher timeframe (default 4H, same ATR length and base multiplier as the LTF). Note this HTF reference does **not** use the adaptive conviction logic — it is a stable structural anchor, not a second adaptive instance. It derives three display elements:

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
| Adaptivity | Less difference between regimes (0 = plain Supertrend at base) | Strong narrowing in high-conviction trends, strong widening in chop |
| Chop Cutoff | Only flags extreme chop | Flags moderate ranges too |
| Fast/Slow EMA | Controls trend force sensitivity | Longer slow EMA = smoother trend force signal |
| Trend Force Full Conviction | Reaches full trend-force conviction sooner | Requires stronger EMA separation before conviction maxes out |
