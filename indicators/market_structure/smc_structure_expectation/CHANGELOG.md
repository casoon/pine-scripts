# Changelog

## v1.1.1 — 2026-06-29
- Alerts: messages standardized to `SMCE · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.1.0 — 2026-06-11
- Fix: displacement window input ("Displacement Lookback" / auto-adjust window) is now actually used — displacement was previously hardcoded to a 3-bar window regardless of settings
- Fix: BOS cross detection (`ta.crossover`/`ta.crossunder`) and Layer-4 swing-break crosses moved to global scope — calling them inside conditional branches builds inconsistent history and could miss or fake cross events after a BOS level was consumed
- Fix: expectation zone now uses a single tracked box instead of creating a new box every bar (stacked transparency, box-limit churn)
- Dashboard and OB rejection heatmap converted to the standard light-theme table style
- Removed dead code: unused `medianRange` series and write-only `legHigh`/`legLow` state

## v1.0.0
- Initial release
