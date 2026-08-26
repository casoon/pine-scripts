# Changelog

## v1.0.1 — 2026-08-26
- Made dominance directionally consistent across all four pressure engines
- Confirmed exhaustion and divergence signals at bar close and moved divergence markers from the historical pivot to the actual confirmation bar
- Split exhaustion timing into independent extreme-recency and price-push windows and fixed the recency-window boundary
- Added an explicit Dual Exhaustion state, marker, and alert for bars satisfying both directions
- Added a separate Pressure Acceleration display toggle and preserved unavailable normalization values during indicator warm-up

## v1.0 — 2026-08-26
- Initial release: four pressure engines (Classic / Directional / True Range / Close-Weighted Elder), selectable consensus (EMA/RMA/SMA/WMA/HMA/VWMA) and normalization (Raw/ATR/Average Range/Percent/RMS), net/gross pressure, dominance, pressure impulse/acceleration, percentile extremes, exhaustion detection, pivot divergences, and whole-bar position vs. consensus
