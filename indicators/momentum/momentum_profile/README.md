# Momentum Profile

Analog to a volume-profile or money-flow delta profile, but for momentum: maps average WaveTrend and MFI values per price zone over a configurable lookback window to identify dominant-momentum levels (zones where strong, oscillator-backed moves occurred) versus mixed or fragile levels (zones where buyers and sellers were roughly balanced and price is likely to be revisited).

## Features

- WaveTrend average per price zone — bars extend right from the anchor line, green = bullish average, red = bearish average
- MFI average per zone as a colored reference band (green = net buying pressure, red = net selling, gray = neutral/mixed)
- Momentum POC: the zone with the highest absolute average WaveTrend value, highlighted separately
- Configurable lookback, row count, profile width (bars), and horizontal bar offset
- Dashboard showing overall bias, average WT, average MFI, and the mPOC price level

## Settings

| Group | Setting | Default | Notes |
|---|---|---|---|
| Profile | Lookback | 200 | Bars used to build the profile (max 1500) |
| Profile | Rows | 25 | Number of price zones |
| WaveTrend | Channel Length | 10 | WT channel EMA length |
| WaveTrend | Average Length | 21 | WT smoothing EMA length |
| MFI | MFI Length | 14 | MFI calculation period |
| MFI | Show MFI Reference Band | on | Toggle the reference band overlay |
| Visualization | Profile Width (bars) | 60 | Horizontal width of the drawn profile |
| Visualization | Bar Offset | 40 | Offset from the right edge of the chart |
| Visualization | Momentum POC | on | Highlight the dominant-momentum zone |
| Visualization | Dashboard | on | Show the summary table |
