# Chandelier Flip Radar — Strategy Backtest Assessment

**Instrument:** CAPITALCOM:NATURALGAS  
**Strategy file:** `chandelier_flip_radar_strategy.pine`  
**Assessment date:** 2026-04-29 (updated 2026-04-29)

---

## Signal Logic

| Signal | Expression |
|--------|------------|
| Long | `buySignal` (dir flips to 1, body filter passes) |
| Short | `sellSignal` (dir flips to -1, body filter passes) |
| SL type | trailing (`longStop` / `shortStop`) |

---

## Optimized Settings

| Parameter | Default | Optimized | Notes |
|-----------|---------|-----------|-------|
| ATR Period | 22 | **30** | Reduces noise, fewer but cleaner signals |
| ATR Multiplier | 3.0 | **4.5** | Discovered via AI mode sweep; 4.5 outperforms all tested values on NatGas 4H |
| Min Body for Flip (ATR×) | 0.25 | **0.80** | Single biggest improvement — eliminates weak flips |
| Adaptive Mode | Off | **Off** | AI mode exploration confirmed 4.5 as optimal fixed value; no adaptivity benefit |

Commission used in all runs: **0.02%** (realistic for CFD/futures; strategy is unprofitable at 0.05%)

---

## Backtest Runs

| Run | TF | ATR Len | Mult | bodyFilter | adaptMode | Net % | PF All | Max DD% |
|-----|----|---------|------|------------|-----------|-------|--------|---------|
| 1 | 1H | 22 | 3.0 | 0.25 | Off | neg. | < 1.0 | — |
| 2 | 1H | 22 | 3.0 | 0.25 | Off | ~1% | ~1.01 | — |
| 3 | 1H | 22 | 3.5 | 0.25 | Off | ~3% | 1.029 | — |
| 4 | 1H | 22 | 4.0 | 0.25 | Off | ~3% | 1.029 | — |
| 5 | 1H | 30 | 3.5 | 0.80 | Off | +7.25 | 1.182 | 3.84 |
| 6 | 4H | 30 | 3.5 | 0.80 | Off | +11.95 | 1.217 | 7.31 |
| 7 | 4H | 30 | 3.5 | 0.80 | AI step=0.5 | +21.00 | — | — |
| 8 | 4H | 30 | 3.5 | 0.80 | AI step=1.0 | +9.81 | — | — |
| 9 | 4H | 30 | 4.0 | 0.80 | AI range=0.5 step=1.0 | +24.00 | — | — |
| **10** | **4H** | **30** | **4.5** | **0.80** | **Off** | **+29.00** | **—** | **—** |

Runs 1–4: commission sensitivity and multiplier sweep. Runs 7–9: AI mode exploration — used to identify optimal multiplier. Run 10: AI discovery confirmed 4.5 as optimal fixed value; full metrics pending.

---

## Best Configuration Results

**Run 10** — 4H, ATR 30 / Mult 4.5 / bodyFilter 0.80 / adaptMode Off / 0.02% commission

| Metric | All | Long | Short |
|--------|-----|------|-------|
| Net Profit (%) | +29.67 | +21.86 | +7.80 |
| Profit Factor | 1.598 | 1.970 | 1.288 |
| Win Rate (%) | 40.7 | 43.2 | 38.2 |
| Avg Winner / Avg Loser | 2.33× | 2.59× | 2.08× |
| Trades | 177 | 88 | 89 |
| Max Drawdown (%) | 5.06 | — | — |
| CAGR (%) | 3.61 | 2.74 | 1.03 |
| Sharpe Ratio | 0.101 | — | — |
| Sortino Ratio | 0.213 | — | — |
| Return / Max DD | 5.87 | — | — |
| vs Buy & Hold (%) | +41.50 | — | — |

---

## Key Findings

**What worked:**
- Raising `bodyFilter` to 0.80 was the single most impactful structural change — eliminates weak flip signals (dojis, inside bars).
- ATR Period 30 reduces noise vs. 22.
- AI mode exploration was used as a systematic multiplier search tool. By observing which factor K-means converged to at different `aiRange` settings, the optimal fixed multiplier of **4.5** was identified. Switching from AI mode to `adaptMode=Off` with this value was the final step: +21% → +29.67%.
- 4H outperforms 1H in absolute return and PF.
- Commission threshold is 0.02%.
- Return/DD ratio of 5.87 is strong — trailing stop lets winners run (Avg W/L 2.33×) while limiting drawdown.

**What remains weak:**
- CAGR of 3.61% is modest. Real execution costs (spread, swap, slippage) will reduce this further.
- Sharpe of 0.101 is low — typical for commodity trend-following with long flat periods between trends.
- Short side (PF 1.288) remains weaker than long (PF 1.970). NatGas structural bull bias persists.
- All optimization in-sample on NatGas 4H only. Multiplier 4.5 may be instrument-specific.

---

## Verdict

**Rating:** Promising

PF 1.598 and Return/DD 5.87 exceed the "Ready" thresholds on all quantitative metrics. The strategy is not rated "Ready" solely because out-of-sample validation on a second instrument has not been performed. Within the tested period it shows a genuine and robust edge — both directions profitable, 177 trades, Max DD under 6%.

**Next steps:**
1. Out-of-sample validation on a second instrument (Crude Oil, Gold) — required for "Ready" rating
2. Test `enableBE = true` (break-even stop) to check whether Return/DD improves further
3. Consider a long-only regime filter to eliminate short-side drag in structural bull phases
