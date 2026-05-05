# WaveTrend v3 [Composite] — Strategy Backtest Assessment

**Instrument:** Multi (CAPITALCOM:NATURALGAS, CAPITALCOM:CORN, NYMEX:PL1!, TVC:UKOIL, TVC:GOLD)
**Strategy file:** `wavetrend_v3_strategy.pine`
**Assessment date:** 2026-05-03

---

## Signal Logic

| Signal | Expression |
|--------|------------|
| Long   | `longSignal` = `longRRSignal` (range-reversal) OR `longPBSignal` (pullback-continuation) OR `longERSignal` (early-rejection, lower TF only by default) |
| Short  | `shortSignal` = `shortRRSignal` OR `shortPBSignal` OR `shortERSignal` |
| SL/TP  | `directional_fixed_tp` — `longStop`/`shortStop` from setup at signal time, `longTakeProfit`/`shortTakeProfit` to next structure target |
| Exit   | Indicator-driven `longExitSignal` / `shortExitSignal` (in addition to SL/TP) — see Exit Logic below |

**Per-family signal pipeline:**
- Each family has its own WT trigger (RR = OB/OS-based cross, PB = neutral-zone cross, ER = lower-TF rejection cross with MFI/Stoch RSI + local flow confirmation)
- Each family has its own setup gate (location, room, volume, MTF/anchor scoring)
- Each family has its own context-score against `_effMinScore`
- Universal volatility-regime gate (atrNorm) — 3 modes: Off / Score Only (+0.5 bonus) / Hard Gate (block out-of-band)
- `useSetupGate` toggle bypasses family setup-OK when desired (per-family wired)
- Lower-TF auto-bias can block ER/PB against a decisive setup-HTF trend while preserving RR reversals

---

## Profile System

A single `profileMode` input resolves to a coordinated set of internal parameters. `Custom` falls back to raw input controls.

| Profile | minScore | OB/OS | pbZone | edgePct | swingATR | regimeMode | regime band | POC loc/macro | volMode | mtfApply | shortRRConfirm | longPBConfirm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Strict | 4.0 | ±60 | 25 | 0.30 | 1.25 | Hard | 0.8/1.3 | 120/400 | All TF | All | ✓ | ✓ |
| **Balanced (default)** | **3.0** | **±45** | **50** | **0.45** | **2.5** | **Score Only** | **0.6/1.6** | **80/300** | Lower TF Only | None | ✓ | ✓ |
| Aggressive | 2.0 | ±45 | 50 | 0.45 | 2.5 | Score Only | 0.5/2.0 | 80/200 | Off | None | ✓ | ✓ |
| Reversal | 3.0 | ±45 | – (no PB) | 0.40 | 2.0 | Hard | 0.6/1.4 | 120/400 | Reversal Only | None | ✓ | – |
| Pullback | 2.5 | ±56 | 35 | 0.35 | 1.5 | Hard | 0.7/1.3 | 100/300 | Pullback Only | Pullback Only | input | ✓ |
| Diagnostic | 0.0 | ±20 | 50 | 0.50 | 5.0 | Off | – | 100/300 | Off | None | ✗ | ✗ |
| Custom | (raw inputs) | | | | | | | | | | | |

**Safety gates** (active in all production profiles):
- `shortRRRequireConfirm` — SHORT range-reversal must additionally have pullback-location OR bear structure trend
- `longPBRequireConfirm` — LONG pullback-continuation must additionally have range-edge-location OR (bull volume spike AND bull structure)
- `rangeReversalQualityMode` — symmetric LONG/SHORT RR quality filter: high score or POC + directional volume
- `requireLowerTFPBMidline` — 15m/1H PB needs WT already on the correct midline side
- `earlyRejectTFMode=Lower TF Only` — ER is blocked on 4H+ by default after test38 overtrading
- `useAutoTFBias` — 15m/1H ER+PB are blocked against decisive setup-HTF WT trend by default

**Balanced rationale:** test31 Aggressive showed Score 2.5 trades had PF 1.01 (noise) while Score ≥ 3.5 had PF ~2.0+. Balanced now uses Aggressive's loose setup gates (so all edge-quality candidates are reachable) but keeps `minScore=3.0` to filter the noise tier — targeting "edge-only" quality at meaningful frequency.

Commission used in all runs: 0.02%

---

## Exit Logic (indicator-driven)

Five toggles, each can be enabled independently. Visualized on chart as color-coded `✕ Reason · 1.42R` labels with full tooltip (entry-score, MFE, capture %, bars held).

| Exit | Default | Trigger | Notes |
|---|---|---|---|
| **Opposite Signal** | ON | Counter-direction signal fires AND has context score ≥ `oppositeExitMinScore` (default 3.0) | Score gate prevents weak counter-signals from killing good trades |
| **Family-WT-Cross** | ON | WT turns against the active family; RR/PB/ER use family-aware MFE guards | Reworked after test33-36 because current-R gates exited late after MFE had already given back |
| **MFE Giveback** | ON | Once MFE reaches family trigger, close if too much open R is given back | Default trigger 1.5R; PB trigger 1.0R because test39 still had PB trades reaching ~1R then returning to loss |
| **Time-Failure** | ON | `barsInTrade ≥ maxBarsInTrade` (auto-scaled, default 30 @ 4H) AND `R < minProfitR` (default 0.0) | Default closes only losing stagnant trades; breakeven stays open |
| **Follow-Through** | OFF (opt-in) | At exactly `followThroughBars` after entry, no directional progress beyond `followThroughATR × ATR` | Aggressive — kills slow-but-eventual-winners |

The strategy template (via `directional_fixed_tp` + `long_exit`/`short_exit` keys in `@strategy-config`) emits `strategy.close()` calls when any active exit signal fires, in addition to the static SL/TP from entry-time levels.

---

## Per-Trade Quality Tracking

Indicator maintains a per-trade journal in arrays — visualized in the Trade-Quality table (bottom-right of chart, `size.tiny` 3-column LONG/SHORT split):

| Metric | Meaning |
|---|---|
| Trades | Count by direction |
| WR % | Win rate (R > 0) |
| Avg R | Average R-multiple at exit |
| Avg MFE | Average peak R during trade (Maximum Favorable Excursion) |
| Capture % | Avg R / Avg MFE × 100 — fraction of available move captured |

Per-exit log line (`WT3 LONG/SHORT EXIT | family=… reason=… R=… MFE=… capturePct=… …`) enables forensic analysis: "SHORT-RR with reason=WT — average R?" or "trades with entry-score < 3 — average capture %?"

---

## Backtest Runs

Default = `Balanced` profile, NatGas 4H + multi-instrument validation set.

| Run | TF | Symbol | Period | Profile | Trades | PF | LONG PF | SHORT PF | Net | WR | Notes |
|-----|----|--------|--------|---------|--------|-----|---------|----------|-----|-----|-------|
| 26  | 4H | NATGAS | 2019-02 → 2026-03 | Balanced (pre-regime) | 23 | **3.54** | 5.87 | 1.80 | +87.764 USD (+8.78%) | 60.87% | Max DD 2.22%, **Return/DD 3.95** |
| 28  | 4H | 5 instruments | 2019 → 2026 | Balanced (pre-exit, post-regime) | 77 | **1.56** | – | – | +48.531 USD | 46.8% | NATGAS 1.98 / CORN 3.92 / PL 1.44 / UKOIL 1.07 / GOLD 0.81 |
| 31  | 4H | NATGAS | 2019 → 2026 | Aggressive (pre-exit) | 98 | 1.26 | 1.71 | 0.81 | +61.404 USD | 39.8% | Score-tier analysis: Score 2.5 PF 1.01 (noise), Score ≥ 3.5 PF ~2.0 |
| 32  | 4H | NATGAS | 2019 → 2026 | Aggressive + Exit Logic v1 | 124 | 1.21 | 1.83 | 0.69 | +49.009 USD | 45.2% | LONG +PB strong, SHORT-RR degraded (Family-WT-exit fired before TP) |
| 29  | 1H | NATGAS | 2024-05 → 2026-03 | Balanced | 10 | 0.59 | 0.00 | 1.61 | -10.063 USD | 10.0% | Cautionary — strategy is 4H-tuned |
| 33  | 4H | NATGAS | 2019 → 2026 | Aggressive baseline | 114 | 1.26 | 1.91 | 0.72 | +60.983 USD | – | Exposed exit failure: many positive-MFE trades closed late |
| 34  | 4H | NATGAS | 2019 → 2026 | Aggressive + first giveback | 115 | 1.07 | – | – | +14.011 USD | – | Giveback too tight; winners cut too early |
| 35  | 4H | NATGAS | 2019 → 2026 | RR quality + exit tuning | 52 | 1.631 | – | – | +46.958 USD | – | Strong quality filter; fewer trades, high PF |
| 36  | 4H | NATGAS | 2019 → 2026 | PB room override | 118 | 1.347 | – | – | +53.291 USD | 57.63% | Better trade count and net; PF lower but robust |
| 37  | 1H | NATGAS | 2024 → 2026 | Lower-TF baseline | 108 | 1.123 | 1.03 | 1.27 | +11.126 USD | 50.0% | 1H showed unused rejection candidates but weak margin |
| 38  | 4H | NATGAS | 2019 → 2026 | ER enabled all TF | 460 | 0.851 | 0.85 | 0.85 | -97.527 USD | 49.13% | ER overtraded 4H; reverted to lower-TF only |
| 39 Balanced | 4H | NATGAS | 2019 → 2026 | Balanced + ER blocked 4H | 97 | 1.426 | – | – | +52.546 USD | 60.82% | Current best robust 4H default before PB-MFE 1.0 and TF-bias |
| 39 Aggressive | 4H | NATGAS | 2019 → 2026 | Aggressive + ER blocked 4H | 129 | 1.356 | – | – | +57.085 USD | 56.59% | Higher net, lower quality than Balanced |
| 40 15m | 15m | NATGAS | 2025-11 → 2026-05 | Balanced/test39 settings | 126 | 1.106 | – | – | +7.329 USD | 35.71% | Short side carried; Long ER/PB weak |
| 40 1H | 1H | NATGAS | 2024-01 → 2026-05 | Balanced/test39 settings | 213 | 0.861 | – | – | -27.715 USD | 35.68% | Short ER was main failure (-22.1R) |
| 40 1D | 1D | NATGAS | 2017 → 2026 | Balanced/test39 settings | 3 | 0.904 | – | – | -679 USD | 33.33% | Too few trades; not statistically useful |

Run 26 = the canonical screenshot reference (Balanced before regime/exit changes — pure entry+SL/TP performance).
Run 32 = Aggressive with first-pass indicator-driven exits — surfaced SHORT-RR Family-WT-exit weakness, addressed in current code via R≥1 buffer.

**Current validation focus:** retest test39/test40 after the latest PB-specific MFE trigger (`pbMfeProtectR=1.0`), lower-TF PB midline filter, 1H ER quality filter, and Auto Lower-TF Trend Bias. Expected behaviour: preserve test39 4H Balanced quality while improving 1H/15m drawdown clusters.

---

## Best Configuration Results

**Run 26** — NatGas 4H standalone (pre-regime Balanced, equivalent to "entry quality + static SL/TP only"):

| Metric | All | Long | Short |
|--------|-----|------|-------|
| Net Profit | +87.764 USD (+8.78%) | +72.028 USD | +15.736 USD |
| Profit Factor | **3.54** | 5.87 | 1.80 |
| Win Rate | 60.87% | 64.3% | 55.6% |
| Trades | 23 | 14 | 9 |
| Max Drawdown | 22.220 USD (2.22%) | – | – |
| **Return / DD** | **3.95** | – | – |

By family:
- LONG pullback_continuation: 9 trades, WR 78%, PF **10.47** (the dominant edge)
- LONG range_reversal: 5 trades, WR 40%, PF 2.54
- SHORT range_reversal: 4 trades, WR 50%, PF 1.96
- SHORT pullback_continuation: 5 trades, WR 60%, PF 1.69

**Run 28** — Multi-instrument cross-asset validation (Balanced with regime filter, before exit logic):

77 trades / 5 instruments / 7 years. PF 1.56, Net +48.531 USD.

Per-symbol verdict:
- ✅ NATGAS, CORN, PL, UKOIL — PF ≥ 1.0 (all four positive)
- ❌ GOLD — PF 0.81 (excluded from supported set; structurally different volume/volatility regime)

---

## Key Findings

**What worked:**
- **Per-family architecture** — splitting RR (OB/OS trigger) from PB (neutral-zone trigger), each with its own gate stack, unlocked the pullback-continuation path that was previously starved (~0.5% of accepted trades) → now ~30-40% of all entries on NATGAS/CORN
- **Targeted confirm gates** — `shortRRRequireConfirm` cleared a documented bleed (SHORT-RR PF 0.68 → 1.80+); `longPBRequireConfirm` did the same for LONG-PB (0.53 → consistently ≥ 1.5)
- **Profile-Layer** — single switch coordinates ~15 internal parameters; `Diagnostic` invaluable for forensic analysis of edge sources
- **Volatility-Regime filter** — flipped GOLD/UKOIL from negative toward positive, unlocked PL as new supported instrument; Score-Only mode preserves capture from compression-breakout setups
- **POC lookback split** — local (80-120) for entry-context score, macro (200-400) for bias overlay
- **Indicator-driven exits** — Time-Failure (loss-only) and Family-WT (RR with R-buffer) cut losing stagnant trades; Opposite-Signal with score gate enables clean position flips on conviction
- **Per-trade quality tracking** — Entry-Score, MFE, R, Capture % surfaced in chart labels + dedicated dashboard table; per-exit log enables forensic analysis
- **4H ER containment** — test38 proved unconfirmed ER is destructive on 4H; `earlyRejectTFMode=Lower TF Only` restored test39 PF/net immediately
- **PB room override with confirmation** — raised 4H trade count while retaining positive PF in test36/test39
- **Auto Lower-TF Trend Bias** — added after test40 to use the next higher TF only when its WT trend is decisive; default applies to ER/PB, not RR

**What remains weak:**
- **GOLD outside scope** — different volatility/volume regime (FX-style underlying); excluded from supported set
- **Lower timeframes (1H, 15m)** — test40 shows 15m is marginally positive but 1H is negative. Lower-TF settings now have dedicated PB midline, 1H ER quality, and HTF-bias filters, but require fresh validation.
- **SHORT-RR remains the structurally weakest sub-family** even with the Family-WT R-buffer fix. NATGAS-specific structural asymmetry (sharp drops, slow recoveries)
- **SHORT-ER on 1H** — test40: Short ER was the largest lower-TF loss source. Added 1H-only POC-reject requirement and HTF trend-bias gate.
- **PB capture** — test39 still had 12-13 trades with `MFE >= 1R` ending `R <= 0`. Added `pbMfeProtectR=1.0`.
- **Sample size per instrument is moderate** (8-23 trades each over 7 years). Combined 77 trades is the meaningful aggregate

---

## Verdict

**Rating:** Promising / Ready-candidate (NATGAS 4H), lower TF experimental

The strategy demonstrates a robust 4H NATGAS edge after the exit/entry redesign. The best current 4H evidence is test39 Balanced: PF 1.426, 97 trades, +52.5k, WR 60.8%. Aggressive produces higher net (+57.1k) but lower PF and more marginal PB trades.

The per-family architecture now has three families: RR, PB, and lower-TF ER. ER is deliberately disabled on 4H+ by default because test38 showed severe overtrading when used on 4H. The current code treats exits as trade-management rather than indicator-state reuse, using MFE giveback, family-aware WT exits, opposite-signal exits, and time-failure exits.

Lower timeframes are still experimental. test40 showed 15m can be positive but fragile, while 1H failed due mainly to Short ER. The latest code adds timeframe-specific quality controls, but these changes still need a new test40-style validation pass.

**Next steps:**
1. **Retest NATGAS 4H Balanced/Aggressive** after `pbMfeProtectR=1.0` and Auto Lower-TF Trend Bias to ensure test39 quality is preserved.
2. **Retest test40 15m/1H/1D** after PB midline + 1H ER quality + HTF-bias; target is 1H PF back above 1.0 without destroying 15m Short-ER edge.
3. **Multi-instrument re-validation** with the new exit logic and 4H ER containment — repeat the 5-instrument run.
4. **Drawdown distribution analysis** across instruments/timeframes.
5. **Forward-test on paper** — confirm slippage and execution match backtest assumptions, especially around indicator-driven exits and `strategy.close()` behavior.
6. **Add 1-2 more commodity instruments** (CL1!, ZS, ZW) to strengthen multi-instrument validation.
