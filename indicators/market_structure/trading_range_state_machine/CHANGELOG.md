# Changelog

## v1.1 — 2026-07-04
- Background heat now scales continuously with the range score within each state (instead of a flat, low-alpha gray for Building) so a strengthening range is visible before the next state boundary
- Breaking state now distinguishes direction: bullish (green) vs bearish (red) breakout coloring, dashboard "Direction" row, and split "Range Breaking Up" / "Range Breaking Down" alerts (replaces the single "Range Breaking" alert)
- Added a "Position" dashboard row: % location within the range plus an Upper/Mid/Lower zone label
- Fix: dashboard label cells rendered white text on a transparent background, invisible on TradingView's default light theme; now follows the repo's standard light-theme table style (dark-gray label text, light-gray header/border, colored status cells only where a state is shown)

## v1.0 — 2026-07-04
- Initial release: pivot-cluster range detection, 8-factor weighted range score, Inactive/Building/Confirmed/Mature/Breaking state machine, range lines/midline/touch markers/background heat/ribbon, dashboard, and alerts (Range Confirmed / Range Mature / Range Breaking)
