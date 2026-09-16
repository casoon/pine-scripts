---
title: Strategies
description: Strategy wrappers put one indicator's signal logic into TradingView's Strategy Tester. They are standalone scripts, maintained by hand.
order: 3
---

Each strategy is a self-contained `strategy()` script. It replicates the signal logic of one
indicator and adds entry and exit management. There is no generator: a change to an indicator
does not reach its strategy by itself, and pulling a strategy back in line is a deliberate step.

## Scripts

| Strategy                                                                                                                                                   | Based on                                                                             | Stop                          |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------- |
| [`chandelier_flip_radar_strategy.pine`](https://github.com/casoon/pine-scripts/blob/main/strategies/chandelier_flip_radar/chandelier_flip_radar_strategy.pine) | [Chandelier Flip Radar](../../trend-direction/chandelier-flip-radar/)                 | trailing, ATR envelope        |
| [`commodity_pulse_matrix_v4_strategy.pine`](https://github.com/casoon/pine-scripts/blob/main/strategies/commodity_pulse_matrix/commodity_pulse_matrix_v4_strategy.pine) | [Commodity Pulse Matrix](../../composite/commodity-pulse-matrix/) v4                 | directional fixed SL/TP       |
| [`market_average_relationship_engine_strategy.pine`](https://github.com/casoon/pine-scripts/blob/main/strategies/market_average_relationship_engine/market_average_relationship_engine_strategy.pine) | [Market–Average Relationship Engine](../../trend-direction/market-average-relationship-engine/) | trailing, MA ∓ ATR multiple   |
| [`oscillator_divergence_zones_strategy.pine`](https://github.com/casoon/pine-scripts/blob/main/strategies/oscillator_divergence_zones/oscillator_divergence_zones_strategy.pine) | [Oscillator Divergence Zones](../../momentum/oscillator-divergence-zones/)            | pivot plus ATR buffer         |
| [`reversal_engine_score_strategy.pine`](https://github.com/casoon/pine-scripts/blob/main/strategies/reversal_engine_score/reversal_engine_score_strategy.pine) | [Reversal Engine Score](../../momentum/reversal-engine-score/)                        | structural, R-multiple target |
| [`smooth_trend_radar_strategy.pine`](https://github.com/casoon/pine-scripts/blob/main/strategies/smooth_trend_radar/smooth_trend_radar_strategy.pine)       | [Smooth Trend Radar](../../trend-direction/smooth-trend-radar/)                       | fixed, TP1/TP2/TP3 levels     |
| [`wavetrend_v4_strategy.pine`](https://github.com/casoon/pine-scripts/blob/main/strategies/wavetrend/wavetrend_v4_strategy.pine)                            | [WaveTrend](../../momentum/wavetrend/) v4                                             | trailing                      |

## What every wrapper adds

- **Trade direction:** both, long only or short only.
- **Entries on the confirmed bar**, on by default, so historical and realtime entries match.
- **Cooldown** in bars after an exit, and an optional **break-even stop** that moves the
  existing stop instead of adding a second exit.
- **Filters:** session, date range, maximum drawdown, maximum intraday loss, losing-streak
  limit.

## Standard candles only

Every strategy draws a red warning label on Heikin Ashi, Renko, Kagi, Line Break, Point & Figure
and Range charts. Orders there fill at synthetic bar prices, and the result says nothing about
the market — it is reliably flattering and never reproducible.

## Shared defaults

| Setting       | Value           | Note                                              |
| ------------- | --------------- | ------------------------------------------------- |
| Position size | 10 % of equity  | change in the strategy's properties               |
| Commission    | 0.02 %          | raise it for crypto maker/taker fees              |
| Slippage      | 1 tick          | raise it for illiquid instruments                 |
| Entries       | confirmed bar   | prevents repainting                               |

Overnight and roll financing on CFDs is not priced in. On multi-day holds that is a known cost
the Strategy Tester does not show.

## Known limitations

- **Entry timing:** signals fire on the bar close and the strategy enters at the next bar's
  open, which is the realistic case. Filling at the exact close is useful for comparison only.
- **Pivot-anchored stops** can sit several bars in the past. On illiquid instruments, check that
  the resulting distance still describes a tradable risk.
- **Higher-timeframe pivots** use the non-repainting pattern of `request.security()` with
  lookahead against an offset series. It needs enough history to warm up.

## Testing a strategy

1. Run it on at least two instruments and two timeframes before drawing a conclusion.
2. Record the baseline with default settings. Fewer than 30 trades is not a result.
3. Change one input group at a time, measure again, keep or revert.
4. Validate on data outside the window you tuned on. A parameter set that only works where it
   was fitted has been fitted, not found.
5. Test long only and short only separately; an average can hide one healthy side and one
   broken one.

Backtest figures are kept in each strategy's assessment file in the repository, together with
instrument, timeframe and sample size. This documentation does not quote them.
