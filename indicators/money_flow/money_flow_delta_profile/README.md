# Money Flow Delta Profile

**TradingView:** https://de.tradingview.com/script/NUAePC98/

A directional volume/money flow profile. Every price row shows two bars anchored on the left, both extending to the right: a faint gray **reference bar** (total flow at that level) and a colored **delta bar** on top (green = net buying, red = net selling). The width of the delta bar relative to the gray bar shows how decisively one side dominated — a row where the delta bar almost fills the reference bar is a high-conviction level; a row where it barely appears despite wide gray is a contested zone.

## Features

- **Delta bars** — all extend rightward from the anchor, sized by net flow, colored by direction (green = bull, red = bear)
- **Total Flow Reference** — gray bars behind the delta bars showing raw activity at each level; colored by node type (HVN/LVN/AVN)
- **HVN / LVN / AVN classification** — reference bars colored by relative flow density (HVN = warm orange, LVN = faded gray, AVN = neutral gray)
- **LVN Supply/Demand Zones** — adjacent Low Volume Node rows merged into zone boxes: red above POC (supply), green below POC (demand); optional minimum zone width and forward projection to the right chart edge
- **Point of Control (POC)** — dashed yellow line at the price row with highest total flow
- **Value Area** — configurable percentage (default 70%) of total flow; shows VAH/VAL boundaries
- **Delta POC** — optional dotted line marking the most decisively directional row
- **Recency Weighting** — exponential decay so recent bars contribute more than older ones
- **Bull% label** — buying share shown inside each significant row
- **Source** — Money Flow (volume × mid-price) or raw Volume
- **Polarity method** — Bar Polarity (close > open) or Close Location (proportional)
- **Intrabar Delta (optional)** — bull/bear split per bar from real lower-timeframe volume direction instead of the close-location approximation (chart TF ÷ granularity, clamped to 1 minute; automatic fallback when no LTF data is available)
- **Absorption Profile (optional)** — wick-volume per price row drawn as a mirror profile left of the anchor: flow at prices the bar visited but closed away from (rejection)
- **Absorption Peak Zones (optional)** — local absorption maxima (≥ both neighbors and ≥ 50% of the absorption max) projected as S/R zones across the lookback window

## How to read it

- **Wide gray + wide green delta** → high-volume demand zone (buyers dominated convincingly) → HVN
- **Wide gray + narrow delta** → high-volume contested level (both sides fought) → HVN, but watch for reversal
- **Narrow gray** → thin area, LVN — price moved through quickly, likely to do so again
- **LVN zone above price** → air pocket / supply — potential fast move if price re-enters
- **LVN zone below price** → air pocket / demand — potential fast move downward if lost
- **POC** → the most-traded level overall, common reversion target
- **Tall absorption row** → price was pushed there repeatedly and rejected — resting liquidity; expect a reaction on revisit

## Visualization layout

```
Chart  | gap | anchor
                |──[gray ref bar]──────────────>|   (total flow)
                |──[delta bar]────>|                (net direction, same anchor, shorter)
```

Both bars start at the anchor line on the left. The gray bar sets the maximum width (= 100% flow at that row). The delta bar fills a fraction of that width proportional to `|bull − bear| / total`. Color is green when buyers won, red when sellers won.

## Differences from classic volume profile

| Feature | Classic profile | MF Delta Profile |
|---|---|---|
| Orientation | All bars go right | All bars go right |
| What it shows | Volume at level | Total flow (gray) + net direction (colored) |
| Read | Compare bar length | Color = who won; delta/gray ratio = by how much |
| POC | Longest bar | Highest total flow (may differ from strongest delta) |
| Contested levels | Long bar = high activity | Long gray + short delta = balanced (contested) |
| Thin areas | Short bar | Short gray = LVN, shown as zone overlay |

## Settings

| Group | Setting | Default | Notes |
|---|---|---|---|
| Profile | Lookback | 200 | Bars back from current bar |
| Profile | Rows | 25 | Price bins |
| Profile | Source | Money Flow | Volume × mid-price vs raw volume |
| Profile | Polarity | Bar Polarity | How bull/bear flow is split |
| Weighting | Recency Weighting | off | Exponential decay on older bars |
| Weighting | Decay Factor | 0.015 | Higher = faster fade |
| Node Classification | HVN Threshold | 80% | Rows above this share colored as HVN |
| Node Classification | LVN Threshold | 20% | Rows below this share colored as LVN |
| Node Classification | LVN Zone Overlay | on | Supply/demand zone boxes from LVN rows |
| Node Classification | Min Zone Rows | 1 | Skip zones with fewer adjacent LVN rows (1 = off) |
| Node Classification | Extend Zones Right | off | Project zone boxes to the right chart edge |
| Visualization | Value Area % | 70 | Fraction of total flow in VA |
| Visualization | Bar Offset | 3 | Gap between last candle and profile |
