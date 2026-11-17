# Long results contain the market's drift

On an instrument that rose during the test period almost every long entry wins, including a random
one. On a falling one, almost every short entry does. "Long only works, short does not" is very often
just the direction of the market in that period.

## A measurement trap found on the way

To remove the drift, signals were compared with a base of all bars of the same instrument and year.
That base turned out to leak: the drift of the whole year is not known at the time of a signal in
March. Short signals looked better than their base only because the base contained the rest of the
year. The lesson: a baseline has to be **causal**, built from the time before the signal or from
random entries in the same window, never from a period that extends past the signal.

## What follows

- Every result is split by side, and each side is compared with its own base: random entries on the
  same side, same exit, same period.
- Buy and hold is not a proper base for a long strategy on CFDs, because holding a CFD costs
  financing every night (see [07](07-cfd-costs.md)).
- An asymmetry between long and short is a question, not a finding. A gate hard-coded for one
  direction ("shorts only on 4h") needs a reason that would also explain the mirror case. Without
  one it is fitted to the drift of the test window.
