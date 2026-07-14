# Changelog

## v1.9.3 — 2026-07-09
- Fix: `npoc_already_touched` now guards against `na` prev POC explicitly
- Naked POC: added "Naked POC Min Distance (ATR)" input — filters out noise-driven POC shifts before tracking a new naked POC (default 0.1 ATR)

## v1.9.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.9.1 — 2026-06-29
- Alerts: messages standardized to `VST · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.9
- Initial release
