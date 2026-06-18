# Oscillator Footprint

Shows WaveTrend, StochRSI, and MFI momentum energy directly beside each price candle as ATR-normalized mini-bars. Each bar extends to the right of the candle, with three horizontal lanes — one per oscillator — offset to avoid overlap. Bar height is proportional to oscillator reading relative to ATR, so signal strength is visually comparable across different symbols and timeframes. Color encodes acceleration state: bright shades indicate building momentum; dark shades indicate fading momentum. Because Pine Script imposes a hard limit on the number of boxes, only the most recent N bars are drawn (configurable).

## Features

- Per-bar momentum mini-bars rendered in price space, to the right of each candle
- Three independent lanes: WaveTrend, StochRSI, MFI — each horizontally offset to avoid overlap
- Height scaled by ATR so oscillator strength is comparable across symbols
- Color encodes acceleration: bright = momentum building, dark = momentum fading
- Configurable lookback window (max bars drawn) and height scale factor

## Settings

| Group | Setting | Default | Notes |
|---|---|---|---|
| Profile | Bars to Display | 60 | Historical bars rendered (limited by Pine's 500-box cap) |
| Profile | Height Scale | 0.5 | Mini-bar height relative to ATR per full oscillator deflection |
| Profile | Lane Offset (bars) | 1 | Gap between candle right-edge and first lane |
| Profile | Lane Width (bars) | 2 | Width of each lane in bars |
| WaveTrend Lane | Show | on | |
| WaveTrend Lane | Channel Length | 10 | |
| WaveTrend Lane | Average Length | 21 | |
| StochRSI Lane | Show | on | |
| StochRSI Lane | RSI Length | 14 | |
| StochRSI Lane | Stoch Length | 14 | |
| StochRSI Lane | K Smoothing | 3 | |
| MFI Lane | Show | off | Disabled by default to reduce visual noise |
| MFI Lane | MFI Length | 14 | |
