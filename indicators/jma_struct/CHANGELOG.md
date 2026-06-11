# Changelog

## v2.3.1 — 2026-06-11
- Fixed: 3-bar timeout for armed pattern signals (Spring, Upthrust, Wyckoff Spring/UT, Exhaustion) never fired — armed signals persisted until a confirmation eventually triggered, producing late entries. Signals now reset 3 bars after the pattern bar as documented.
- Fixed: bullish Break-of-Structure check guarded with the wrong swing variables (no functional crash, but inconsistent na-handling).
- Performance: removed duplicate standard-deviation calculation for the reversion zone.

## v2.3.0
- Initial release
