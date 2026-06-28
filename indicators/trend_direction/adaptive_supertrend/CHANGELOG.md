## v1.7 — 2026-06-28
- ATR Rank's chop fallback is now an input (`ATR Conviction in Chop`, default 0.50) instead of a hardcoded 0.35 — unconfirmed volatility counts as neutral rather than near-zero, avoiding a double chop penalty alongside the chop multiplier

## v1.6 — 2026-06-28
- Adaptive multiplier now symmetric around base: high conviction tightens the band *below* the base multiplier (previously base was the floor), neutral conviction = base, low conviction widens it — clamped to `baseMult × 0.60 … 1.80`
- ATR Rank only adds conviction when trend force confirms a real move; otherwise contributes a neutral value so volatility spikes (panic, news, blow-off) no longer score as conviction
- Trend force now maps to conviction against an absolute cap (`Trend Force Full Conviction`, default 2.0) instead of a rolling 100-bar percentile — no longer over-scores "less weak" moves in persistently weak markets
- Softened the chop penalty from ×0.35 to ×0.50 so ranges still widen the band without crushing conviction (the ATR-rank gate already handles part of the chop case)
- Conviction table now clears when the table is toggled off (no stale last-state)
- Clarified tooltips: HTF layer is a fixed-multiplier reference Supertrend (not adaptive), overextension is a late-entry / trail-risk warning (not a reversal signal), JMA is a JMA-like approximation

## v1.5 — 2026-06-10
- RSI filter reworked: now blocks flips when RSI is already overextended in the flip direction (RSI > threshold for longs, RSI < 100−threshold for shorts) — default threshold 70

## v1.4 — 2026-06-10
- JMA (Jurik Moving Average) added to smoothing options
- Candle coloring switched from plotcandle() to barcolor() — fixes random revert to default colors
- Default Up/Down colors changed to green (#00c853) and red (#d50000)

## v1.3 — 2026-06-10
- MTF confluence layer: higher-TF Supertrend via configurable timeframe (default 4H)
- Pullback zones: subtle background tint when LTF trend opposes HTF — stronger when LTF overextended (ready state)
- Confluence signals: diamond marker replaces triangle when a qualified flip aligns with HTF direction
- HTF stop line: secondary step-line showing the HTF Supertrend level
- Table: added HTF direction and Setup rows (Watch / Ready / —)
- Alerts: HTF Confluence Long and HTF Confluence Short added
- Unified zone background replaces separate overextension bgcolor

## v1.2 — 2026-06-10
- Adjustable source smoothing: None / EMA / WMA / SMA with configurable length
- Smoothing applied only to band computation — ratchet, flip logic, cloud and conviction remain on raw source

## v1.1 — 2026-06-10
- Body filter: flip signals blocked when flip-bar body < N×ATR (default off)
- Trap markers: orange X when wick crosses stop but close holds on wrong side
- Overextension alert: amber candles + subtle background when stop-distance in top percentile
- Table: added Body % and Ovext % rows
- Alerts: Bull Trap / Bear Trap added

## v1.0 — 2026-06-10
- Initial release
- Conviction score from ATR rank + trend force + chop penalty
- Adaptive multiplier: `baseMult × (1 + adaptivity × (1 − conviction))`
- Optional RSI alignment filter for flip signals
- Conviction table with live component breakdown
- Gradient trend cloud, glow effect, flip dot markers
