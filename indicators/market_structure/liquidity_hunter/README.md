# Liquidity Hunter

Ranks equal highs and equal lows by quality, detects sweep-and-reclaim events with a composite score, and surfaces the two most relevant levels on each side — so the chart shows only the levels that actually matter.

## Features

- **Ranked liquidity levels** — each pivot cluster is scored by touch count, freshness, and ATR distance from price; only the top two per side are drawn
- **Primary and secondary lines** — primary (solid, thick) and secondary (dashed, faded) levels with score and touch count labels
- **Sweep vs. breakout** — a touch that closes back on its own side is a Sweep (small, unlabeled triangle); a touch whose close already sits beyond the level is a Breakout (subtle, unlabeled dot) — acceptance and rejection are never conflated
- **Reclaim detection** — confirms sweep + close-back + volume condition; a "Reclaim" label with a hover tooltip (level, score, volume) marks the event
- **Composite level scoring** — `f_level_score`: touch count (max 5×20 pts), age penalty, ATR-distance penalty
- **Composite event scoring** — `f_event_score`: wick depth, close-back depth, volume ratio, session boost, structural (micro-BOS) bonus, optional regime/context bonus; capped at 100
- **Bias output** — combines reclaim direction and level proximity into a Bullish / Neutral / Bearish bias with numeric value
- **Armed level highlight** — background color when price is within the alert distance ATR of a primary level
- **Fair Value Gaps** — 3-candle imbalance (`low > high[2]` / `high < low[2]`) drawn as magnet-zone boxes until filled
- **Stop hunt detection** — sweep through a known level + wick-rejection quality (wick ratio + close position in bar) + volume spike; a "Hunt" label with a hover tooltip marks the event
- **Regime Context (optional, off by default)** — range-vs-trend efficiency-ratio regime + premium/discount range location, added as a bounded score bonus to reclaim events; informational, never gates a signal
- **Level Lifecycle (optional, off by default)** — a level that breaks with full acceptance is re-tracked on the opposite side instead of discarded (old resistance -> candidate support, and vice versa)
- **Exhaustion Events (Momentum Hybrid)** — sweeps/hunts qualified by built-in WaveTrend extreme (+MFI context); an "Exhaustion" label with a hover tooltip (WT value vs. threshold) marks the event
- **Session filter** — optionally restricts reclaim scoring and bias boost to a defined session window
- **Event priority + hover tooltips** — Hunt/Reclaim/Exhaustion each get a short label (`H x<vol>` / `R <score>` / `EX WT <value>`) with a full explanation on hover instead of cryptic plotshape text; same-bar duplicates are suppressed globally by priority (Exhaustion > Hunt > Reclaim > Sweep > Breakout), regardless of direction
- **Dashboard (on by default)** — compact top-right table with a dynamic row count: bias, primary BSL/SSL price + score + ATR distance, last event, Liquidity State (Idle / Approaching / Swept / Reclaim Active / Breakout Accepted), optional Regime row, FVG/hunt counts, optional WT/MFI + exhaustion state
- **14 alert conditions** — BSL/SSL near, sweep, breakout, stop hunt, reclaim, premium reclaim (score ≥ 65), exhaustion bear/bull

## Scoring

### Level score (for ranking and display selection)

```
score = min(touches, 5) × 20  +  18  −  age_penalty  −  dist_penalty
age_penalty  = min(barsSinceTouch / maxLevelAge, 1.0) × 18
dist_penalty = min(distAtr, maxLevelDistance) × 7
```

A level with 3+ touches, touched recently, and close to price scores highest.

### Event score (for reclaim quality)

```
score = min(touches,5)×12  +  min(wickAtr,1.5)×18  +  min(closeBackAtr,1.5)×24
      + max(0, min(volRatio,3.0)−1.0)×12  +  sessionBoost(0 or 10)
      + structBonus(0 or 10)  +  ctxBonus(0..contextBonusMax, if Regime Context enabled)
```

`structBonus` rewards a micro-BOS: the reclaim bar closes beyond the prior bar's high/low in the
reclaim direction. `ctxBonus` (only added when Regime Context is enabled) rewards bearish reclaims
from the premium half of the recent range / a range or downtrend-aligned regime, and mirrors for
bullish reclaims from the discount half / an uptrend-aligned regime — capped, and only ever added,
never used to block an event.

Capped at 100. Events with score ≥ 65 trigger the "Premium" alert.

## Inputs

| Group | Input | Default |
|---|---|---|
| Liquidity Levels | Pivot Length | 8 |
| | Equal Level Tolerance (ATR) | 0.12 |
| | Minimum Touches | 2 |
| | Max Tracked Levels / Side | 30 |
| | Max Level Age (bars) | 400 |
| | Max Level Distance (ATR) | 8.0 |
| Premium Events | Min Sweep Depth (ATR) | 0.05 |
| | Reclaim Window (bars) | 3 |
| | Min Close-Back Distance (ATR) | 0.10 |
| | Min Volume Ratio | 1.2 |
| | Max Premium Events | 6 |
| Stop Hunts | Volume Spike Multiplier | 1.5 |
| | Min Rejection Wick Ratio | 0.45 |
| | Max Close Position in Bar | 0.45 |
| | Max Hunts to Show | 8 |
| Fair Value Gaps | Max FVGs to Display | 5 |
| | Min FVG Size % | 0.05 |
| | Show FVG Labels | on |
| Regime Context | Enable Regime / Premium-Discount Context | off |
| | Regime Lookback (bars) | 50 |
| | Trend Efficiency Threshold | 0.35 |
| | Max Context Bonus (score pts) | 12.0 |
| Level Lifecycle | Flip Broken Levels into Opposite Zone | off |
| Context | Active Session Filter | off |
| | Alert Distance (ATR) | 1.0 |
| | Recent Event Memory (bars) | 30 |
| Momentum Hybrid | Exhaustion Event Detection | off |
| | WT Extreme Threshold | 53 |
| | MFI Length | 14 |
