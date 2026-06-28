# Changelog

## v1.3 — 2026-06-28
- Reset stuck Accumulation/Distribution back to Neutral when the trading-range context is lost or the phase dwells past a configurable bar cap, so the state machine no longer freezes in Phase B indefinitely.
- Refresh the locked range while still building cause (Phase A/B) so the phase zone tracks current structure; it freezes once a Spring/UTAD advances to Phase C.
- Increase active phase-zone fill visibility (transparency 88 → 80).

## v1.2 — 2026-06-28
- Rename script title to Modern Wyckoff State Machine Lite to distinguish it from the full `wyckoff_schematics` engine.
- Add Spring/UTAD quality grading using sweep depth, wick ratio, candle ATR and relative volume.
- Add stored Spring/UTAD test logic: tests now reference the event price and require lower relative volume than the event.
- Make LPS/LPSY pivot-confirmed with pivot-bar volume checks and labels anchored on the pivot bar.
- Add hover breakdowns for Spring/UTAD quality, Spring/UTAD tests and pivot-confirmed LPS/LPSY labels.

## v1.1 — 2026-06-28
- Lock the active trading range after state start so events and Phase E breakouts are judged against a fixed Wyckoff range.
- Add event cooldowns for SC/BC, Spring/UTAD, Test, SOS/SOW and LPS/LPSY labels and alerts.
- Add Cause Score for Phase B using compression, dwell, swing presence, volume dry-up and range respect.
- Add Phase E breakout confirmation bars to reduce one-bar false releases.
- Add old-zone handling modes: Delete, Fade, Hide Labels and Current Only.
- Add dashboard rows for Cause and Locked Range, plus event-label cap management.

## v1.0 — 2026-06-28
- Initial version: lightweight Wyckoff state machine with A-E phase tracking, range-bounded phase zones, event labels, accumulation/distribution scoring, dashboard and alerts.
