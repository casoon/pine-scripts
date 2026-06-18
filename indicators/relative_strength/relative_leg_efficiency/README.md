# Relative Leg Efficiency

Scores each price leg — from pivot to pivot — on how efficiently price moved: how direct the path was, how fast, and how much counter-pressure it absorbed along the way. The RLE score (0–100) makes legs comparable across a chart and filters clean, directional moves from choppy ones. The in-progress leg is scored live from the last confirmed pivot to the current bar.

## Features

- Live RLE scoring during the active leg
- Path efficiency: straight-line (air) distance vs. actual path distance of the chosen source
- Time efficiency: speed normalization against recent leg history, time penalty, or a combination
- Counter-pressure: opposing candle count, body-weighted pressure, or both — optionally restricted to meaningful bodies (ATR filter)
- Pivot-based legs with minimum-bars and minimum-move (ATR) filters
- Optional spike guard: caps the score of legs dominated by a single oversized candle
- Leg line coloring by score band, completed-leg and live labels, RLE histogram (overlay or pane mode)
- Alert on completed legs with RLE above a configurable threshold

## Scoring

```
RLE = 100 · (wPath · PE + wTime · TE + wCounter · CP) / (wPath + wTime + wCounter)
```

- **PE (path efficiency)** = air distance / path distance, clamped to 0–1
- **TE (time efficiency)** = leg speed normalized against the average of recent legs (Speed Norm), `1 / (1 + bars/medianBars)` (Time Penalty), or the average of both (Combined)
- **CP (counter-pressure)** = 1 − counter ratio, where the counter ratio is the share of opposing bars (Count), opposing body volume vs. total body volume (Body Weighted), or a 30/70 blend (Both)

Score bands: ≥ High Threshold = green, ≥ Mid Threshold = yellow, below = red.

## Leg detection

Legs run between alternating confirmed pivots (`ta.pivothigh`/`ta.pivotlow`). Same-type pivots replace the previous one if more extreme. A leg only completes if it spans at least *Minimum Bars per Leg* and moves at least *Minimum Leg Move (ATR)*. Completed-leg metrics are computed from cumulative series, so the per-bar cost stays constant.
