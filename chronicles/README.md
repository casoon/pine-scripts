# Chronicles

Lessons learned while building, reviewing and measuring the scripts in this repository.

The scripts here were written over many iterations, reviewed file by file, and a large part of them
was later rebuilt and measured outside TradingView in a separate research project: with fixed rules,
real CFD costs, random-entry baselines and checks on data that was not used for the choice. These
notes collect what came out of that work, the lessons that changed how the scripts should be built,
read and tested.

## Ground rules for these notes

- **No figures.** No win rates, profit factors, R values or returns. A figure without its full
  context (instrument, timeframe, period, sample size, cost model) misleads, and with full context it
  belongs in a measurement record, not here.
- **Only what is clear.** A lesson is included when it held across instruments, timeframes and
  periods, with a large sample and a counter-check. Single observations and hints are left out.
- **Lessons, not verdicts on indicators.** An indicator shows a market state. A note saying an
  event type gives no measurable edge as an entry signal does not make the display wrong.
- **What was not measured stays open.** Real exchange volume, very short timeframes and contexts
  outside the tested instruments are not covered.

## Measurement

1. [Smoothing type is not an edge](01-smoothing-is-not-an-edge.md)
2. [Win rate follows from geometry](02-win-rate-follows-geometry.md)
3. [Long results contain the market's drift](03-drift-and-the-side-baseline.md)
4. [A filter must beat random omission](04-filters-vs-random-omission.md)
5. [Per-instrument tuning does not carry forward](05-per-instrument-tuning.md)
6. [Trailing exits do not beat a fixed exit](06-trailing-exits.md)
7. [CFD costs are spread and financing](07-cfd-costs.md)
8. [Candle alignment changes the result](08-candle-alignment.md)
9. [Hindsight measures are ceilings, not results](09-hindsight-measures.md)
10. [Correlated indicators are one vote](10-correlated-votes.md)
11. [Event types without a measurable entry edge](11-event-types-without-edge.md)

## Building

12. [The iteration spiral](12-the-iteration-spiral.md)
13. [Running higher-timeframe values](13-running-htf-values.md)
14. [Volume is not always volume](14-volume-is-not-always-volume.md)
15. [Recurring bug classes](15-recurring-bug-classes.md)
16. [Exits that never fire](16-exits-that-never-fire.md)
17. [Labels that claim more than the math](17-labels-that-claim-more.md)

## Rules derived from it

18. [What an indicator should show](18-what-an-indicator-should-show.md)
19. [Ground rules for strategies](19-ground-rules-for-strategies.md)
