# Kestrel Opportunity Lens — Strategy Backtest Assessment

**Instrument:** — (not yet tested)
**Strategy file:** `kestrel_opportunity_lens_strategy.pine`
**Assessment date:** 2026-11-17

---

## Signal Logic

| Signal | Expression |
|--------|------------|
| Long   | `longSide.setupEv` — long window (Williams ≤ zone), recovery from the window extreme in Williams and close (ATR), optional rising WaveTrend |
| Short  | `shortSide.setupEv` — mirror image (Williams ≥ 100 − zone) |
| SL type | none — time exit on the close of the `exitBars`-th held bar; optional break-even only |

Signal logic is a copy of indicator 0.2.0 (plus the export fix from its Unreleased section).
Entries fill on the next open; the evaluation measures from the signal close.

---

## Purpose: evaluation, not a trading system

The Strategy Tester trades are a side view. The main output is the evaluation table and the
Pine Logs:

- **Every** setup is measured, independent of open positions: return after 3 / 6 / 12 / 24 bars,
  MFE and MAE over bars 1–24, all in ATR of the signal bar, signed in signal direction.
- Grouped by direction × trend context (with / counter / mixed), with `n` in every row.
- **Baseline:** plain Williams zone exit (cross back over the zone), measured the same way.
  The setup only adds value if it beats this row for the same direction.
- **Pine Logs:** one `KOL PROBE` line per finished probe, incl. `overlap` (probes already open
  when this one started). Overlapping probes are not independent observations — filter or weight
  them before any statistic.

Points to settle before reading results:

- Review lock on/off changes the setup sample (off = every valid opportunity).
- Probes still open at the last bar are not counted.
- Means are sensitive to single large moves (NatGas); judge with the log data, not the table alone.
- Report `n` next to every figure; no conclusion from rows with n < 30.

---

## Backtest Runs

| Run | Instrument | TF | Review lock | n long | n short | n base L/S | Notes |
|-----|------------|----|-------------|--------|---------|------------|-------|
| — | — | — | — | — | — | — | not yet run |

---

## Verdict

**Rating:** Not ready — nicht getestet

No run exists yet. The first question is not profitability but whether setup rows differ from
the baseline rows at all, per direction and context, with sufficient `n`.

**Next steps:**
1. First run on CAPITALCOM:NATURALGAS 4h with defaults, review lock off; record table and logs here.
2. Compare setup vs. baseline per direction; only then look at trend context.
3. Repeat on a second instrument before drawing any conclusion.
