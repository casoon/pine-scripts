# Ground rules for strategies

For a strategy to show in the tester whether it pays, it has to follow these rules. Each of them came
from a mistake that made a result look good once.

## Execution

- Signal on the confirmed close, entry at the **next open**. No `process_orders_on_close` as default,
  no `calc_on_every_tick`, no `calc_on_order_fills`.
- Gaps fill at the open, not at the stop price.
- When target and stop fall in the same bar, **the stop counts first**. The TradingView tester guesses
  the intrabar path, and a strategy with close targets can profit from that guess systematically.
- Higher-timeframe values only confirmed (`[1]` with `lookahead_on`). Pivots only from their
  confirmation bar ([13](13-running-htf-values.md), [09](09-hindsight-measures.md)).
- Standard candles only. Note the candle alignment ([08](08-candle-alignment.md)).

## Costs

- Spread as an input in price points instead of commission in percent.
- Financing per night as an input, long and short separately, with the weekday that carries the
  weekend. Deducted per held night in the result table.
- A cost stress switch (for example ×1.5). A strategy that flips under stress does not pay.
- Position size by risk at the stop, not a share of equity ([07](07-cfd-costs.md)).

## Baseline

- A **random entry** mode: same side, same frequency, same exit, fixed seed. Only the distance to
  that base is the contribution of the signal ([02](02-win-rate-follows-geometry.md),
  [03](03-drift-and-the-side-baseline.md)).
- For every filter, a **random omission** mode that removes the same number of trades
  ([04](04-filters-vs-random-omission.md)).
- Long and short judged separately, each against its own base.

## Exit

- At least one **fixed exit** (target, stop, time limit in ATR), even when the strategy is built
  around a trailing exit ([06](06-trailing-exits.md)).
- Stop distance frozen at the signal.
- The distribution of exit reasons in every report ([16](16-exits-that-never-fire.md)).

## Measures

- **Net result per trade in R** as the main measure, with its spread. Profit factor alone hides
  sample size and distribution.
- Drawdown from equity **including open positions**, bar by bar, not only from closed trades.
- Win rate only next to its base rate.

## Inputs and testing

- Inputs set **once** on a development period, then tested **unchanged** on a later period and on
  instruments that played no part in the choice. No tuning per instrument and timeframe
  ([05](05-per-instrument-tuning.md)).
- Few inputs. Each one is a degree of freedom.
- **Sample size:** thirty trades are not enough. Separating a realistic edge of well under half an R
  per trade from zero takes several hundred trades. Fewer is a hint, not a result.
- Before judging "no edge", check that the test would detect an edge if there were one: plant a known
  advantage into the data and see whether the measurement finds it. Otherwise "no edge" and "measured
  too weakly" look the same.
- Record how many variants were tried. The number of attempts belongs to the result.

## Ratings

- **Not ready** is the default.
- **Promising** only when the result is net of financing and cost stress, above the random baseline,
  on data that was not used for the choice. A result from the fitting window does not qualify.
- Every assessment states the cost model, candle alignment, fitting and test period, and the number of
  variants tried.
