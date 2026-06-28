# Signal Quality Engine

A range-fade signal engine for commodities, futures, stocks and indices. One thing done well: it fades the range edges — long the exhausted lows, short the exhausted highs — when the market is ranging, price is stretched from the mean, structure says "edge", and a candle rejects. A regime gate (ADX + EMA slope) stands the tool down in strong trends, so it never fades a trend pullback. No regime switching, no MTF, no divergence, no pivot-based signals — a single, legible logic with an **Edge → Setup → Watch → Trigger** read.

## The one logic (mirrored both sides)

Range regime ok → price stretched to an edge (distance + structure) → momentum turns back off the edge → candle rejects → score high enough → **Trigger** (fade).

1. **Edge** — which side is exhausted (the dominant of the top/bottom exhaustion scores). Situation-driven: being stretched to the low *is* a long-fade situation. Shown as `Low → Long`, `High → Short`, or `Mid-range`.
2. **Setup** (gray circle) — exhaustion is building at an edge (score over the setup threshold).
3. **Watch** (yellow circle) — the exhaustion score has reached its threshold (the "extreme"); a rejection is still pending.
4. **Trigger** (label) — a candle rejects (closes back off the edge) within the confirmation window of the extreme (cooldown permitting). Momentum is already inside the exhaustion score, so there is no separate momentum gate.

## Exhaustion score (0–100)

Adapted from the Exhaustion Scanner top/bottom logic, trimmed to three components and weighted:

| Component | Weight | What it measures |
|---|---|---|
| Distance | 40% | stretch past the mean — `(close−EMA50)/ATR` and Bollinger-Z |
| Structure | 30% | recent high/low proximity + wick rejection + close beyond the band |
| Momentum | 30% | RSI / StochRSI / WaveTrend overbought–oversold extreme |

Computed for both edges; the dominant side is the Edge. A Trigger fires only on the dominant edge, when its score clears the threshold, the candle rejects, and the cooldown has elapsed.

## Features

- **Range regime gate** — triggers, markers and alerts are suppressed unless `ADX < 24` and the EMA50 slope is flat (`< 0.45 ATR/bar`); in a trend the dashboard reads `Trending — fade off`.
- **Edge detection** — "near high/low" requires both proximity to the 80-bar extreme and price in the outer fifth of that range, so a trending extreme alone is not an edge.
- **Sweep-and-reclaim rejection** — the candle trigger looks for a liquidity sweep of the prior bar's extreme that closes back inside, or a strong opposing wick.
- **Edge bias from the situation** — the exhausted side, not a trend guess; stable because it reflects where price actually sits in the range.
- **Candle-rejection confirmation** — the trigger waits for price to close back off the edge.
- **Confirmation window** — a rejection within `Confirmation Window` bars (default 3) of the exhaustion extreme still triggers, so a one-bar timing miss doesn't void the setup.
- **Market profiles (asset-aware)** — each profile sets band width, edge proximity, and the regime tolerance (`adxMax` / `slopeMax`) that decides how trendy the tape can be and still be faded. Commodities (esp. Natural Gas) mean-revert through choppy trends, so they fade readily with wider bands; Stocks/Indices trend persistently and get a stricter range filter with tighter bands.
- **Strictness presets** — Very Strict / Strict / Balanced set both the exhaustion threshold and the cooldown.
- **ATR risk levels** — SL beyond the edge, TP1 at the mean, TP2 at the opposite band (mean-reversion oriented).
- **Pivot reference markers** — control overlay only; never feed any signal, grade or gate.
- **Light-theme dashboard** with a "why no trigger" status line, and four alerts (long / short / any / watch).

## Design notes

- **One model, on purpose: a range fader.** In a strong trend it is intentionally quiet — it does not also try to be a trend system. Use a trend tool there.
- **Pivots are a control overlay, never an input.** Edge location is judged through pivot-free measures (distance, band, recent high/low, wick, momentum).
- **Rules are symmetric.** Long-fade and short-fade logic mirror each other; the asymmetry is the situation (which edge is exhausted).
- **Chart-TF only** — no `request.security`, so confirmed-bar signals do not repaint. Intended primarily for the 4H timeframe.
