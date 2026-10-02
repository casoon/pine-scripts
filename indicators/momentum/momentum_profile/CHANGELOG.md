# Changelog

## v1.0.2 — 2026-10-02
- Data validity: MFI now requires real trade volume (`syminfo.volumetype` base/quote). Without it the MFI series is na, the reference band stays neutral and the dashboard shows Avg MFI as "n/a" (previously a volume floor of 1 turned price-only data into a pseudo-MFI). Data Contract block added to the header

## v1.0.1 — 2026-10-02
- Fix: per-zone WaveTrend and MFI averages are now divided by the same overlap weights used for the sums. Previously a bar spanning several zones added its value only fractionally but counted fully in every zone, so averages were diluted (a +20 WT bar spanning four zones read as +5) and the dashboard Avg WT / Avg MFI were understated

## v1.0 — 2026-05-15
- Initial release
- WaveTrend average per price zone, center-out profile (bullish right, bearish left)
- MFI reference band per zone (green = volume-backed, red = selling pressure)
- Momentum POC: zone with highest absolute average WaveTrend
- Configurable lookback, row count, profile width, and bar offset
- Dashboard with overall bias, average WT, average MFI, and mPOC
