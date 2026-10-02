# WaveTrend v4 — Strategy Backtest Assessment

> ⚠️ **STALE — pending re-validation.** The run below (`test92`) was measured on strategy
> **v4.21**. The shipped file is **v4.89**. Gate configuration, thresholds and exit handling
> changed in between. Re-run on NatGas before relying on any figure here.

**Instrument:** CAPITALCOM:NATURALGAS
**Strategy file:** `wavetrend_v4_strategy.pine` (standalone, v4.89)
**Assessment date:** 2026-09-08 (results measured 2026-05-04 on v4.21)

---

## Signal Logic

| Signal | Expression |
|---|---|
| Long | WT cross below the oversold level, all active gates passed |
| Short | WT cross above the overbought level, all active gates passed |
| SL type | Trailing (ATR envelope) + break-even |

Gate configuration at the time of `test92`:

| Gate | Setting |
|---|---|
| StochRSI | on |
| ATR Rank | on — 1H 35–85, 4H 30–90, 1D 20–95 |
| BB Expansion | on — compression recently + expanding now |
| Chop | on — max 58 |
| Pivot Proximity | off |
| Liquidity Sweep | off |
| Structural Exit | off |

---

## Backtest Runs

### test92 — v4.21, NatGas

| TF | Trades | WR | PF | Net % | Max DD % |
|---|---|---|---|---|---|
| 1H | 62 | 26% | 3.96 | +51.6 | -7.3 |
| 4H | 54 | 11% | 0.67 | -15.3 | -30.7 |
| 1D | 5 | 20% | 2.32 | +9.8 | -11.1 |

The 1D row is n = 5 — reported for completeness only, it carries no information about the
signal. The 4H short leg was the dominant loss block (WR 7%, avg R −0.39 over 41 trades).

---

## Key Findings

**What worked:**
- On 1H the gate stack produced a strongly positive expectancy within the tested window.

**What remains weak:**
- **The gates are close to selection-neutral.** Pivot-to-pivot baseline analysis
  (`scripts/analyze_gates.py`, section 0) found 2687 theoretically available trades at
  avg R +2.75 across the window. The strategy caught 55 of them (2%) at avg R +2.89. All
  gates together block 94% of WT crosses while selecting barely better than the market
  average — the cost is enormous and the benefit marginal.
- 4H is outright unprofitable, driven by the short side.
- Three gate hypotheses (late-entry, low-ATR-noise, stale-structure) were designed, built and
  measured, and **all three were discarded** — each removed good and bad trades in similar
  proportion. The lesson recorded from that round: hypotheses derived from aggregates across
  timeframe and direction mask the per-bucket patterns that actually matter, and a gate
  blocking under ~5% of signals cannot move the result at all.

---

## Verdict

**Rating:** Promising — *under review, see caveats*

The rating is carried over from the project record and is **not** confirmed by the data in this
file. What `test92` actually shows is one profitable timeframe (1H), one outright unprofitable
one (4H), and no usable sample on 1D. The 1H result rests on a gate stack that the
pivot-to-pivot baseline shows to be barely more selective than the market average, and the file
is 68 minor versions past the measurement.

**Open gap:** the root README previously carried a "PF 3.07, NatGas 1D" figure for this
strategy. No run in the repo reproduces it — `test92` measured PF 2.32 on 1D at n = 5. Either a
later run exists outside the repo record, or the figure drifted. It has been removed from the
README until a run backs it.

**Next steps:**
1. Re-run v4.89 on NatGas 1H/4H/1D — the current numbers describe a different script
2. Address the 4H short leg specifically rather than tuning shared thresholds
3. Work the exit side before adding further entry gates — capture rate, not selectivity, is
   where this strategy loses (the repo's own "Fundament vor Feintuning" principle)
4. Second instrument before any rating above "Not ready"
