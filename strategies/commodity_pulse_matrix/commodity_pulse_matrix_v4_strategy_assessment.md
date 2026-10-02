# Commodity Pulse Matrix v4 — Strategy Backtest Assessment

**Instrument:** — (not yet run)
**Strategy file:** `commodity_pulse_matrix_v4_strategy.pine` (standalone, v4.1.1)
**Assessment date:** 2026-09-08 — placeholder, no backtest performed

---

## Signal Logic

| Signal | Expression |
|---|---|
| Long | Composite matrix long trigger |
| Short | Composite matrix short trigger |
| SL type | Directional fixed SL/TP — frozen at entry per direction |
| Exit | Optional indicator-driven close on opposing signal |

Signal and stop variables are declared in the `@strategy-config` block at the end of
`indicators/composite/commodity_pulse_matrix/commodity_pulse_matrix_v4.pine`.

---

## Backtest Runs

None. This file exists so the strategy is not silently untracked.

---

## Verdict

**Rating:** Not ready — not backtested

No run exists on any instrument or timeframe, so there is nothing to rate. The strategy is a
complete, loadable script; that is all that is established.

**Next steps:**
1. Baseline run on the intended instrument with defaults — record trades, WR, PF, net, max DD
2. Note that this is the largest script in the repo (~5500 lines); check the `request.*` budget
   and compile time before assuming it loads alongside other scripts on one chart
3. Direction split (Long Only / Short Only) before any parameter work
