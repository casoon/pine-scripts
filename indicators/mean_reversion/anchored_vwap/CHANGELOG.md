# Changelog

## v1.0.3 — 2026-09-05
- Data validity: added a hard Exchange-only gate — `volumeIsReal` checks `syminfo.volumetype` (`base`/`quote` only) and the running VWAP/σ accumulation now runs on a gated `vol` value that is `na` on invalid instruments, instead of raw `volume`
- On instruments without real trade volume, the AVWAP line, σ bands, anchor markers, stretched markers, and dashboard now go fully blank instead of silently accumulating on tick/n/a volume
- Added a Data Contract header block (`Verdict: Exchange-only`)
- Added a one-time "benötigt echtes Handelsvolumen" warning label on the last bar when volume is not real, showing the detected `syminfo.volumetype`

## v1.0.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.0.1 — 2026-06-29
- Alerts: messages standardized to `AVWAP · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.0 — 2026-06-27
- Initial release: anchored VWAP with swing-pivot / session / week / month / year / manual-date anchors
- Auto modes re-seed from the real pivot bar (pivR back), not the confirmation bar
- Volume-weighted σ bands at two configurable multiples
- Distance-from-value in σ as a symmetric Location output, stretched/anchor context markers, light-theme dashboard, alerts