# Pine Scripts by WavesUnchained

**Pine Version:** v6 &nbsp;·&nbsp; **License:** [MIT](LICENSE) &nbsp;·&nbsp; **Author:** [WavesUnchained](https://www.tradingview.com/u/WavesUnchained/)

> A collection of custom TradingView indicators built around composable analysis — market structure, trend, momentum, and confluence scoring.

---

## About this repository

This is a running collection of ideas, not a finished product catalog. Its purpose is to
explore Pine Script and chart-technical concepts, with quality treated as an ongoing process
carried out with AI assistance. That process covers fundamentals, not just code correctness:
whether an indicator's logic is conceptually sound, whether it's plausible on the specific
instrument it's meant to run on, and whether it consumes the right inputs in the first place
rather than data that looks available but carries no real signal (e.g. volume on instruments
where it doesn't reflect real trades). The project's Claude Code skills (`.claude/skills/`)
exist to enforce exactly that: `instrument-data-validity` checks input plausibility per
instrument, `indicator-review` diagnoses signal-logic soundness, and `indicator-code-audit`
covers technical correctness and repo conventions.

---

## Getting Started

1. Open any `.pine` file and copy its contents
2. In TradingView: **Pine Script Editor → Paste → Add to Chart**

---

## Data validity

Which data class carries a real signal on which instrument type — volume, VWAP, open interest,
term structure, cross-symbol requests: [`DATA_VALIDITY.md`](DATA_VALIDITY.md).
Run `python3 scripts/audit_data_sources.py` to scan all scripts against it.

---

## Indicators

Full indicator index, grouped by focus, with one-line descriptions and links to each script:
[`INDICATORS.md`](INDICATORS.md). Status, quality ratings and version history:
[`CATALOG.md`](CATALOG.md).

---

## Strategies

Every strategy under `strategies/` is **standalone and hand-maintained**. Each wraps one
indicator's signal logic in a `strategy()` call and adds a trade direction filter,
confirmed-bar gate, cooldown, optional break-even stop and a non-standard-chart-type guard.

Building or updating one is a guided task rather than a script — the Claude Code skill
`strategy-from-indicator` (`.claude/skills/`) carries the input groups, the exit patterns
and the transformation rules.

| Strategy | Based on | SL type | Status |
|----------|----------|---------|--------|
| [`chandelier_flip_radar_strategy.pine`](strategies/chandelier_flip_radar/chandelier_flip_radar_strategy.pine) | Chandelier Flip Radar | Trailing | Promising |
| [`market_average_relationship_engine_strategy.pine`](strategies/market_average_relationship_engine/market_average_relationship_engine_strategy.pine) | Market–Average Relationship Engine | Trailing (MA ∓ ATR×) | Not ready — not yet backtested |
| [`oscillator_divergence_zones_strategy.pine`](strategies/oscillator_divergence_zones/oscillator_divergence_zones_strategy.pine) | Oscillator Divergence Zones | Pivot ATR | Promising |
| [`smooth_trend_radar_strategy.pine`](strategies/smooth_trend_radar/smooth_trend_radar_strategy.pine) | Smooth Trend Radar | Fixed TP | Promising (Long Only) |
| [`wavetrend_v4_strategy.pine`](strategies/wavetrend/wavetrend_v4_strategy.pine) | WaveTrend v4 | Trailing | Promising |
| [`reversal_engine_score_strategy.pine`](strategies/reversal_engine_score/reversal_engine_score_strategy.pine) | Reversal Engine Score | Structural + R-multiple TP | Not ready |
| [`commodity_pulse_matrix_v4_strategy.pine`](strategies/commodity_pulse_matrix/commodity_pulse_matrix_v4_strategy.pine) | Commodity Pulse Matrix v4 | Directional fixed TP | Not ready — not yet backtested |

Backtest results and parameter notes live in `strategies/<name>/<name>_strategy_assessment.md`
— that is the only place figures belong. Schema: [`strategies/ASSESSMENT_SCHEMA.md`](strategies/ASSESSMENT_SCHEMA.md).

---

*These scripts are for educational and informational purposes only. Not financial advice. Trading involves substantial risk of loss.*
