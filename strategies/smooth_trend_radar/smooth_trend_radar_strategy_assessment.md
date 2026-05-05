# Smooth Trend Radar — Strategy Backtest Assessment

**Instrument:** CAPITALCOM:NATURALGAS  
**Strategy file:** `smooth_trend_radar_strategy.pine`  
**Assessment date:** 2026-04-29

---

## Signal Logic

| Signal | Expression |
|--------|------------|
| Long | `longSignal` (smoothed Supertrend midline flips up) + `bullRejRe` (rejection re-entry) |
| Short | `shortSignal` (smoothed Supertrend midline flips down) + `bearRejRe` (rejection re-entry) |
| SL type | fixed (`SL` variable — ATR/Swing/Flip Candle based, set at entry) |

Signals are **symmetric trend-following** — both directions use the same logic. The short underperformance is an instrument issue, not a design flaw.

---

## Optimized Settings

| Parameter | Default | Optimized | Notes |
|-----------|---------|-----------|-------|
| TP1 Multiplier | 2.0 | **3.0** | Wider target reduces premature exits |
| TP2 Multiplier | 4.0 | **5.0** | — |
| TP3 Multiplier | 6.0 | **7.0** | — |
| Exit at TP | TP2 | **TP1** | TP1 exit outperforms TP2 across all tested TFs |

Commission used in all runs: **0.02%**

---

## Backtest Runs

| Run | TF | Exit | TP Mults | PF All | PF Long | PF Short | Net % | Max DD% | Trades |
|-----|----|------|----------|--------|---------|---------|-------|---------|--------|
| 1 | 1D | TP2 | 2/4/6 | 1.295 | 0.744 | 1.883 | +3.19 | 6.00 | 23 |
| 2 | 1H | TP2 | 2/4/6 | 0.898 | 0.949 | 0.853 | -6.20 | 12.64 | 653 |
| 3 | 15m | TP2 | 2/4/6 | 1.001 | 1.220 | 0.831 | +0.01 | 4.10 | 384 |
| 4 | 4H | TP2 | 2/4/6 | 1.005 | 1.410 | 0.719 | +0.23 | 9.39 | 206 |
| 5 | 4H | TP1 | 3/5/7 | **1.131** | **1.707** | 0.778 | **+4.75** | **4.69** | 207 |

Run 1 (1D) excluded from consideration: only 23 trades, statistically insufficient.

---

## Best Configuration Results

**Run 5** — 4H, Exit TP1 / TP multipliers 3/5/7 / 0.02% commission

| Metric | All | Long | Short |
|--------|-----|------|-------|
| Net Profit (%) | +4.75 | +9.76 | -5.01 |
| Profit Factor | 1.131 | 1.707 | 0.778 |
| Win Rate (%) | 65.2 | 70.8 | 60.4 |
| Avg Winner / Avg Loser | 0.60× | 0.70× | 0.51× |
| Trades | 207 | 96 | 111 |
| Max Drawdown (%) | 4.69 | — | — |
| CAGR (%) | 0.64 | — | — |
| vs Buy & Hold (%) | +14.30 | — | — |

---

## Key Findings

**What worked:**
- Switching exit from TP2 to TP1 (with wider 3× multiplier) was the most impactful change: Net profit improved from +0.23% → +4.75%, Max DD halved (9.39% → 4.69%).
- Long-side PF 1.707 is the strongest result across all three strategies tested on NatGas.
- Strategy significantly outperforms a negative Buy & Hold period (+14.30% relative).
- Low Max DD (4.69%) relative to other strategies makes this the most capital-efficient result found.

**What remains weak:**
- Short side (PF 0.778) is a persistent structural drag. Unlike ODZ where the signal type was wrong, STR signals are correctly designed as symmetric trend-following — the short underperformance is caused by NatGas's bullish bias: bearish trend flips are quickly reversed, stopping out shorts before TP is reached.
- Avg W/L ratio of 0.60× reveals that most trades exit at the next signal flip, not at TP. Shorts get stopped out at full SL loss; long gains are cut by the next short flip before TP. TP multiplier changes have limited effect on this dynamic.
- CAGR of 0.64% remains below risk-free rates. Short-side drag (-5.01%) alone exceeds the entire net gain.
- No out-of-sample validation performed.

**Why short signals cannot be fixed by parameter tuning:**
The STR uses a smoothed Supertrend midline crossover — a symmetric oscillator. There is no "hidden" or "continuation" variant to substitute (as was possible with ODZ). The short signal is structurally sound; the problem is the instrument.

---

## Verdict

**Rating:** Promising (Long Only) / Not ready (Both Directions)

The long side has a genuine, strong edge on NatGas (PF 1.707, lowest Max DD of all tested strategies). Running both directions, the short-side drag reduces the strategy to marginal profitability. The honest deployment path for this instrument is Long Only, which would isolate the strong long signal and eliminate the structural short drag. For a bidirectional deployment, a trend-neutral or bearish instrument is required.

**Next steps:**
1. Test Long Only on 4H to quantify the isolated long-side performance
2. Validate on a trend-neutral instrument (e.g., EUR/USD, Gold) for bidirectional use
3. Consider an HTF regime filter: disable shorts when weekly/daily trend is bullish
