# Swing Conviction Radar

Scores each price swing (pivot-to-pivot leg) by three conviction factors: how fast the move was (speed), how consistently bars moved in the leg's direction (cleanliness), and whether volume was increasing toward the end of the leg (volume gradient). The combined score per leg ranges 0–100. The core signal is divergence: when price makes a new high/low but the swing that drove it there had lower conviction than the previous one, the move is losing internal energy — an early reversal warning without any oscillator involved.

## Features

- **Per-leg conviction score**: weighted blend of speed, cleanliness, and volume gradient
- **Speed**: ATR-normalized distance covered per bar in the leg
- **Cleanliness**: fraction of bars in the leg that moved in the leg's direction
- **Volume gradient**: whether volume was higher in the second half of the leg (conviction building vs. fading)
- **Bearish divergence**: price higher high + conviction lower → hidden weakness, plotted at pivot bar
- **Bullish divergence**: price lower low + conviction lower → exhausted sellers, plotted at pivot bar
- **Step-line history**: running conviction line for bull and bear legs
- **Dashboard**: last and previous conviction scores for each direction, active divergence state

## Settings

| Group | Setting | Default | Purpose |
|---|---|---|---|
| Pivot Settings | Left Bars | 5 | Pivot confirmation bars left |
| Pivot Settings | Right Bars | 5 | Pivot confirmation bars right |
| Pivot Settings | Max Leg Bars | 100 | Cap on bars scanned per leg (increase for long swings) |
| Scoring | Speed Weight | 0.4 | Contribution of ATR-normalized speed |
| Scoring | Cleanliness Weight | 0.4 | Contribution of on-trend bar fraction |
| Scoring | Volume Gradient Wt | 0.2 | Contribution of volume build toward pivot |
| Scoring | ATR Length | 14 | ATR period for speed normalization |
| Scoring | Speed Reference | 3.0 | ATR×/bar at which speed conviction maxes out |
| Display | Show Divergence Labels | On | DIV labels at pivot bars |
| Display | Show Dashboard | On | Toggle the info table |

## Divergence logic

A **bearish divergence** fires when the current confirmed pivot high is above the previous pivot high, but the leg that drove price there has a lower conviction score. A **bullish divergence** fires when the current confirmed pivot low is below the previous pivot low with lower leg conviction. Both are plotted as triangles and optionally as "DIV ↓ / ↑" labels at the exact pivot bar.
