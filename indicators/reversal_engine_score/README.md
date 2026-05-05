# Reversal Engine Score v1

Score-based liquidity sweep reversal detector. A signal fires only when a confirmed sweep of a prior swing high/low is accompanied by HTF trend alignment and enough evidence points to meet the configurable minimum score. The score aggregates up to 12 individual conditions, each weighted by importance.

## Features

- Score gate (0–12 pts) — signal requires sufficient evidence before firing
- Liquidity sweep detection: swing violation with recovery close on the same bar
- HTF trend filter via dual EMA (fast / slow) on any configurable timeframe
- ATR volatility filter and candle body size minimum
- Scoring across EMA slope, RSI momentum, close position, candle direction, and prior bar break
- 15M-only lockout with orange background on other timeframes
- Cooldown gate to suppress signal chasing after a recent entry
- ATR-based SL/TP levels rendered as line-break plots
- Hidden strategy-ready plots: direction, score, entry, stop, take
- Alert conditions for BUY / SELL / either

## Scoring

Each long or short signal earns points from ten conditions. Maximum possible score is 12.

| Condition | Points |
|-----------|--------|
| HTF trend aligned (bullTrend / bearTrend) | 2 |
| Liquidity sweep with recovery close | 2 |
| Momentum (EMA + RSI side) | 1 |
| Close in upper / lower third of candle range | 1 |
| ATR above baseline × factor | 1 |
| Body above ATR × factor | 1 |
| EMA slope in signal direction | 1 |
| RSI rising / falling | 1 |
| Close breaks prior bar high / low | 1 |
| Bull / bear candle | 1 |

## Recommended starting parameters

| Parameter | Default | Strict |
|-----------|---------|--------|
| Minimum Score | 7 | 8–9 |
| Sweep Lookback | 10 | 10 |
| Cooldown | 5 | 8–12 |
| SL ATR Mult | 1.2 | 1.2 |
| TP ATR Mult | 2.0 | 2.5 |
