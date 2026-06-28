# Trend Persistence Score

A single-role **trend-strength** oscillator that grades how *persistent, clean and durable* the current trend is on one continuous 0–100 axis. It fuses four trend-efficiency sensors — **Regression R²**, **Kaufman Efficiency Ratio**, **ADX strength + slope**, and a **Fractal Dimension Index** — each measuring the same property (how directly price travels vs. how much it chops). The score answers one question only: *"how strong is the trend right now?"* It is **direction-agnostic** by design — the magnitude is the signal; direction is shown as visual context, never mixed into the score.

This sits alongside [`regime_classifier`](../regime_classifier/) as the *graded-magnitude* complement: `regime_classifier` produces a categorical Trend / Range / Chaos *permission* gate for the reversal pipeline, while TPS produces a continuous *how-strong* reading you can plot, threshold and alert on.

## Features

- Four trend-efficiency sensors on one comparable 0–100 persistence axis
- Role-level **sensor weights** (R² 40 · ER 25 · ADX 20 · FDI 15 by default) plus per-sensor lines so you can see *which* sensor drives the verdict
- **State** read — Strong / Healthy / Transition / Weak / Dead — with one-band **hysteresis** so it does not flip on score noise
- **ADX damping** — ADX measures movement, not directional cleanliness; when both structure sensors (R², ER) are weak, its sub-score is damped so raw activity cannot rescue a dead-structure score
- **Transition Risk** readout — a derived inverse of TPS for "how likely is the trend to break down" (display + alert only, not a structure-break detector)
- **Calibration anchors** (ADX range/trend, FDI trend/range, damp threshold/factor) exposed as inputs — no hardcoded thresholds buried in the signal logic
- **Two-dimensional oscillator read** (default `Direction × Strength`): the line **height** is persistence, its **colour** is direction (green = up-efficiency, red = down, grey = no clear direction, from the regression sign), and its **saturation** scales with strength (vivid in a clean trend, pale in a dead market) — plus an optional **heat column** fill to zero. A strong green column = clean uptrend; a fading green column = uptrend losing power; a shift to red = down-structure forming. Direction stays *visual only*, never fed into the score. Switch to `Persistence State` mode for the classic band colours.
- **Directional context** (▲ Up / ▼ Down / • Flat / • Compress) also in the table — the flat read distinguishes measured **Compression** (Bollinger-width percentile rank) from plain Flat
- Optional light-theme dashboard (default **off**) and a **debug log** on every state change (records which sensor drove the move)
- Weakening / Transition / Recovery / Transition-Risk-High **alerts**

## Sensors

| Sensor | Formula | Reads | Strong-trend reading |
|---|---|---|---|
| **Regression R²** | `correlation(src, bar_index, n)²` | fit of price to a straight line | high R² |
| **Efficiency Ratio** (Kaufman) | `\|Δsrc(n)\| / Σ\|Δsrc\|` | how directly price travelled | high ER |
| **ADX strength + slope** | `ta.dmi` ADX mapped + 3-bar slope | trend strength and whether it is building | high & rising ADX |
| **Fractal Dimension** | `log(pathLength / range) / log(n) + 1` | path roughness (≈1 clean … ≈2 noisy) | low FDI |

Each sensor is mapped to a 0–100 sub-score via its own calibration anchors, then combined by the role-level weights into the composite. Because the four sensors measure correlated facets of the same property, the score is an intentional **robustness ensemble** — no single sensor can dominate or veto the reading.

## Score and state

1. **TPS** = weighted mean of the four sub-scores, EMA-smoothed by `Score Smoothing`.
2. **State** is read from `State Levels`: `≥ Strong` → Trend Strong; `≥ Healthy` → Trend Healthy; `≥ Transition` → Transition; `≥ Weak` → Weak / Range; below → Trend Dead. Upgrades apply immediately; downgrades require a 3-point overshoot below the band edge (hysteresis).

## How to use

- **Trend-following filter:** only take trend entries while TPS is in Healthy/Strong; stand aside in Transition/Dead.
- **Reversal context:** a high score rolling over (Strong → Transition) flags a maturing trend; a Dead reading marks range conditions where mean-reversion logic is more appropriate.
- **Attribution:** when the score disagrees with your read, the sub-score lines and the dashboard show exactly which sensor is responsible.

## Notes

- Direction-agnostic on purpose — pair it with a Trend-direction module if you need a directional bias; the Bias cell is a convenience read only.
- Default `Main Length` 34 suits swing timeframes; shorten for intraday, lengthen for higher timeframes.
