# Oscillator Divergence Zones

Detects regular and hidden divergences by comparing consecutive price pivots with the corresponding oscillator values. Supports RSI (default), CCI, MFI, Fisher Transform, TSI, Schaff Trend Cycle (STC), DPO, Ehlers Roofing Filter and Ehlers Cyber Cycle — selectable via a single dropdown. Confirmed signals appear as labeled markers on both the oscillator pane and the main chart, and project ATR-wide horizontal price zones that stay active until the underlying structure fully breaks.

This is **Stage 2** (exhaustion/momentum) of the reversal pipeline. The Fisher Transform and TSI sources are the *ruhige Oszillatoren* — they react more smoothly than RSI, which tends to produce the cleanest divergences (see the `indicator-design` skill, §6.1). STC, DPO, Roofing and Cyber Cycle are added as additional divergence sources so their reversal-signal quality can be evaluated against the existing oscillators within one comparable framework.

## Features

- **Oscillator selector**: RSI, CCI, MFI, Fisher, TSI, STC, DPO, Roofing, Cyber — one dropdown, all settings adapt automatically including the pane midline (50 for RSI/MFI/STC, 0 for CCI/Fisher/TSI/DPO/Roofing/Cyber) and auto OB/OS levels (Fisher ±1.5, TSI ±25, STC 75/25, unbounded types use a rolling ±1.5σ band)
- **TSI two-length control**: the main Length is the TSI long smoothing; a separate TSI Short Length sets the second (classic 25/13)
- **Regular divergence**: price makes a lower low while the oscillator makes a higher low (bullish), or price makes a higher high while the oscillator makes a lower high (bearish) — reversal signal
- **Hidden divergence**: price/oscillator diverge in trend direction rather than against it — continuation signal, toggled separately with distinct visual style (dashed edge, transparent fill, triangle markers)
- **Level filter (three modes)**: Off / Fixed (percentage of the OB–OS range) / Dynamic Zones (adaptive percentile thresholds from recent oscillator history) — suppresses signals in the neutral oscillator zone
- **StdDev filter**: optional statistical overextension gate — regular divergences only fire when the oscillator is outside its rolling mean ± N×StdDev band at the pivot
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
| Fisher | 1.5 | −1.5 | 0 | smoother than RSI |
| TSI | 25 | −25 | 0 | long/short = Length / TSI Short Length |
| STC | 75 | 25 | 50 | MACD via double stochastic; Fast/Slow Length params |
| DPO | +1.5σ | −1.5σ | 0 | unbounded; displaced SMA; prefer Dynamic Zones |
| Roofing | +1.5σ | −1.5σ | 0 | unbounded; HighPass + SuperSmoother params |
| Cyber | +1.5σ | −1.5σ | 0 | unbounded; Cyber Cycle Alpha param |

**Auto Source per Oscillator** (default on) picks each oscillator's canonical input automatically — `close` for RSI/STC/DPO/TSI, `hl2` for Fisher and the Ehlers filters (Roofing/Cyber), `hlc3` for CCI/MFI. Turn it off to force the manual *Source (manual)* input on every oscillator.

With **Auto OB/OS per Oscillator** enabled (default), the script applies these levels automatically when switching oscillators. The unbounded types (DPO/Roofing/Cyber) have no fixed OB/OS, so auto mode uses a rolling ±1.5σ band as a visual guide — for these, the **Dynamic Zones** level filter (percentile-based) is the recommended filter mode. Disable Auto OB/OS to set custom values; the fixed filter thresholds are defined as a percentage of the OB–OS range and adapt either way.

## Zone Behavior

Active zones (solid edge + filled box) extend `zoneExtend` bars into the future each bar. A **bullish zone** breaks when the full candle falls at or below the level; a **bearish zone** breaks when the full candle rises at or above it. On break, the edge switches to dotted and the box grays out — the zone remains visible as structural history but is no longer tracked. Broken zones do not count toward `Max Active Zones`.

Hidden divergence zones use a dashed edge and transparent fill to visually distinguish them from regular divergence zones.

## Divergence Detection

Bar distance between consecutive pivots is measured between the actual pivot bars, not the confirmation bars. Pivots are detected on price (low for bullish, high for bearish), with the oscillator used only for momentum confirmation.

Price pivots set the **timing** of a divergence; the oscillator side uses the **window extreme** (the oscillator's trough for bull, peak for bear within the pivot window) for both the comparison and the draw point. So the pane markers and divergence lines sit on the oscillator's own high/low rather than on a mid-slope reading at the exact pivot bar. Each line connects the matched prior pivot's oscillator extreme (one of the last three preceding pivots in range) to the current one. Regular and hidden divergences use separate zone arrays and separate line styles (dotted/full opacity for regular, dashed/reduced opacity for hidden).
