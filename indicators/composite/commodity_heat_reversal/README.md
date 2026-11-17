# Commodity Heat Reversal v1.7.0

Mean-reversion reversal and pullback-continuation signal indicator for commodity futures (designed for 4H). It checks for an overextended, exhausted move — RSI extreme or Bollinger Band breach, a rejection wick, and stretch from MA50 or ATR expansion — and fires a long or short signal when all of them are present and a bar-close confirmation triggers.

The indicator also tracks an optional higher-timeframe EMA bias. When a heat setup happens as a pullback inside the higher-timeframe trend, it can mark a separate `PB` continuation signal instead of treating the move only as a local reversal.

## Features

- **Reversal heat** — ATR distance to MA50 and ATR expansion (0–2), required on top of the exhaustion and wick-rejection gates
- **Pullback heat** — explicit condition for the pullback-continuation gate: RSI reset
- **Confirmation gate** — signal requires close beyond previous bar's range or MA9
- **Quality gate** — selectable Early / Balanced / Strict confirmation plus same-direction cooldown
- **Countertrend handling** — show, mark, or hide weak non-extreme countertrend reversals
- **Trend filter** — optional MA200 direction filter with configurable override at extreme reversal heat
- **HTF bias** — optional higher-timeframe EMA direction and slope context
- **Pullback continuation** — optional diamond signals when a heat pullback resolves back in aligned local/HTF trend
- **Selectable MA smoothing** — EMA / RMA / SMA / WMA / HMA / JMA (default HMA) for all MAs
- **SL/TP overlay** — swing-high/low stop + MA20 mean-reversion target drawn on signal bars
- **Dashboard** — table showing whether long/short pullback heat is present (`PB Heat`, Yes / –), active signal, trend direction, HTF bias, RSI
- **Alerts** — alert conditions for reversal, pullback-continuation, and any signal

## Reversal gates

Reversal signals require the exhaustion gate (RSI > 72 / < 28 or a close outside the 2σ Bollinger Band) and the wick-rejection gate (rejection wick > 35% of the candle range), plus **reversal heat** from the two stretch components that are not gates: ATR distance to MA50 (`close` beyond `ma50 ± 2.5×atr14`) and ATR expansion (`atr14 > atr50 × 1.5`), 0–2. Default reversal heat threshold: 1 (distance or expansion). Extreme threshold (for counter-trend override): 2 (both).

## Pullback heat

The pullback-continuation gate uses an explicit condition:

| Side | Condition |
|------|-----------|
| Long | `rsi < 45` |
| Short | `rsi > 55` |

The setup already requires price on the trend side of the MA50 and a touch of the MA20/MA50, so a stretch condition against the MA50 could never hold there; RSI reset is the only heat condition. The `PB Heat` column of the dashboard shows whether the condition holds on the current bar.

## Quality Gate

A reversal is counter-trend when a long fires below a flat-or-falling MA50 or a short above a flat-or-rising MA50. Counter-trend reversal signals use `Balanced` confirmation by default:

- **Early** — original confirmation: close beyond prior bar or MA9
- **Balanced** — close beyond MA9 plus prior-bar break or wick pressure
- **Strict** — candle direction, MA9 reclaim/loss, prior-bar break, and wick pressure

Default same-direction cooldown: 3 bars.

Weak countertrend reversals can be displayed in three modes:

- **Show** — plot them as normal reversal triangles
- **Mark** — plot them as small x markers instead of normal signals
- **Hide** — suppress them unless reversal heat reaches the Extreme Heat Threshold, so a counter-trend reversal effectively needs the extreme threshold instead of the normal one. This is the default.

## Pullback Continuation

Continuation signals are separate from the original reversal signals:

- **Long PB** — MA20 above rising MA50, HTF up bias, recent MA20/MA50 pullback with pullback heat, then bullish close above MA9 / prior high
- **Short PB** — MA20 below falling MA50, HTF down bias, recent MA20/MA50 pullback with pullback heat, then bearish close below MA9 / prior low

Default lookback: 12 bars. Default PB cooldown: 8 bars.

## Stop / Take-Profit

- **SL** — 10-bar swing high/low ± `slAtrMult × atr14` (default 1.2×)
- **TP** — MA20 (mean reversion target); dynamic, follows price
