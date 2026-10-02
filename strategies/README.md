# Backtesting

Strategy wrappers for selected WavesUnchained indicators. Each script is a self-contained
Pine Script v6 `strategy()` that replicates the indicator logic and adds entry/exit
management for TradingView's Strategy Tester.

All strategies are **standalone and hand-maintained**. There is no generator: an indicator
change does not propagate by itself, pulling a strategy back in line is a deliberate step.
The Claude Code skill `strategy-from-indicator` carries the build rules.

---

## Scripts

| Directory | Based on | SL type |
|---|---|---|
| `chandelier_flip_radar/` | Chandelier Flip Radar | Trailing (ATR envelope) |
| `commodity_pulse_matrix/` | Commodity Pulse Matrix v4 | Directional fixed SL/TP |
| `market_average_relationship_engine/` | Market–Average Relationship Engine | Trailing (MA ∓ ATR×) |
| `oscillator_divergence_zones/` | Oscillator Divergence Zones | Pivot + ATR buffer |
| `reversal_engine_score/` | Reversal Engine Score | Structural + R-multiple TP |
| `smooth_trend_radar/` | Smooth Trend Radar | Fixed, TP1/TP2/TP3 levels |
| `wavetrend/` | WaveTrend v4 | Trailing |

Each directory holds the `.pine` file and its `<name>_strategy_assessment.md` — the only
place backtest figures belong. Schema: [`ASSESSMENT_SCHEMA.md`](ASSESSMENT_SCHEMA.md).

---

## How to load in TradingView

1. Open the Pine Editor
2. Paste the contents of one of the `.pine` files
3. **Add to chart** — the Strategy Tester tab appears below
4. Set the range in Strategy Tester → Properties → Backtest Range

**Use standard candles/bars only.** Every strategy draws a red warning label on Heikin Ashi,
Renko, Kagi, Line Break, P&F and Range charts: orders there fill at synthetic bar prices and
the result is meaningless — reliably flattering, never reproducible.

---

## Shared defaults

| Setting | Value | Note |
|---|---|---|
| Position size | 10% of equity | Change via TradingView Properties |
| Commission | 0.02% | Realistic for CFD/futures; raise for crypto maker/taker |
| Slippage | 1 tick | Increase for illiquid instruments |
| Entries | On confirmed bar | `confirmClose` input, on by default — prevents repainting |

Overnight/roll financing on CFDs is **not** priced in. On multi-day holds that is a known,
unquantified drag on every rating in this directory.

Shared inputs: Trade Direction (Both / Long Only / Short Only), Cooldown Bars After Exit,
Break-Even Stop + trigger, plus a Filters group (session, date range, max drawdown, max
intraday loss, losing-streak limit).

---

## Optimization workflow

**Step 1 — instrument and timeframe.** Run on at least 2 instruments and 2 timeframes before
drawing any conclusion. Candidates: ES/SPY (1H, 4H, D), NQ/QQQ (1H, 4H), EURUSD (4H, D),
BTCUSD (1H, 4H, D), CL crude (1H, 4H), NG natural gas (1H, 4H, D).

**Step 2 — baseline.** Run with defaults first and record net profit %, max drawdown %,
win rate, profit factor and trade count. Under 30 trades is not a result.

**Step 3 — one group at a time.** Optimizing all parameters at once produces an overfit set.
Change one group, re-measure, keep or revert.

**Step 4 — walk-forward.** Validate on data outside the optimization window. A parameter set
that only works on the window it was fitted to is fitted, not found.

**Step 5 — direction split.** Test Long Only and Short Only separately. Trend-following
strategies are frequently asymmetric on a given instrument, and an aggregate that looks
mediocre often hides one healthy side and one broken one.

Every run that informs a decision belongs in the strategy's assessment file with its
instrument, timeframe and sample size attached. A figure without that context is not a result.

---

## Known limitations

- **Entry execution** — signals fire on bar close, the strategy enters at the next bar's open.
  That is the realistic case. `process_orders_on_close=true` fills at the exact close: useful
  for comparison, not for expectations.
- **Pivot-anchored stops** — the SL can sit several bars in the past. On illiquid instruments
  check that the resulting distance still describes a tradable risk.
- **HTF pivots via `request.security`** use `lookahead=on` against `[1]`-offset series. That
  is the correct non-repainting pattern, but it needs sufficient history to warm up.

---

## Adding a strategy

Invoke the `strategy-from-indicator` skill — it holds the input groups, the six exit patterns,
the `indicator()` → `strategy()` transformation and the traps (`alertcondition()` is a compile
error in a strategy; break-even must fold into the existing stop, not become a second exit).

Candidates: `vein_pullback` (explicit pullback-end signals with a structural SL),
`vein_execution` (15M execution module with TRIGGER status).
