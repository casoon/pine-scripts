# Changelog

## v1.0.2 — 2026-10-02
- Oscillator scale no longer inherits the chart symbol's price precision (values like 80,0000 on 4-decimal symbols such as NATGAS) — shows 2 decimals

## v1.0.1 — 2026-09-05
- Added hard Exchange-only data validity gate: real trade volume is checked via `syminfo.volumetype` (`base`/`quote`), routed through a single gated `vol` variable that all Volume Force formula variants read
- On CFDs/Forex/indices (no real trade volume) the oscillator, signal line, histogram, regime engine, and divergence/event detection now go blank instead of computing on tick-count volume
- Added `Data Contract` header block (`Verdict: Exchange-only`)
- Added a one-time warning label ("benötigt echtes Handelsvolumen — aktuell: …") on the last bar when volume is not real

## v1.0.0 — 2026-08-26
- Initial release: Klinger Volume Oscillator with selectable Volume Force formula (Original 1997 / TradingView documentation / signed-volume baseline), zero-preserving normalization (Relative Force / StdDev / Raw), hysteretic regime engine (Bull/Neutral/Bear + Strong states), confirmed-pivot regular/hidden divergence with quality filter, Flow Rejection and Flow-Confirmed structure-break events, Clean/Analysis/Research visual modes, dashboard, and research diagnostics
