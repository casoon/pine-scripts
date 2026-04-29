# Strategy Assessment Schema

Template for all `*_strategy.pine` backtest assessments.
One `*_strategy_assessment.md` file per strategy, placed in `strategies/`.

---

## File naming

`{indicator_name}_strategy_assessment.md`

---

## Schema

```markdown
# {Indicator Name} — Strategy Backtest Assessment

**Instrument:** {exchange}:{symbol}
**Strategy file:** `{indicator_name}_strategy.pine`
**Assessment date:** YYYY-MM-DD

---

## Signal Logic

| Signal | Expression |
|--------|------------|
| Long   | {long signal variable(s)} |
| Short  | {short signal variable(s)} |
| SL type | trailing / fixed / pivot_atr |

---

## Optimized Settings

| Parameter | Default | Optimized | Notes |
|-----------|---------|-----------|-------|
| ...       | ...     | ...       | ...   |

Commission used in all runs: X.XX%

---

## Backtest Runs

| Run | TF | {param1} | {param2} | ... | PF All | PF Long | PF Short | Net % | Max DD% |
|-----|----|----------|----------|-----|--------|---------|---------|-------|---------|
| 1   | 1H | ...      | ...      | ... | ...    | ...     | ...     | ...   | ...     |

---

## Best Configuration Results

**Run:** {N} — {TF}, {key settings summary}

| Metric | All | Long | Short |
|--------|-----|------|-------|
| Net Profit (%) | | | |
| Profit Factor | | | |
| Win Rate (%) | | | |
| Avg Winner / Avg Loser | | | |
| Trades | | | |
| Max Drawdown (%) | | | |
| CAGR (%) | | | |
| vs Buy & Hold (%) | | | |

---

## Key Findings

**What worked:**
- ...

**What remains weak:**
- ...

---

## Verdict

**Rating:** Not ready / Promising / Ready

{2–4 sentence summary of edge quality, real-world viability, and what would need to change to improve the rating.}

**Next steps:**
1. ...
```

---

## Rating definitions

| Rating | Criteria |
|--------|----------|
| **Not ready** | PF < 1.15, CAGR below risk-free rate, or Return/DD < 1.5 |
| **Promising** | PF ≥ 1.15, both sides positive, but not yet validated out-of-sample |
| **Ready** | PF ≥ 1.3, CAGR meaningfully above risk-free rate, Return/DD ≥ 2.0, validated on ≥ 2 instruments |
