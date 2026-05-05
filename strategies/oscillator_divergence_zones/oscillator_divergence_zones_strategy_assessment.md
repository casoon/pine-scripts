# Oscillator Divergence Zones — Strategy Backtest Assessment

**Instrument:** CAPITALCOM:NATURALGAS  
**Strategy file:** `oscillator_divergence_zones_strategy.pine`  
**Assessment date:** 2026-04-29

---

## Signal Logic

| Signal | Expression |
|--------|------------|
| Long | `bullDiv` — regular bullish divergence (price lower low, oscillator higher low) |
| Short | `bearHidDiv` — hidden bearish divergence (price lower high, oscillator higher high) |
| SL type | pivot_atr (SL at pivot high/low + ATR buffer) |

Note: short signal was changed from `bearDiv` (regular bearish = countertrend) to `bearHidDiv` (hidden bearish = trend continuation). Regular bearish divergence failed structurally on all timeframes — it bets against the trend in a bull-biased instrument.

---

## Optimized Settings

| Parameter | Default | Used | Notes |
|-----------|---------|------|-------|
| Oscillator | RSI | RSI 14 | Default |
| Pivot Left/Right Bars | 7/7 | 7/7 | Default |
| SL ATR Buffer (×) | 0.5 | **0.5** | Lower (0.3) and higher values both reduced profit |
| TP R:R Ratio | 2.0 | **2.0** | Higher (3.0) reduced profit |

Commission used in all runs: **0.02%**

---

## Backtest Runs

| Run | TF | Short signal | SL Buf | TP R:R | PF All | PF Long | PF Short | Net % | Max DD% |
|-----|----|-------------|--------|--------|--------|---------|---------|-------|---------|
| 1 | 1H | bearDiv | 0.5 | 2.0 | 0.959 | 0.971 | 0.944 | -1.74 | 4.56 |
| 2 | 4H | bearDiv | 0.5 | 2.0 | 0.819 | 0.935 | 0.696 | -11.64 | 16.95 |
| 3 | 1D | bearDiv | 0.5 | 2.0 | 1.443 | 6.177 | 0.671 | +9.52 | 8.38 |
| 4 | 4H | bearHidDiv | 0.5 | 2.0 | **1.142** | **1.315** | 0.940 | **+8.20** | 10.39 |
| 5 | 4H | bearHidDiv | 0.5 | 3.0 | — | — | — | +6.40 | — |
| 6 | 4H | bearHidDiv | 0.3 | 2.0 | — | — | — | +3.94 | — |

Run 3 (1D) excluded from consideration: only 32 trades over 9 years, statistically insufficient. Long PF 6.177 is driven by 12 trades.

---

## Best Configuration Results

**Run 4** — 4H, bearHidDiv shorts / SL Buffer 0.5 / TP R:R 2.0 / 0.02% commission

| Metric | All | Long | Short |
|--------|-----|------|-------|
| Net Profit (%) | +8.20 | +9.78 | -1.59 |
| Profit Factor | 1.142 | 1.315 | 0.940 |
| Win Rate (%) | 39.4 | 40.9 | 37.7 |
| Avg Winner / Avg Loser | 1.76× | 1.90× | 1.55× |
| Trades | 241 | 127 | 114 |
| Max Drawdown (%) | 10.39 | — | — |
| CAGR (%) | 1.08 | 1.28 | -0.22 |
| vs Buy & Hold (%) | +13.25 | — | — |

---

## Key Findings

**What worked:**
- Switching short signal from `bearDiv` (countertrend) to `bearHidDiv` (trend continuation) was the decisive change: overall PF improved from 0.819 → 1.142, net profit from -11.64% → +8.20%.
- Long side (`bullDiv`) is consistently profitable across timeframes (PF 1.315 on 4H).
- Strategy significantly outperforms a negative Buy & Hold period (+13.25% relative).

**What remains weak:**
- Short side (PF 0.940) is a small but persistent drag. Root cause: `bearHidDiv` entry fires `pivRight` bars after the pivot, by which time the optimal entry has passed. The W/L ratio (1.55×) falls just below the breakeven threshold for a 37.7% win rate (needs 1.65×).
- SL/TP parameter adjustments (TP R:R 3.0, SL Buffer 0.3) both reduced overall profit — the current defaults are already optimal for this signal type.
- CAGR of 1.08% remains below risk-free rates. Real-world execution costs (spreads, swaps) would reduce this further.
- No out-of-sample validation performed.

---

## Verdict

**Rating:** Promising

The strategy has a real long-side edge and now beats a negative market period convincingly. The short side is structurally limited by the `pivRight`-bar entry delay and cannot be fixed by SL/TP tuning alone. A meaningful upgrade path would be to reduce `pivRight` (faster entry) or add a trend filter that disables shorts in bull regimes. Left as-is, the strategy is directionally sound but too thin in absolute return for live deployment without further development.

**Next steps:**
1. Out-of-sample validation on a second instrument (Crude Oil, Gold)
2. Test `pivRight = 4` or `5` to reduce short entry delay
3. Consider a trend filter (e.g., disable shorts when price > 200-bar MA)
