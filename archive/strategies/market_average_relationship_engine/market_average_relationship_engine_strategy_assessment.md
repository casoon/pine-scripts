# Market–Average Relationship Engine — Strategy Backtest Assessment

**Instrument:** not yet tested
**Strategy file:** `market_average_relationship_engine_strategy.pine`
**Assessment date:** 2026-08-01 (generated, not yet backtested)

---

## Signal Logic

| Signal | Expression |
|--------|------------|
| Long   | `strategyLongSignal` = `bullishPullback or bullishMomentum` |
| Short  | `strategyShortSignal` = `bearishPullback or bearishMomentum` |
| SL type | trailing (`longStop`/`shortStop` = reference MA ∓ `stopAtrMultInput` × ATR) |

Divergence and Turn From Extreme are deliberately excluded from entries — both are reversal-style, early signals, while Pullback/Momentum are continuation setups already gated on an established, quality-checked trend. Mixing the two into one OR'd signal would blend trend-following and reversal logic in a single trigger, which this repo's indicator-design rules call out as an anti-pattern. A separate reversal-flavored variant (Divergence/Turn only) is a candidate for a future strategy, not this one.

---

## Optimized Settings

| Parameter | Default | Optimized | Notes |
|-----------|---------|-----------|-------|
| MA family / length | EMA / 50 | — | not yet tuned |
| Minimum trend quality | 55 | — | not yet tuned |
| Minimum respect | 55 | — | not yet tuned |
| Pullback prior extension (ATR) | 0.70 | — | not yet tuned |
| Compression / acceleration thresholds | 65 / 60 | — | not yet tuned |
| Stop distance from MA (ATR×) | 2.5 | — | not yet tuned |

Commission used in all runs: 0.02%

---

## Backtest Runs

No runs yet.

---

## Best Configuration Results

Not yet available.

---

## Key Findings

**What worked:**
- Not yet tested.

**What remains weak:**
- No backtest has been run. Score-model thresholds (trend quality, respect, extension, exhaustion) were carried over from the indicator's plausible starting defaults, not empirically calibrated.
- The trailing stop (`ma ∓ ATR×`) has not been checked for viability against the default 50-length MA — on a slow MA this may sit far from price on the first entries of a new trend, before the ratchet-free per-bar envelope tightens.

---

## Verdict

**Rating:** Not ready

Freshly generated from `market_average_relationship_engine.pine` v1.2.0 — no backtest data exists yet. Next step is a first Strategy Tester pass on 1–2 instruments/timeframes to establish a baseline before any parameter tuning.

**Next steps:**
1. Run a baseline backtest (1H/4H/1D) on at least one liquid instrument.
2. Check whether the MA-anchored trailing stop (`stopAtrMultInput`) needs a different anchor (e.g. `close`-based chandelier) if the 50-length default MA proves too slow to trail effectively.
3. Validate Pullback vs. Momentum entries separately (split PF) before judging the combined signal.
