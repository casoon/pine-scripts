# Changelog

## v1.1.0 — 2026-11-17
- The stretch alerts fire only on a move beyond the level after the σ window is valid, not on the first valid bar when price already sits beyond it
- σ bands now also wait for "Min bars since anchor" (default 20, moved to the Bands group): until then the band plots stay empty, the σ cell reads "not yet valid" and Distance (σ) / Location show "—"
- Stretched markers renamed to "Stretched above AVWAP" / "Stretched below AVWAP"; the "short location" / "long location" wording is gone from markers and tooltips. The dashboard shows "Within ±Xσ" instead of "Near value"
- Dashboard: header shows the version, new "Anchor" row with the anchor mode and the number of bars since the anchor
- Alerts rebuilt as neutral event descriptions, always on the confirmed bar. Removed: "Stretched Above Value", "Stretched Below Value", "Price Crossed AVWAP" and the input "Alerts only on bar close (confirmed)". New: "Close Crossed Above AVWAP", "Close Crossed Below AVWAP", "Close Beyond Upper Stretch", "Close Beyond Lower Stretch". A cross on a re-anchor bar no longer counts — the AVWAP moved, not price. Existing alerts must be recreated

## v1.0.5 — 2026-11-17
- Stretched flags, markers and alerts start only after "Min bars since anchor" (new input, default 20); right after a re-anchor σ came from a handful of bars and flagged stretches too easily

## v1.0.4 — 2026-10-12
- Volume check fixed: only `tick` volume is rejected; `n/a` counts when the feed actually delivers volume. Most non-crypto feeds report `n/a`, so the old `base`/`quote` check treated futures and stocks with real volume (e.g. EUREX:FDAX1!) as volume-less — volume-based parts are active there again, which can change scores, gates and signals on those markets
- Without real volume a short "… not available" notice sits in the bottom-right corner instead of a label on the last candle

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