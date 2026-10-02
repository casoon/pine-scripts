# Changelog

## v1.0.5 — 2026-10-02
- Oscillator scale no longer inherits the chart symbol's price precision (values like 80,0000 on 4-decimal symbols such as NATGAS) — shows 2 decimals

## v1.0.4 — 2026-10-02
- Fixed: "CCI Lead" trigger mode did not apply the MFI momentum confirmation its tooltip describes — the CCI confirm check is always true on a CCI zero cross, so every cross fired. CCI Lead signals now require MFI rising (bull) or falling (bear) on the cross bar; without real trade volume they stay silent like the other MFI-based signals
## v1.0.3 — 2026-09-05
- Hard Exchange-only gate: MFI (and everything derived from it — line, signal, histogram, flow states, signals) now requires real trade volume (`syminfo.volumetype` `base`/`quote`); on `tick`/`n/a` instruments MFI plots nothing and a one-time "needs real trade volume" label appears instead. The volume-independent CCI line and turn markers are unaffected and keep plotting on any instrument
- Data Contract added to header (`Verdict: Exchange-only`)

## v1.0.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.0.1 — 2026-06-29
- Alerts: messages standardized to `CFT · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.0 — 2026-06-18
- Initial release
- Manual MFI with pluggable smoothing (EMA, SMA, RMA, WMA)
- CCI confirmation layer normalized to MFI scale for visual alignment
- 4-state flow background: bull/bear expansion vs. accumulation/distribution
- 4-state color-coded MFI histogram
- Extreme-zone reversal signals with optional CCI gate
- Midline confirmation dots (MFI crosses 50 with aligned CCI)
- Gradient MFI line color (bull at OS, bear at OB)
- Fill between MFI and signal line
- Alert conditions for all signal types