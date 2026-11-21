# Situation Brief

Describes the current chart situation in plain words instead of a score: which way the swing structure points, what state the last breakout is in, how stretched price is, and the four levels that decide what happens next. Everything is shown in one table plus level lines on the chart. It produces no entries and no trade quality rating — it answers "where are we right now, and what would change the picture?". Long and short follow the same mirrored rules.

## Features

- Trend from confirmed swing breaks, with the number of breaks in a row
- Depth of the last pullback as a share of the prior leg
- Breakout state: on this bar, holding, retesting, back inside the retest zone, failed
- Breakout bar: where it closed within its range and its volume against the average (real trade volume only)
- Stretch: RSI, distance to the Bollinger band in trend direction, distance to a fast and a slow EMA — all distances in ATR
- Bars since the last new extreme, as a sign of hesitation
- Level ladder with distance from the close: trend extreme, broken level, failure level, protected swing
- Level lines, a shaded retest zone, event markers and three alerts

## Structure logic

Swings are pivots with `Swing pivot: bars left` / `bars right`. Every state change happens on a close.

| Event | Uptrend (downtrend mirrored) |
|---|---|
| **Break (BOS)** | Close above the highest confirmed swing high since the last break, provided that swing is also the trend high. The broken swing becomes the *broken level*; the lowest low since that swing becomes the *protected low*. |
| **Trend change** | Close below the protected low, or below the lowest swing low that has formed after the trend high (a lower high followed by a lower low). |
| **Failed breakout** | Close below the *failure level* = broken level − `Retest zone depth` × ATR of the breakout bar. The trend itself stays until a trend change. |

The first structure on the chart is set by the first close beyond the latest swing high or low.

A new high counts as a break only once the prior high is a confirmed swing. In a straight run without a confirmed pullback the trend high moves up, but the break counter and the protected low stay where they are.

## Level ladder

| Level | Meaning in an uptrend |
|---|---|
| Trend high | Highest high since the last break. Beyond it the move continues. |
| Broken level | The swing that was broken. A pullback to here is a normal retest. |
| Failure level | A close below it means the breakout failed. |
| Protected low | A close below it ends the uptrend. Shows the counter swing after the trend high when one has formed, otherwise the pullback low the last break started from. |

The retest zone is the band between broken level and failure level.

## Table

| Row | Content |
|---|---|
| Trend / Breaks in a row / Last pullback | Structure direction, continuation count, pullback depth (below 50 % reads as shallow) |
| Breakout / Breakout bar | Breakout state and bars since the break; close location and volume of the breakout bar |
| RSI / To band / From EMA | Stretch readings; distances are signed (positive = above) |
| Last new high / low | Bars since the trend extreme; more than zero means price is not extending |
| Levels | The four levels with price and distance from the close in ATR |

## Alerts

- **Structure break** — close beyond the last swing in trend direction
- **Trend change** — protected or counter swing broken
- **Breakout failed** — close beyond the retest zone

## Settings

| Group | Setting | Default | Purpose |
|---|---|---|---|
| Structure | Swing pivot: bars left / right | 5 / 2 | Size and confirmation delay of swings |
| Structure | Retest zone depth (ATR) | 0.5 | Distance from broken level to failure level |
| Structure | Maximum scan length | 500 | How far back the protected swing is searched |
| Stretch | RSI, EMA, Bollinger, ATR, volume lengths | 14 / 9, 21 / 20, 2.0 / 14 / 20 | Stretch readings |
| Display | Level lines, markers, table, position, line extension | on / on / on / top right / 8 | Chart output |

## Limits

- The reading belongs to the chart timeframe. Use it on the timeframe whose structure you want described; a daily uptrend can coexist with a 4h trend change.
- Swings are confirmed `bars right` bars late; the protected low after a break is available at once because it is the lowest low since the broken swing.
- Values on the open bar can change until it closes.
