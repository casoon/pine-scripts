---
title: Alerts
description: How the scripts name, format and time their alerts, so that alert rules keep working across versions.
order: 2
---

## Named conditions

Scripts expose alerts with `alertcondition()`: each event is its own entry in TradingView's
**Create Alert** dialog, and you pick the one you want.

Some scripts additionally offer one combined `alert()` rule that carries more context, such as a
score or a regime. Their code states that you set up either the named alerts or the combined
rule, not both — otherwise the same event fires twice.

## Message format

```text
<code> · <event> · {{ticker}} {{interval}}
```

- **Code** — a short identifier per indicator, for example `CPM4`, `SMCE` or `WYS`. Codes are
  listed in
  [`indicators/ALERT_KUERZEL.md`](https://github.com/casoon/pine-scripts/blob/main/indicators/ALERT_KUERZEL.md)
  and never renamed.
- **Event** — what happened: `LONG`, `EXIT LONG`, `WATCH LONG`, `REGIME CHANGE`.
- **`{{ticker}} {{interval}}`** — TradingView fills these in, so the message names its chart
  when the same script runs on several charts.

Where it helps, a message adds state: the price as `@ {{close}}`, or a plotted value such as a
score.

Alert **titles** stay the same across versions, because TradingView binds existing alert rules
to the title. A new version changes the message format at most, never the title.

## Bar-close confirmation

An alert must not fire on a bar that is still forming and then vanish when the bar closes. The
repository convention:

- Scripts with named alerts carry an input **Alerts only on bar close (confirmed)**, on by
  default. Where the signal itself is already defined on the closed bar, the input is not needed.
- Runtime `alert()` calls use the frequency *once per bar close*, unless the code explains why
  an event should fire intrabar.

Choosing *Once Per Bar Close* in the alert dialog is still possible, but the scripts do not
rely on it.

## Kinds of alert

Alert kinds follow the signal types of the indicator design:

| Kind                   | Example title             | Purpose                                         |
| ---------------------- | ------------------------- | ----------------------------------------------- |
| Entry / trigger        | `XYZ Long`, `XYZ Short`   | the actionable core signal                      |
| Exit                   | `XYZ Exit Long`           | only where the indicator defines exits          |
| Watch / setup          | `XYZ Watch Long`          | early warning, always separate from the entry   |
| Regime / context       | `XYZ Regime Change`       | context, not a trade signal                     |
| Quality / confluence   | `XYZ High-Quality Setup`  | optional note on how strong a setup is          |
| Invalidation / warning | `XYZ Bull Weakness`       | reversal risk or trap                           |

Watch and entry are always two alerts, so you decide how much lead time you want.
