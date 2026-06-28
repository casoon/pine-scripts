## v1.0 — 2026-06-28
- Initial release — 4-sensor trend-persistence oscillator (Regression R², Kaufman Efficiency Ratio, ADX strength+slope, Fractal Dimension) on a 0–100 axis
- State read (Strong / Healthy / Transition / Weak / Dead) with one-band hysteresis
- Calibration anchors (ADX range/trend, FDI trend/range) and state levels exposed as inputs
- ADX damping — when both structure sensors (R², ER) are weak, the ADX sub-score is multiplied down so raw movement cannot prop up a dead-structure score (threshold + factor as inputs)
- Transition Risk readout — derived inverse of TPS (0.7·(100−TPS) + 0.3·(100−ER)); display + alert only, not a structure-break detector
- Two-dimensional oscillator colouring (`Direction × Strength` default): line/heat-column coloured by trend direction (corr sign), saturation scaled by strength; `Persistence State` mode keeps the classic band colours
- Directional context (▲/▼/•) from regression sign — visual only, not scored; flat read distinguishes measured Compression (Bollinger-width percentile rank) from plain Flat
- Optional light-theme dashboard (default **off**: summary block TPS / State / Transition Risk / FDI Score / Bias, then sensor breakdown), per-sensor lines (default off), debug log on state change, and Weakening / Transition / Recovery / Transition-Risk-High alerts
