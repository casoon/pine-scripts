# MTF StochRSI Pair Score

Multi-timeframe StochRSI confluence scorer. Computes a per-timeframe StochRSI score (−100…+100) on six configurable timeframes, combines adjacent timeframes into weighted pairs with a sync bonus and conflict penalty, and aggregates everything into a smoothed total score. A Bias / Quality / Timing state engine turns the score, the TF Agreement Index, and the per-TF exhaustion state into a single-glance readout instead of requiring the viewer to interpret multiple lines and a raw table.

## Features

- Per-TF StochRSI score with exhaustion dampening (score reduced when K and D are both deep in the extreme zone without a fresh counter-cross)
- Pair confluence: lower/higher TF weighted blend, sync bonus when both agree, conflict penalty when they oppose
- Weighted total across up to 5 configurable TF pairs (each pair toggleable and weightable)
- Smoothed total score — EMA / RMA / SMA / WMA / HMA / JMA (default JMA)
- TF Agreement Index: directional consensus across all 6 TFs in steps of ±33.3
- Bias / Quality / Timing state engine — a single dashboard readout derived from the scores above (see below)
- Signal markers: threshold-crossing Long/Short (fires on entry into the zone) with optional confirmed-bar gate and minimum-agreement filter
- Dashboard table: Bias/Quality/Timing state block by default; per-TF and per-pair breakdown behind a "Show Debug Table" toggle
- Alerts: Long/Short Bias

## State Engine

The state engine is a pure readout — it does not add gates or change what the Long/Short signal markers or alerts fire on. It reformats the existing scores into three independent readings:

| Dimension | States | Derived from |
|---|---|---|
| **Bias** | LONG/SHORT CONFIRMED, LONG/SHORT BUILDING, CONFLICT, NO EDGE | Total score vs. Strong Long/Short Level and Agreement vs. Min Agreement; CONFLICT when the score and the TF Agreement Index point opposite ways |
| **Quality** | CLEAN (≥66% agreement), MIXED (≥33%), WEAK (<33%) | TF Agreement Index |
| **Timing** | FRESH (within the Fresh Window of the confirmed cross), ACTIVE, LATE (majority of TFs already past the Upper/Lower Zone in the bias direction) | `barssince` on the Long/Short trigger and the per-TF K exhaustion count |

## Scoring

Per TF (clamped to ±100):

| Component | Points |
|---|---|
| K above / below D | ±20 |
| K rising / falling | ±20 |
| K/D distance (continuous) | (k − d) × 0.5 |
| K momentum (continuous) | (k − k[1]) × 0.8 |
| Fresh K/D cross up / down | ±15 |
| Cross inside the oversold / overbought zone | additional ±30 |
| K beyond zone and still pushing | ±10 |
| Exhaustion (K and D both beyond zone, no counter-cross) | score × 0.65 |

Pair score = lower TF × minor weight + higher TF × (1 − minor weight), then × sync bonus (both same direction) or × conflict penalty (opposing), clamped to ±100. Total = weight-normalized sum of all enabled pairs.
