# Regime Detector (MA Zones Overlay)

MA-zone based trend regime overlay with an adaptive core engine, higher-timeframe gate, an optional trade engine (one entry per regime start), and an optional SSA (Smart Signals Assistant) layer with trade management.

## Features

- **Adaptive core engine** — KAMA-style hybrid line; smoothing alpha adapts to the efficiency ratio of recent price action (configurable alpha range and gamma)
- **Regime detection** — Bull / Bear / Flat classification from normalized line slope and efficiency ratio, with enter/exit hysteresis on both ER and confidence
- **Volatility dimension** (v1.1) — a second axis (Quiet / Normal / Volatile) from ATR percentile + Bollinger-width percentile, combining with direction into "Quiet Bull", "Volatile Range", "Compression" etc.
- **Regime maturity** (v1.1) — Fresh / Mature / Mature-strong / Aging-weakening, with a transition warning when slope turns against the regime, efficiency drops below the exit threshold, or strength fades below 50% of its peak
- **RS vs. benchmark** (v1.1, optional) — relative strength vs. SPY/QQQ as an equities modifier, shown as a dedicated panel line
- **Modern visuals** (v1.1) — Visual Theme selector (Modern / Soft / Classic), soft gradient ATR bands, a volatility-aware regime heatmap, and a default-on Regime Candle Tint (direction × volatility); info panel defaults to Bottom Left (clear of the SSA table and broker overlay)
- **Context labels** (v1.1) — COMPRESS / EXPAND / AGING markers on the chart for the volatility and maturity transition events
- **Multi-timeframe gate** — three higher timeframes (auto-stacked from the chart TF) vote with configurable weights; signals require a minimum weighted agreement
- **Advanced filters** — volatility (static/adaptive/dynamic ATR%), optional volume filter, market-condition classification, combined into one explicit filter condition
- **Profile presets** — Smart, Futures, Spot, ETF, Crypto parameter sets
- **MA Overlay Zones** — optional regime-gated entry/SL zones from an MA fan (SMA/EMA/DEMA/TEMA/JMA)
- **SSA layer** — signal engine (Trend/Reversal mode) or RDP-event driven entries, Fair Value Trail, trend bias band, ATR clouds
- **Trade management** — TP/SL boxes with risk/reward ratio, trailing stop (FVT/Cloud/Line source), time stop
- **Alert builder** — up to 7 chainable conditions (AND/OR) including external series inputs
- **Logging** — optional Pine-log export of label metrics (last 2000 bars, step 10) for offline analysis

## Engine pipeline

1. **Adaptive Engine** — adaptive line, ATR, efficiency ratio, normalized slope
2. **Regime Detection** — regime state with hysteresis (separate enter/exit thresholds)
3. **MTF Gate** — weighted HTF agreement via `request.security` (EMA-50 side per TF, last closed HTF bar — no repaint)
4. **Filter System** — filter condition and market condition (Trending/Neutral/Choppy)
5. **Signal Generation** — one entry per regime start (after confirmation bars, filter and HTF gate), band/regime-based exits, cooldown

## Filter condition

With **Enable Advanced Filter System** on, an RDP entry and the SSA gate (with **Use RDP as Primary Gate**) need:

`volOk and (volGate or trendScore > 0.2)`

- `volOk` — ATR/price at or above the volatility threshold (Static / Adaptive / Dynamic mode)
- `volGate` — volume at or above `Volume Quantile × Volume MA`; passes when the volume filter is off or the symbol has no real trade volume
- `trendScore` — average absolute normalized slope over the Market Analysis Period

With the filter system off, the condition always passes. The alert builder offers it as `Filter OK`; the Pine-log export writes it as `filter=true/false`.

## Signals & visuals

- Triangle markers: RDP entries (trade engine on)
- Warning labels: `MTF` (HTF divergence), `CHOP` (ranging), `VOL` (low volatility) — event-based with cooldown
- Regime heatmap background, ATR entry/exit bands, adaptive line
- SSA: long/short markers, FVT line, bias band, clouds, TP/SL boxes
- Info panel and SSA status table (light-theme style)

## Regime Context (v1.1)

The context layer is additive — it does not change the direction engine, it interprets it.

Combined regimes: Quiet / Normal / Volatile × Bull / Bear / Range (Quiet Range = Compression). Maturity and the AGING label describe how far the current regime has run; RS leading/lagging shows whether the symbol outpaces its benchmark (default SPY; QQQ for tech/momentum names).

## Notes

- Inputs marked **(WIP)** are exposed but not yet wired into the engine
- The volatility rank and RS both need history (`Volatility Rank Lookback`, `RS MA Length`) before they read meaningfully; on fresh charts they start neutral
