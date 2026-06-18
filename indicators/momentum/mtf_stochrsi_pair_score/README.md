# MTF StochRSI Pair Score

Multi-timeframe StochRSI confluence scorer. Computes a per-timeframe StochRSI score (−100…+100) on six configurable timeframes, combines adjacent timeframes into weighted pairs with a sync bonus and conflict penalty, and aggregates everything into a smoothed total score. An Agreement Index, QQE layer, Squeeze Momentum, Williams VIX Fix background, Fractal Alignment, and an Oscillator Compression detector add context around the core score.

## Features

- Per-TF StochRSI score with exhaustion dampening (score reduced when K and D are both deep in the extreme zone without a fresh counter-cross)
- Pair confluence: lower/higher TF weighted blend, sync bonus when both agree, conflict penalty when they oppose
- Weighted total across up to 5 configurable TF pairs (each pair toggleable and weightable)
- Smoothed total score — EMA / RMA / SMA / WMA / HMA / JMA (default JMA)
- TF Agreement Index: directional consensus across all 6 TFs in steps of ±33.3
- Signal markers: edge-triggered Strong Long/Short with optional confirmed-bar gate and minimum-agreement filter
- QQE Agreement Layer: weighted RSI + adaptive trailing stop per TF; optional signal gate, optional per-TF score boost/penalty, QQE divergences vs price
- Squeeze Momentum: BB-vs-KC compression state dot + LinReg momentum histogram + compression background
- Bidirectional Williams VIX Fix background: bull fear / bear greed extremes (BB band or percentile threshold)
- Breadth Discrepancy markers: Agreement Index and Total Score moving in opposite directions (delta-based, not pivot-based)
- Fractal Momentum Alignment: gradient consistency across the TF chain — 100 = all adjacent TF pairs agree, 0 = chaos
- Oscillator Compression Detector: background when the sum of absolute TF scores falls below a threshold (all TFs near zero — pressure buildup)
- Dashboard table: per-TF scores, per-pair scores (disabled pairs grayed), Agreement, Total, Alignment, Compression state
- Alerts: Long/Short Bias, Bull/Bear Breadth Discrepancy, QQE Bullish/Bearish Divergence

## Scoring

Per TF (clamped to ±100, before optional QQE weighting):

| Component | Points |
|---|---|
| K above / below D | ±20 |
| K rising / falling | ±20 |
| Fresh K/D cross up / down | ±30 |
| Cross inside the oversold / overbought zone | additional ±30 |
| K beyond zone and still pushing | ±10 |
| Exhaustion (K and D both beyond zone, no counter-cross) | score × 0.65 |

Pair score = lower TF × minor weight + higher TF × (1 − minor weight), then × sync bonus (both same direction) or × conflict penalty (opposing), clamped to ±100. Total = weight-normalized sum of all enabled pairs.

## Background priority

WVF extreme > Oscillator Compression > Squeeze ON.
