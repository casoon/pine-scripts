# Futures Context Module

Daily-only context module that surfaces the futures information a CFD or spot chart cannot
provide on its own: Open Interest, ΔOI read against the front contract's own price change, and
the front/next term structure (Contango/Backwardation, curve trend). It never compares the
chart symbol's price against the futures price — the front/next spread is two legs of the same
futures feed and is internally consistent on its own.

This is the single, repo-wide place for the futures-context dimension described in
[`DATA_VALIDITY.md`](../../../DATA_VALIDITY.md) §4. It intentionally does not belong to any
indicator suite — the function (OI, term structure, real futures volume) is not specific to any
one signal engine and should not sit behind a suite namespace.

## Features

- Explicit Front-Month and Next-Month futures symbol inputs — no auto-mapping from the chart
  symbol (see "Design decision" below for why)
- Daily-only gate — on any intraday timeframe the table shows a visible notice and no
  interpretation is computed
- Open Interest for the front contract, with a visible "no OI feed for `<symbol>`" state instead
  of silently showing zero when a contract has no OI feed
- ΔOI read against the front contract's own price change (single feed, no cross-feed price
  comparison), classified into the four standard OI×Price quadrants (new longs / new shorts /
  short covering / long liquidation)
- Front/Next term structure: Contango / Backwardation / Flat, plus a curve-trend read (rising /
  falling / flat) from the EMA of the spread
- Real-volume validity check on the front contract via `syminfo.volumetype` (`base`/`quote` only)
  — degrades to a visible "not real" state on tick-volume or missing-volume feeds, never silently
  passes through
- Visible "not configured" state when the Front/Next symbols are left empty or identical
- Visible "no data feed" state when the configured symbols return no data at all
- Light-theme dashboard table in the repo-standard style, no chart-price plots
- No entry signals, no `alertcondition`/`alert()` — pure context, never a trigger

## Design decision: explicit symbols, not auto-mapping

[`vein_spread_context.pine`](../../trend_direction/vein/vein_spread_context.pine) already builds
a front/next spread, but maps the chart symbol to a futures pair automatically via
`str.contains()`. On an unmapped symbol that auto-mapping silently does nothing. This module uses
two explicit `input.symbol()` fields (Front, Next) instead — the user states the pair directly,
and an unconfigured or misconfigured pair (empty, or Front == Next) is shown as a visible
"NOT CONFIGURED" status rather than a silent blank table.

The default pair (`NYMEX:NG1!` / `NYMEX:NG2!`) matches the repo's reference instrument
(`CAPITALCOM:NATURALGAS`).

## Chart settings

- **CME data latency:** NYMEX/COMEX/CBOT futures data is delayed by roughly 10 minutes without a
  paid CME data package. On Daily this is negligible — a settled Daily bar is unaffected by an
  intraday latency of a few minutes. This module is Daily-only by design, so the latency
  condition from [`DATA_VALIDITY.md`](../../../DATA_VALIDITY.md) §9.3 does not apply in practice
  here; it would matter if the same request pattern were ever reused intraday.
- Historical depth for the Front/Next symbols depends on the user's TradingView plan and is
  independent of the chart symbol's own history.
