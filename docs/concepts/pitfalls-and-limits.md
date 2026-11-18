---
title: Pitfalls and limits
description: What made scripts in this collection produce wrong or misleading results, which of those patterns may still be in older scripts, and what Pine Script can and cannot be used for.
order: 4
---

This page is self-criticism. Most of the patterns below were found in scripts of this
collection, some only after the same logic was rebuilt outside TradingView in a separate
research engine (Kestrel, written in Rust) and checked bar by bar against TradingView's own
values. Many were fixed or the script was archived; the reviews are not complete, so older or
less checked scripts may still contain some of them. The catalog shows how far each script
has been checked.

None of these errors throws a compile error. The script runs and the chart looks fine. That
is what makes them expensive.

## Data that carries no signal

- **Tick volume read as trade volume.** CFDs and many forex feeds deliver a `volume` series
  that counts price updates, not traded contracts. MFI, VWAP, OBV, volume profiles and volume
  spikes computed from it look like money flow and are not. Scripts now check
  `syminfo.volumetype` and whether the series contains anything at all, and switch volume
  parts off visibly. See [Data validity](../data-validity/).
- **`nz(volume)` as a guard.** It turns missing volume into `0`: a filter like
  `volume > sma(volume)` then blocks every bar, and a division by volume divides by zero.
- **Fallback `volume = 1.0`.** An MFI with constant volume is an RSI of typical price, still
  labelled "volume-backed".
- **Moving the weight of missing evidence.** When the volume part drops out of a score, its
  weight went to a price oscillator, or the remaining sum was stretched back to 100 %. On a
  feed without volume the score then showed the same certainty as with exchange volume, built
  from one price series counted twice.
- **The chart feed is not the trading feed.** A CFD broker fills on its own bid/ask prices,
  not on the feed TradingView shows. Futures charts can show back-adjusted continuous
  contracts or settlement prices as close. Levels and crosses can differ by a bar or a tick.

## The chart looks better than it was

- **Pivots and divergences are drawn at the extreme, but known later.** A pivot is confirmed
  only after its right-hand bars have closed, a divergence only after the second pivot is
  confirmed. In the rebuilt engine, which only knows bars up to the current one, confirmed
  divergences arrived several bars after the low, when price had already moved away from it.
  On the TradingView chart the label sits exactly on the low. Much of "it looks great on the
  chart" comes from this.
- **Higher-timeframe values from the running bar.** `request.security()` with
  `lookahead_on` and no `[1]` offset reads a higher-timeframe bar that has not closed yet. On
  history the value is final; live it keeps changing. The two safe patterns are
  `expression[1]` with `lookahead_on`, or `lookahead_off` for display only.
- **Forward-looking labels.** One research script labelled reversals using bars that come
  after them. That is fine for offline labelling and fatal if anyone reads it as a signal. It
  is archived.
- **Scores computed after the outcome.** Some scripts rated a breakout or a reversal only
  once the reaction had already happened. That is a measurement of the past, not an indicator.
  Also archived.
- **Calculated only on the last bar.** A volume profile computed inside `barstate.islast` has
  no history: no backtest, no alert, nothing to check it against.

## Pine v6 traps

- **Stateful `ta.*` calls behind `and`, `or`, `?:` or inside an `if`.** Pine v6 evaluates
  these lazily. `alertOk and ta.crossover(a, b)` skips the crossover on bars where `alertOk`
  is false, and the function's internal history is then incomplete. The same holds for
  `ta.atr` inside `if enableBreakEven`, `ta.mfi` behind `volumeIsReal ? … : na`, and
  `ta.pivothigh`, `ta.ema`, `ta.barssince` and others. The value is wrong without any error.
  Compute `ta.*` unconditionally first, then gate the result.
- **`obj[1]` on a user-defined type inside `request.security()`.** Types are references;
  the offset has to go on the primitive fields (`obj.field[1]`).

## Scores that measure something else

- **The same information counted several times.** RSI, StochRSI, CCI and WaveTrend are
  transformations of one price series. Four oversold readings are one piece of evidence, not
  four. Scores now take one sensor per family: momentum, trend, structure, volatility, volume.
- **Direction from a quantity without direction.** Low volatility scored `+1`, high
  volatility `-1`, added into a long/short score: quiet markets then lean long and volatile
  markets lean short, regardless of price.
- **Long and short not mirrored.** One ported score checked `RSI > 50` for both sides and gave
  the short side fewer points. On real data it produced many times more shorts than longs.
  Rules are now symmetric; any asymmetry has to come from the market situation, not from the
  direction.
- **Names that promise more than the formula.**
  - A "Hurst exponent" computed as `log(range / stdev) / log(len)` does not scale like a Hurst
    estimate.
  - A "dominant cycle" counted from zero crossings of an oscillator measures noise in
    sideways phases.
  - A "divergence" built from a fast oscillator falling while its slow version rises is a
    pullback in a running trend, not a divergence between price and oscillator.
  - Point tables labelled "Probability %", "Confidence" or "Signal quality" are not
    calibrated probabilities. Used as a `minGrade` filter, they silently block valid triggers.
- **Overextension warnings during a trend.** Warnings like "do not chase" fire again and again
  in a steady trend. They describe where price is, not that it is about to turn.

## Strategy Tester traps

- **No stop on the first bar.** `strategy.entry` fills at the next bar's open. If
  `strategy.exit` is only placed inside `if strategy.position_size > 0`, that first bar runs
  without stop or target. The exit has to be queued in the entry block as well.
- **Costs left out.** Spread and overnight financing on CFDs, with the weekend charged three
  times, decide whether a short-term signal survives. The strategies here book them in a
  separate cost model per trade.
- **Only the last 500 bars.** A `last_bar_index - 500` cutoff, meant to save computation,
  limits the backtest to a fraction of the history.
- **Tables gated on `barstate.islast` only** stay empty in a historical backtest without a
  live tick. Use `barstate.islastconfirmedhistory or barstate.islast`.
- **Synthetic chart types.** Heikin Ashi, Renko and similar charts produce fills at prices
  that never traded. The strategies show a warning on them.
- **No comparison against chance.** A result means little without a baseline that enters at
  the same rate at random. Each strategy carries such a random-entry shadow test.
- **Tuned and tested on the same data.** Every filter variant tried against the same window
  makes a good result on that window less meaningful. Several filter ideas derived from
  aggregated statistics fell apart once split by timeframe and direction: what looked bad in
  the aggregate was the best setup in one combination.

## What Pine is good for

- **Showing where the market stands.** Structure, trend, momentum, volatility and context,
  computed bar by bar on the chart's own symbol and drawn where a trader looks anyway.
- **Alerts on a closed bar** from named, stable conditions.
- **Prototyping an idea quickly.** A formula is on a chart in minutes, and an obviously bad
  idea is visible quickly.
- **A rough plausibility check** in the Strategy Tester: one symbol, one timeframe, with
  costs and a random baseline.
- **Reference values.** A Pine script can export its values bar by bar (data window, chart
  export, Pine logs) so another implementation can be checked against it.

## What Pine is not good for

- **Proving that a signal beats chance.** That needs many instruments and timeframes, a
  hypothesis fixed before the measurement, out-of-sample data, a random null and a correction
  for the number of variants tried. The Strategy Tester offers none of that.
- **Data TradingView does not deliver for the symbol.** Order flow, bid/ask, real delta,
  open interest and term structure are missing on most symbols, and always on CFDs. Pine can
  only fake them from OHLC.
- **Portfolio and cross-market work.** A script sees one chart symbol, the number of
  `request.*` calls is capped, and the depth of history depends on the plan.
- **Persistent state and external data.** A script cannot keep results between sessions,
  read a database or call an API.
- **Exact execution.** The broker emulator fills at bar prices with assumptions about the
  path inside the bar. Real fills, partial fills and broker-specific prices are outside it.

That split is why measurement now happens outside TradingView and the scripts in this
repository concentrate on display: they show where the market stands, and judgement alerts
remain only for event types that have a chance of carrying an edge.
