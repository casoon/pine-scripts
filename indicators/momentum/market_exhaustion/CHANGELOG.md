# Changelog

## v1.2.1 — 2026-10-02
- Oscillator scale no longer inherits the chart symbol's price precision (values like 80,0000 on 4-decimal symbols such as NATGAS) — shows 2 decimals

## v1.2.0 — 2026-10-02
- Change: divergence reaction is now measured from the pivot-bar close over the "Reaction window" bars after the pivot (previously capped at the pivot confirmation bars, so the window input had no effect). Divergences are drawn at confirmation with a provisional score and finalized (score, tooltip, line width) once the window has passed; score-based alerts would have to fire at finalization
- Change: fatigue component removed from the divergence score (it duplicated the MFI delta); its weight is redistributed proportionally over the remaining components. "Fatigue lookback" input removed
- Fix: bull/bear divergence sequence count now resets when a confirmed pivot low/high is not a divergence of that direction (was unbounded)
- Data validity: MFI (chart and HTF) now requires real trade volume (`syminfo.volumetype` base/quote); without it MFI parts go na and the CCI mode keeps working. Data Contract block added to the header

## v1.1.3 — 2026-10-02
- Fix (CCI / MFI+CCI with CCI engine): the divergence OS/OB area check now uses zones built from the active oscillator instead of the MFI zones, so CCI divergences are tested against their own range
- Internal: divergence score lookbacks are now computed on every bar instead of inside the divergence branch (no change in values)

## v1.1.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.1.1 — 2026-06-30
- Alerts: messages standardized to `<KÜRZEL> · EVENT · {{ticker}} {{interval}}` for a uniform format across the library (titles unchanged)

## v1.1.0 — 2026-06-11
- Alert conditions added for long/short signals
- HTF request now passes `lookahead=barmerge.lookahead_off` explicitly
- Label budget raised to 500 — with high "Max divergence objects" settings the two labels per divergence could exceed the old cap of 300, silently dropping the oldest divergence labels

## v1.0.0
- Initial release
