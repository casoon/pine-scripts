# Changelog

## v3.1.0 — 2026-06-11
- Fix: break/role-reversal logic, sweep scoring and retest scoring no longer depend on the label display toggles — hiding "Show Breaks/Retests/Sweeps" previously also disabled the underlying zone state and scoring
- New alerts: Zone Break Up, Zone Break Down, Zone Retest, Zone Sweep
- Performance: removed two redundant `request.security` ATR calls — the HTF ATR returned by the swing engine is reused instead

## v3.0.0
- Initial release
