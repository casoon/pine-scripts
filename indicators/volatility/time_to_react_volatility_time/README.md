# Time-to-React + Volatility-Time

Measures how quickly and cleanly price reacts after key market structure events — Break of Structure (BOS), liquidity sweeps, and Order Block taps — and scores that reaction relative to the current volatility environment. Runs as a separate panel (0–100 scores) with optional event labels and candle coloring on the chart.

## Features

- Event engine: BOS, liquidity sweep, and Order Block tap detection with configurable priority order
- Single-active-event model — one event is tracked at a time until validated or expired
- Reaction score (0–100): weighted blend of reaction speed and validation quality
- Speed score: how many bars until the first reaction candle, normalized to a timeframe-dependent reaction window
- Validation score: break of the reaction extreme (component A) plus ATR-proportional move progress (component B), weights normalizable
- Volatility activity score (0–100): tanh-shaped ratio of current ATR to its baseline average
- Timeframe presets (15m / 1h / 4h / D / M) with Auto-detection from the chart timeframe and a full Custom override
- Optional event and reaction labels on the chart, optional gradient candle coloring by reaction score

## Scoring

When an event fires, the indicator waits for the first reaction candle in the event direction. The speed score scales from 100 (immediate reaction) to 0 (reaction at the edge of the reaction window). From the reaction onward, the validation window tracks two components: A — close beyond the reaction extreme, B — progress of the move from the event reference level toward an ATR-multiple target. The final reaction score is the normalized weighted blend of speed and validation. If no reaction occurs within the reaction window, all scores are set to 0 and the event expires.

## Presets

Reaction/validation windows are defined in minutes and converted to bars for the chart timeframe. Auto mode selects the preset tier from the chart timeframe (≤20m, ≤90m, ≤300m, ≤1W, above). Custom mode exposes all windows and weights as inputs.
