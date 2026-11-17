# Changelog

## v1.1.0 — 2026-11-17
- **Breaking:** "Smoothing Type" now offers `RMA` (default, the original core) and `T3` (slower, fewer crosses, misses more turns). SMA/EMA/RMA/WMA are practically the same line, and the ranking of the other cores did not hold between periods — the choice only changed signal density, not quality. Removed: SuperSmoother, KAMA, JMA Approx and the JMA Phase / Power inputs. Saved chart settings that used a removed type must be re-selected

## v1.0.3 — 2026-10-02
- Fixed: Percentile Rank counted the current bar in its own comparison window, so it could never read below 100/N. It now ranks the current ATR against the previous N bars and spans the full 0-100 range
## v1.0.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.0.1 — 2026-06-29
- Alerts: messages standardized to `ATRA · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.0 — 2026-06-18
- Initial release: ATR with four display modes (Raw, ATR%, Normalized, Percentile Rank), pluggable smoothing, gradient visualization, and expansion/contraction alerts