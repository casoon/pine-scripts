# Changelog

## v1.1.3 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v3.2.3 (wavetrend_v3) — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v2.0.3 (wavetrend_v2) — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.1.2 — 2026-06-30
- Alerts: messages standardized to `WT · EVENT · {{ticker}} {{interval}}` for a uniform format across the library (titles unchanged)

## v3.2.2 (wavetrend_v3) — 2026-06-30
- Alerts: messages standardized to `WT3 · EVENT · {{ticker}} {{interval}}` for a uniform format across the library (titles unchanged)

## v2.0.2 (wavetrend_v2) — 2026-06-30
- Alerts: messages standardized to `WT2 · EVENT · {{ticker}} {{interval}}` for a uniform format across the library (titles unchanged)

## v1.1.1 — 2026-06-29
- Fix: WaveTrend cross alerts no longer repaint intrabar — `alert()` now fires once per bar close instead of the default once-per-bar (which could fire on a forming bar that later un-crosses)

## v3.2.1 (wavetrend_v3) — 2026-06-11
- Fix: exit-reason texts rewritten from multi-line ternaries to if/else (Pine v6 compile error CE10156)
- Fix: max_bars_back raised 500 → 1000 — auto-scaled macro POC lookback can reach 1000 bars on sub-4H charts and would exceed the old history buffer at runtime
- Dashboard tables now include the standard frame styling

## v2.0.1 (wavetrend_v2) — 2026-06-11
- Fix: JMA-approx smoothing used the length as the alpha exponent (`beta^length` ≈ 0 → effectively no smoothing); now uses the standard power of 2, consistent with all other JMA implementations in this repo
- Dashboard table now includes the standard frame styling

## v1.1 — 2026-06-11
- Fix: dashboard bias label used integer equality checks on a fractional score (momentum contributes ±0.5), so values like +1.5 fell through to "Strong Bear" — buckets are now range-based

## v1.0
- Initial release
