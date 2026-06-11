# Changelog

## v1.1 — 2026-06-11
- Acceleration shading implemented: mini-bars darken (extra transparency) when the oscillator's absolute value is shrinking vs the previous bar — the documented bright/dark encoding was previously not in the code

## v1.0 — 2026-05-15
- Initial release
- Per-bar momentum mini-bars drawn in price space beside each candle
- Three lanes: WaveTrend, StochRSI, MFI — each offset horizontally to avoid overlap
- Height scaled by ATR so signal strength is comparable across symbols
- Color encodes acceleration state: bright = building, dark = fading
- Configurable lookback window and height scale factor
