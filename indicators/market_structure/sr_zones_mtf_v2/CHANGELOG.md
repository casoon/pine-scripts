# Changelog

## v3.2.1 — 2026-10-12
- Fix: compile error CE10163 ("Ternary operations cannot return tuples") on the optional HTF 2 request — the request now runs unconditionally and its values are masked when HTF 2 is off
- Fix: compile error CE10235 (if/else branches with different return types) in zone add/merge — the max-zones cleanup now runs after the branch; behaviour unchanged
- Fix: runtime error RE10045 on bar 0 ("array.get() index 0 out of bounds") — in Pine v6 `for i = 0 to n - 1` counts down when n is 0; all loops over the zone arrays are now skipped when the arrays are empty
- Without real volume, the "break volume filter inactive" notice is now a short "volume not available" note in the bottom-right corner instead of a label on the last candle
- Volume check fixed: only `tick` volume is rejected; `n/a` counts when the feed actually delivers volume. Most non-crypto feeds report `n/a`, so the old `base`/`quote` check treated futures and stocks with real volume (e.g. EUREX:FDAX1!) as volume-less — volume-based parts are active there again, which can change scores, gates and signals on those markets

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
