# Market Pressure Scale

**TradingView:** https://de.tradingview.com/script/y36Lhppi/

Two-component oscillator that separates **Setup Pressure** (market coiling for a move) from **Impulse Pressure** (active directional momentum). Both run on a 0–100 scale in the same sub-pane. A phase label, signal markers, and a Move Strength column gauge complete the picture.

## Why two components?

Classic volatility indicators (ATR, Bollinger Width) measure compression but go quiet right when a breakout fires. Momentum oscillators do the opposite. This indicator tracks both simultaneously so you can see the full coil-and-release cycle in one panel.

## Curves

| Curve | Color | What drives it |
|---|---|---|
| Setup Pressure | Orange (thick) | ATR compression, BB compression, S/R proximity, volume drying up |
| Impulse Pressure | Green (thick) | Range expansion vs ATR, relative volume, candle body ratio |

## Phases

Priority order — first match wins:

| Phase | Condition |
|---|---|
| **Sideways / Chop** | Range Chop Filter active (ADX < 16, \|DI+ − DI−\| < 5, price mid-range) |
| **Impulse Running** | Impulse > 70 |
| **Sideways / Quiet** | Setup < 40 and Impulse < 40 |
| **Neutral** | everything else |

### Range Chop Filter

A chop filter (ADX < 16 and DI+/DI− within 5 of each other while price sits in the middle 60% of the range) takes priority over every other phase, and gates Failed Coil and Reversal so they only evaluate at a genuine range extreme, not on coincidental compression in the middle of a dead range.

## Move Strength

Blue columns (Show Columns toggle, default on), plotted behind Setup/Impulse Pressure rather than as a full-pane background so they add information without washing out the two curves. Tracks the expected magnitude of the eventual move — not whether a setup exists, but how forceful the release is likely to be once it fires. Built from compression depth (energy stored), range-edge proximity (location), and ADX (trend confirmation), and suppressed to a third of its value while the Range Chop Filter is active. Colored in 5 opacity bands (near-invisible → faint → medium → strong → near-solid blue) rather than a continuous gradient, so consecutive bars read as a clear step change instead of a near-uniform tint. Also shown as a numeric 0–100 row in the dashboard table with the same banded cell color.

## Signal markers

Small labels in the oscillator panel with hover tooltips. Each marker is individually toggleable.

| Label | Trigger | Meaning |
|---|---|---|
| `FC` red | Setup drops below 52 without Impulse ever reaching 45, AND price falls back toward the middle of the range (25–75 %) | Failed Coil — breakout stalled, range continues |
| `NI` red | Impulse > 70, Setup drops below 40, AND ADX < 25 | Naked Impulse — move without structural backing or trend confirmation |
| `◆` green / red | Reversal score crosses 60 at a range extreme, confirmed by the trigger candle's close | Reversal — Impulse fading from its own recent high + rejection wick, weighted by Setup compression |

### Reversal

A DMI-free counter-trend signal, built from the four-stage reversal pipeline (regime veto → exhaustion → confirmation → quality):

- **Regime veto** — only active at a genuine range extreme and outside chop (`reversalActive = validSetupZone and not chopMarket`)
- **Exhaustion** — how far Impulse Pressure has faded from its own 10-bar high (only counts if that high was itself above 50)
- **Confirmation** — a rejection wick against the extreme, sized relative to the bar's range, AND the trigger candle itself must close in the reversal's direction (a big wick that closes back toward the extreme doesn't count)
- **Quality** — Setup Pressure (compression) reused as-is

The three scored components combine into one score per direction (`exhaustionScore × 0.45 + wickRatio × 0.30 + setupPressure × 0.25`), and the signal fires when that score crosses 60 on the correct side of the range with a confirming candle close (long only near the range low, short only near the range high). It never touches DMI, so it isn't exposed to the lag a DMI-based directional read would have at actual turning points.

## Dashboard table

Top-right panel (Show Table toggle, default off):

| Row | Content |
|---|---|
| Phase | Current phase, color-coded |
| Setup | Value / 100 + direction arrow (orange) |
| Impulse | Value / 100 + direction arrow (green) |
| Bias | Bullish / Bearish / Flat from configurable MA cross |
| Range Pos. | Where close sits within the N-bar high/low range (0–100 %) |
| Move Str. | Move Strength value / 100, blue-tinted by magnitude |
| Action | Plain-language read (Ignore/Chop, Watch Setup, Trend Running, Long/Short Reversal, Wait) — same priority order as the phase/signals above |

## Inputs

**Main** — Normalisation window, ATR / BB lengths, BB multiplier, Volume MA, S/R Lookback

**Bias** — MA type (EMA / RMA / SMA / WMA / HMA / JMA), Fast length (default 9), Slow length (default 21)

**Smoothing** — applied to both output curves; type (EMA / RMA / SMA / WMA / HMA / JMA) + length; JMA Phase + Power

**Signal Markers** — master toggle + individual toggle per marker

**Move Strength** — Show Columns toggle (default on)

**Debug** — "Log Reversal Context" toggle (default off): writes the full Reversal calculation (range position, chop state, Setup/Impulse, exhaustion, both wick ratios, both direction scores) to Pine Logs on every confirmed bar at a range extreme, so a specific historical bar can be inspected for why a Reversal signal did or didn't fire
