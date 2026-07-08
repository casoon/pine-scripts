# Predictability Regime Index

Classifies whether the current market rewards momentum/trend-following or mean-reversion, by fusing four statistical predictability sensors — Variance Ratio, return autocorrelation, a Hurst exponent approximation, and a fractal efficiency ratio — onto one signed −100..+100 axis. It is a context/regime read, not a trade trigger.

## Features

- Variance Ratio across three horizons (fast/medium/slow), VR > 1 = momentum tendency, VR < 1 = mean-reversion tendency
- Return autocorrelation across the same three windows (positive = momentum, negative = reversion)
- Hurst exponent approximation via range/stdev scaling (H > 0.5 = persistent, H < 0.5 = anti-persistent)
- Fractal efficiency ratio (directional path vs. noisy path)
- Composite −100..+100 Predictability Regime Index (PRI) with EMA smoothing and a signal line
- Confidence read combining distance from the random-walk centerline with sensor agreement
- Momentum / Reversion / Noise / Mixed regime classification with background zones
- Regime-shift markers on threshold crosses, alerts, and a light-theme dashboard

## Scoring

Each sensor produces a −1..+1 score (positive = momentum-favoring, negative = reversion-favoring):

| Sensor | Weight | Reads |
|---|---|---|
| Variance Ratio | 0.38 | ratio of k-period to 1-period return variance vs. the random-walk expectation |
| Autocorrelation | 0.24 | correlation of consecutive log returns |
| Hurst approximation | 0.23 | rescaled-range proxy for path persistence |
| Fractal efficiency | 0.15 | net displacement vs. total path length |

The weighted sum is scaled to −100..+100 and EMA-smoothed into the **PRI**; a further EMA of the PRI produces the **Signal** line.

## Regime classification

- **Momentum**: `PRI > 25` and `Confidence > 35`
- **Reversion**: `PRI < -25` and `Confidence > 35`
- **Noise**: `|PRI| ≤ 20` or `Confidence < 25`
- **Mixed**: everything else

**Confidence** = `|PRI| / 65 × agreement × 100`, where agreement falls as the Variance Ratio, autocorrelation, and Hurst scores disagree with each other — a high PRI reading with sensors in conflict is down-weighted.
