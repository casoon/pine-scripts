# Money Flow Delta Profile

A center-out diverging volume/money flow profile. Instead of the classic sideways histogram, each price row shows a bar that extends **right** (green, net buying) or **left** (red, net selling) from a center zero line — so you see at a glance which levels are demand zones and which are supply zones, without mentally comparing two bar widths.

## Features

- **Delta bars** — center-out bars sized by absolute net flow, colored by direction (bull/bear)
- **Total Flow Reference** — faint gray bars behind the delta view showing raw activity at each level
- **Point of Control (POC)** — dashed yellow line at the price row with highest total flow
- **Value Area** — configurable percentage (default 70%) of total flow; shows VAH/VAL boundaries
- **Delta POC** — optional dotted line marking the most decisively directional row
- **Recency Weighting** — exponential decay so recent bars contribute more than older ones
- **Source** — Money Flow (volume × mid-price) or raw Volume
- **Polarity method** — Bar Polarity (close > open) or Buying/Selling Pressure (close location)
- **Dashboard** — POC/VAH/VAL levels, bull%, source, lookback

## How to read it

- Rows where the **green bar reaches far right** → strong net buying at that level (demand)
- Rows where the **red bar reaches far left** → strong net selling (supply)
- Rows with **barely any delta bar** but a wide gray reference bar → high activity but balanced (contested level / consolidation)
- **POC** marks the most-traded level overall — common reversion target
- **Value Area** is the price band containing the configured % of total flow

## Visualization layout

```
Chart  | gap |  [LEFT — bear half | center line | RIGHT — bull half]
               |<──────────── profile width ────────────>|
               leftBI          centerBI              rightBI
```

The gray reference bar always extends rightward from `leftBI`, filling proportionally to the row's total flow. The delta bar always anchors on `centerBI` and extends in the dominant direction.

## Differences from classic volume profile

| Feature | Classic profile | MF Delta Profile |
|---------|----------------|-----------------|
| Orientation | All bars go right | Bars diverge left/right |
| What it shows | Volume at level | Net directional flow at level |
| Read | Compare bar length | Read direction + length |
| POC | Longest bar | Separate from delta — may differ |
| Contested levels | Long bar = high activity | Long gray ref + short delta bar |

## Settings

| Group | Setting | Default | Notes |
|-------|---------|---------|-------|
| Profile | Lookback | 200 | bars back from current |
| Profile | Rows | 25 | price bins |
| Profile | Source | Money Flow | volume × mid-price vs raw volume |
| Profile | Polarity | Bar Polarity | how bull/bear flow is split |
| Weighting | Recency Weighting | off | exponential decay on older bars |
| Weighting | Decay Factor | 0.015 | higher = faster fade |
| Visualization | Width % | 15 | profile width as % of lookback |
| Visualization | Bar Offset | 3 | gap between last price bar and profile |
| Visualization | Value Area % | 70 | fraction of total flow in VA |
