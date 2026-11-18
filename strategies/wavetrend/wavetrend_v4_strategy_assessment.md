# WaveTrend v4 — Strategy Backtest Assessment

> ⚠️ **NOT MEASURED — v5.0 has no backtest.** v5.0 (2026-11-17) removed every entry gate that
> was tuned on the NatGas window (test92–test166) and reduced the inputs from 268 to 61. The run
> recorded below (`test92`) was measured on **v4.21** with a gate stack that no longer exists. No
> figure in this file describes the shipped script.

**Instrument:** CAPITALCOM:NATURALGAS (historical runs only)
**Strategy file:** `wavetrend_v4_strategy.pine` (standalone, v5.0)
**Assessment date:** 2026-11-17 (last measurement 2026-05-04 on v4.21)

---

## Signal Logic (v5.0)

| Signal | Expression |
|---|---|
| Long | `crossover(wt1, wt2)` and `wt1 ≤ −level` (level per timeframe: 15M 10, 1H 20, 4H 5, 1D 20) |
| Short | `crossunder(wt1, wt2)` and `wt1 ≥ +level` — same level, mirrored |
| Stop | ATR × 1.5 from the fill, frozen ATR of the signal bar |
| Exit | Break-even at 1R, trailing stop from 2R (replaces the fixed target), structural exit from 2–3R; `Fixed` mode = ATR target + stop + time limit |
| Filters | Session, date range, cooldown, losing-streak limit, max drawdown — all off by default |
| WT smoothing | One kernel on every timeframe: `Smoothing Type` EMA (default, classic WaveTrend) or T3. Replaces the fixed per-TF smoothers of v4.x (15M RMA, 1H HMA, 4H JMA, 1D SMA) |

The per-timeframe levels, target multiples and structural-exit thresholds are carried over
from v4.93 unchanged. They were also set on the NatGas window and are part of what a first
run has to test, not a calibrated result.

The per-timeframe levels were set with the old per-TF smoothers. With one EMA kernel, `wt1`
reaches the levels with a different depth and timing on 15M/1H/4H/1D, so the levels are even
less of a calibrated value than before — a first run should check them per timeframe.

### Removed in v5.0

| Removed | Why |
|---|---|
| Quality gates A, D, H, J, K, L, M (per-TF/per-direction block bands) | Iterated against one NatGas window (test141–166); several fire on a single TF and side only — asymmetry without a situation that explains it |
| Gate B2 (15M needs 1H OS/OB), Gate C (HTF exhaustion), Gate G (counter-trend range, 15M/1H only), Gate I (StochRSI persistence) | Same window; B2/G hard-coded to specific timeframes |
| Exits E (fail-fast) and F (no-follow), 1H only, and the Grind Engine | Hard-coded to 1H from in-sample logs |
| OS/OB depth cap on 1D (±48) | Derived from in-sample setup classification |
| StochRSI gate, ATR rank, BB expansion, chop, pivot proximity, liquidity sweep filters | Default off since v4.2x; the `test92` stack that used them was close to selection-neutral |
| Separate OS and OB inputs per TF | Replaced by one symmetric level per TF (defaults were already mirrored) |
| Per-TF smoother switch (RMA/HMA/JMA/SMA) and JMA phase/power | Chosen per timeframe on the same NatGas window; replaced by one kernel for all TFs |

None of these gates was ever checked outside the window it was tuned on (Plan 34, Phase 2 never
ran). With no new test data coming, the decision rule from Plan 34 — "OOS contradicts or is
neutral → gate off" — cannot be met in the gates' favour, so they are removed rather than kept
switched off.

---

## Historical run (v4.21 — not this script)

### test92 — v4.21, NatGas

| TF | Trades | WR | PF | Net % | Max DD % |
|---|---|---|---|---|---|
| 1H | 62 | 26% | 3.96 | +51.6 | -7.3 |
| 4H | 54 | 11% | 0.67 | -15.3 | -30.7 |
| 1D | 5 | 20% | 2.32 | +9.8 | -11.1 |

Gate stack at the time: StochRSI on, ATR rank on (1H 35–85, 4H 30–90, 1D 20–95), BB expansion
on, chop max 58, structural exit off. The 1D row is n = 5 and carries no information. Pivot-to-
pivot analysis on the same window found the gate stack blocked 94% of WT crosses while selecting
barely better than the market average (2687 available moves, 55 caught).

---

## Verdict

**Rating:** Not ready — v5.0 not backtested; earlier runs measured a different script, only in
the window it was tuned on.

**What a first run of v5.0 has to show** (when data exists again):
1. Signal vs. random baseline (built-in table) per side, `Fixed` exit mode, on NatGas and on at
   least one instrument the defaults were not set on
2. `Existing` vs. `Fixed` exit on the same entries — the dynamic exits must beat the fixed one
3. Cost table with spread and financing set; a result that flips under stress ×1.5 does not carry
