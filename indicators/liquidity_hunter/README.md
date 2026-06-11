# Liquidity Hunter

Ranks equal highs and equal lows by quality, detects sweep-and-reclaim events with a composite score, and surfaces the two most relevant levels on each side — so the chart shows only the levels that actually matter.

## Features

- **Ranked liquidity levels** — each pivot cluster is scored by touch count, freshness, and ATR distance from price; only the top two per side are drawn
- **Primary and secondary lines** — primary (solid, thick) and secondary (dashed, faded) levels with score and touch count labels
- **Sweep detection** — marks wick-through events above BSL / below SSL with orange triangle markers
- **Reclaim detection** — confirms sweep + close-back + volume condition; labeled with direction, event score, and volume ratio
- **Composite level scoring** — `f_level_score`: touch count (max 5×20 pts), age penalty, ATR-distance penalty
- **Composite event scoring** — `f_event_score`: wick depth, close-back depth, volume ratio, session boost; capped at 100
- **Bias output** — combines reclaim direction and level proximity into a Bullish / Neutral / Bearish bias with numeric value
- **Armed level highlight** — background color when price is within the alert distance ATR of a primary level
- **Unfilled gaps** — price gaps between consecutive bars drawn as magnet-zone boxes until filled
- **Stop hunt detection** — same-bar sweep through a known level + volume spike + reversal close, labeled HUNT
- **Exhaustion Events (Momentum Hybrid)** — sweeps/hunts qualified by built-in WaveTrend extreme (+MFI context); marked with large "EX" triangles
- **Session filter** — optionally restricts reclaim scoring and bias boost to a defined session window
- **Dashboard** — top-right table: bias, primary BSL/SSL price + score + ATR distance, armed state, last event, premium scores, gap/hunt counts, WT/MFI state, exhaustion state
- **12 alert conditions** — BSL/SSL near, sweep, stop hunt, reclaim, premium reclaim (score ≥ 65), exhaustion bear/bull

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
```

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
| | Max Hunts to Show | 8 |
| Gaps | Max Gaps to Display | 5 |
| | Min Gap Size % | 0.05 |
| Context | Active Session Filter | off |
| | Alert Distance (ATR) | 1.0 |
| | Recent Event Memory (bars) | 30 |
| Momentum Hybrid | Exhaustion Event Detection | on |
| | WT Extreme Threshold | 53 |
| | MFI Length | 14 |
