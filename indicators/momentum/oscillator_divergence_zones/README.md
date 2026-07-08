# Oscillator Divergence Zones

Detects regular and hidden divergences by comparing consecutive price pivots with the corresponding oscillator values. Supports RSI (default), CCI, MFI, Fisher Transform, TSI, Schaff Trend Cycle (STC), DPO, Ehlers Roofing Filter and Ehlers Cyber Cycle — selectable via a single dropdown. Confirmed signals appear as labeled markers on both the oscillator pane and the main chart, and project ATR-wide horizontal price zones that stay active until the underlying structure fully breaks.

This is **Stage 2** (exhaustion/momentum) of the reversal pipeline. The Fisher Transform and TSI sources are the *ruhige Oszillatoren* — they react more smoothly than RSI, which tends to produce the cleanest divergences (see the `indicator-design` skill, §6.1). STC, DPO, Roofing and Cyber Cycle are added as additional divergence sources so their reversal-signal quality can be evaluated against the existing oscillators within one comparable framework.

## Features

- **Oscillator selector**: RSI, CCI, MFI, Fisher, TSI, STC, DPO, Roofing, Cyber — one dropdown, all settings adapt automatically including the pane midline (50 for RSI/MFI/STC, 0 for CCI/Fisher/TSI/DPO/Roofing/Cyber) and auto OB/OS levels (Fisher ±1.5, TSI ±25, STC 75/25, unbounded types use a rolling ±1.5σ band)
- **TSI two-length control**: the main Length is the TSI long smoothing; a separate TSI Short Length sets the second (classic 25/13)
- **Regular divergence**: price makes a lower low while the oscillator makes a higher low (bullish), or price makes a higher high while the oscillator makes a lower high (bearish) — reversal signal
- **Hidden divergence**: price/oscillator diverge in trend direction rather than against it — continuation signal, toggled separately with distinct visual style (dashed edge, transparent fill, triangle markers)
- **Hidden divergence trend filter** (off by default): restricts hidden bullish to above the Trend EMA and hidden bearish to below it, so continuation signals align with the prevailing trend
- **Level filter (three modes)**: Off / Fixed (percentage of the OB–OS range) / Dynamic Zones (adaptive percentile thresholds from recent oscillator history) — suppresses signals in the neutral oscillator zone
- **StdDev filter**: optional statistical overextension gate — regular divergences only fire when the oscillator is outside its rolling mean ± N×StdDev band at the pivot
- **Divergence Quality Score (0-100)**: combines pivot spacing, oscillator divergence magnitude, OB/OS extremity, and trend context into one informational score — shown in the signal tag/tooltip and reflected in zone shading; never filters or blocks a signal
- **ATR-based zone width**: half-width is locked at creation-time ATR × factor, so the band reflects the volatility at the time of the signal
- **Break trigger**: full-candle through the zone boundary (wick-resistant, default) or close-based — configurable
- **Zone retest counter**: each active zone tracks how often price re-enters it without breaking (debounced — a multi-bar stay inside counts once); displayed as `×N` at the right edge with tooltip
- **Dashboard**: oscillator type, last signal + quality score, active zone count, filter mode, trend bias
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

Active zones (solid edge + filled box) extend `zoneExtend` bars into the future each bar. The break check is always against the actual zone boundary (level ± half-width), not the bare pivot level. In the default full-candle mode a **bullish zone** breaks as soon as the low wicks below the lower boundary; a **bearish zone** breaks as soon as the high wicks above the upper boundary. With **Break on Close** enabled, the check uses the candle close instead (slower, ignores wicks). On break, the edge switches to dotted and the box grays out — the zone remains visible as structural history but is no longer tracked. Broken zones do not count toward `Max Active Zones`.

Hidden divergence zones use a dashed edge and transparent fill to visually distinguish them from regular divergence zones. When the Quality Score is enabled, zones with a score ≥70 get a heavier border and a less transparent fill so the strongest setups stand out.

## Divergence Detection

Bar distance between consecutive pivots is measured between the actual pivot bars, not the confirmation bars. Pivots are detected on price (low for bullish, high for bearish), with the oscillator used only for momentum confirmation.

Price pivots set the **timing** of a divergence; the oscillator side uses the **window extreme** (the oscillator's trough for bull, peak for bear within the pivot window) for both the comparison and the draw point. So the pane markers and divergence lines sit on the oscillator's own high/low rather than on a mid-slope reading at the exact pivot bar. Each line connects the matched prior pivot's oscillator extreme (one of the last three preceding pivots in range) to the current one. Regular and hidden divergences use separate zone arrays and separate line styles (dotted/full opacity for regular, dashed/reduced opacity for hidden).

## Quality Score

When enabled (default on), every fired divergence gets a 0-100 score averaging four components, each normalized 0-100:

- **Pivot spacing** — how far apart the matched pivots are, from `Min Bars Between Pivots` (weak) to `Max Bars Between Pivots` (strong)
- **Oscillator divergence magnitude** — the size of the oscillator's move between the two pivots relative to its own rolling standard deviation
- **Extremity** — how far the pivot's oscillator value sits past the active filter boundary (Fixed mode's `Max for Bull`/`Min for Bear` level), not the hard OB/OS line — so a signal that only just clears the filter still earns partial credit instead of scoring near zero
- **Trend context** — distance from the Trend EMA in ATR units; regular divergences score higher when they occur against an overextended trend (reversal setup), hidden divergences score higher when aligned with the trend (continuation setup)

The score is purely informational — it never gates or suppresses a signal. It appears as a suffix on the signal tag (e.g. `RD+ 78`), in the tooltip, and as zone shading (heavier border/fill at ≥70).
