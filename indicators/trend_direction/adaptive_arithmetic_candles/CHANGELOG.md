## v1.2 — 2026-07-05
- Added Data Window debug plots (direction, quality, regression slope, efficiency ratio, strongBull/strongBear state, breakHigh/breakLow) to diagnose why a signal did or didn't fire at a given bar

## v1.1 — 2026-07-05
- Added Long/Short breakout signals: Setup (`strongBull`/`strongBear`) + Trigger (close breaks prior `Signal Breakout Length` bars' high/low), replacing "flip = trade" with Setup+Trigger
- `Minimum Signal Quality` input now drives the `strongBull`/`strongBear` quality threshold (previously hardcoded at 65)

## v1.0 — 2026-07-05
- Initial release: adaptive efficiency-smoothed arithmetic candles, regression-anchored body boost, synthetic wicks
- Trend Quality Score (0-100) from efficiency, regression slope, body ratio, and follow-through
- Strong/weak bull/bear candle coloring, quality score line/dots, and quality-confirmed flip signals with alerts
