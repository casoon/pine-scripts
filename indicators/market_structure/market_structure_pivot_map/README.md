# Market Structure Pivot Map

A **Location**-role structure map. It draws pivot levels for any timeframe (or the chart's own), the Central Pivot Range (CPR), previous high/low, the current-day open, and ADR/ATR-based range projections — then reports where price currently sits relative to that structure. It deliberately does **not** generate entry signals: its only job is to answer *where are we* (nearest support/resistance, CPR context, confluence), not *buy/sell now*.

## Features

- Classic or Fibonacci pivot formulas (P, R1–R4, S1–S4)
- Central Pivot Range (CPR: P / TC / BC) with a width regime classification (Narrow / Normal / Wide) relative to daily ATR
- Previous high/low and current-day open reference lines
- Range projections (0.25 / 0.50 / 1.00) off Day Open, Previous Close, or Pivot — using ADR, previous-day range, or ATR
- Confluence zones via greedy clustering of all drawn levels across timeframes
- Nearest support and resistance readout with ATR-normalized distance
- Free timeframe choice (blank = chart's own) plus two optional overlay timeframes
- Light-theme status table and CPR-cross / context alerts

## Timeframe

- **Pivot Timeframe** — an `input.timeframe()` field. Leave it **blank** and the chart's currently selected timeframe applies; set a **fixed** timeframe (`D`, `W`, `M`, `240`, `60`, …) to lock the pivots regardless of the chart. This primary timeframe drives the CPR context, projections, and status table.
- **2nd / 3rd Timeframe** — optional overlays, each any timeframe, drawn at a configurable extra transparency so the primary stands out. They also feed the nearest-S/R and confluence calculations.

## Levels

| Level | Meaning |
|---|---|
| P | Pivot point — `(H+L+C)/3` of the previous HTF period |
| TC / BC | CPR top / bottom — central value band |
| R1–R4 / S1–S4 | Resistance / support pivots (Classic or Fibonacci) |
| Prev High / Low | Previous HTF period extremes |
| Day Open | Current daily open |
| ±0.25 / 0.50 / 1.00R | Range projections off the chosen base |

All HTF data is read with `lookahead_on` on the **previous** completed period, so pivot levels are fixed for the current period and do not repaint.

## Status table

Deliberately slim — it shows only what the chart itself does not already make obvious:

| Row | Reads |
|---|---|
| CPR Width | Narrow / Normal / Wide and the CPR/ATR ratio |
| Resistance | Nearest level above price, name + distance in ATR |
| Support | Nearest level below price, name + distance in ATR |

Everything else (location vs CPR, confluence, projections) is read directly off the drawn levels.

## Confluence

Every drawn level is collected, sorted, and greedily clustered: adjacent levels within `Confluence Distance ATR Mult × ATR` form one zone. A zone is drawn only when it contains at least `Minimum Levels in Zone` levels. Cross-timeframe overlaps (e.g. a Daily R1 sitting on a Weekly P) are where the meaningful confluence appears.

## Role & scope

This indicator is intentionally single-purpose (Location). It does not fold in trend, momentum, or trigger logic. The optional CPR-context alerts (Bullish/Bearish) describe where price sits relative to the CPR band — they are not trade signals. Combine it with a separate trigger/momentum tool for entries.
