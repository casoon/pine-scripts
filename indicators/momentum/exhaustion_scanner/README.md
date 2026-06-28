# Exhaustion Scanner

Role-separated overextension / reversal-risk context. Three distinct role scores — **Stretch** (location), **Exhaustion** (momentum), **Reaction** (trigger) — are combined into a single 0–100 score, scaled by a volatility multiplier, and framed by a regime classifier. The regime never blocks a signal: it shifts the threshold and re-labels the signal as **Continuation Risk**, **Trend Exhaustion**, or **Range Fade**. This is a context / risk tool, not a blind buy/sell generator — it answers "don't keep chasing here", not "reverse now".

It generalizes the [commodity_heat_reversal](../commodity_heat_reversal/) concept (discrete 0–7 points, commodity-tuned) into a continuous, market-adaptive, role-attributable score.

## Roles

The score is built from three roles so every signal is attributable to *what* drove it:

- **Stretch (Location)** — close vs. EMA in ATR units, Bollinger z-score, proximity to the N-bar high/low, band breach. *Is price overextended?*
- **Exhaustion (Momentum)** — RSI, smoothed StochRSI, WaveTrend level, active WT divergence, and Money Flow (MFI + volume spike). *Is the move tiring?*
- **Reaction (Trigger)** — reclaim-fail (poke beyond the band/extreme then close back inside), WT cross *from* an extreme zone, wick rejection. *Did the market actually react?*

**Volatility** is applied as a multiplier (`0.85 + volScore/100 × 0.30`), not as a fourth directional component — high volatility amplifies a setup but does not by itself create exhaustion on both sides.

## Regime classifier

An EMA stack (fast/slow) plus ADX classifies the backdrop as **Trend ↑**, **Trend ↓**, or **Range**. The regime does two things — it never vetoes the signal:

1. **Threshold shift** — a signal that fights an established trend (e.g. a top signal in an uptrend) needs more score (the Countertrend Threshold Penalty) before it labels.
2. **Risk framing** — the label kind comes from the regime:

   | Signal | Trend ↑ | Trend ↓ | Range |
   |---|---|---|---|
   | Top (upside overextension) | Continuation Risk | Trend Exhaustion | Range Fade |
   | Bottom (downside overextension) | Trend Exhaustion | Continuation Risk | Range Fade |

   A *Continuation Risk* label is a warning against fading a live trend; a *Trend Exhaustion* label is the more actionable counter-move setup.

## Market presets

Per-market role-weight profiles. Money Flow is folded into the Exhaustion role and auto-disabled where there is no real centralized volume.

| Preset | Stretch | Exhaustion | Reaction | Money Flow |
|---|---|---|---|---|
| Stocks | 35 | 35 | 30 | on |
| Commodities | 40 | 35 | 25 | on |
| Forex/CFD | 45 | 30 | 25 | off |
| Crypto | 35 | 40 | 25 | on |
| Custom | free | free | free | toggle |

## Signals

- **Signal modes** — Early (base threshold 30), Normal (40), Conservative (50). The *effective* threshold per side is the base ± regime penalty − divergence relief.
- **One score** drives both the dashboard and the label — the number on the label is the same number in the dashboard.
- **Confirmation modes**:
  - **Score Only** — marks the first bar the score reaches the effective threshold
  - **Candle Reaction** — additionally requires a reaction (reclaim-fail / WT-cross-from-extreme / wick rejection)
- **Divergence assist** — an active WT divergence lowers the effective threshold by a configurable relief, so stretched + diverging price can label earlier. Divergences invalidate when price breaks beyond the divergence pivot, not just on the validity timer.
- **Signal spacing** — optional minimum bars between same-side labels.
- **Exhaustion zones** — each signal draws a box over the overextended price area (Bollinger band → extreme). The zone keeps extending right until price reclaims the band or it reaches the configured max age, so the *region* to avoid chasing into stays visible, not just the bar.
- **Heatmap background** — full intensity at signal level, faint at setup level.
- **Setup candidates** as faint dots; bold labels (▼/▲ headline) carry the risk kind, the dominant-role reason (Stretch / Momentum / Rejection / Divergence) and the score, with the full role breakdown — Score/threshold, Stretch/Exhaustion/Reaction, regime+ADX, vol multiplier — on hover; WT divergence triangles.
- **Dashboard** — per-role breakdown (Stretch / Exhaustion / Reaction) for both sides, effective threshold, volatility multiplier, regime + ADX, and the signal reason.
- **Alerts** — Top Risk, Bottom Risk, Any Risk.

## Relation to commodity_heat_reversal

Same idea, different mechanics: CHR scores discrete points (0–7) with a trend filter and SL/TP overlay — tuned for commodity 4H mean reversion. The scanner produces a continuous role-attributable score with market presets, a regime frame, and optional reaction confirmation. Use CHR for commodity reversal *entries*, the scanner for cross-market overextension *context*.
