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
