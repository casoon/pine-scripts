# Volume Strata

Fixed-range volume profile anchored to the right edge of the lookback window, showing where volume actually traded across price levels — split by up and down volume, with the value area, Point of Control, high/low-volume node markers, and an expanded context table.

## Features

- **Right-anchored profile** — bars grow leftward into the candle range; up-volume occupies the right (inner) side, down-volume extends further left
- **Blue / yellow split** — buy volume in blue, sell volume in yellow (volume profile convention)
- **Value area** — configurable percentage (default 70%) highlighted in distinct colors; rows outside the area are shown in lighter tones
- **Point of Control (POC)** — dashed horizontal line at the highest-volume price row, with a right-side price label
- **VAH / VAL** — dotted lines at the top and bottom of the value area with price labels
- **Value Area Fill** — light shaded zone between VAH and VAL across the lookback range; the "fair value" band at a glance
- **HVN zones** — horizontal shaded bands at high-volume node rows (mean + 1σ) extended across the lookback; the strongest reaction zones
- **LVN zones** — horizontal shaded bands at local-minima rows below mean − 1σ; price tends to move quickly through these — potential breakout zones
- **Naked POC tracking** — previous POCs that haven't been retested are drawn as faint dashed lines extending right; removed once price touches them. New naked POCs are tracked from script load forward
- **Expanded info table** — levels, VA width, range, POC strength, up-vol %, total volume, profile shape, VA state, Virgin POC, developing POC, POC distance
- **Alerts** — POC cross, VA entry/exit, VAH/VAL touch

## Inputs

| Input | Default | Description |
|-------|---------|-------------|
| Lookback Bars | 150 | Number of historical bars included in the range |
| Rows | 24 | Number of price buckets |
| Value Area % | 70 | Volume percentage defining the value area |
| Profile Offset | 150 | Bars to the right where the profile is drawn |
| POC color / width | red, 2 | Style of the POC line |
| VAH / VAL color | gray | Style of the value area boundary lines |
| HVN color | gold | Color of high-volume node markers |
| LVN color | cyan | Color of low-volume node markers |
| Up / Down Volume colors | blue / yellow | Volume direction split |
| Show Profile / POC label / VAH-VAL / VA Fill / HVN zones / LVN zones / Naked POCs / Info table | on | Independent display toggles |

## Info Table Reference

| Field | Meaning |
|-------|---------|
| **POC** | Price at the highest-volume row |
| **VAH / VAL** | Top / bottom of the value area |
| **VA Width** | Value area as % of full range — green < 30% (compact), orange > 60% (wide), gray otherwise |
| **Range** | High − low of the lookback window |
| **POC Str** | Volume at the POC as % of total — concentration measure. Green ≥ 15%, red ≤ 8% |
| **Up Vol** | Buy volume as % of total. Green > 55%, red < 45% |
| **Total Vol** | Total volume in the range, formatted (K/M/B) |
| **Shape** | Profile shape: **D** (balanced), **P** (POC in upper third → accumulation), **b** (POC in lower third → distribution), **B** (≥ 3 HVNs → double distribution) |
| **VA State** | Whether close is Inside / Above / Below value area |
| **POC** | Virgin (untouched in last 5 bars) or Touched |
| **Dev POC** | Direction of POC vs. previous bar (rising / falling / stable) |
| **POC Dist** | Current close distance from POC, expressed in ATR(14) |

## Volume split method

Each candle's volume is split into three components — body, upper wick, and lower wick — using their relative height as weights. Wick volume is attributed 50/50 between up and down; body volume goes entirely to the candle's direction. This gives a more accurate buy/sell split than treating the full bar volume as directional.

## Profile Shape interpretation

- **D-shape (balanced)**: normal distribution, market is in equilibrium — trade at the edges (VAH/VAL), fade toward POC
- **P-shape (accumulation)**: high volume in the upper third — common at the end of a downtrend, suggests buying on lower prices
- **b-shape (distribution)**: high volume in the lower third — common at the end of an uptrend, suggests selling on higher prices
- **B-shape (double distribution)**: two or more high-volume nodes — transition between regimes, watch for breakout from the inactive node
