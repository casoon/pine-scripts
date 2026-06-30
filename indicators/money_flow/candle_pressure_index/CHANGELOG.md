# Changelog

## v1.1.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.1.1 — 2026-06-29
- Alerts: messages standardized to `CPI · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.1 — 2026-06-11
- 4 alert conditions added: CPI Long, CPI Short, Initiation Spike, Absorption Spike (alerts fire independently of the "Show Zero-Cross Signals" display toggle)
- na-volume bars are now treated as 0 instead of propagating na through the CPI EMA

## v1.0 — 2026-05-16
- Initial release
- Per-bar pressure from close location × body ratio × volume rank (no derived oscillators)
- CPI oscillator (EMA, −1 to +1) with momentum (1st derivative) line
- Initiation/Absorption spike markers on extreme-pressure bars
- Zero-cross long/short signals with momentum gate
- Dashboard: state, CPI, momentum direction, raw bar pressure
