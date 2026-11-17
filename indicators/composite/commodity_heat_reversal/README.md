# Commodity Heat Reversal v1.4.3

Mean-reversion reversal and pullback-continuation signal indicator for commodity futures (designed for 4H). It checks for an overextended, exhausted move — RSI extreme or Bollinger Band breach, a rejection wick, and stretch from MA50 or ATR expansion — and fires a long or short signal when all of them are present and a bar-close confirmation triggers.

The indicator also tracks an optional higher-timeframe EMA bias. When a heat setup happens as a pullback inside the higher-timeframe trend, it can mark a separate `PB` continuation signal instead of treating the move only as a local reversal.

## Features

- **Reversal heat** — ATR distance to MA50 and ATR expansion (0–2), required on top of the exhaustion and wick-rejection gates
- **Pullback heat score** — long and short points (0–7) from ATR distance (2), ATR expansion (2), RSI extreme (1), wick pressure (1), BB breach (1); used only by the pullback-continuation gate
- **Confirmation gate** — signal requires close beyond previous bar's range or MA9
- **Quality gate** — selectable Early / Balanced / Strict confirmation plus same-direction cooldown
- **Countertrend handling** — show, mark, or hide weak non-extreme countertrend reversals
- **Trend filter** — optional MA200 direction filter with configurable override at extreme reversal heat
- **HTF bias** — optional higher-timeframe EMA direction and slope context
- **Pullback continuation** — optional diamond signals when a heat pullback resolves back in aligned local/HTF trend
- **Selectable MA smoothing** — EMA / RMA / SMA / WMA / HMA / JMA (default HMA) for all MAs
- **SL/TP overlay** — swing-high/low stop + MA20 mean-reversion target drawn on signal bars
- **Dashboard** — table showing the current long/short pullback heat (`PB Heat`, x / 7), active signal, trend direction, HTF bias, RSI
- **Alerts** — alert conditions for reversal, pullback-continuation, and any signal

## Pullback heat score

| Component | Points | Short condition | Long condition |
|-----------|--------|-----------------|----------------|
| ATR distance | 2 | `close > ma50 + 2.5×atr14` | `close < ma50 − 2.5×atr14` |
| ATR expansion | 2 | `atr14 > atr50 × 1.5` | same |
| RSI extreme | 1 | `rsi > 72` | `rsi < 28` |
| Wick pressure | 1 | upper wick > 35% of candle range | lower wick > 35% |
| BB breach | 1 | `close > bbUpper` | `close < bbLower` |

Reversal signals require the exhaustion gate (RSI extreme or BB breach) and the wick-rejection gate, plus **reversal heat** from the two stretch components that are not gates: ATR distance to MA50 and ATR expansion (0–2). Default reversal heat threshold: 1 (distance or expansion). Extreme threshold (for counter-trend override): 2 (both). The 0–7 pullback heat score above does not enter the reversal signal; it feeds the pullback-continuation gate and the `PB Heat` column of the dashboard.

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

- **Long PB** — MA20 above rising MA50, HTF up bias, recent MA20/MA50 pullback with heat or RSI reset, then bullish close above MA9 / prior high
- **Short PB** — MA20 below falling MA50, HTF down bias, recent MA20/MA50 pullback with heat or RSI reset, then bearish close below MA9 / prior low

Default pullback heat threshold: 2/7. Default lookback: 12 bars. Default PB cooldown: 8 bars.

## Stop / Take-Profit

- **SL** — 10-bar swing high/low ± `slAtrMult × atr14` (default 1.2×)
- **TP** — MA20 (mean reversion target); dynamic, follows price
