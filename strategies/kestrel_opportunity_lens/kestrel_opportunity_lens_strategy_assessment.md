# Kestrel Opportunity Lens — Strategy Backtest Assessment

**Instrument:** CAPITALCOM:NATURALGAS (CFD)
**Strategy file:** `kestrel_opportunity_lens_strategy.pine`
**Assessment date:** 2026-11-17

---

## Signal Logic

| Signal | Expression |
|--------|------------|
| Long   | `longSide.setupEv` — long window (Williams ≤ zone), recovery from the window extreme in Williams and close (ATR) |
| Short  | `shortSide.setupEv` — mirror image (Williams ≥ 100 − zone) |
| SL type | none — time exit on the close of the `exitBars`-th held bar; optional break-even only |

Signal logic is a copy of indicator 0.2.0 (plus the export fix from its Unreleased section).
Since strategy 0.2.0 the input `Setup model` selects the setup definition; `Recovery (original)`
is the indicator's rule and the default. Run 1 used it.

| Setup model | Setup fires when … | Window ends without setup |
|-------------|--------------------|---------------------------|
| Recovery (original) | Williams and close recover from the window extreme (indicator rule) | after `deadline` bars from the start |
| Early in zone | close recovers ≥ `priceRecovery` ATR and Williams turns while still inside the zone | zone left, or `deadline` from the start |
| Confirmation after exit | a later close beyond the zone-exit bar's high (short: low), window extreme intact | new extreme, or `deadline` bars after the exit |
| Higher-low retest | after the exit Williams pulls back, then turns with the close, window extreme intact | new extreme, or `deadline` bars after the exit |

The last three can never fire on the zone-exit bar itself, so they separate from the baseline by
construction. Comparing four models against the same NatGas data is a multiple comparison: a
model that wins here still needs the later-period / second-instrument test before it replaces the
indicator rule.
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
| 1 | CAPITALCOM:NATURALGAS | 4h | default (on), not confirmed | 306 | 300 | 644 / 672 | Defaults, 2020-01-02 – 2026-11-17, in-sample |
| 2 | CAPITALCOM:NATURALGAS | 4h | default (on) | 306 | 300 | 644 / 672 | Strategy 0.2.0, Setup model = Recovery (original); cost-free |
| 3 | CAPITALCOM:NATURALGAS | 4h | default (on) | 155 | 144 | 644 / 672 | Setup model = Early in zone; cost-free |
| 4 | CAPITALCOM:NATURALGAS | 4h | default (on) | 192 | 155 | 644 / 672 | Setup model = Confirmation after exit; cost-free |
| 5 | CAPITALCOM:NATURALGAS | 4h | default (on) | 176 | 164 | 644 / 672 | Setup model = Higher-low retest; cost-free |

Runs 2–5: same data window as run 1 (2020-01-02 – 2026-11-17), all other inputs at default
(neutral band 0.1, stress 1.5, `exitBars` 12).

**Cost model:** run 1: commission 0.02 % per side + 1 tick slippage (placeholder). Runs 2–5:
commission 0 / slippage 0, CFD cost model inputs not set (table shows "NOT SET – cost-free").
Capital spread (~0.005, roughly 0.1–0.15 ATR round trip at ATR ≈ 0.04) and overnight financing
not applied in any run.
**Mean holding time:** 12 bars (time exit, default) — 2.6 calendar nights on average (cost table).
**Random baseline:** not measured; the Williams zone exit serves as the comparison baseline.
**Variants tried:** 4 setup models (runs 2–5) against the same dataset — multiple comparison.

### Run 1 — evaluation table (mean, ATR of the signal bar, signed in signal direction)

| Row | n | +3 | +6 | +12 | +24 | MFE | MAE |
|-----|---|----|----|-----|-----|-----|-----|
| Long · with trend | 31 | 0.17 | 0.25 | 0.18 | 0.28 | 3.08 | 2.44 |
| Long · counter-trend | 238 | 0.00 | 0.12 | 0.44 | 0.35 | 3.22 | 2.49 |
| Long · mixed | 37 | 0.09 | 0.22 | 0.51 | 0.61 | 3.35 | 2.43 |
| Long · all | 306 | 0.03 | 0.15 | 0.42 | 0.37 | 3.22 | 2.48 |
| Short · with trend | 30 | −0.05 | 0.19 | 0.49 | 0.06 | 2.89 | 2.83 |
| Short · counter-trend | 234 | −0.17 | −0.19 | −0.24 | −0.36 | 2.67 | 3.50 |
| Short · mixed | 36 | −0.19 | −0.09 | 0.10 | −0.55 | 2.66 | 3.04 |
| Short · all | 300 | −0.16 | −0.14 | −0.12 | −0.34 | 2.69 | 3.38 |
| Baseline long (zone exit) | 644 | 0.06 | 0.13 | 0.20 | 0.43 | 3.15 | 2.52 |
| Baseline short (zone exit) | 672 | −0.10 | −0.14 | −0.21 | −0.51 | 2.61 | 3.48 |

Probes overlap (`overlap` 1–6 in the logs), so the effective number of independent observations
is well below `n`. Setup and baseline probes often fire on the same bar with identical values —
the setup is largely a subset of the zone exit, which narrows any possible difference.

### Run 1 — Strategy Tester side view (both directions, 12-bar time exit, 10 % of equity)

| Metric | All |
|--------|-----|
| Net Profit (%) | +22.21 |
| Profit Factor | 1.269 |
| Win Rate (%) | 53.83 (232 / 431) |
| Trades | 431 |
| Max Drawdown (%) | 8.37 |

Long/short split of the tester trades not recorded. Equity is roughly flat from 2020 to early
2025; most of the net profit comes from 2025–2026.

### Runs 2–5 — setup models compared (mean, ATR; baseline rows identical in all runs)

Long · all:

| Model | n | +3 | +6 | +12 | +24 | MFE | MAE |
|-------|---|----|----|-----|-----|-----|-----|
| Baseline long (zone exit) | 644 | 0.06 | 0.13 | 0.20 | 0.43 | 3.15 | 2.52 |
| Recovery (original) | 306 | 0.03 | 0.15 | 0.42 | 0.37 | 3.22 | 2.48 |
| Early in zone | 155 | −0.07 | 0.06 | 0.42 | 0.47 | 3.23 | 2.47 |
| Confirmation after exit | 192 | 0.09 | 0.18 | 0.39 | 0.60 | 3.43 | 2.55 |
| Higher-low retest | 176 | 0.01 | 0.26 | 0.27 | 0.40 | 3.33 | 2.67 |

Short · all:

| Model | n | +3 | +6 | +12 | +24 | MFE | MAE |
|-------|---|----|----|-----|-----|-----|-----|
| Baseline short (zone exit) | 672 | −0.10 | −0.14 | −0.21 | −0.51 | 2.61 | 3.48 |
| Recovery (original) | 300 | −0.16 | −0.14 | −0.12 | −0.34 | 2.69 | 3.38 |
| Early in zone | 144 | −0.18 | −0.18 | −0.20 | −0.29 | 2.64 | 3.34 |
| Confirmation after exit | 155 | −0.04 | 0.08 | −0.17 | −0.42 | 2.63 | 3.25 |
| Higher-low retest | 164 | 0.08 | 0.04 | 0.18 | −0.22 | 2.96 | 3.19 |

Context rows with n ≥ 30 that matter for the comparison:

| Model | Row | n | +12 | +24 |
|-------|-----|---|-----|-----|
| Confirmation after exit | Long · with trend | 41 | 0.26 | 0.64 |
| Confirmation after exit | Long · counter-trend | 75 | 0.56 | 0.71 |
| Confirmation after exit | Long · mixed | 76 | 0.30 | 0.47 |
| Confirmation after exit | Short · counter-trend | 54 | −0.85 | −1.04 |
| Higher-low retest | Long · mixed | 33 | −0.27 | −1.04 |
| Higher-low retest | Short · counter-trend | 90 | −0.06 | −0.46 |

Early in zone has n = 4 (long) and n = 0 (short) with the trend — by construction the trend runs
against the setup while Williams is still in the zone.

Strategy Tester side view (both directions, 12-bar time exit, cost-free):

| Run | Model | Trades | Win % | PF | Net % | Max DD % |
|-----|-------|--------|-------|----|-------|----------|
| 2 | Recovery (original) | 431 | 54.06 | 1.30 | +24.70 | 8.17 |
| 3 | Early in zone | 256 | 52.34 | 1.21 | +9.96 | 7.96 |
| 4 | Confirmation after exit | 270 | 49.63 | 1.13 | +7.65 | 6.68 |
| 5 | Higher-low retest | 273 | 54.21 | 1.35 | +17.67 | 5.16 |

Table and tester disagree: the tester mixes both directions and, with pyramiding 0, takes only
non-overlapping trades. Run 4's weak PF comes with its short counter-trend row (−0.85 at +12);
run 5's PF advantage comes from a less negative short side, not from a better long side.

---

## Key Findings

**What worked:**
- Long side positive at every horizon from +6 on (n = 306), MFE above MAE.

**What remains weak:**
- Long setup does not clearly beat the baseline: ahead at +12 (0.42 vs 0.20), behind at +3
  (0.03 vs 0.06) and +24 (0.37 vs 0.43), MFE/MAE practically equal. The positive long
  expectation belongs to the zone exit itself, not to the recovery rules.
- Short side negative for setup and baseline alike (setup −0.34 at +24, n = 300; MAE 3.38 > MFE 2.69).
  After an overbought zone exit NatGas tends to keep rising on this sample.
- Trend-context rows other than long/short counter-trend sit at n = 30–37 — no reading of
  context differences.
- Tester profit concentrated in 2025–2026; single instrument, single period, in-sample.
- Runs 2–5: only Confirmation after exit separates from the baseline on the long side at most
  horizons (+24: 0.60 vs 0.43, n = 192), consistently across all three contexts (n ≥ 41). The
  margin is about 0.17 ATR — within what overlap and a four-way comparison can produce.
- No setup model turns the short side positive at +24; NatGas up-skew dominates every variant.

---

## Verdict

**Rating:** Not ready

On NatGas 4h the Kestrel setup adds no clear value over the plain Williams zone exit; the long
side is positive in both, the short side negative in both. The tester PF of 1.27 rests on a
placeholder cost model and a profit curve concentrated in the last two years. Promising would
need both sides positive and an unchanged test on a later period and a second instrument.

Of the alternative setup models, Confirmation after exit is the only long-side candidate; it
stays a candidate until the margin holds in a sub-period split. The indicator keeps its rule.

**Open points:**
1. Sub-period check (e.g. 2020–2023 vs. 2024–2026) for Confirmation after exit — the evaluation
   table ignores the strategy's Date Range filter, so this needs a change first.
2. Setup vs. baseline without same-bar overlap (setup probes that are not also a zone-exit probe)
   is not measured separately.
3. Long/short split of the tester trades and a realistic CFD cost model are missing.
4. Second instrument / later period not tested (no new test data planned for now).
