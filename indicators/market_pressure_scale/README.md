# Market Pressure Scale

Two-component oscillator that separates **Setup Pressure** (market coiling for a move) from **Impulse Pressure** (active directional momentum). Both run on a 0–100 scale in the same sub-pane. A phase label, signal markers, StochRSI overlay, and Impulse divergence complete the picture.

## Why two components?

Classic volatility indicators (ATR, Bollinger Width) measure compression but go quiet right when a breakout fires. Momentum oscillators do the opposite. This indicator tracks both simultaneously so you can see the full coil-and-release cycle in one panel.

## Curves

| Curve | Color | What drives it |
|---|---|---|
| Setup Pressure | Orange (thick) | ATR compression, BB compression, S/R proximity, relative volume |
| Impulse Pressure | Green (thick) | Range expansion vs ATR, relative volume, candle body ratio |
| StochRSI K | Blue (thin, optional) | Standard StochRSI K line |
| StochRSI D | Orange-blue (thin, optional) | Standard StochRSI D line |

## Phases

Priority order — first match wins:

| Phase | Condition |
|---|---|
| **Impulse Running** | Impulse > 70 |
| **Breakout Watch** | Setup > 55 and Impulse ≥ 45 |
| **Coiling** | Setup > 65 and Impulse < 45 |
| **Sideways / Quiet** | Setup < 40 and Impulse < 40 |
| **Neutral** | everything else |

## Signal markers

Small labels in the oscillator panel with hover tooltips. Each marker is individually toggleable.

| Label | Trigger | Meaning |
|---|---|---|
| `▲` gold | Setup crosses 65 with Impulse < 40 | Coiling — spring loading |
| `ℹ` orange | Impulse crosses 45 with Setup > 55 | Breakout Watch — watch for follow-through |
| `FC` red | Setup drops below 52 without Impulse ever reaching 45 | Failed Coil — breakout stalled |
| `NI` red | Impulse > 70, Setup drops below 40 | Naked Impulse — move without structural backing |
| `DP` purple | Both components above 65 simultaneously | Double Peak — sharp move imminent |
| `DF` gray | Both falling from above 60, one crosses below 55 | Dual Fade — momentum exhausting |

## Impulse divergence

Bullish/bearish divergence between price pivots and Impulse Pressure, drawn the same way as WaveTrend v4:
- **Bull** — price makes lower low, Impulse makes higher low → momentum holds despite price weakness
- **Bear** — price makes higher high, Impulse makes lower high → momentum fading despite price strength

## Dashboard table

Top-right panel, 5 rows:

| Row | Content |
|---|---|
| Phase | Current phase, color-coded |
| Setup | Value / 100 + direction arrow (orange) |
| Impulse | Value / 100 + direction arrow (green) |
| Bias | Bullish / Bearish from configurable MA cross |
| Range Pos. | Where close sits within the N-bar high/low range (0–100 %) |

## Inputs

**Main** — Normalisation window, ATR / BB lengths, BB multiplier, Volume MA, S/R Lookback

**Bias** — MA type (EMA / RMA / SMA / WMA / HMA / JMA), Fast length (default 9), Slow length (default 21)

**Smoothing** — applied to both output curves; type (EMA / RMA / SMA / WMA / HMA / JMA) + length; JMA Phase + Power

**Signal Markers** — master toggle + individual toggle per marker

**StochRSI** — show toggle, K smoothing, D smoothing, RSI length, Stoch length

**Divergence** — Bull / Bear toggles, pivot left / right lookback, min / max bar range
