# Changelog

## v2.0 — 2026-06-11
- Signals are now confluence-based and actionable: a LONG mark fires only when the stock both outperforms the benchmark (Mansfield > 0) AND is in its own uptrend (price above the trend EMA); SHORT requires both weak. This structurally rules out the old contradiction where a bullish mark appeared while price was falling (pure relative strength is decoupled from the chart).
- Markers follow standard trading convention again (now that they are real entries): long = green up-triangle below the line, short = red down-triangle above.
- New "Price Trend EMA" input defines the absolute-trend filter.
- Dashboard reworked: Relative Strength, Price Trend, and a "Setup" verdict (LONG / SHORT / Neutral); right-edge tag shows the live setup.
- Alerts renamed to Long/Short Confluence.

## v1.1 — 2026-06-11
- Cleaner leadership markers: removed the repeated "RS" text that cluttered the line; markers are now small color-coded triangles only
- Markers annotate RS-line extremes (not buy/sell entries): green crowns RS highs (above the line), red tags RS lows (below) — consistent with the line's shape. Fires on the breakout bar (no delay); offset uses the line's standard deviation (steady gap), adjustable via the new "Marker Distance from Line" input
- Added a single tidy right-edge tag showing the live leadership state and Mansfield value (RS ▲/▼ x.x%)

## v1.0 — 2026-06-11
- Initial release
- RS line (price ÷ benchmark) and Mansfield RS oscillator display modes
- Mansfield RS: % distance of RS from its moving average, color-coded around zero
- IBD leadership signal: RS new high before price new high (and the bearish mirror)
- Trend state (Leading / Lagging × rising / fading) and RS rank in the dashboard
- Configurable benchmark (default SPY), light-theme dashboard
- Alerts: RS leadership up/down, Mansfield zero-cross up/down
