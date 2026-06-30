# Changelog

## v3.1.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v3.1.1 — 2026-06-29
- Alerts: messages standardized to `SRZ · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v3.1.0 — 2026-06-11
- Fix: break/role-reversal logic, sweep scoring and retest scoring no longer depend on the label display toggles — hiding "Show Breaks/Retests/Sweeps" previously also disabled the underlying zone state and scoring
- New alerts: Zone Break Up, Zone Break Down, Zone Retest, Zone Sweep
- Performance: removed two redundant `request.security` ATR calls — the HTF ATR returned by the swing engine is reused instead

## v3.0.0
- Initial release
