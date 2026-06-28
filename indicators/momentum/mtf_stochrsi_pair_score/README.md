# MTF StochRSI Pair Score

Multi-timeframe StochRSI confluence scorer. Computes a per-timeframe StochRSI score (−100…+100) on six configurable timeframes, combines adjacent timeframes into weighted pairs with a sync bonus and conflict penalty, and aggregates everything into a smoothed total score. A directional Agreement Index across all six timeframes adds consensus context around the core score.

## Features

- Per-TF StochRSI score with exhaustion dampening (score reduced when K and D are both deep in the extreme zone without a fresh counter-cross)
- Pair confluence: lower/higher TF weighted blend, sync bonus when both agree, conflict penalty when they oppose
- Weighted total across up to 5 configurable TF pairs (each pair toggleable and weightable)
- Smoothed total score — EMA / RMA / SMA / WMA / HMA / JMA (default JMA)
- TF Agreement Index: directional consensus across all 6 TFs in steps of ±33.3
- Signal markers: edge-triggered Strong Long/Short with optional confirmed-bar gate and minimum-agreement filter
- Dashboard table: per-TF scores, per-pair scores (disabled pairs grayed), Agreement, Total
- Alerts: Long/Short Bias

## Scoring

Per TF (clamped to ±100):

| Component | Points |
|---|---|
| K above / below D | ±20 |
| K rising / falling | ±20 |
| Fresh K/D cross up / down | ±30 |
| Cross inside the oversold / overbought zone | additional ±30 |
| K beyond zone and still pushing | ±10 |
| Exhaustion (K and D both beyond zone, no counter-cross) | score × 0.65 |

Pair score = lower TF × minor weight + higher TF × (1 − minor weight), then × sync bonus (both same direction) or × conflict penalty (opposing), clamped to ±100. Total = weight-normalized sum of all enabled pairs.
