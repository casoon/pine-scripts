# Changelog

## v1.1.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.1.1 — 2026-06-30
- Alerts: messages standardized to `<KÜRZEL> · EVENT · {{ticker}} {{interval}}` for a uniform format across the library (titles unchanged)

## v1.1 — 2026-06-11
- Alert conditions added: Bull Zone Entry (score crosses above +60) and Bear Zone Entry (score crosses below −60)
- Header description corrected: structure detection compares rolling highest-high/lowest-low against N bars ago (not pivot-based)

## v1.0 — 2026-05-16
- Initial release
- Structural state per TF via highest-high / lowest-low comparison (no oscillators)
- Four timeframes: current + three configurable HTFs (defaults: 60m, 240m, Daily)
- Weighted confluence score −100 to +100 (HTF3 = 2.0×, HTF2 = 1.5×, HTF1 = 1.0×, current = 0.5×)
- Dashboard: per-TF Bull/Bear/Mixed state + score
