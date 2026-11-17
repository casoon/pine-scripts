# Candle alignment changes the result

A 4h candle can start at 00:00 UTC or at a session anchor (for example 18:00 New York for many CFD
and futures markets). The same strategy on the same instrument produces different signals and
different trades depending on where the candles start.

## What was seen

When a Pine strategy was rebuilt outside TradingView, its trades only matched once the candles were
built with the same anchor TradingView uses for that symbol, and once the stop mode of the exact
script version was reproduced. Before that, the rebuild produced a different strategy with the same
name.

Measured over several alignments of the same candles, results shifted noticeably between alignments,
without any change in the rule.

## What follows

- A backtest is valid for the candle alignment it was run on. Note it in every assessment.
- Two runs with different alignments are not comparable, and a rule that only works on one alignment
  is fitted to that alignment.
- When a script is ported or rebuilt, reproduce the trades of the original first, then measure.
