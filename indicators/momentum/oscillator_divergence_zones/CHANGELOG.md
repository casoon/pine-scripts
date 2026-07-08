# Changelog

## v1.5.0 — 2026-07-08
- Fix: zone break logic now checks the actual zone boundary (level ± half-width) instead of the bare pivot level; the default "full-candle" mode was requiring the entire candle to clear the level (effectively stricter than close-based), so it now breaks on a wick piercing the boundary as intended
- Fix: retest counter no longer over-counts — a touch is only registered on the bar price re-enters the zone, not on every bar it stays inside; touch check now compares the full candle range against both zone edges symmetrically
- Add optional Trend Context filter (off by default): when enabled, hidden bullish divergence only fires above the Trend EMA and hidden bearish only below it, since hidden divergences are continuation signals
- Add Divergence Quality Score (0-100): combines pivot spacing, oscillator divergence magnitude, extremity relative to the active filter boundary, and trend context; shown in the signal tag, tooltip, and zone shading (stronger border/fill for higher scores) — informational only, never filters a signal
- Add Dashboard: oscillator type, last signal + quality score, active zone count, filter mode, trend bias
- Signal tags shortened: `RD+`/`RD-` for regular, `HD+`/`HD-` for hidden (was "Reversal"/"Cont.")

## v1.4.3 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.4.2 — 2026-06-30
- Alerts: messages standardized to `ODZ · EVENT · {{ticker}} {{interval}}` for a uniform format across the library (titles unchanged)

## v1.4.1 — 2026-06-29
- Fix: combined `alert()` divergence calls no longer repaint intrabar — now fire once per bar close instead of once per bar (the named alertcondition() alerts were already user-controlled)

## v1.4.0 — 2026-06-27
- Add four oscillator sources for divergence evaluation: Schaff Trend Cycle (STC, bounded 0–100, auto 75/25), Detrended Price Oscillator (DPO), Ehlers Roofing Filter, Ehlers Cyber Cycle
- DPO/Roofing/Cyber are unbounded/centered — auto OB/OS uses a rolling ±1.5σ band; prefer the Dynamic Zones level filter for them
- New params: STC Fast/Slow Length, Roofing HighPass/SuperSmoother, Cyber Cycle Alpha
- Fix: divergence lines now connect the two pivots that actually form each divergence (matched prior pivot → current pivot) instead of chaining consecutive signals, which could draw lines that visually contradicted the divergence
- Divergence lines restyled (cleaner opacity) with a subtle midpoint node whose hover tooltip explains the setup (type, price vs oscillator behaviour, oscillator values)
- Auto Source per Oscillator (default on): each oscillator now uses its canonical source automatically — close for RSI/STC/DPO/TSI, hl2 for Fisher/Roofing/Cyber, hlc3 for CCI/MFI; turn off to force the manual Source for all
- Chart signals restyled: the former transparent-text markers are now solid coloured label bubbles (accent fill, white text) at the pivot, each with a hover tooltip explaining the divergence
- Retest counter cleaned up: now text-only (×N) that stays invisible until price actually re-enters a zone, instead of an empty coloured arrow bubble dangling on every untouched zone
- Divergence now uses the oscillator's window extreme (trough for bull, peak for bear) for both the comparison and the draw point — pane markers and lines sit on the oscillator's own high/low instead of mid-slope; price pivots still set the timing

## v1.3.0 — 2026-06-27
- Add Fisher Transform and TSI as oscillator sources (ruhige Oszillatoren → cleaner divergences); auto OB/OS Fisher ±1.5 · TSI ±25; new TSI Short Length input
- Pane midline now centers on 0 for Fisher/TSI as well as CCI

## v1.2.1 — 2026-06-11
- Fix: oscillator selection rewritten from a multi-line ternary to `switch` (Pine v6 compile error CE10156)

## v1.2
- Initial release
