# Changelog

## v1.0.1 — 2026-10-02
- Oscillator scale no longer inherits the chart symbol's price precision (values like 80,0000 on 4-decimal symbols such as NATGAS) — shows 2 decimals

## v1.0 — 2026-07-04
- Initial release: seven-state regime classifier (Noise/Compression/Expansion/Trend Up/Trend Down/Exhaustion/Reversion) with dwell + hysteresis debouncing
- Directional Transition Pressure oscillator
- State-change events (Compression→Expansion, Expansion→Trend, Trend→Exhaustion, Exhaustion→Reversion)
- Dashboard with state, next-bias, transition %, state age, VolPct, Efficiency, Variance Ratio
- Alerts for each state-change event plus a general state-change alert, gated by bar-close confirmation
