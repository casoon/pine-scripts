# Smoothing type is not an edge

Many scripts in this collection offer a choice of six to nine smoothing kernels: EMA, SMA, RMA, WMA,
HMA, ZLEMA, T3, KAMA, SuperSmoother, a JMA approximation. The idea behind it is plausible: some
kernels lag less, so crosses should come earlier and closer to the turn.

## What was measured

WaveTrend, StochRSI and RSI, each with eight kernels at the same length, on 1h, 4h and daily bars,
over three event types: line cross, exit from an extreme zone, divergence. For each combination:
number of signals, distance to the confirmed price pivot, share of false crosses, and the result of a
fixed exit compared with random entries on the same side.

## What came out

- The kernel changes the **density** of signals, not their **quality**. Fast kernels (ZLEMA, HMA)
  produce far more crosses and correspondingly more false ones. A slow kernel (T3) halves the crosses
  and misses more turns. The share of good signals stays the same across all kernels.
- The **lead** of fast kernels is real on a sine wave and disappears on price data. With many
  crosses per period there is always one near the turning point. That looks like lead but is density.
- SMA, EMA, WMA and RMA produce almost the same line. They differ in when the line crosses, not in
  what it says.
- No kernel was better than another in a way that held across periods. The ranking of kernels
  flipped between periods.

## What follows for the scripts

- A selector with eight equivalent kernels invites picking the kernel that happened to look best on
  the current chart. That is fitting to the past (see [05](05-per-instrument-tuning.md)).
- Keep the indicator's original kernel as the default. At most, one slow kernel can remain as a
  display option for a calmer picture, described as "fewer crosses, misses more turns".
- Phrases like "less lag", "zero lag" or "earlier crosses" describe the filter on a sine wave. They
  do not describe better signals in the market and should not be written as if they did.
