# Changelog

## v2.3.5 — 2026-09-06
- Volume validity is now decided by `syminfo.volumetype`. Every Wyckoff entry pattern required `relVolume` above 1.3–1.5; on feeds without real trade volume those comparisons could never be true, so Spring, Upthrust and the Wyckoff spring entry silently stopped firing
- Confirming thresholds (entry patterns, secondary tests, SOS/SOW breakouts) now pass through when trade volume is unavailable
- Climax and absorption events are withheld in that case rather than approximated
- Shock-bar detection is explicitly tied to volume availability (behaviour unchanged, intent now stated)
- Added a chart note and the Data Contract header block

## v2.3.3 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v2.3.2 — 2026-06-29
- Alerts: messages standardized to `JMAS · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v2.3.1 — 2026-06-11
- Fixed: 3-bar timeout for armed pattern signals (Spring, Upthrust, Wyckoff Spring/UT, Exhaustion) never fired — armed signals persisted until a confirmation eventually triggered, producing late entries. Signals now reset 3 bars after the pattern bar as documented.
- Fixed: bullish Break-of-Structure check guarded with the wrong swing variables (no functional crash, but inconsistent na-handling).
- Performance: removed duplicate standard-deviation calculation for the reversion zone.

## v2.3.0
- Initial release
