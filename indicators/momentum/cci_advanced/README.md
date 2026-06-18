# CCI Advanced

CCI with pluggable smoothing, three scale modes, and rich visualization. The indicator builds a smoothed main line and a signal line from the raw CCI value, producing a histogram and a gradient line that reflects the current extreme level.

## Features

- **CCI core:** `ta.cci(src, len)` → averaged main line → signal line via the shared smoothing kernel
- **Pluggable smoothing:** EMA, SMA, RMA, WMA, SuperSmoother, T3, KAMA, JMA Approx — applied to both main and signal line
- **Three scale modes:** Classic (unbounded raw CCI), Clamp ±200 (hard clip), Adaptive ±100 (shared rescale using recent range)
- **Shared adaptive scale:** both CCI and signal are divided by the same lookback maximum, preventing phantom crossovers
- **Signals on raw values:** crossover detection uses the unscaled CCI so display mode changes never affect signal logic
- **4-state histogram:** rising/falling × positive/negative drives four opacity states
- **Gradient line:** `color.from_gradient()` from bull teal to bear pink based on oscillator level
- **Shadow fills:** 6-argument `fill()` places gradient shadows between the CCI line and zero
- **OB/OS zone fills:** configurable ±100 and ±200 levels with translucent fills
- **Signal markers:** configurable OB/OS-zone filter for crosses; optional zero-line cross dots
- **Alert conditions:** bull/bear cross from extreme zone; zero-line cross up/down

## Scoring

The optional extreme filter requires the main CCI line to have visited the oversold (or overbought) zone within the last N bars before a cross qualifies as a signal. This eliminates mid-range crosses that lack mean-reversion context.
