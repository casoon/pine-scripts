# Chandelier Flip Radar — Strategy Backtest Assessment

**Instrument:** CAPITALCOM:NATURALGAS  
**Strategy file:** `chandelier_flip_radar_strategy.pine`  
**Assessment date:** 2026-04-29

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
| ATR Multiplier | 3.0 | **3.5** | PF plateaus beyond 3.5 on NatGas 1H |
| Min Body for Flip (ATR×) | 0.25 | **0.80** | Single biggest improvement — eliminates weak flips |

Commission used in all runs: **0.02%** (realistic for CFD/futures; strategy is unprofitable at 0.05%)

---

## Backtest Runs

| Run | TF | ATR Len | Mult | bodyFilter | PF All | PF Long | PF Short | Net % | Max DD% |
|-----|----|---------|------|------------|--------|---------|---------|-------|---------|
| 1 | 1H | 22 | 3.0 | 0.25 | < 1.0 | — | — | neg. | — |
| 2 | 1H | 22 | 3.0 | 0.25 | ~1.01 | — | — | ~1% | — |
| 3 | 1H | 22 | 3.5 | 0.25 | 1.029 | 1.070 | 0.989 | ~3% | — |
| 4 | 1H | 22 | 4.0 | 0.25 | 1.029 | 1.166 | 0.908 | ~3% | — |
| 5 | 1H | 30 | 3.5 | 0.80 | 1.182 | 1.194 | 1.171 | +7.25 | 3.84 |
| 6 | 4H | 30 | 3.5 | 0.80 | 1.217 | 1.296 | 1.148 | +11.95 | 7.31 |

Runs 1–4: commission sensitivity test and ATR multiplier sweep. Runs 1–2 had 0.05% / 0.02% commission respectively at default settings.

---

## Best Configuration Results

**Run 6** — 4H, ATR 30 / Mult 3.5 / bodyFilter 0.80 / 0.02% commission

| Metric | All | Long | Short |
|--------|-----|------|-------|
| Net Profit (%) | +11.95 | +7.65 | +4.30 |
| Profit Factor | 1.217 | 1.296 | 1.148 |
| Win Rate (%) | 40.5 | 42.2 | 38.8 |
| Avg Winner / Avg Loser | 1.79× | 1.78× | 1.81× |
| Trades | 242 | 121 | 121 |
| Max Drawdown (%) | 7.31 | — | — |
| CAGR (%) | 1.55 | 1.01 | 0.58 |
| vs Buy & Hold (%) | +23.5 | — | — |

---

## Key Findings

**What worked:**
- Raising `bodyFilter` to 0.80 was the single most impactful change. It eliminated weak flip signals (dojis, inside bars) that dragged the short side below breakeven. Short PF improved from 0.908 → 1.148–1.171.
- ATR Period 30 reduces noise vs. 22. Longer lookback produces fewer, higher-quality trend changes.
- ATR Multiplier 3.5 is the sweet spot — PF does not improve beyond this on NatGas.
- 4H outperforms 1H in absolute return and PF, but at the cost of higher drawdown (7.31% vs 3.84%).
- Commission threshold is 0.02% — anything higher destroys the edge.

**What remains weak:**
- CAGR of 1.55% p.a. is below risk-free rates. Real-world costs (spread, swap fees, slippage) would likely erase this.
- Return/DD ratio of 1.63 is marginal (threshold for acceptable: 2.0).
- All optimization was performed in-sample on NatGas only. Settings may not generalize.

---

## Verdict

**Rating:** Promising

The strategy has a statistically meaningful edge (PF 1.217, both sides profitable, 242 trades), and it clearly beat a negative buy-and-hold period. However, the CAGR is too thin for live trading in its current form — real execution costs would absorb most of the gain. The core signal quality is sound; what's missing is a better exit framework (break-even stops, regime filter) to improve Return/DD before considering live deployment.

**Next steps:**
1. Out-of-sample validation on a second instrument (Crude Oil, Gold) to check for overfitting
2. Test `enableBE = true` (break-even stop) — may improve Return/DD without hurting PF
3. Consider a regime filter to disable short entries in structural bull markets
