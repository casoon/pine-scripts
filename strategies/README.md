# Backtesting

Strategy wrappers for selected WavesUnchained indicators. Each script is a
self-contained Pine Script v6 `strategy()` that replicates the indicator logic
exactly and adds entry/exit management for TradingView's Strategy Tester.

---

## Scripts

| File | Based on | Signal type |
|------|----------|-------------|
| `cfr_strategy.pine` | Chandelier Flip Radar v1.2 | Trend flip (ATR trailing stop) |
| `str_strategy.pine` | Smooth Trend Radar v3.3 | Trend flip + pivot rejection |
| `odz_strategy.pine` | Oscillator Divergence Zones v1.0 | RSI/CCI/MFI divergence |

---

## How to load in TradingView

1. Open Pine Editor (`/` → Pine Editor or bottom panel)
2. Paste the contents of one of the `.pine` files
3. Click **Add to chart** — the Strategy Tester tab appears below the chart
4. Set the date range in Strategy Tester → Properties → Backtest Range

---

## Default settings

All strategies share these defaults:

| Setting | Value | Note |
|---------|-------|------|
| Position size | 10% of equity | Change in `strategy()` header or via TradingView Properties |
| Commission | 0.05% per side | Adjust for your broker/instrument |
| Slippage | 1 tick | Increase for illiquid instruments |
| Entries | On bar close | Next-bar open execution (conservative) |

---

## Strategy-specific notes

### cfr_strategy.pine
- Default behavior: enters on flip, exits on next opposite flip (no TP limit)
- Enable **Use Fixed ATR Take Profit** to add a hard profit target
- The **Chandelier trailing stop** is the SL — it ratchets in the direction of the trade every bar
- Best for: trending markets, medium to high timeframes (1H+)

### str_strategy.pine
- **Entry Mode**: choose Flip Only, Rejection Only, or both
- **Exit at TP**: selects which TP level (TP1/TP2/TP3) is used as the exit limit order. `None` = ride until the next flip closes the trade
- **TP Method**: `R-Multiple` is most portable across instruments (no session dependency). `Pivot` requires clean daily/weekly pivots
- **Trail to BE**: once TP1 is reached, SL moves to entry — useful for reducing drawdown without capping upside
- Rejection signals fire `_efPivBars` bars after the actual pivot — this is non-repainting by design

### odz_strategy.pine
- Signals fire `pivRight` bars after the actual divergence pivot (confirmed, non-repainting)
- SL is anchored to the **divergence pivot** (low for bull, high for bear) + ATR buffer — not to the entry bar
- TP is a fixed R:R from entry close, using the SL distance as the unit
- Hidden divergence (continuation) can be added via **Include Hidden Divergence Entries**
- Best for: counter-trend reversals on daily/4H; continuation trades on 1H/15M with hidden div

---

## Optimization workflow

### Step 1 — Choose instrument and timeframe
Run each strategy on at least 2 different instruments and 2 timeframes before drawing
conclusions. Recommended combinations to test first:

| Instrument | Timeframes |
|------------|-----------|
| ES / SPY | 1H, 4H, Daily |
| NQ / QQQ | 1H, 4H |
| EURUSD | 4H, Daily |
| BTC/USDT | 1H, 4H, Daily |
| CL (crude oil) | 1H, 4H |

### Step 2 — Baseline run
Before optimizing, run with defaults. Record:
- Net profit %
- Max drawdown %
- Win rate %
- Profit factor
- Number of trades (< 30 = insufficient data)

### Step 3 — Optimize one group at a time
Avoid optimizing all parameters simultaneously — it leads to overfitting.
Suggested order:

**CFR:** `atrLen` → `atrMult` → `bodyFilter` → `tpMult` (if TP enabled)

**STR:** `stFactor` → `slMultiplier` → `exitLevel` → `tpMode` → `tp multipliers`

**ODZ:** `pivLeft`/`pivRight` → `oscLen` → `slBuf` → `tpRR` → `oscType`

### Step 4 — Walk-forward check
After finding good parameters, test on **out-of-sample** data (the period NOT used
for optimization). A parameter set that works only on the optimized window is overfit.

Typical split: optimize on bars up to 2024-01-01, validate on 2024-01-01 → present.

### Step 5 — Direction filter
Test each strategy with `Long Only` and `Short Only` separately. Many trend-following
strategies perform significantly better in one direction on a given instrument.

---

## Important limitations

- **Entry execution**: signals fire on bar close; the strategy enters at the **next bar's open**.
  This is realistic. If you set `process_orders_on_close=true` in the `strategy()` call,
  entries execute at the exact close price — useful for comparison but not realistic.
- **Pivot-based TP (STR)**: uses `request.security` with `lookahead=on` for prior-session
  pivots. This is correct (uses *previous* session's H/L/C), but requires sufficient history.
- **ODZ SL anchor**: the SL is set at the divergence pivot price, which can be several bars
  in the past. On illiquid instruments, check that `pivRight` is not so large that the
  pivot's SL distance makes the trade unrealistic.
- **Commission and slippage**: the defaults (0.05%, 1 tick) are conservative for futures/FX
  spot. For crypto with maker/taker fees, increase commission to 0.1%.

---

## Adding more strategies

To wrap another indicator:
1. Copy the indicator's full Pine Script
2. Replace `indicator(...)` with `strategy(...)` (add `default_qty_type`, `commission_type`, etc.)
3. Add a `g_strat = "Strategy"` input group with direction filter and exit level inputs
4. Remove all `label.new()`, `line.new()`, `linefill.new()`, `alertcondition()` calls
5. Keep `plot()` and `barcolor()` — useful for visual review of trades
6. Add `strategy.entry()` on signal conditions
7. Add `strategy.exit()` on `strategy.position_size != 0` every bar with current SL/limit

Good candidates for future wrappers:
- `vein_pullback.pine` — explicit pullback-end signals with clear SL (EMA + structure)
- `vein_execution.pine` — 15M execution module with TRIGGER status
- `chandelier_flip_radar` + `smooth_trend_radar` combined (CFR as filter, STR as entry)
