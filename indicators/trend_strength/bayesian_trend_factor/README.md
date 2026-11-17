# Bayesian Trend Factor

Bayesian Trend Factor is a Bayesian-inspired probabilistic **trend-quality filter** that maps the current directional thesis to a signed `-100..+100` score and a separate `0..100` confidence reading. It answers one question first: *is the active trend context clean enough to trust, and in which direction?*

The model fuses directional evidence blocks into log-odds: regression direction, gated trend strength and exhaustion risk. Volatility is kept out of direction and acts as a quality multiplier. Confidence measures whether the evidence quality is high enough for the factor to matter. Optional modules add Pullback / Continuation triggers and HAMA-style smoothed trend candles.

## Evidence blocks

| Block | What it measures | Role |
|---|---|---|
| Direction | Linear-regression slope normalized by ATR | Primary directional thesis |
| Strength | ADX, Kaufman Efficiency Ratio and Regression R2 | Confirms whether movement is clean and persistent |
| Volatility | ATR percentile in an optimal regime zone | Quality multiplier only, never directional evidence |
| Exhaustion | Overextension plus rejection or momentum fade | Penalizes late or rejected trend moves |

## Interpretation

| Factor | Read |
|---|---|
| `+80..+100` | Strong bullish trend |
| `+55..+79` | Bullish trend active |
| `-54..+54` | Neutral, transition or low-quality trend |
| `-55..-79` | Bearish trend active |
| `-80..-100` | Strong bearish trend |

The confidence gate soft-neutralizes the factor when evidence quality is below the configured minimum. Trend state uses hysteresis: it activates at `Trend Threshold` and exits at `Trend Exit Threshold`, so the state does not flicker around the main threshold. A high positive or negative factor with low confidence should be treated as unfinished context, not a signal.

## Features

- Signed `-100..+100` Bayesian Trend Factor plus `0..100` Confidence
- Four evidence blocks (three weighted in log-odds, volatility as multiplier) with exposed role weights
- Volatility kept out of directional log-odds and applied only as a quality multiplier
- Strength evidence gated until regression direction is meaningful
- Exhaustion is a malus only; low exhaustion no longer adds confidence by itself
- Optional short factor smoothing to reduce state flicker
- Trend-state hysteresis via separate activation and exit thresholds
- Final Bull/Bear evidence score derived from the smoothed factor, with raw evidence score still exposed for diagnostics
- Confidence gate that scales down low-quality directional reads
- Fair Path regression line plus optional `+/-2 ATR` bands
- Candle coloring by trend state and optional score labels on threshold/large-score changes
- Optional Pullback / Continuation module with PB setup labels and continuation trigger labels (`RECLAIM` / `BOS` / `REJECT`), both with hover explanations
- Optional HAMA-style smoothed overlay candles with BTF-gradient coloring and visible wick/border styling
- Dashboard with factor, state, confidence, bull evidence score and key evidence scores
- Alerts for bull/bear activation, strong trend states, neutral transition, pullback setups and continuation triggers

## Trend Candles

The Trend Candles module draws a second, smoothed candle layer with `plotcandle()` and is enabled by default. It is a visual layer, not an input to the BTF or continuation logic.

| Synthetic value | Default source |
|---|---|
| Open | MA of `(open[1] + close[1]) / 2` |
| High | EMA of `max(high, close)`, clamped above smoothed open/close |
| Low | EMA of `min(low, close)`, clamped below smoothed open/close |
| Close | MA of `ohlc4` |

Color modes:

- **BTF Gradient** — candle color follows the signed BTF score: weak/strong bull, neutral, weak/strong bear.
- **Smoothed Candle Direction** — candle color follows the smoothed candle body direction, with the MA line using an advance/decline gradient.

Use `Hide Native Candle Coloring` if you want the chart's real candles to keep their default appearance while the smoothed overlay carries the trend read. The smoothed candles keep lightly transparent wicks/borders so candle range information remains visible.

## Pullback / Continuation module

The continuation layer is gated by BTF direction and confidence. It does not create its own trend bias. It runs as an explicit per-direction state machine — **Idle → Armed → Mature → Triggered / Invalidated** — so every continuation can be attributed to the stage it came from (exposed in the Data Window and dashboard).

1. **Trend gate** — BTF must be in a bull or bear trend, confidence must clear the configured minimum, and exhaustion must not be extreme.
2. **Armed (`PB`)** — price comes from above/below the Pullback EMA and Fair Path, then re-enters the stricter pullback zone. Depth is measured from the impulse high/low; a touch that is already deeper than `Max Pullback Depth (ATR)` does not arm, and no `PB` label or alert appears when the pullback is invalidated on its start bar.
3. **Mature** — the pullback is now old enough (`Min Pullback Bars`) and its depth lies between `Min Pullback Depth (ATR)` and `Max Pullback Depth (ATR)`. Only a mature pullback can accept a continuation trigger; shallow pullbacks stay Armed.
4. **Validity checks** — price must hold the last confirmed swing level (`lastLow` in bull trends, `lastHigh` in bear trends) and pullback depth stays inside the configured ATR range. A close through that swing level, a pullback deeper than `Max Pullback Depth (ATR)`, a timeout, or loss of the trend gate moves the state to **Invalidated**.
5. **Triggered** — fires when a mature pullback reclaims the Pullback EMA (`RECLAIM`), breaks the prior bar in trend direction (`BOS`), or prints a rejection wick from the pullback zone (`REJECT`).

The `PB` and trigger labels include hover tooltips with the setup context, trigger reason, factor, confidence, pullback depth and exhaustion.

## Notes

- The base script is a trend-quality filter; the optional continuation layer is the only entry-style component.
- The swing level uses confirmed pivots (`Swing Level Pivot Length`). It is only the level a pullback must hold; it is not part of the Trend Factor.
- Volatility confirms whether the environment is suitable, but does not create or strengthen a bullish/bearish view by itself.
- Exhaustion is intentionally a penalty against the active direction; positive acceleration alone is not treated as exhaustion.
