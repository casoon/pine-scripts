# Running higher-timeframe values

A review of all scripts that use `request.security` found two problems that make history look better
than live trading.

## Real lookahead

One script read daily ATR and daily range with `lookahead_on` on the **current** daily bar, not the
previous one. Historical intraday bars received the final daily value, which was not known at that
time. Levels projected from it looked more precise in history than they ever could live.

The correct pattern for confirmed values: `request.security(sym, tf, expr[1], lookahead = barmerge.lookahead_on)`.

## Running HTF values in signals

Sixteen packages read the **running** higher timeframe (`lookahead_off`) and used it in signals,
scores or alerts. A lower-timeframe bar can be confirmed while the daily or 4h bar is still forming.
After a reload the same historical bar shows the final HTF value. The alert that fired live and the
signal visible in history are then not the same.

Bar-close gating on the chart timeframe does not fix that.

## What follows

- Two explicit tracks when an HTF value matters:
  1. confirmed HTF: the last closed bar, for signals, alerts and backtests;
  2. forming HTF: a live state, displayed as provisional and never stored as a historical signal.
- A strategy backtest that uses running HTF values is optimistic by construction.
- Cross-symbol requests need a neutral `na` branch. A missing reference value means "unknown", not 0.
  Only normalised quantities (returns, ratios, ranks) are compared across symbols, never raw prices.
