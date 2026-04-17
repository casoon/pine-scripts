# Oscillator Divergence Zones

Detects regular and hidden divergences by comparing consecutive price pivots with the corresponding oscillator values. Supports RSI (default), CCI, and MFI — selectable via a single dropdown. Confirmed signals appear as labeled markers on both the oscillator pane and the main chart, and project ATR-wide horizontal price zones that stay active until the underlying structure fully breaks.

## Features

- **Oscillator selector**: RSI, CCI, MFI — one dropdown, all settings adapt automatically including the pane midline (50 for RSI/MFI, 0 for CCI)
- **Regular divergence**: price makes a lower low while the oscillator makes a higher low (bullish), or price makes a higher high while the oscillator makes a lower high (bearish) — reversal signal
- **Hidden divergence**: price/oscillator diverge in trend direction rather than against it — continuation signal, toggled separately with distinct visual style (dashed edge, transparent fill, triangle markers)
- **OB/OS filter**: optional level thresholds suppress signals in the neutral oscillator zone; defaults tuned for RSI/MFI, tooltips suggest values for CCI
- **ATR-based zone width**: half-width is locked at creation-time ATR × factor, so the band reflects the volatility at the time of the signal
- **Break trigger**: full-candle through level (wick-resistant, default) or close-based — configurable
- **Zone retest counter**: each active zone tracks how often price re-enters it without breaking; displayed as `×N` at the right edge with tooltip
- **Dual-pane display**: markers and dotted connector lines in the oscillator pane; labeled overlays and zone boxes on the chart
- **Alerts**: four conditions — bullish/bearish regular and bullish/bearish hidden; fire via both `alertcondition()` and `alert()`

## Oscillator Settings

| Oscillator | OB | OS | Midline | Notes |
|---|---|---|---|---|
| RSI | 70 | 30 | 50 | default |
| CCI | 100 | −100 | 0 | update filter thresholds to ~±25 |
| MFI | 80 | 20 | 50 | requires volume data |

OB/OS and filter thresholds must be set manually when switching oscillators — the script does not auto-update them.

## Zone Behavior

Active zones (solid edge + filled box) extend `zoneExtend` bars into the future each bar. A **bullish zone** breaks when the full candle falls at or below the level; a **bearish zone** breaks when the full candle rises at or above it. On break, the edge switches to dotted and the box grays out — the zone remains visible as structural history but is no longer tracked. Broken zones do not count toward `Max Active Zones`.

Hidden divergence zones use a dashed edge and transparent fill to visually distinguish them from regular divergence zones.

## Divergence Detection

Bar distance between consecutive pivots is measured between the actual pivot bars, not the confirmation bars. Pivots are detected on price (low for bullish, high for bearish), with the oscillator used only for momentum confirmation.

Regular and hidden divergences use separate zone arrays and separate connector line styles (dotted/full opacity for regular, dashed/reduced opacity for hidden).
