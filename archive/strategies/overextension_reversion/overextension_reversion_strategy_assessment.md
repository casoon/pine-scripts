# Overextension Reversion — Strategy Backtest Assessment

**Instrument:** CAPITALCOM:NATURALGAS
**Strategy file:** `overextension_reversion_strategy.pine`
**Assessment date:** 2026-11-05

---

## Signal Logic

| Signal | Expression |
|--------|------------|
| Long   | `longSignal` — close crosses back above EMA − band, RSI[1] ≤ `oversold`, RSI and close rising, range regime, target/stop ≥ `minRewardRisk` |
| Short  | `shortSignal` — mirror image at EMA + band with `overbought` |
| SL type | fixed (tick-rounded ATR × `stopAtr` from fill) + fixed limit target at signal-bar EMA + time exit after `maxHold` bars |

Range regime: `ADX ≤ maxAdx` and `|EMA slope| ≤ maxSlope` (ATR per bar).

---

## Changes against the submitted draft (2026-11-05)

- Signal, regime and exit logic unchanged — the draft was sound (re-entry trigger, frozen target,
  fill-relative stop, no lookahead).
- Stop is re-issued as a price level once the position is open (same level as the `loss=` ticks),
  so the standard break-even can fold into the same `strategy.exit()`.
- Status panel moved to the repo light table style (`size.small`, state-coloured status cell).
- Standard strategy features added (trade direction, confirmed-bar entries, cooldown, break-even,
  filters, chart-type guard); commission set to the repo default 0.02 %.

---

## Backtest Runs

Range 2025-01-02 – 2026-11-05, default settings, commission 0.02 %, 10 % of equity per trade.
Timeframe not recorded with the run.

| Run | Version | TF | Settings | PF All | Win % | Trades | Net % | Max DD % |
|-----|---------|----|----------|--------|-------|--------|-------|----------|
| 1 | 1.0.0 | n/a | defaults (fixed 1.5 ATR stop) | 1.11 | 50.0 | 62 | +0.48 | 1.04 |

Run 1: nearly all of the gain comes from the first trades up to Jun 2025 (n < 10); from Jul 2025
on the equity moves sideways. Average winner ≈ average loser, flat drawdown — the mechanics work,
the edge is not there.

## Changes in 1.1.0 (after run 1)

- **Stop Mode "Swing Extreme" (new default)** — stop beyond the low/high of the overextension swing
  (`swingBars`, default 5) plus `stopBufferAtr` (0.25 ATR). That is the level whose break
  invalidates the reversion thesis; the fixed 1.5 ATR stop from the fill sat at an arbitrary place
  relative to it. The target/stop ratio check now uses the stop actually placed.
- "Fixed ATR" keeps the 1.0.0 behaviour for a direct comparison.

Not yet re-run.

---

## Key Findings

**Open design risks:**
- Default `minRewardRisk = 0.75` accepts targets closer than the stop; combined with costs that
  needs a high hit rate to break even — check the target/stop distribution before tuning entries.
- The target is the EMA at the signal bar: after a 2 ATR stretch, a quick re-entry signal can sit
  only ~1 ATR from the target, so the ratio filter blocks many signals on short `meanLength`.
- ADX + slope ceiling are both trend filters on overlapping information; measure each one's block
  volume separately before keeping both.

---

## Verdict

**Not ready** — not yet backtested.
