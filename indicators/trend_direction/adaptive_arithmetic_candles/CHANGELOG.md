# Changelog

## v1.3.0 — 2026-11-17
- Breaking: Trend Quality Score removed (efficiency + slope + body ratio + follow-through composite). Removed inputs: `Minimum Signal Quality`, `Show Quality Score Line`, `Show Quality Dots`, `Show Flip Labels`; removed plots: quality score line, "High Quality Candle" dots, `Debug: Quality Score`; flip labels ("AQ <score>") removed
- Strong bull/bear state is now candle direction plus regression-slope agreement, without a score threshold — strong coloring, flip markers and Long/Short breakout signals can appear more often than before
- Flip signals no longer require a minimum score; they fire on a direction change with regression-slope confirmation. Flip alert texts no longer mention quality
- Indicator title renamed to "Adaptive Arithmetic Candles [WavesUnchained]"

## v1.2.1 — 2026-11-17
- Fix: Long/Short breakout signals fire only on the first structure break of each strong bullish/bearish run, instead of on every new high/low while the strong state lasts

## v1.2 — 2026-07-05
- Added Data Window debug plots (direction, quality, regression slope, efficiency ratio, strongBull/strongBear state, breakHigh/breakLow) to diagnose why a signal did or didn't fire at a given bar

## v1.1 — 2026-07-05
- Added Long/Short breakout signals: Setup (`strongBull`/`strongBear`) + Trigger (close breaks prior `Signal Breakout Length` bars' high/low), replacing "flip = trade" with Setup+Trigger
- `Minimum Signal Quality` input now drives the `strongBull`/`strongBear` quality threshold (previously hardcoded at 65)

## v1.0 — 2026-07-05
- Initial release: adaptive efficiency-smoothed arithmetic candles, regression-anchored body boost, synthetic wicks
- Trend Quality Score (0-100) from efficiency, regression slope, body ratio, and follow-through
- Strong/weak bull/bear candle coloring, quality score line/dots, and quality-confirmed flip signals with alerts
