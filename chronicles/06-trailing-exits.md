# Trailing exits do not beat a fixed exit

Trailing stops feel like the natural way to "let winners run". Several strategies here use only a
trailing exit: chandelier, ATR envelope, moving average minus ATR.

## What was measured

On the same entries, a fixed exit (target, stop and time limit in ATR) against: break-even stop,
partial profit with a trailing rest, plain trailing stops of different widths, exit at the opposite
extreme, and time exits.

## What came out

- None of the dynamic exits beat the fixed exit, already before costs.
- Holding longer mostly buys **financing nights** (see [07](07-cfd-costs.md)). After costs the gap
  grew.
- A break-even stop on an exit shape with a high win rate cuts winners more often than it saves
  losers.

## What follows

- A trailing exit is not wrong. A strategy that only offers a trailing exit simply cannot show
  whether the trailing adds anything.
- Every strategy should offer at least one fixed exit (target, stop, time limit) as a comparison.
- Freeze the stop distance at the signal. Recomputing it with a later ATR changes the risk of a trade
  that is already open.
