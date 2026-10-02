# Reversal Engine Score — Strategy Backtest Assessment

> ⚠️ **STALE — pending re-validation.** The runs below were measured on **v1.1 – v1.4** of
> the signal logic. The shipped strategy file is **v1.6.1**. Re-run on NatGas 15M before
> relying on any figure here. Historical record retained because the *direction* of each
> finding drove the current design.

**Instrument:** CAPITALCOM:NATURALGAS
**Strategy file:** `reversal_engine_score_strategy.pine` (standalone, v1.6.1)
**Assessment date:** 2026-09-08 (results measured 2026-05 … 2026-09 on v1.1–v1.4)

---

## Signal Logic

| Signal | Expression |
|---|---|
| Long | Liquidity sweep of a prior swing low + recovery close, mandatory gates passed, quality ≥ `minQualityLong` |
| Short | Liquidity sweep of a prior swing high + recovery close, mandatory gates passed, quality ≥ `minQualityShort` |
| SL type | Structural — sweep low/high ∓ `slAtrBuffer` × ATR |
| TP | R-multiple — `entry ± (entry − SL) × tpRMult` |

Gate model is **mandatory gates + a 0–2 quality count**, not an additive score. That change
came out of test131 (below) and is the central design decision of this strategy.

---

## Backtest Runs

| Run | Version | TF | Settings | Trades | WR | PF | Net % | Max DD % |
|---|---|---|---|---|---|---|---|---|
| test131 | v1.1 | 15M | additive score baseline | 298 | 41% | 0.95 | — | — |
| test134 | v1.2 | 15M | `minQuality=1`, `slAtrMult=1.2`, `tpAtrMult=2.0` | 71 | 45% | 1.03 | — | -1.21 |
| test136 | v1.3 | 15M | `minQualityLong=3`, `minQualityShort=2`, `slAtrBuffer=0.30`, `tpRMult=1.5` | 55 | 58% | 2.15 | +2.0 | -0.46 |
| test138 | v1.4 | 15M | `minQualityLong=2`, `minQualityShort=1`, otherwise as test136 | 55 | 58% | 2.15 | +2.0 | -0.46 |

test138 is numerically identical to test136 by design: v1.4 removed the EMA gate from
scoring, which had a 100% hit rate in both directions and therefore never filtered anything.

### test138 split (n small — see caveat)

| | n | WR | PF |
|---|---|---|---|
| Long | 6 | 83% | 4.06 |
| Short | 49 | 55% | 1.95 |
| Short, `noHH` + `rsi>50` | 24 | 58% | 2.22 |
| Short, one gate only | 25 | 52% | 1.72 |

**The long side is n = 6.** That is far below any threshold at which a win rate or a profit
factor says something about the signal. It is reported here only so the sample size travels
with it; it must not be read as a property of long entries.

---

## Key Findings

**What worked:**
- Replacing the additive score with mandatory gates + quality count. In test131 the additive
  score was inverted — the top bucket (score 12) was the *worst* (WR 21%, PF 0.49) and score 7
  the best. Summing loosely correlated conditions produced a number that ranked setups
  backwards.
- Inverting the short optionals. `rsi < 50` and `close < ema` were **negative** discriminators
  for shorts (hit WR 30%/33% vs. miss WR 61%/54%). A short reversal after a sweep high occurs
  while RSI is still elevated and price still above the EMA — the old conditions were selecting
  trend continuation, not reversals.
- Structural SL at the sweep extreme with an ATR noise buffer, replacing the flat ATR stop.
- `noHH` is the strongest short discriminator across every run.

**What remains weak:**
- Net profit is +2.0% over the tested window. The PF is carried by a small number of trades.
- Losers left money on the table: 38% of losing trades reached ≥ $500 favorable excursion
  before reversing (MFE/Loss ratio 0.65). A break-even stop or structural exit is the obvious
  next lever — this is the concrete open item.
- `atrOk` as a minimum threshold correlated *negatively* with winners on NatGas: high ATR there
  means news/chaos, not opportunity. Replaced by an ATR corridor.
- Single instrument, single timeframe, in-sample throughout.

---

## Verdict

**Rating:** Not ready

The design iterations fixed real, diagnosed defects rather than curve-fitting parameters, and
the direction of travel (PF 0.95 → 2.15) reflects that. But the current file is two versions
ahead of the last measurement, the long side has no usable sample, and nothing has been run
out-of-sample or on a second instrument. Until v1.6.1 is measured, there is no rating to give.

**Next steps:**
1. Re-run v1.6.1 on NatGas 15M — re-establish the baseline against the shipped logic
2. Add MFE/MAE logging staggered by bar count (3/5/10/20) to see whether the entries or the
   exits are the constraint
3. Test the break-even stop against the 38%-of-losers-with-favorable-excursion finding
4. Second instrument before any rating above "Not ready"
