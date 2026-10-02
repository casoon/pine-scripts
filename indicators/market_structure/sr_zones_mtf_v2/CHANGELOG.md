# Changelog

## v3.2.0 — 2026-10-02
- Break bonus now has a failure path: if price closes back on the old side of the broken zone edge within *Break Failure Window* bars (new input, default 5 — provisional), the break's score bonus is subtracted again. Role reversal and break/retest labels are unchanged

## v3.1.4 — 2026-10-02
- Fixed: a sweep bar was also counted as a test (touch counter +1, wick bonus added twice, extra "T" label). A wick beyond the zone that closes back inside now scores as a sweep only

## v3.1.3 — 2026-09-06
- Break volume filter now checks `syminfo.volumetype` and passes breaks through on feeds without real trade volume, instead of filtering against tick-volume noise
- Added a chart note for the case where the filter is enabled but cannot work
- Added the Data Contract header block

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
