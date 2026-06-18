# ADX Advanced

ADX/DI system with pluggable smoothing on the ADX line, rich visualization of DI± divergence, and a 4-state histogram for trend strength clarity. The indicator separates the directional signal (DI± crossover) from the trend strength reading (ADX vs thresholds) so both can be read independently.

## Features

- **ADX/DI core:** `ta.dmi(diLen, adxSmoothing)` produces DI+, DI−, and ADX raw
- **Pluggable smoothing:** EMA, SMA, RMA, WMA, SuperSmoother, T3, KAMA, JMA Approx — applied to the ADX signal line
- **ADX histogram:** ADX minus smoothed signal; 4-state coloring (above/below threshold × rising/falling)
- **DI± display:** optional lines with a fill between DI+ and DI− — fill color tracks which direction dominates
- **Gradient ADX line:** `color.from_gradient()` maps weak-threshold to strong-threshold using amber/orange tones
- **Shadow fill:** gradient fill between ADX and zero below the weak threshold
- **Signal markers:** DI crossover triangles; ADX threshold activation diamonds
- **Alert conditions:** DI cross bull/bear; ADX threshold cross up/down

## Levels

Two configurable thresholds — weak (default 20) and strong (default 40) — control both the hline display and the gradient bounds. The histogram uses the weak threshold to split "ranging" from "trending" coloring.
