# Exhaustion Scanner

Weighted top/bottom exhaustion score (0–100) built from five component scores — distance, momentum, money flow, volatility, structure — with per-market weight presets and a component breakdown dashboard. Generalizes the [commodity_heat_reversal](../commodity_heat_reversal/) concept (discrete 0–7 points, commodity-tuned) into a continuous, market-adaptive score.

## Features

- **Five components** (each 0–100):
  - **Distance** — close vs. EMA50 in ATR units, Bollinger z-score
  - **Momentum** — RSI, smoothed StochRSI, WaveTrend level, active WT divergence
  - **Money Flow** — MFI extreme + volume spike (spike counts toward both sides: blow-off tops *and* capitulation bottoms)
  - **Volatility** — ATR expansion vs. 50-bar average + bar range in ATR
  - **Structure** — proximity to the N-bar high/low (ATR-scaled), wick pressure, BB breach
- **Market presets** with weight profiles:

  | Preset | Distance | Momentum | Flow | Volatility | Structure |
  |---|---|---|---|---|---|
  | Stocks | 25 | 25 | 30 | 10 | 10 |
  | Commodities | 30 | 25 | 10 | 25 | 10 |
  | Forex/CFD | 35 | 35 | 0 | 20 | 10 |
  | Crypto | 25 | 30 | 20 | 20 | 5 |
  | Custom | free | free | free | free | free |

  Stocks weight Flow highest (real centralized volume), Forex/CFD disables it (no reliable volume).
- **Signal modes** — Early (≥ 30), Normal (≥ 40), Conservative (≥ 50)
- **Trigger score** — labels use the strongest signal evidence (weighted total, component stretch, or divergence boost), while the dashboard still shows the weighted component total
- **Confirmation modes**:
  - **Score Only** — marks the first bar that reaches the selected threshold
  - **Candle Reaction** — waits for a rejection candle / close-through behavior before labeling
  - **Pivot Confirmed** — delayed, but anchors the label on the confirmed swing high/low
- **Divergence assist** — WT divergences near stretched price or structure can create setup labels before the full weighted score reaches exhaustion level
- **Signal spacing** — optional minimum bars between same-side labels to reduce clusters in trends
- **Heatmap background** — full intensity at signal level, faint within 10 points below
- **Extreme candidates** as faint dots; confirmed exhaustion labels with score; WT divergence triangles with validity window
- **Dashboard** — total + per-component breakdown for both sides, preset and mode
- **Alerts** — Top Exhaustion, Bottom Exhaustion, Any

## Relation to commodity_heat_reversal

Same idea, different mechanics: CHR scores discrete points (0–7) with a trend filter and SL/TP overlay — tuned for commodity 4H mean reversion. The scanner produces a continuous weighted score with market presets, component transparency, and optional signal confirmation. Use CHR for commodity reversal *entries*, the scanner for cross-market exhaustion *monitoring*.
