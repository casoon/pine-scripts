# Changelog

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
