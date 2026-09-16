---
title: Data validity
description: An indicator can only measure what its input data contains. The rule set decides, per script, which data carries a signal on which instrument.
order: 1
---

Correct maths on data that lacks the information it is supposed to measure produces a clean,
meaningless line. Volume is the usual case: many feeds deliver a `volume` series that is not
trade volume. There is no blanket policy; each script is decided on its own, against the
criteria below.

## Information classes

Data is classified by where the information comes from, not by indicator family:

| Class                | Content                                                                    | Source                                      |
| -------------------- | -------------------------------------------------------------------------- | ------------------------------------------- |
| A — Chart price      | OHLC and time, and what derives from them: range, returns, structure, volatility | chart symbol                                |
| B — Reference price  | OHLC of the underlying market                                              | `request.security()` on a future or underlying |
| C — Reference volume | real trade volume, VWAP, volume profile                                    | the reference market, never a CFD           |
| D — Positioning      | open interest, change in open interest, COT                                | futures and derivatives markets             |
| E — Term structure   | front and next month, calendar spread, contango and backwardation          | futures curve                               |
| F — Fundamentals     | storage, weather, production, macro data                                   | external, mostly unavailable in Pine        |

Class A exists on every instrument. Everything from B onwards is a deliberate extra decision
with its own costs: a cross-symbol request, session alignment, repaint risk.

## Is the volume real?

Scripts decide from `syminfo.volumetype`, not from the instrument type and not from the fact
that a `volume` series exists:

| `syminfo.volumetype` | Meaning                               | Trade volume?        |
| -------------------- | ------------------------------------- | -------------------- |
| `base`               | volume in base currency or contracts  | yes                  |
| `quote`              | volume in quote currency (crypto)     | yes, different unit  |
| `tick`               | number of price updates               | no                   |
| `n/a`                | no volume                             | no                   |

The repository deliberately keeps no table of which provider reports which volume type for
which symbol. That is a property of the feed and it changes; the script asks the symbol at
runtime.

`nz(volume)` is not a guard. It turns missing volume into zero, and zero compared with its own
average makes a volume condition permanently true or permanently false without anyone noticing.

## When there is no trade volume

- A volume component degrades to neutral instead of voting.
- Weighted scores renormalise the remaining weights, so the total does not sink on feeds
  without trade volume.
- The chart shows it: a dashboard row or a label states that the volume part is inactive.
- Scripts that make no sense without real volume — volume profiles, cumulative delta, Klinger —
  are marked `Exchange-only` and switch off visibly.

## No reference market inside an indicator

A single indicator does not request a second symbol to replace missing volume. A reference
market brings latency, settlement and back-adjustment differences, session offsets, request
budget, repaint risk, and a symbol mapping that silently goes wrong on unknown symbols.

It is worth that cost only where it adds a dimension the chart symbol does not have at all —
open interest, term structure, trade volume as regime context — and that belongs in one
dedicated context module rather than in twenty scripts: the
[Futures Context Module](../../composite/futures-context-module/).

## The Data Contract

A `.pine` file declares which data classes it needs at the end of its header. The block is being
added to every script; not all of them carry it yet.

```text
// Data Contract:
//   Price:     REQUIRED   chart symbol
//   Volume:    OPTIONAL   real trade volume only — degrades to neutral
//   OI:        NO
//   Reference: NO
//   Verdict:   CFD-safe
```

- `Price` is always `REQUIRED`.
- `Volume` and `OI` are `NO`, `OPTIONAL` (the part degrades) or `REQUIRED` (the script is
  pointless without it).
- `Reference` is `NO` or names the symbol source when classes B to E are used.
- `Verdict` is one of:
  - `CFD-safe` — runs anywhere, needs nothing beyond class A.
  - `CFD-degraded` — runs anywhere; the volume or open-interest part switches off visibly.
  - `Reference-required` — needs a reference market; not valid on a CFD alone.
  - `Exchange-only` — needs real trade volume (`base` or `quote`). On `tick` or `n/a` the
    script switches off visibly instead of degrading.

The verdict describes the data requirement, not an instrument class. Whether a given symbol
meets it is decided by the runtime check, so a contract never says that a script "does not run
on CFDs".

## Beyond the data class

Some conditions change the series a script calculates on without the script seeing them:

- **Back-adjustment** on continuous futures shifts historical prices, and with them every level
  and Fibonacci retracement.
- **Settlement as close**: the daily close of a future is the settlement price by default, not
  the last trade. A CFD's daily close and a future's daily close are different quantities.
- **Extended or regular session** produces different bars, highs, lows and daily closes.
- **Non-standard chart types** — Heikin Ashi, Renko, Kagi, Point & Figure, Line Break — deliver
  synthetic OHLC.
- **Delayed data**: CME group markets are delayed by about ten minutes without a paid data
  package, which matters intraday.
- **Realtime values** of the open bar change until it closes, and `request.security()` returns
  unconfirmed values in realtime.

The complete rule set, in German, with the matrix per instrument type and the runtime patterns:
[`DATA_VALIDITY.md`](https://github.com/casoon/pine-scripts/blob/main/DATA_VALIDITY.md).
