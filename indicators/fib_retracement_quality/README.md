# Fibonacci Retracement Quality

Scores how precisely each confirmed retracement aligns with a Fibonacci level. After every three-point pivot sequence (swing start → swing end → retracement pivot), the retracement depth is measured as a ratio of the prior swing and compared against the five standard levels (0.236, 0.382, 0.5, 0.618, 0.786). The quality score (0–100) combines proximity to the nearest level with a level-specific multiplier — 0.618 scores highest, 0.236 lowest. High-quality scores indicate that price respected a meaningful Fibonacci level, a precondition for higher-probability reversal setups. This is different from `zigzag_fibo_pullback_map`, which draws the levels; this indicator scores adherence to them.

## Features

- **Bullish retracement scoring**: prior low (A) → swing high (B) → retracement low (C); ratio = (B−C)/(B−A)
- **Bearish retracement scoring**: prior high (A) → swing low (B) → retracement high (C); ratio = (C−B)/(A−B)
- **Fibonacci levels**: 0.236, 0.382, 0.5, 0.618, 0.786 — nearest level identified automatically
- **Quality score 0–100**: proximity to nearest level × level multiplier (0.618→1.0, 0.5→0.9, 0.382→0.8, 0.786→0.7, 0.236→0.5)
- **Signal**: long/short plotshape when quality ≥ threshold (default 65)
- **Labels**: score + level hit at the exact retracement pivot bar
- **Step-line history**: running quality trace for both directions
- **Dashboard**: last quality score and level for bull and bear retracements + active signal

## Settings

| Group | Setting | Default | Purpose |
|---|---|---|---|
| Pivot Settings | Left Bars | 5 | Pivot confirmation bars left |
| Pivot Settings | Right Bars | 5 | Pivot confirmation bars right |
| Fibonacci Scoring | Level Tolerance | 0.05 | Max distance from Fibonacci level to score (ratio units) |
| Fibonacci Scoring | Min Swing Size | 0.5 | Minimum swing in ATR multiples (filters noise swings) |
| Fibonacci Scoring | ATR Length | 14 | ATR period for minimum swing filter |
| Signals | Signal Threshold | 65 | Minimum quality to emit a long/short signal |
| Signals | Show Signals | On | Toggle long/short plotshapes |
| Display | Show Score Labels | On | Labels at pivot bars with score + level |
| Display | Show Dashboard | On | Toggle the info table |

## Scoring

A tolerance of 0.05 means a ratio within 5 percentage points of a level still scores. At exactly the level, proximity = 1.0; at the edge of tolerance, proximity = 0. Swings smaller than `Min Swing Size × ATR` are ignored — this prevents scoring tiny corrective moves as meaningful Fibonacci retracements.
