# Changelog

## v1.1.4 — 2026-06-30
> Consolidated entry, reconstructed from the diff — v1.1.0–v1.1.3 were shipped without
> individual changelog entries.

- HTF trend direction is now slope-based and ATR-normalized: `htfSlopeAtr = (ema - ema[slopeLen]) / htfAtr` against a new `htfSlopeMin` input (default 0.10), so a flat HTF EMA reads as flat instead of flipping direction on noise
- Coil scoring no longer credits stale compression: `coilNowMin` (default 0.45) sets a floor on current-bar compression, and recent coil evidence is scaled down when the current bar is no longer compressed
- Base Break gained two filters — `baseMinShare` (default 0.35, share of the break window that must have been a base before a counter-trend break is allowed) and `breakAtrMin` (default 0.10 ATR, minimum close distance beyond the broken band) — which reject one-tick band breaks
- Added an optional compression box (`showBox`, on) and optional Watch/Setup markers (`showSetups`, off) with `setupMarkerShare`; the markers are explicitly not entry signals, BRK/REV remains the only trigger
- Regime background now defaults to off; `max_boxes_count=50` added to the `indicator()` call

## v1.0.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.0.1 — 2026-06-29
- Alerts: messages standardized to `CFR · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.0 — 2026-06-28
- Initial release: compression coil detection (symbolic-entropy complexity + box-counting fractal dimension + efficiency) with a scored release-break engine
- Role-separated design — band break is the only trigger; the Setup Score is multiplicative (coil ceiling × release dynamics) so a high coil alone cannot fire, instead of a hard AND-chain
- HTF regime classifies each break as Release (continuation) or Base Break (counter-trend structural change, higher threshold)
- Per-direction signal cooldown; single choppiness quality veto; Watch → Setup → Trigger staging
- Light-theme dashboard with role-score breakdown and a debug log on every break (including the block reason)