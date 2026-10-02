# Changelog

## v1.2.0 — 2026-10-02
- Speed Reference default 3.0 → 1.0 ATR×/bar (provisional, not yet validated on data). Typical swing legs move well below 3 ATR per bar, so the Speed component stayed in the bottom third of its range and contributed only about 13 of its 40 points; at 1.0 it uses its full range

## v1.1.3 — 2026-09-05
- Fix: Volume Gradient used raw `volume` with no check on `syminfo.volumetype` — on feeds that report tick volume, its 20% default weight scored conviction against a meaningless tick count. Added a `volumeIsReal` guard (`base`/`quote` only); the gradient's weight now drops to 0 when volume isn't real, and Speed/Cleanliness renormalize through the existing `totalW` division instead of the score being silently distorted by tick noise
- Data Contract header block added (`Volume: OPTIONAL`, `Verdict: CFD-degraded`)

## v1.1.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.1.1 — 2026-06-29
- Alerts: messages standardized to `SCR · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.1 — 2026-06-11
- Fixed `ta.atr()` being called inside conditional pivot blocks (inconsistent series calculation) — ATR is now computed once per bar in global scope
- Fixed multi-line ternary with series operands in the leg-scan loop (compile error) — rewritten as if/else
- Volume sums now use `nz()` so instruments without volume data no longer produce na scores
- Added alert conditions for bearish and bullish conviction divergences

## v1.0 — 2026-05-16
- Initial release
- Per-leg conviction score 0–100: speed (ATR-normalized) + cleanliness (on-trend bar fraction) + volume gradient (volume rising toward pivot)
- Bearish divergence: price higher high, conviction lower → hidden weakness
- Bullish divergence: price lower low, conviction lower → exhausted sellers
- Step-line conviction history for both bull and bear legs
- Divergence labels at exact pivot bar positions
- Dashboard: last/prev leg scores for each direction, divergence state
