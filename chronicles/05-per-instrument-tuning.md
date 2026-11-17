# Per-instrument tuning does not carry forward

The usual workflow for a strategy is: pick an instrument, optimise the inputs, then confirm on a
walk-forward. Several strategies from this collection were put through exactly that, done properly
and outside TradingView.

## How it was done

For each instrument, an adaptive search over the strategy's inputs, using only data available at the
time of each decision. The chosen setting was then traded in the following half year. That repeated
every half year. As a control: a random search with the same budget, and the unchanged defaults.

## What came out

- The setting chosen per instrument was **not better than randomly chosen settings** in the period
  after.
- For several strategies even the **ranking** of settings did not carry over from one period to the
  next. What was best last year was not more likely to be good next year.
- Fixed settings used for all instruments were more stable than any choice from many candidates.
- Small changes to the search (starting values, grid) shifted the optimised result strongly. A single
  optimised run is noise until it has been repeated on untouched data.

## What follows

- Inputs are set **once**, on a development period or a development set of instruments, and then
  tested **unchanged** on a later period and on instruments that played no part in the choice.
- Fewer inputs. Every input is a degree of freedom the optimiser will use. A strategy with hundreds
  of inputs cannot be tested honestly.
- An optimised result is marked as "in the fitting window". It is not a rating.
