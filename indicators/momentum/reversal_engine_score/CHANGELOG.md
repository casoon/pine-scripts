# Changelog

## v1.7.0 — 2026-07-01
- Gate I — Session-Filter: optionaler Zeitfenster-Gate (default: aus); filtert Signale außerhalb der konfigurierbaren Session (HHMM-HHMM Börsenzeit, Voreinstellung 0700-1200)

## v1.6.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.6.1 — 2026-06-30
- Alerts: messages standardized to `<KÜRZEL> · EVENT · {{ticker}} {{interval}}` for a uniform format across the library (titles unchanged)

## v1.5 — 2026-05-06
- Initial release (mandatory gate model + 0–2 optional quality score, structural SL, R-multiple TP)
