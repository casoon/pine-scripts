# Similar Market States — Strategy Backtest Assessment

**Instrument:** CAPITALCOM:NATURALGAS
**Strategy file:** `similar_market_states_strategy.pine`
**Assessment date:** 2026-11-05

---

## Signal Logic

| Signal | Expression |
|--------|------------|
| Long   | `longSignal` — `setupDir == 1` (close > EMA, EMA rising over 5 bars, momentum > 0) and `modelPass` |
| Short  | `shortSignal` — `setupDir == -1` and `modelPass` |
| SL type | fixed (signal close ∓ ATR(14) × `stopAtr`) + time exit after `horizon` bars |

`modelPass`: exactly `neighbors` past setups of the same direction found within `maxDistance`;
their replayed trades (entry next open, same fixed stop, time exit at close of bar s+horizon)
average above `costHurdle + minNetMove` and are favourable in at least `minAgreement` % of cases.
`useModel = false` trades every base setup — the comparison baseline.

---

## Changes against the submitted draft (2026-11-05)

- **Feature scaling** — each feature distance is divided by the feature's rolling stdev over
  `lookback`. Before, the EMA distance (in ATR, often ± several units) dominated the distance and
  RSI (±1) and the volatility ratio barely mattered. `maxDistance` now has a different scale.
- **Neighbour population = traded setup** — neighbours must have formed the same base setup
  (trend **and** momentum sign), not just the same trend sign.
- **Neighbour outcome replays the trade** — fixed stop and gap fills are simulated over the holding
  window instead of using the raw open→close move. The model now evaluates the trade it filters.
- **Time exit on the close** — `strategy.close(immediately=true)` on the `horizon`-th held bar,
  matching the replayed exit at close(s+horizon). The submitted draft was truncated before its exit logic.
- Standard strategy features added (trade direction, confirmed-bar entries, cooldown, break-even,
  filters, chart-type guard); commission set to the repo default 0.02 %.

---

## Backtest Runs

Range 2025-01-02 – 2026-11-05, default settings, commission 0.02 %, 10 % of equity per trade.
Timeframe not recorded with the run (the ~4-month warm-up before the first trade points to 1H).

| Run | Version | TF | Settings | PF All | Win % | Trades | Net % | Max DD % |
|-----|---------|----|----------|--------|-------|--------|-------|----------|
| 1 | 1.0.0 | n/a (≈1H) | defaults, `neighbors` 12 | 0.99 | 48.4 | 368 | −0.19 | 2.15 |

Run 1: equity oscillates around zero for the whole range; the only sustained rise (Feb–May 2026)
is a single phase. No edge after costs.

## Changes in 1.1.0 (after run 1)

- **Decision in R instead of %** — neighbour outcomes are measured in multiples of their own stop
  distance, the cost estimate is converted into R of the current trade. On NatGas (ATR ≈ 1 % on
  intraday TFs) a fixed 0.2 % hurdle is a small fraction of one neighbour's noise and passed
  almost anything.
- **Uncertainty discount** — the neighbour mean is reduced by `confK` standard errors before the
  cost check (`confK = 0` restores the plain-mean rule). With n = 12 the standard error of the
  mean is large enough that a few lucky neighbours passed as an edge.
- `neighbors` default 12 → 20 to reduce that standard error.

Not yet re-run. Compare 1.1.0 against `useModel = false` on the same range — only the difference
tells whether the filter selects anything.

---

## Key Findings

**Open design risks:**
- `neighbors = 12` makes `agreement` coarse (steps of 8.3 %) and the mean noisy; any edge has to
  survive that small per-decision sample.
- `costHurdle` / `minNetMove` are fixed percentages, not volatility-scaled — their bite depends
  heavily on timeframe and instrument.
- The model is fitted on the same history it trades on (rolling, no lookahead) — still, parameter
  sweeps over `lookback` / `neighbors` / `maxDistance` are a multiple-testing risk; compare against
  `useModel = false` on data outside the tuning window.
- Break-even and cooldown are not part of the replay; enabling them decouples trade and model.

---

## Verdict

**Not ready** — not yet backtested.
