# Pine Scripts by WavesUnchained

**Pine Version:** v6 &nbsp;·&nbsp; **License:** [MIT](LICENSE) &nbsp;·&nbsp; **Author:** [WavesUnchained](https://www.tradingview.com/u/WavesUnchained/) &nbsp;·&nbsp; **Docs:** [casoon.github.io/pine-scripts](https://casoon.github.io/pine-scripts/)

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

## Known pitfalls and limits of Pine

Several scripts in this collection produced wrong or misleading results without any compile
error. Many were fixed or archived; older or less checked scripts may still contain some of
these patterns:

- **Data without signal:** tick volume read as trade volume, `nz(volume)` or `volume = 1.0` as
  a "guard", and the weight of a missing volume part moved onto price oscillators.
- **Hindsight on the chart:** pivots and divergences drawn at the extreme although they are
  confirmed bars later; `request.security()` reading the unclosed higher-timeframe bar; labels
  and scores computed from bars after the event.
- **Pine v6 short-circuiting:** stateful `ta.*` calls behind `and`/`or`/`?:` or inside an `if`
  skip bars and return wrong values silently.
- **Scores that measure something else:** one price series counted as four votes (RSI,
  StochRSI, CCI, WaveTrend), direction derived from volatility, long and short not mirrored,
  and names like "Hurst", "dominant cycle", "divergence" or "Probability %" that the formula
  does not support.
- **Strategy Tester traps:** no stop on the first bar after entry, costs left out, history cut
  to 500 bars, and filters tuned and judged on the same data.

Pine is good for showing where the market stands, alerts on closed bars, quick prototypes and
reference values for another implementation. It cannot show that a signal beats chance, has no
order flow, open interest or bid/ask on most symbols, and sees one symbol at a time. Rebuilding
the logic outside TradingView (Kestrel, a separate Rust engine) is where several of these errors
surfaced. Details: [Pitfalls and limits](docs/concepts/pitfalls-and-limits.md).

---

## Indicators

Full indicator index, grouped by focus, with one-line descriptions and links to each script:
[`INDICATORS.md`](INDICATORS.md). Status, quality ratings and version history:
[`CATALOG.md`](CATALOG.md).

---

## Strategies

Every strategy under `strategies/` is **standalone and hand-maintained**. Each wraps one
indicator's signal logic in a `strategy()` call and adds a trade direction filter,
confirmed-bar gate, cooldown, optional break-even stop, a non-standard-chart-type guard, a CFD cost
model (spread, financing, stress factor) and a random-entry baseline for comparison.

Building or updating one is a guided task rather than a script — the Claude Code skill
`strategy-from-indicator` (`.claude/skills/`) carries the input groups, the exit patterns
and the transformation rules.

| Strategy | Based on | SL type | Status |
|----------|----------|---------|--------|
| [`chandelier_flip_radar_strategy.pine`](strategies/chandelier_flip_radar/chandelier_flip_radar_strategy.pine) | Chandelier Flip Radar | Trailing | Not ready — measured before the v1.6 ratchet fix |
| [`oscillator_divergence_zones_strategy.pine`](strategies/oscillator_divergence_zones/oscillator_divergence_zones_strategy.pine) | Oscillator Divergence Zones | Pivot ATR | Not ready |
| [`smooth_trend_radar_strategy.pine`](strategies/smooth_trend_radar/smooth_trend_radar_strategy.pine) | Smooth Trend Radar | Fixed TP | Not ready — measured only in the window it was tuned on |
| [`wavetrend_v4_strategy.pine`](strategies/wavetrend/wavetrend_v4_strategy.pine) | WaveTrend v4 | Trailing | Not ready — v5.0 not yet backtested |
| [`reversal_engine_score_strategy.pine`](strategies/reversal_engine_score/reversal_engine_score_strategy.pine) | Reversal Engine Score | Structural + R-multiple TP | Not ready |
| [`kestrel_opportunity_lens_strategy.pine`](strategies/kestrel_opportunity_lens/kestrel_opportunity_lens_strategy.pine) | Kestrel Opportunity Lens | Time exit, no stop (evaluation) | Not ready — NatGas 4h tested, 4 setup models |

Backtest results and parameter notes live in `strategies/<name>/<name>_strategy_assessment.md`
— that is the only place figures belong. Schema: [`strategies/ASSESSMENT_SCHEMA.md`](strategies/ASSESSMENT_SCHEMA.md).
Archived indicators and strategies with reasons and recovery notes: [`archive/README.md`](archive/README.md).

---

*These scripts are for educational and informational purposes only. Not financial advice. Trading involves substantial risk of loss.*
