# Changelog

## v1.1.2 — 2026-09-05
- Fix: OB volume bonus (relative-volume score tiers) and the optional "Require Volume > SMA(20)" filter used raw `volume` with no check on `syminfo.volumetype` — on CFD feeds with tick volume, this scored/gated order blocks against a meaningless tick count. Added a `volumeIsReal` guard (`base`/`quote` only); the score bonus now degrades to +0 (na) instead of a fabricated tier, and the volume filter passes through neutrally instead of blocking OB creation when volume isn't real
- Added a one-time chart label on the last bar when volume isn't real, so the degradation is visible instead of silent
- Data Contract header block added (`Volume: OPTIONAL`, `Verdict: CFD-degraded`)

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
