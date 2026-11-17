# Labels that claim more than the math

Several scripts give their output a name that promises more than the calculation delivers.

## Examples

- **"Probability"** for a hand-weighted evidence score. Without a calibrated model or a measured
  frequency it is a score from 0 to 100, not a probability.
- **"Hurst exponent"** for a sensor that is not a reliable Hurst estimator, and "predictability"
  derived from it.
- **"Reliable"** with a minimum sample count that was lowered so that signals become reachable. The
  threshold has to follow from what a sample can show, not from whether the indicator produces
  signals.
- **"High-probability reversal"**, "best signal", "the actual edge" in descriptions and tooltips.
- **Win-rate panels** with no base rate and no costs (see [02](02-win-rate-follows-geometry.md)).

## What follows

- Name the output after what it computes: "evidence score", "persistence ratio", "state".
- A word like probability, reliable or edge is used only when there is a measurement behind it, with
  its sample size.
- Never state a 100 % win rate. It describes the sample, not the signal.
