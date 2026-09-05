# Changelog

## v1.1.3 — 2026-09-05
- Hard Exchange-only gate: indicator now requires real trade volume (`syminfo.volumetype` `base`/`quote`); on `tick`/`n/a` instruments (all CFDs incl. `CAPITALCOM:NATURALGAS`, Forex, most Indices) it plots nothing and shows a one-time "needs real trade volume" label instead of falling back to a neutral `volume_rank` of 0.5
- Data Contract added to header (`Verdict: Exchange-only`)

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
