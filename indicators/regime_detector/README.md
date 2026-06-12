# Regime Detector (MA Zones Overlay)

MA-zone based trend regime overlay with an adaptive core engine, higher-timeframe gate, tiered signal quality, and an optional SSA (Smart Signals Assistant) layer with trade management.

## Features

- **Adaptive core engine** — KAMA-style hybrid line; smoothing alpha adapts to the efficiency ratio of recent price action (configurable alpha range and gamma)
- **Regime detection** — Bull / Bear / Flat classification from normalized line slope and efficiency ratio, with enter/exit hysteresis on both ER and confidence
- **Volatility dimension** (v1.1) — a second axis (Quiet / Normal / Volatile) from ATR percentile + Bollinger-width percentile, combining with direction into "Quiet Bull", "Volatile Range", "Compression" etc.
- **Regime maturity** (v1.1) — Fresh / Mature / Mature-strong / Aging-weakening, with a transition warning when slope turns against the regime, efficiency drops below the exit threshold, or strength fades below 50% of its peak
- **Playbook line** (v1.1) — plain-language action hint for the current combined regime
- **RS vs. benchmark** (v1.1, optional) — relative strength vs. SPY/QQQ as an equities modifier; appends RS leading/lagging to the playbook + a dedicated panel line
- **Modern visuals** (v1.1) — Visual Theme selector (Modern / Soft / Classic), soft gradient ATR bands, a volatility-aware regime heatmap, and a default-on Regime Candle Tint (direction × volatility); info panel defaults to Bottom Left (clear of the SSA table and broker overlay)
- **Context labels** (v1.1) — COMPRESS / EXPAND / AGING markers on the chart for the volatility and maturity transition events
- **Multi-timeframe gate** — three higher timeframes (auto-stacked from the chart TF) vote with configurable weights; signals require a minimum weighted agreement
- **Advanced filters** — volatility (static/adaptive/dynamic ATR%), optional volume filter, market-condition classification, confluence scoring
- **Quality tiers** — entries are graded A / B / LOWQ from confidence, HTF agreement, and signal quality thresholds
- **Profile presets** — Smart, Futures, Spot, ETF, Crypto parameter sets
- **MA Overlay Zones** — optional regime-gated entry/SL zones from an MA fan (SMA/EMA/DEMA/TEMA/JMA)
- **SSA layer** — signal engine (Trend/Reversal mode) or RDP-event driven entries, Fair Value Trail, trend bias band, ATR clouds, Strong/Super tiers
- **Trade management** — TP/SL boxes with risk/reward ratio, pending limit-style entries with touch/close-confirm activation, trailing stop (FVT/Cloud/Line source), time stop
- **Alert builder** — up to 7 chainable conditions (AND/OR) including external series inputs
- **Logging** — optional Pine-log export of label metrics (last 2000 bars, step 10) for offline analysis

## Engine pipeline

1. **Adaptive Engine** — adaptive line, ATR, efficiency ratio, normalized slope
2. **Regime Detection** — regime state with hysteresis (separate enter/exit thresholds)
3. **MTF Gate** — weighted HTF agreement via `request.security` (EMA-50 side per TF)
4. **Filter System** — signal quality score 0..1 and market condition (Trending/Neutral/Choppy)
5. **Signal Generation** — tiered entries, band/regime-based exits, cooldown
6. **Performance Tracking** — win rate / profit factor of the internal position model (informational)

## Signals & visuals

- Triangle markers: RDP entries (solid = Tier A, faded = Tier B); `LOWQ` labels for rejected candidates
- Warning labels: `MTF` (HTF divergence), `CHOP` (ranging), `VOL` (low volatility) — event-based with cooldown
- Regime heatmap background, ATR entry/exit bands, adaptive line
- SSA: `L/S`, `L+/S+` (Strong), `L++/S++` (Super) markers, FVT line, bias band, clouds, TP/SL boxes
- Info panel and SSA status table (light-theme style)

## Regime Context (v1.1)

The context layer is additive — it does not change the direction engine, it interprets it.

| Combined regime | Typical playbook |
|---|---|
| Quiet Bull / Bear | Healthy trend — buy pullbacks / sell rallies |
| Volatile Bull / Bear | Strong but stretched — ride, trail tight (climax risk) |
| Trend, aging | Tighten stops / bank profit |
| Compression (Quiet Range) | Await breakout |
| Volatile Range | Choppy — fade edges / stay out |

For equities, enable **RS vs. Benchmark** (default SPY; use QQQ for tech/momentum names). A bull regime with RS leading is a far higher-quality long than a bull regime that is merely riding the index.

## Notes

- Inputs marked **(WIP)** are exposed but not yet wired into the engine
- The performance metrics are based on a simplified internal position model, not a backtest
- The volatility rank and RS both need history (`Volatility Rank Lookback`, `RS MA Length`) before they read meaningfully; on fresh charts they start neutral
