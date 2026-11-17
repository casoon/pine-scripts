# Changelog

## [Unreleased]

## v1.8.0 — 2026-11-17

### Removed
- **Quality tier and quality thresholds.** The A/C tier was derived from a single RSI condition. Removed inputs: `Min. Qualität Long`, `Min. Qualität Short`; removed the hidden `Signal Score` plot; signal labels read "BUY" / "SELL" without a tier

### Changed
- The RSI condition is now an honestly named optional filter, `RSI confirms direction` (default off): RSI above 50 for longs, below 50 for shorts. With the default settings the signals are the same as before (the quality minimum defaulted to 0). The label tooltip shows the RSI value instead of a quality point
- Input `Score am Signal anzeigen` renamed to `Signal-Label anzeigen`
- The strategy file carries the same change; its entry log shows the RSI value and filter state instead of quality and tier

## v1.7.4 — 2026-11-17

### Fixed
- HTF trend filter (Gate F) and the 1H/4H WaveTrend gates (G/H) read the last closed higher-timeframe bar, so their values no longer change while the higher-timeframe bar is still forming
- The optional quality point is mirrored: RSI above 50 for longs, RSI below 50 for shorts (shorts previously also counted RSI above 50). Min. Quality defaults are now equal for both sides (0 — quality is optional)
- Cooldown runs per direction: a long signal no longer blocks the next short signal and vice versa
- Gate F (HTF trend) failed open while the higher-timeframe EMAs were not yet available (warm-up): "not bearish" was true for missing data. It now requires the HTF EMAs to exist

### Changed
- **Quality no longer depends on pivots.** The "no LL / no HH" point is removed from the quality score; the score is now one RSI point (0–1). Min. Quality inputs are 0–1. Pivot markers and the structure line in the tooltip stay as display. Long signals that failed only because of a lower-low now pass; the strategy file carries the same change

## v1.7.3 — 2026-10-12
- The "backtest invalid" notice on non-standard chart types (Heikin Ashi, Renko …) now sits in the bottom-right corner as a short note instead of a label on the last candle

## v1.7.2 — 2026-10-02
- Script header corrected: the quality score runs 0–2 (not 0–7), and the short RSI condition is RSI > 50 (elevated), not "overbought" — matching the code and README

## v1.7.1 — 2026-09-05
- Added chart-type guard: visible warning label when loaded on a non-standard chart (Heikin Ashi, Renko, Kagi, Line Break, P&F, Range) since the underlying strategy's backtest results are invalid there

## v1.7.0 — 2026-07-01
- Gate I — Session-Filter: optionaler Zeitfenster-Gate (default: aus); filtert Signale außerhalb der konfigurierbaren Session (HHMM-HHMM Börsenzeit, Voreinstellung 0700-1200)

## v1.6.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.6.1 — 2026-06-30
- Alerts: messages standardized to `<KÜRZEL> · EVENT · {{ticker}} {{interval}}` for a uniform format across the library (titles unchanged)

## v1.5 — 2026-05-06
- Initial release (mandatory gate model + 0–2 optional quality score, structural SL, R-multiple TP)
