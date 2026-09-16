---
title: Overview
description: What the collection contains, what it deliberately leaves out, and how this documentation is organised.
order: 0
---

pine-scripts is a collection of TradingView indicators and strategies written in Pine Script v6.
The source is on GitHub under the MIT licence; some scripts are also published on TradingView
under the name WavesUnchained.

It is a running collection of ideas, not a finished product catalogue. Quality is treated as an
ongoing process, carried out with AI assistance, and it covers more than code correctness:
whether an indicator's idea is sound, whether it is plausible on the instrument it is meant for,
and whether it reads data that actually carries a signal there.

## What it covers

- **Indicators** in nine groups: market structure, trend direction, trend strength and regime,
  momentum, mean reversion, money flow and volume, volatility, relative strength, and composite
  indicators that combine several of them.
- **Strategies** that wrap the signal logic of a few indicators for TradingView's Strategy
  Tester.
- **A data validity rule set** that decides, per script, which data can carry a signal on which
  instrument, and a Data Contract in the script header that states the result. The Data
  Contract is being added to every script; not all of them carry it yet.

## How the scripts are built

- **One role per indicator.** An indicator measures one thing — structure, trend strength,
  exhaustion — instead of voting on everything at once. Composite indicators combine roles
  explicitly and show which part drives the reading.
- **Degrade instead of guessing.** Where a script uses volume, it checks whether the feed
  delivers real trade volume. If not, the volume part switches off visibly and the remaining
  weights are renormalised.
- **Confirmed alerts.** The repository convention is that alerts fire on the closed bar, not on
  a bar that is still forming.

## Where it stops

- **Not advice.** The scripts are for education and chart analysis. Nothing here recommends a
  trade, and no page states how profitable a signal is.
- **Status varies.** Many indicators are drafts that have not been validated on live charts yet.
  The `CHANGELOG.md` next to each script records what changed and when.
- **TradingView only.** The scripts run inside TradingView. Nothing here fetches market data,
  connects to a broker or places orders.

## How the docs are organised

- **Getting started:** add a script to a chart, a first walkthrough, and the indicator index.
- **Concepts:** data validity and the Data Contract, alerts, and the strategy wrappers.
- **Indicator groups:** one page per indicator directory, built from the `README.md` in that
  directory. The README on GitHub and the page here are the same text.

<small>Trading involves substantial risk of loss. Past behaviour of an indicator says nothing
about future results.</small>
