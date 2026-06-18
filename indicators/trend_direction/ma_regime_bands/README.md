# MA Regime Bands

Regime overlay that classifies the market as Bull, Bear, or Neutral using the alignment of three configurable moving averages, gated by an ATR-normalized trend-strength filter. On a regime flip it anchors an entry level at the MA stack edge and an ATR-based stop level, rendered as a stop zone on the chart.

## Features

- Three configurable MAs (SMA, EMA, DEMA, TEMA, JMA) — default 21 / 55 / 89
- Regime classification on confirmed closes: Bull (close above all MAs), Bear (close below all MAs), Neutral otherwise
- Trend-strength gate: regime only triggers when the MA spread / ATR exceeds a minimum threshold
- Three strength-normalization modes: Off (fixed threshold), By MA Type (threshold scaled per MA type), Auto (threshold scaled by current vs. long-run average MA slope)
- ATR-based stop zones: entry at the MA stack edge, stop at entry ∓ ATR × multiplier, drawn as a filled zone while the regime holds
- Regime labels (BULL / BEAR / NEUTRAL) and optional background tint
- Alerts on Bull regime start, Bear regime start, and regime end (neutral/transition)

## Regime Logic

A regime requires both conditions on a confirmed bar close:

1. **Alignment** — close is on the same side of all three MAs
2. **Strength** — `(highestMA − lowestMA) / ATR ≥ minStrength`

When the strength gate fails, the regime is Neutral even if price is aligned — this suppresses signals in tight, overlapping-MA ranges.

## Stop Zones

On a Bull flip, the entry level is set to the highest MA and the stop to `entry − ATR × multiplier`. On a Bear flip, the entry is the lowest MA and the stop `entry + ATR × multiplier`. Levels persist unchanged until the regime ends.

## Inputs

| Group | Inputs |
|---|---|
| Moving Averages | MA type, three lengths, show MAs / average MA |
| ATR Stop Zones | ATR length, stop-loss multiplier, show zones |
| Trend Strength | Normalization mode, base min strength, auto-normalize lookback |
| UI | Regime labels, label size, background tint |
