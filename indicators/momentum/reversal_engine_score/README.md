# Reversal Engine Score v1

Score-based liquidity sweep reversal detector with HTF trend confluence. A signal fires only when all mandatory gates pass on a confirmed bar and the optional quality score meets the per-direction minimum. Designed and tested for the 15M timeframe (optional lockout on other TFs).

## Features

- Mandatory gate model — sweep + close position + body size + ATR corridor + HTF trend + spike filter must all pass
- Quality score (0–1 optional condition) with per-direction thresholds (Long/Short configurable separately)
- Optional quality condition mirrored per direction (RSI above 50 for longs, below 50 for shorts)
- Liquidity sweep detection: swing violation with recovery close on the same bar
- ATR corridor filter — rejects both low-volatility noise and spike/news regimes
- Spike filter — blocks sweeps deeper than N×ATR (real breakdowns, not reversals)
- Structural SL: sweep low/high plus configurable ATR noise buffer; TP as R-multiple of actual risk
- HTF trend filter via dual EMA on a configurable timeframe (last closed HTF bar, no repaint)
- Configurable Reclaim MA (EMA / RMA / SMA / WMA / HMA / JMA)
- Price structure labels (HH / HL / LH / LL) at confirmed pivots (optional)
- Outcome tracking: signal label turns blue when no follow-through within N bars
- Cooldown gate per direction to suppress signal chasing
- 15M-only lockout with orange background on other timeframes
- Hidden strategy-ready plots: direction, score, entry, stop, take
- Alert conditions for BUY / SELL / either

## Signal model

**Mandatory gates (all required):**

| Gate | Long condition |
|------|----------------|
| Liquidity sweep | `low < prevSwingLow` and `close > prevSwingLow` |
| Close position | Close in upper third of the bar range |
| Body size | Body > ATR × minBodyAtr |
| ATR corridor | `atrLowFactor × atrBase < ATR < atrHighFactor × atrBase` |
| HTF trend | HTF fast EMA not below slow EMA (not bearish) |
| Spike filter | Sweep depth ≤ ATR × spikeAtrMult |

Shorts mirror all conditions, except the HTF gate (not bullish) and the optionals below.

**Optional quality point (0–1):**

| Direction | +1 |
|-----------|----|
| Long | RSI > 50 |
| Short | RSI < 50 |

Quality tiers: A (1), C (0). Signals require `minQualityLong` / `minQualityShort` (both default 0 — quality is optional). Pivot structure (LL / HH) is shown in the tooltip only.

## SL / TP

- **SL (long):** `min(low, prevSwingLow) − ATR × slAtrBuffer` — structure is the primary stop, the ATR buffer absorbs noise
- **TP (long):** `entry + risk × tpRMult` where risk = distance entry → structural SL

## Status

Under active rework — see `strategies/reversal_engine_score/todo.md` for the test131 analysis and v1.2 strategy roadmap.
