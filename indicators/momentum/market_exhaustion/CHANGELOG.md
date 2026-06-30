# Changelog

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
