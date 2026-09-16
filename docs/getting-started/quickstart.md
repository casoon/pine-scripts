---
title: Quickstart
description: From choosing an indicator to a first alert, with the checks that decide whether its reading means anything on your symbol.
order: 2
---

## 1. Pick an indicator

The [indicator index](../indicators/) lists every indicator with one sentence each; the sidebar
groups them by what they measure. Start from the question you want answered — where is the
structure, is there a trend, is a move exhausted — rather than from a signal.

## 2. Check what data it needs

Scripts declare their data requirements in a Data Contract at the end of the header. The block
is being added to every script; where it is still missing, the README describes which data the
indicator reads.

```text
// Data Contract:
//   Price:     REQUIRED   chart symbol
//   Volume:    OPTIONAL   real trade volume only — degrades to neutral
//   OI:        NO
//   Reference: NO
//   Verdict:   CFD-degraded
```

The verdict tells you whether the script can work on your symbol:

| Verdict              | Meaning                                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------------------ |
| `CFD-safe`           | Price only. Works on any symbol.                                                                             |
| `CFD-degraded`       | Works on any symbol. Volume or open-interest parts switch off visibly when the feed has no real trade volume. |
| `Reference-required` | Needs a reference market in addition to the chart symbol.                                                    |
| `Exchange-only`      | Needs real trade volume. Without it the script switches off visibly instead of degrading.                    |

Why this matters: [Data validity](../../concepts/data-validity/).

## 3. Add it to the chart

Follow [Add a script to TradingView](../installation/). Keep the defaults on the first run; the
input tooltips explain what each setting does and why it exists.

## 4. Use a standard chart type

Indicators read the bars the chart gives them. Heikin Ashi, Renko, Kagi, Line Break and Point &
Figure produce synthetic prices. Use candles or bars when you act on a reading.

## 5. Create an alert

Scripts with alerts expose each event as a named condition in TradingView's **Create Alert**
dialog. Messages follow one format, so an alert stays identifiable when the same script runs on
several charts:

```text
<code> · <event> · {{ticker}} {{interval}}
```

Codes, event names and the bar-close rule are described under [Alerts](../../concepts/alerts/).
