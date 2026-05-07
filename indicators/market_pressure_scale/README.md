# Market Pressure Scale

**TradingView:** https://de.tradingview.com/script/y36Lhppi/

Two-component oscillator that separates **Setup Pressure** (market coiling for a move) from **Impulse Pressure** (active directional momentum). Both run on a 0–100 scale in the same sub-pane. A phase label, signal markers, StochRSI and MFI overlays with divergences, and price-chart markers complete the picture.

## Why two components?

Classic volatility indicators (ATR, Bollinger Width) measure compression but go quiet right when a breakout fires. Momentum oscillators do the opposite. This indicator tracks both simultaneously so you can see the full coil-and-release cycle in one panel.

## Curves

| Curve | Color | What drives it |
|---|---|---|
| Setup Pressure | Orange (thick) | ATR compression, BB compression, S/R proximity, relative volume |
| Impulse Pressure | Green (thick) | Range expansion vs ATR, relative volume, candle body ratio |
| StochRSI K | Blue (thin, optional) | Standard StochRSI K line |
| StochRSI D | Orange-red (thin, optional) | Standard StochRSI D line |
| MFI | Lavender (thin, optional) | Money Flow Index — RSI applied to Typical Price × Volume |

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

## Divergences

All divergences share the same pivot lookback and bar range settings. A master toggle controls all sources; Bull/Bear are individually toggleable beneath it.

**Impulse Pressure** — divergence between price pivots and Impulse Pressure, drawn on the oscillator in the same visual style as WaveTrend v4.

**StochRSI K** — same pivot logic applied to the StochRSI K line. Divergence lines shown in the oscillator when StochRSI is enabled.

**MFI** — same pivot logic applied to the MFI line. Detects when directional volume flow diverges from price. Divergence lines shown in the oscillator when MFI curve is enabled; `◆` price-chart markers are independently toggleable (visible even with MFI curve off).

## Price-chart markers

Markers drawn directly on the candlestick chart, decoupled from oscillator curve visibility:

| Marker | Color | Meaning |
|---|---|---|
| `●` green | Lavender | StochRSI K crosses above D in oversold zone |
| `●` red | Red | StochRSI K crosses below D in overbought zone |
| `◆` lavender | Lavender | MFI divergence (bullish or bearish) |

StochRSI cross dot size scales with Setup Pressure — larger dot = more structural backing.

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

**StochRSI** — show toggle; Divergences sub-toggle; Crosses sub-toggle with Zone Low / Zone High thresholds (cross dots only in overbought / oversold zone, sized by Setup Pressure); K smoothing, D smoothing, RSI length, Stoch length

**MFI** — show toggle; Divergences sub-toggle (oscillator, active only when MFI on); Chart Markers sub-toggle (price chart, independent of MFI curve); Length

**Divergence** — master Show Divergences toggle; Bull / Bear sub-toggles; pivot left / right lookback, min / max bar range
