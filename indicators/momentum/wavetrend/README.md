# WaveTrend [WavesUnchained]

WaveTrend momentum oscillator with configurable cross signals, divergence detection, and an optional price-chart overlay. Four optional extensions address overextension, signal quality, wave persistence, and wave anatomy.

## Features

- Configurable cross signals: Strong (extreme zones only), All, or None
- Divergence detection — regular and hidden, bullish and bearish
- Optional price-chart overlay with Top / Middle / Bottom placement (off by default)
- Optional Compare Symbol — intermarket WaveTrend zone as a dashboard row (off by default)
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

## Chart Overlay (optional)

Projects `wtOsc`, `wtSig`, and the histogram directly onto the price panel — the classic on-chart WaveTrend visual, ported and bug-fixed rather than just documented. Off by default; purely cosmetic, reads the same `wtOsc`/`wtSig` series used for signals but has no effect on them.

- **Placement** — Top (above price), Middle (overlaps price), Bottom (below price)
- **Height** — vertical size of the projection relative to the visible price range
- **Vertical Offset** — Top/Bottom only, distance from price
- **Display Length** — bars drawn (capped at 200, not the source's 250, to leave headroom under the shared 500-line budget alongside divergence lines)
- **Highlight** — fills the area between oscillator and signal lines with the leading-side color

Redrawn only on `barstate.islast` via a delete-and-rebuild array pattern (`line`/`box`/`linefill`), matching the source's performance approach.

## Compare Symbol (optional)

Reports the WaveTrend zone (OB / OS / Bull / Bear) of a second symbol (default `BINANCE:BTCUSDT`) as a dashboard row. Off by default, informational only — does not gate or filter signals.

Deliberately not a port of the source's "Compare Symbol" feature: that duplicates the full WT engine and draws a second, parallel set of cross labels on the chart. This reuses the existing `f_getWtOscHTF` helper (already built for the HTF Trend Filter, computing wtOsc only) against a different symbol instead of a different timeframe, and surfaces the result as one dashboard cell — no duplicated engine, no extra chart clutter.

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
| Compare | Optional: WaveTrend zone of a second symbol (OB / OS / Bull / Bear) |

## Bug Fixes vs. Source

- `crossState` and `divState` moved to top-level scope so `[1]` references carry correctly across real-time bars (were previously inside `if barstate.islast`, resetting each bar)
- `divState` changed to `float` so the `× 0.8` decay actually reduces the value (integer `math.round` was freezing at 2)
- Histogram in **Middle** overlay mode now uses the zero-line level as its baseline instead of the bottom price edge, aligning histogram bars with the projected oscillator instead of floating disconnected from it
- Dropped the source's unused `f_drawOnlyLabelX` wrapper and its three color themes — this file's own cross-signal label styling and `colorOsc`/`colorSignal` palette already cover that, so the overlay just reuses them instead of adding a second, redundant color system
- Overlay inputs use an `overlay*` prefix (`overlayPlacement`, `overlayHeight`, ...) instead of the source's bare `osc*`/`color*` names, which collided with this file's own `wtOsc`/`colorOsc` engine variables
