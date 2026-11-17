# The iteration spiral

The WaveTrend strategy went through about thirty iterations on one instrument. Each iteration added a
source, a gate, a score component or a calibration. Looking back, the process taught more than the
strategy did.

## What happened

- **Filters were stacked without understanding their joint effect.** Each one looked like an
  improvement on its own. Together they cancelled out or distorted each other, and nobody could say
  any more which component did what.
- **A bug produced the best result.** A floor on the signal length switched the cross signals off on
  one timeframe completely. That timeframe became the star of the tests. The strategy was in fact a
  different strategy there, without anyone knowing.
- **Tiny samples were read as findings.** A filter with a handful of trades and no losers was taken
  as proof. A handful of trades is a sample, not a signal.
- **Promises ran ahead of the data.** "This filter will carry over to all timeframes" was disproved
  in the next run, partly because other protections had been switched off at the same time.
- **Defaults were tuned instead of the concept questioned.** The basic question, whether the cross
  signal has any edge, was asked last instead of first.
- **Gates were tuned on the same window again and again.** More than a dozen gate variants were
  iterated against one window of one instrument, several of them hard-coded for one direction.

## What follows

- Measure the core signal alone first, against random entries. If it has nothing, no filter will
  give it something.
- Change one thing at a time and keep a record of what was tried, including what failed. The number
  of attempts belongs to the result.
- An unexpectedly good result is first checked for a bug.
- "Statically reviewed" means read, not compiled and not run. Fixes that were never compiled are not
  done.
