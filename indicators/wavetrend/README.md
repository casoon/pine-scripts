# WaveTrend [WavesUnchained]

WaveTrend momentum oscillator with configurable cross signals, divergence detection, intermarket comparison, and a price-chart overlay. Four optional extensions address overextension, signal quality, wave persistence, and wave anatomy.

## Features

- Configurable cross signals: Strong (extreme zones only), All, or None
- Divergence detection — regular and hidden, bullish and bearish
- Compare symbol mode for intermarket correlation (e.g. BTC vs ALT)
- Price-chart overlay with Top / Middle / Bottom placement and three color themes
- Analytics dashboard with composite bias score
- Extension A — Overextension duration
- Extension B — Slope quality filter
- Extension C — Zone persistence
- Extension D — Wave anatomy

## Core Engine

The oscillator is a standard WaveTrend calculation:

```
esa    = EMA(hlc3, channelLength)
d      = EMA(|hlc3 − esa|, channelLength)
ci     = (hlc3 − esa) / (0.015 × d)
wtOsc  = EMA(ci, avgLength)
wtSig  = SMA(wtOsc, sigLength)
```

Cross signals fire when `wtOsc` crosses `wtSig`. Signal strength is classified by the oscillator's position relative to the band thresholds:

| Signal | Condition |
|--------|-----------|
| Strong | Cross inside OB/OS extreme zone |
| Regular | Cross between zero and the threshold |
| Weak | Cross above/below zero (mid-zone) |

## Extensions

### A — Overextension Duration

Tracks consecutive bars inside the OB or OS zone. When the count meets the configured threshold, **weak and regular crosses are suppressed** to avoid chasing whipsaw exits during a sustained trend. Strong crosses (deep in the extreme zone) are never suppressed. The bar count and suppression state are shown in the dashboard row "Ext. Duration" (⚑ marks an active suppression).

### B — Slope Quality Filter

Measures the rate of change of `wtOsc` over a configurable lookback (`slopeLen` bars). A flattening slope inside an OB/OS zone indicates exhaustion and strengthens the case for a reversal. A still-rising slope in OB suggests the trend is extending, not reversing. Slope context is appended to strong cross tooltips and shown in the "Slope" dashboard row.

### C — Zone Persistence

Counts consecutive bars with `wtOsc` above or below zero. When the count reaches the configured minimum, a "Sustained Bull / Bear" signal is shown in the dashboard. This identifies wave-riding conditions where counter-trend signals should be discounted.

### D — Wave Anatomy

Three metrics that describe where a wave is in its lifecycle, independent of timeframe:

**Percentile** — `ta.percentrank(wtOsc, N)` gives the oscillator's position within its own recent distribution (0–100). A value at 90% means the oscillator is near its highest level in the last N bars — historically extreme, regardless of whether it has crossed a fixed band. This makes "how much room is left" measurable.

**Wave Structure** — detects pivot highs and lows in `wtOsc` itself (not price) and compares consecutive peaks and troughs. Rising peaks + rising troughs = wave accelerating. Falling peaks = wave fading even if still in OB territory. This tells you whether the current wave is strengthening or losing steam.

**Correction** — measures how far the current `wtOsc` value has dropped from the last confirmed oscillator peak, expressed as a percentage of the full wave amplitude (trough-to-peak range). Values:
- 0% = currently at the peak (wave intact)
- < threshold = sub-wave, pullback within the trend
- ≥ threshold (⚑) = correction is deep, wave may be ending
- ≥ 100% = wave fully retraced, structure broken

Only valid when the last trough preceded the last peak (a complete trough → peak cycle has formed). Shows `—` otherwise.

## Dashboard

| Row | Description |
|-----|-------------|
| Oscillator | Raw `wtOsc` value |
| Signal | `wtSig` value |
| Zone | Overbought / Oversold / Bullish / Bearish |
| Momentum | Slope direction × oscillator/signal alignment |
| Cross | Latest cross direction with decaying state |
| Divergence | Regular / hidden bullish or bearish |
| Regime | Bull Trend / Bear Trend / Transition (spread-based) |
| Extreme | OB/OS warning |
| Ext. Duration | Extension A: bars in zone + suppression flag |
| Slope | Extension B: oscillator velocity |
| Sustained | Extension C: bars above/below zero |
| Percentile | Extension D: oscillator percentile rank in recent history |
| Wave | Extension D: peak/trough structure (accelerating / fading) |
| Correction | Extension D: pullback depth as % of last wave amplitude |
| Bias | Composite score across all dimensions (with confidence %) |

## Bug Fixes vs. Source

- `crossState` and `divState` moved to top-level scope so `[1]` references carry correctly across real-time bars (were previously inside `if barstate.islast`, resetting each bar)
- `divState` changed to `float` so the `× 0.8` decay actually reduces the value (integer `math.round` was freezing at 2)
- Histogram in **Middle** overlay mode now uses `midLevel` as its baseline instead of `priceLowest`, aligning histogram bars with the zero line
- Removed unnecessary `f_drawOnlyLabelX` wrapper function
- Renamed `oscHight` input to `oscHeight`
