# Changelog

## v1.1.0 — 2026-11-17
- **Breaking:** "Smoothing Type" now offers `EMA` (default, the original core) and `T3` (slower, fewer crosses, misses more turns). SMA/EMA/RMA/WMA are practically the same line, and the ranking of the other cores did not hold between periods — the choice only changed signal density, not quality. Removed: SuperSmoother, KAMA, JMA Approx and the JMA Phase / Power inputs. Saved chart settings that used a removed type must be re-selected

## v1.0.3 — 2026-10-02
- Oscillator scale no longer inherits the chart symbol's price precision (values like 80,0000 on 4-decimal symbols such as NATGAS) — shows 2 decimals

## v1.0.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.0.1 — 2026-06-29
- Alerts: messages standardized to `ADXA · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.0 — 2026-06-18
- Initial release: ADX with DI± display, pluggable signal smoothing, 4-state histogram, gradient line, and DI/threshold alert conditions