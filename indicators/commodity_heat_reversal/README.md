# Commodity Heat Reversal v1

Score-based mean-reversion reversal signal indicator for commodity futures (designed for 4H). It quantifies how much evidence points to an overextended, exhausted move — distance from EMA50, ATR expansion, RSI extremes, wick pressure, and Bollinger Band breach — and fires a long or short signal when the score crosses a threshold and a bar-close confirmation triggers.

## Features

- **Dual Heat Score** — independent long and short scores (0–7 points each), built from five components
- **Score components** — ATR distance to EMA50 (2 pts), ATR expansion (2 pts), RSI extreme (1 pt), wick pressure (1 pt), BB breach (1 pt)
- **Confirmation gate** — signal requires close beyond previous bar's range or EMA9
- **Trend filter** — optional EMA200 direction filter with configurable override at extreme scores
- **SL/TP overlay** — swing-high/low stop + EMA20 mean-reversion target drawn on signal bars
- **Score dashboard** — table showing current long/short score, active signal, trend direction, RSI

## Scoring

| Component | Points | Short condition | Long condition |
|-----------|--------|-----------------|----------------|
| ATR distance | 2 | `close > ema50 + 2.5×atr14` | `close < ema50 − 2.5×atr14` |
| ATR expansion | 2 | `atr14 > atr50 × 1.5` | same |
| RSI extreme | 1 | `rsi > 72` | `rsi < 28` |
| Wick pressure | 1 | upper wick > 35% of candle range | lower wick > 35% |
| BB breach | 1 | `close > bbUpper` | `close < bbLower` |

Default threshold: 5/7. Extreme threshold (for counter-trend override): 6/7.

## Stop / Take-Profit

- **SL** — 10-bar swing high/low ± `slAtrMult × atr14` (default 1.2×)
- **TP** — EMA20 (mean reversion target); dynamic, follows price
