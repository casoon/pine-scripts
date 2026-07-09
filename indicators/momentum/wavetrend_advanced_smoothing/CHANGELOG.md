# Changelog

## v1.1.1 — 2026-07-09
- Fixed Sentiment Bar color: it used `score > 0 ? colBull : colBear`, coloring the overbought side (positive score) bull and the oversold side (negative score) bear — backwards from every other color cue in the panel (gradient line), where `colBull` marks the oversold side and `colBear` the overbought side. Swapped to match.

## v1.1.0 — 2026-07-09
- Added Sentiment Bar (group 7, on by default): live label at the panel's right edge scoring how far WT sits inside its own OB/OS zone, ±100 with a mini bar — ported from Williams VIX Fix Advanced's Sentiment Bar. Computed on raw WT/Overbought1/Oversold1, consistent across all three Scale Modes. No Signal Quality score added — this variant has no trend-context or stall/absorption layer for that weighting to draw on.
- Alerts group label numbered ("8 · Alerts") for consistency with the rest of the input groups.

## v1.0.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.0.1 — 2026-06-29
- Alerts: messages standardized to `WTAS · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.0 — 2026-06-18
- Initial release
- 8 smoothing kernels: EMA, SMA, RMA, WMA, SuperSmoother, T3, KAMA, JMA
- Three scale modes: Classic, Clamp ±100, Adaptive ±100
- Gradient line color (bull ↔ bear based on oscillator level)
- Gradient shadow fills between WT main line and zero
- 4-state color-coded histogram
- Optional fill between WT main and signal lines
- OB/OS zone background fills
- Extreme cross signal markers + subtle dots for all crosses
- Alert conditions for all cross types
