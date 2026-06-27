# Regime Classifier

Stage-1 regime filter for the reversal pipeline. It fuses three classic "is the market trending or not" sensors — the **Fractal Dimension Index**, **Kaufman's Efficiency Ratio** and the **Choppiness Index** — onto a single 0–1 *trendiness* axis and classifies the market into **Trend / Range / Chaos**. Its job is to answer one question — *"is a reversal even sensible here?"* — and expose that as a permission value other modules can gate on. It deliberately produces **no long/short triggers**.

This implements **Stage 1** of the four-stage reversal pipeline (see the `indicator-design` skill, §6.1): Regime → Exhaustion → Confirmation → Quality. Reversals are sensible in Range (fade the edges) and dangerous in a clean strong Trend or in Chaos. Exhaustion detection (Stage 2, e.g. WaveTrend/divergence modules) can legitimately override the Trend damping at the *end* of a trend — this module intentionally does not detect that.

## Features

- Three regime sensors on one comparable trendiness axis (0–1)
- Trend / Range / Chaos classification with threshold **hysteresis** (previous regime is held inside the dead zone, so it does not flip on score noise)
- Symmetric **reversal-permission** and **trend-permission** outputs (0–1) — no hardcoded long/short
- Per-sensor mapped lines so you can see *which* sensor drives the verdict
- Regime-change **watch markers** and alerts (state changes, not entries)
- Light-theme dashboard and a debug log on every regime change

## Sensors

| Sensor | Formula | Reads | Trend ↔ Range |
|---|---|---|---|
| **Efficiency Ratio** (Kaufman) | `|Δclose(n)| / Σ|Δclose|` | how directly price travelled | high ER = Trend |
| **Fractal Dimension** (box-counting) | `(log(r1+r2) − log(r3)) / log 2` over n/2, n/2, n boxes | path roughness, D∈[1,2] | low D = Trend |
| **Choppiness Index** | `100·log10(ΣTR / range) / log10(n)` | range-fill vs. directional travel | low Chop = Trend |

Each sensor is mapped to 0–1 trendiness via its own *full-trend* / *full-range* anchor inputs, then combined with adjustable weights into the composite trendiness score.

## Regime logic

1. **Trendiness** = weighted mean of the three mapped sensors (0–1).
2. **State** — `trendiness ≥ Trend Level` → Trend; `≤ Range Level` → Range; in between the previous state holds (hysteresis).
3. **Chaos override** — fires only when *all three* sensors agree on maximal noise (Chop very high **and** ER very low **and** FDI very high). Chaos is not a tradeable range; it collapses both permissions by the chaos multiplier.

## Outputs (for downstream gating)

- **Reversal OK** = `(1 − trendiness) × chaosMult` — high in Range, low in clean Trend / Chaos.
- **Trend-follow OK** = `trendiness × chaosMult` — the symmetric complement.

These are *Quality* signals (skill §1): they shift the threshold of a downstream reversal/trend module, they do not block its trigger outright (skill §3, the over-filtering failure mode).

## Notes

- FDI length is treated as even (the older/recent half-windows use `length/2`).
- All thresholds are inputs — tune per timeframe/market rather than hardcoding into signal logic.
- HTF regime confirmation is a planned addition; v1.0 runs on the chart timeframe only.
