# Volume Strata

Fixed-range volume profile anchored to the right edge of the lookback window, showing where volume actually traded across price levels — split by up and down volume, with the value area, Point of Control, and high-volume node markers highlighted.

## Features

- **Right-anchored profile** — bars grow leftward into the candle range; up-volume occupies the right (inner) side, down-volume extends further left
- **Value area** — configurable percentage (default 70%) highlighted in distinct colors; rows outside the area are shown in lighter tones
- **Point of Control (POC)** — dashed horizontal line at the highest-volume price row, with a right-side price label
- **VAH / VAL** — dotted lines at the top and bottom of the value area with price labels
- **HVN markers** — small gold ticks to the right of the profile for rows where volume exceeds mean + 1σ; these are the strongest reaction zones
- **Info table** — compact top-right panel showing POC, VAH, VAL, and the buy-volume percentage (green >55%, red <45%, gray otherwise)

## Inputs

| Input | Default | Description |
|-------|---------|-------------|
| Lookback Bars | 150 | Number of historical bars included in the range |
| Rows | 24 | Number of price buckets |
| Value Area % | 70 | Volume percentage defining the value area |
| POC color / width | red, 2 | Style of the POC line |
| VAH / VAL color | gray | Style of the value area boundary lines |
| HVN color | gold | Color of high-volume node markers |
| Show POC label | on | Toggle right-side POC price label |
| Show VAH / VAL | on | Toggle value area boundary lines and labels |
| Show HVN markers | on | Toggle high-volume node ticks |
| Show info table | on | Toggle the top-right key-level panel |

## Volume split method

Each candle's volume is split into three components — body, upper wick, and lower wick — using their relative height as weights. Wick volume is attributed 50/50 between up and down; body volume goes entirely to the candle's direction. This gives a more accurate buy/sell split than treating the full bar volume as directional.
