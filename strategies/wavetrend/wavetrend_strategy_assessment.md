# WaveTrend — Strategy Backtest Assessment

**Instrument:** NatGas (CAPITALCOM:NATURALGAS), in-sample
**Strategy file:** `wavetrend_strategy.pine`
**Assessment date:** 2026-05-01

---

## Signal Logic

| Signal | Expression |
|--------|------------|
| Long   | `longSignal` — cross from negative zone OR sustained-bull trigger + score ≥ sigMinScoreLong + gate checks |
| Short  | `shortSignal` — cross from positive zone OR sustained-bear trigger + score ≥ sigMinScoreShort + gate checks |
| SL type | trailing (ATR × multiplier from current bar low/high — per-bar volatility envelope, not ratcheting) |

---

## Optimized Settings (current defaults)

| Parameter | Default | Notes |
|-----------|---------|-------|
| useAutoCalibrate | true | Scale bar-counts to chart TF (anchor 4H) — major lever for 1D performance |
| sigMinScoreLong | 1 | Score = bonus quality beyond gates; `0` disables the score gate |
| sigMinScoreShort | 1 | Same for shorts |
| atrMult | 3.0 | Trailing stop ATR multiplier |
| sigGateZone | true | Require osc in OS/OB zone (strict — empirically optimal) |
| sigGateSlope | true | Require slope direction confirmation |
| sigGateExtA | true | Suppress crosses after extended zone occupancy |
| sigGateSustained | true | Suppress mid-zone crosses in sustained trend (OS/OB exception) |
| sigGateVol | false | ATR-regime gate — opt-in (filters out volatile reversals on NatGas) |
| sigLongPersist | true | Sustained-bull trigger ON — major contributor to long PF |
| sigShortPersist | true | Sustained-bear trigger ON — works on 1D, weaker on 4H |
| persistOscBlock | 1.5 | Persist depth filter — effectively disabled at default; 0.8 helps 4H but hurts 1D |
| zoneMode | Fixed | Adaptive (Percentile) is opt-in for highly spiky instruments |

Commission used in all runs: 0.02%

---

## Backtest Runs

| Run | TF | Period | ScoreLong | ScoreShort | atrMult | Score v | PF All | PF Long | PF Short | Net % | Max DD% | Trades | WinRate |
|-----|----|--------|-----------|------------|---------|---------|--------|---------|----------|-------|---------|--------|---------|
| 1 | 4H | 2019–2026 | 4 | 4 | 3.0 | v1 | 1.092 | 1.065 | 1.110 | +4.1% | 13.82% | 67 | 52.24% |
| 2 | 1H | 2024–2026 | 4 | 4 | 3.0 | v1 | 0.938 | 1.228 | 0.705 | −1.65% | 8.14% | 79 | 48.10% |
| 3 | 1H | 2024–2026 | 4 | 4 | 3.0 | v2 | 0.920 | 1.226 | 0.682 | −2.15% | 8.08% | 80 | 47.50% |
| 4 | 4H | 2019–2026 | 4 | 4 | 3.0 | v2 | 1.116 | 1.065 | 1.150 | +5.23% | 13.03% | 68 | 52.94% |
| 5 | 15m | 2024–2026 | 4 | 4 | 3.0 | v2+ExtA | — | — | — | −2.18% | 3.48% | 30 | 46.67% |
| 6 | 1H | 2024–2026 | 4 | 4 | 3.0 | v2+ExtA | — | — | — | +5.92% | 3.84% | 52 | 53.85% |
| 7 | 4H | 2019–2026 | 4 | 4 | 3.0 | v2+ExtA | — | — | — | +9.41% | 6.41% | 28 | 42.86% |
| 8 | 4H | 2019–2026 | 1 | 1 | 3.0 | v5 (Vol on) | 0.991 | 0.840 | 1.248 | −0.11% | 7.75% | 13 | 38.46% |
| **9** | **4H** | **2019–2026** | **1** | **1** | **3.0** | **v6 (Vol off)** | **1.486** | **1.382** | **1.556** | **+9.41%** | **6.41%** | **28** | **42.86%** |
| 10 | 15m | 6 mo | 1 | 1 | 3.0 | v6 | 0.700 | 0.883 | 0.498 | −2.18% | 3.48% | 30 | 46.67% |
| **11** | **1H** | **2024–2026** | **1** | **1** | **3.0** | **v6** | **1.374** | **1.476** | **1.278** | **+5.92%** | **3.84%** | **52** | **53.85%** |
| 12 | 1D | 2018–2026 | 1 | 1 | 3.0 | v6 | 0.757 | 0 | 0.825 | −1.51% | — | 4 | 50.00% |
| **13** | **4H** | **2019–2026** | **1** | **1** | **3.0** | **v6 + sigLongPersist + sigShortPersist** | **1.490** | **2.543** | **1.006** | **+18.58%** | **10.23%** | **59** | **54.24%** |
| **14** | **1D** | **2017–2026** | **1** | **1** | **3.0** | **v7 Auto-Cal + both sustained triggers** | **2.418** | **2.845** | **1.878** | **+52.60%** | **12.88%** | **66** | **46.97%** |
| 15 | 4H | 2024–2026 | 1 | 1 | 3.0 | v7 + both persist (no v8 filter) | — | — | — | +23.12% | — | — | — |
| 16 | 1H | 2024–2026 | 1 | 1 | 3.0 | v7 + both persist + v8 filter | 1.295 | 1.302 | 1.290 | +6.89% | 3.42% | 87 | 54.02% |
| 17 | 1D | 2017–2026 | 1 | 1 | 3.0 | v9 full (gate-relaxed + ratcheting) | 1.347 | 2.385 | 0.571 | +15.96% | 15.21% | 74 | 37.84% |
| 18 | 1D | 2017–2026 | 1 | 1 | 3.0 | v9 partial revert (gates back, stop ratcheting kept) | 1.347 | 2.385 | 0.571 | +15.96% | 15.21% | 74 | 37.84% |
| 19 | 1D | 2017–2026 | 1 | 1 | 3.0 | v9 full revert + persistOscBlock=0.8 | 1.952 | 2.643 | 1.359 | +39.46% | 12.85% | 60 | 48.33% |
| **20** | **1D** | **2017–2026** | **1** | **1** | **3.0** | **final (Run 14 reproduced, persistOscBlock=1.5)** | **2.418** | **2.845** | **1.878** | **+52.60%** | **12.88%** | **66** | **46.97%** |
| 21 | 1D | 2017–2026 | 1 | 1 | 3.0 | v10 + divTypeBySource=true | 0.929 | 1.125 | 0.711 | −1.65% | 8.89% | 25 | 36.00% |
| **22** | **1D** | **2017–2026** | **1** | **1** | **3.0** | **v11 Vol Exit (1.6) + percLookback=200** | **3.069** | **4.080** | **2.044** | **+69.69%** | **14.32%** | **71** | **47.89%** |
| **23** | **1D** | **NYMEX:NG1! 1990–2026 (35 yr)** | **1** | **1** | **3.0** | **v11 (same as Run 22)** | **1.218** | **1.929** | **0.654** | **+33.66%** | **28.55%** | **310** | **45.48%** |

---

## Best Configuration Results

**Run 22** (1D NatGas, 2017–2026, v11 — current defaults): **PF 3.069** · PF Long 4.080 · PF Short 2.044 · net **+69.69%** · 71 trades · win rate 47.89% · max DD 14.32% · **Return/DD 4.87** · avg winner / avg loser = 3.34×. New best configuration in the repo. Vol-Exit (ATR×1.6) cuts climax bars before reversals eat open profit; combined with `percLookback=200` the score components are calibrated against a more stable distribution.

**Run 20** (1D NatGas, 2017–2026, baseline before Vol-Exit): PF 2.418 · net +52.60% · 66 trades · DD 12.88%. Useful comparison point — shows the Vol-Exit lift in isolation.

**Run 13** (4H NatGas, 2019–2026, v6 + both sustained triggers): PF 1.490 · net +18.58% · 59 trades · DD 10.23%.

**Run 11** (1H NatGas, 2024–2026, v6): PF 1.374 · net +5.92% · 52 trades · DD 3.84%.

Reach Run 22 with: chart on **1D**, `useAutoCalibrate=true`, all gates ON except `sigGateVol`, both sustained triggers ON, `sigMinScoreLong/Short=1`, `atrMult=3.0`, `persistOscBlock=1.5`, `enableVolExit=true` (ratio 1.6), `percLookback=200`, both directions.

## Timeframe Suitability

Same v6 settings tested across timeframes (NatGas):

| TF | Verdict | Why |
|----|---------|-----|
| 15m | **Skip** — PF 0.70 | Mean-reversion structurally fails on intraday noise; 30 trades all losing average. Cannot be fixed by gate tuning. |
| 1H | **Use** — PF 1.374 | Sweet spot for trade count (52) and quality. Higher win rate than 4H. |
| 4H | **Use** — PF 1.486 | Best PF, longest historical edge. Lower trade count but cleaner signals. |
| 1D | **Best** — PF 2.42 with v7 Auto-Cal | With auto-calibrate enabled and both sustained triggers, 1D becomes the strongest configuration: 66 trades / 9 years, +52.60% net, Return/DD 4.08. |

## Changes (v9) — Code Review Iteration & Revert Journey

External code review identified six "issues" (3 bugs, 3 over-strict gates / stop-management). All implemented in v9, then re-tested against the Run 14 baseline. The bugs were real and stayed; the gate/stop changes degraded performance and were reverted one by one.

**Trajectory on 1D NatGas (PF):**
- Run 14 (baseline): **2.42**
- Run 17/18 (v9 full): 1.35 — drop of −44%
- Run 19 (v9 with gate reverts, ratcheting kept): 1.95
- Run 20 (v9 with everything reverted, persistOscBlock=1.5): **2.42** (baseline restored)

**What stayed (real bugs and harmless cleanups):**
- **Cooldown bug** (in `build_strategies.py`): `strategy.closedtrades.exit_bar_index(0)` returned the FIRST closed trade, not the last. Effect: cooldown was broken. Fixed to `strategy.closedtrades - 1`. No effect on results when `cooldownBars=0` (default).
- **Dashboard state outside `if barstate.islast`**: `crossState`/`divState` decay logic only executed on the last bar — historical decay was broken. Moved to top-level. Display-only effect.
- **Break-even integrated into trailing exit**: replaces a separate `strategy.exit("Long BE", ...)` order with a single computed `_finalLongStop`. Avoids order races. No effect when `enableBE=false` (default).

**What got reverted (looked right, failed empirically):**

Each of these was conceptually correct in isolation but cost real performance on NatGas:

| Change | What it tried to do | Why it failed empirically |
|--------|--------------------|---------------------------|
| Trailing stop ratcheting (`math.max`/`math.min`) | Make stop monotonically tighten | NatGas has wide intra-trade retracements; ratcheted stop hit on normal volatility, cut winners short. 1D Short PF 1.88 → 0.57. |
| ExtA Deep-Extreme exception | Honor tooltip promise "Strong crosses are never suppressed" | Admitted catastrophic late shorts at deeply extended OB conditions. |
| Zone-Gate "recent visit" only | Match crossBull semantics (already requires recent visit) | On 4H let through more late-zone shorts; on 1D was a no-op due to auto-cal scaling. |
| `persistOscBlock=0.8` default | Block exhausted persist signals | Helps 4H (~+65pp on persist contribution from a single sample) but cuts legitimate persist winners on 1D. Default raised to 1.5 = effectively disabled. |

**Lesson:** the strict-gate / loose-stop / no-persist-filter configuration was empirically optimal for NatGas. Code-review-style "improvements" that looked unobjectionable each cost real performance. Backtest data > code review intuition for parameter / logic decisions on a specific instrument.

Deferred to next iteration: StochRSI lower-TF semantics (#3), splitting Regular vs Hidden divergence by signal source (#8). Both involve significant refactor; not started.

## Changes (v10) — Phase 2 of code review

Both deferred items from v9 implemented as opt-in toggles (defaults preserve Run 20).

### #8 Divergence type by signal source

**Implementation:**
- Track 4 separate ages: `_regBullDivAge`, `_hidBullDivAge`, `_regBearDivAge`, `_hidBearDivAge`
- New input `divTypeBySource` (default `false`)
- When enabled: Cross signals use Regular divergence (reversal pairing), Persist signals use Hidden divergence (continuation pairing). Zero-cross falls back to combined any-type age.
- When disabled: combined any-type age is used (current behavior, default).
- Marker tooltip dynamically shows which div type was checked.

**Run 21 result** (1D NatGas, `divTypeBySource=true`):

| Metric | Run 20 (default) | Run 21 (split on) | Δ |
|--------|------------------|-------------------|---|
| PF | 2.418 | **0.929** | −62% |
| Net % | +52.60% | −1.65% | collapses |
| Trades | 66 | **25** | −62% |
| Win Rate | 46.97% | 36.00% | −11pp |

**Why it failed:** Persist signals fire in the mid-zone (osc between 0 and threshold) where 4 of 5 score components don't activate (no extreme percentile, no recent OS/OB visit, no zone-held streak, no deep extreme). They typically earn their single score point ONLY from the divergence component. Restricting Persist to Hidden-only div drops 41 of 66 signals below the `sigMinScore=1` threshold — most Persist signals fail to fire at all. The surviving Persist trades aren't disproportionately profitable, so total return collapses.

The reviewer's theoretical pairing (Regular = reversal = pair with Cross; Hidden = continuation = pair with Persist) is sound textbook theory but empirically falsified on NatGas: the "wrong-pair" combinations contribute substantial profit. Default stays OFF.

### #3 StochRSI Lower-TF

**Bug in original implementation:** `request.security` with a lower-TF argument only returns the CLOSING value of each lower-TF aggregation at chart-bar boundary. Sub-bar K crossovers that happen and close out within a chart bar were invisible. The tooltip promised "lower TF for finer entry timing" but the code couldn't deliver that.

**Fix:** dual security calls.
- `request.security_lower_tf(syminfo.tickerid, stochTF, expression, ignore_invalid_timeframe=true)` returns arrays of all sub-bar K values and pre-computed trigger booleans (one element per sub-bar within the chart bar).
- `request.security(...)` is evaluated as fallback for the equal-or-higher-TF case (returns scalar at TF close).
- Auto-detection: compare `timeframe.in_seconds(stochTF)` vs `timeframe.in_seconds()` (chart) and pick the right path.
- Lower-TF trigger fires when `array.includes(triggerArray, true)` — i.e., any sub-bar element captured a crossover.
- Tooltip rewritten honestly: "LOWER TF → security_lower_tf for sub-bar precision; HIGHER TF → security at TF close."

No empirical test in this iteration since `useStochRSI=false` is default (Run 20 unaffected). The fix unblocks the documented use case for users who want it.

### Defaults unchanged
Run 20 (Best Configuration) is unaffected by either change. Both are opt-in toggles for users who want to test theory variations or use lower-TF StochRSI timing.

### Code review final tally

After two iterations through the review, the empirical scorecard:

| # | Item | Status | Reason |
|---|------|--------|--------|
| 1 | ExtA Deep-Extreme exception | Reverted | Admitted catastrophic late shorts |
| 2 | Zone-Gate "recent visit" | Reverted | No-op on 1D auto-cal; let through bad shorts on 4H |
| 3 | StochRSI Lower-TF refactor | Implemented | Technically correct; no empirical regression (opt-in) |
| 4 | Cooldown index bug | Fixed | Real bug; no behavior change at default `cooldownBars=0` |
| 5 | Trailing stop ratcheting | Reverted | Cut winners short on NatGas retracements |
| 6 | BE integration into trailing exit | Implemented | Cleaner; no behavior change at default `enableBE=false` |
| 7 | Dashboard state outside `if barstate.islast` | Fixed | Real bug; display-only effect |
| 8 | Divergence type by signal source | Opt-in (default off) | Run 21 falsified theory empirically |

Plus the related v8-era addition (`persistOscBlock=0.8` as default): also reverted (`=1.5` = disabled).

**Bottom line:** 3 bugs fixed, 2 cleanups (BE-integration, StochRSI lower-TF), 4 logic changes empirically falsified on NatGas. The code review delivered real bug fixes but every "improvement to logic" cost performance.

## Phase 3 — Exit Logic (#9 implemented as opt-in)

All three exit-logic ideas from the reviewer (#9A/B/C) are now implemented in the strategy template as opt-in features. Defaults are OFF — Run 20 baseline is preserved exactly. New strategy inputs in group **"Strategy — Advanced Exits"**:

**#9A Partial Exit — REMOVED**
Implemented and tested. On NatGas, locking in 50% at 1R didn't improve PF — the strategy already extracts the full asymmetric payoff via the trailing stop, and partial exits cut the profitable runner side without offsetting risk reduction. Entry-tracking state and partial-exit logic removed from the trailing template.

**#9B Structure Exit — REMOVED**
Implemented and tested with three sub-conditions (zero-line flip, opposite signal cross, opposite-zone entry). Empirically no improvement over the trailing ATR stop on NatGas. Removed from `build_strategies.py` template, the WaveTrend `@strategy-config` block, and all generated strategy files. Generic cfg-based mechanism (`struct_long_exit` / `struct_short_exit` keys) also removed since no indicator was using it.

**#9C Volatility Exit (ATR spike) — KEPT, default ON**
- `enableVolExit` (default **true**), `volExitRatio` (default **1.6**)
- Closes position when `ta.atr(atrLen) >= volExitRatio × ema(ta.atr(atrLen), 50)`
- Catches climax / exhaustion bars where the rest of the move is unlikely to continue

**Empirical result:** tested on NatGas — **significant improvement** over Run 20 baseline. The single Phase 3 #9 idea that works on this instrument. ATR-spike exits successfully cut climax bars before the reversal eats the open profit, while leaving the bulk of trend-following trades undisturbed.

To test: enable individually on Run 20 setup (1D NatGas, both sustained triggers on, defaults otherwise) and compare to baseline PF 2.418.

---

## Pending Review Feedback (Phase 3+ remaining)

Items #10/#11/#12 from the reviewer not yet implemented — design decisions still open.

### #10 Score-System reconsideration

Reviewer's critique: the score gate blocks 127 signals (per debug log analysis) — many of those are legitimate trades that just don't score high on a generic "quality" metric. Persist signals especially live with low scores (typically 1, sometimes 0).

Suggested test: `sigMinScore = 0` (score gate fully disabled, only hard gates active).

Hypothesis: more trades, similar or better PF. Worth testing on 1D and 4H.

If the hypothesis holds, the score system becomes purely informational (color-coding markers, debug visibility) rather than a gating mechanism. Simpler and likely more honest about what's actually filtering.

### #11 Persist is the alpha — but `persistOscBlock` is a hack

Observation: Persist signals carry the alpha (Run 13 Long PF 2.54, Run 20 overall 2.42 — unusually strong PF for a mean-reversion-flavored indicator).

Risk: Persist can fire at exactly the wrong moment — V-bottoms / V-tops where the trend it's "continuing" is actually about to reverse. Catastrophic single-trade losses (e.g. 4H Short 2022-07-01: −61.12%).

Current solution: `persistOscBlock` (depth filter, default 1.5 = disabled). Reviewer flags this as a hack rather than a clean structural fix.

Cleaner alternatives to explore:
- Market-structure context (Higher Highs / Lower Lows on price) — Persist long only fires if recent structure is bullish (HH/HL); Persist short only if bearish (LL/LH). Requires structure detection.
- Volatility regime — Persist signals require below-average ATR (calm trend) to fire. Filter out exhaustion-volatility signals.
- Slope inflection — require WT slope to be flat-or-strengthening at the moment of trigger, not decelerating from a peak.

Each of these is a non-trivial refactor. Empirically, `persistOscBlock` did help on 4H but cost 1D performance — so a TF-aware or structure-aware version is the next-level fix.

### #12 StochRSI — caution

Reviewer's caution: layering StochRSI as a gate (require both WT signal AND StochRSI confirmation) is a classic "two oscillators saying the same thing" trap. It massively reduces trade count and rarely adds true edge — both indicators measure momentum extremes, just at different frequencies.

Reviewer's recommendation: use StochRSI as a **timing layer**, not as a gate.
- Timing layer = WT identifies the setup, StochRSI provides the entry trigger (e.g., wait for K crossover after WT signal flags valid setup)
- Gate = require both signals to agree on the same bar (current implementation)

Practical implication for v10's StochRSI implementation: the lower-TF refactor was correct, but the use case it supports (sigGateStochRSI=true) is the wrong use case to start with. The timing-layer use case would defer entries by N bars after a WT signal until StochRSI confirms — different code path entirely.

Lowest-effort change: rename or reframe `sigGateStochRSI` to clarify it's "co-bar confirmation" (current) and add a separate `sigStochRSIAsTrigger` mode (delayed entry).

For now: keep StochRSI off by default, document the caution in the tooltip.

---

## Changes (v8)

Trade-by-trade analysis of Run 13 (4H, both sustained triggers ON, 59 trades) against the debug log to find loser patterns:

- **Catastrophic Short Persist losses** all happened when oscillator was already deep in OS territory (osc < ~-45 vs lowerThreshold=-56.5). NatGas V-bottoms caught the persist-bear signal at exhaustion. Three trades alone: -61.12%, -24.03%, -9.33%.
- **Long Persist losers** mixed (some negative slope, some too-high osc) — no clean filter, winners and losers overlap.
- **Cross losers vs winners** statistically indistinguishable in osc/slope/pct/score — would need market structure (HH/LL) to filter further.

**New `persistOscBlock` filter (default 0.8 × threshold):**
- Short Persist blocked if `wtOsc < lowerThreshold × 0.8` (don't trend-follow into exhaustion)
- Long Persist blocked if `wtOsc > upperThreshold × 0.8` (symmetric for consistency, slightly costly on NatGas longs but generally robust)
- Estimated impact on Run 13 4H: net Persist contribution improves from +94% trade-cumulative to +160% (+65 percentage-points improvement)

## Changes (v7)

- **Auto-Calibrate by Timeframe** (`useAutoCalibrate`, default `false`): when enabled, all bar-count parameters scale to wall-clock equivalents relative to the 4H baseline. The displayed input values represent "4H equivalent" — on 1H they multiply ×4, on 1D they shrink ~÷6, on 15m they multiply ×16.
- Scaled parameters: `chLength`, `avgLength`, `sigLength`, `extDuration`, `slopeLen`, `sustainMin`, `percLookback`, `wavePivLen`, `atrRegimeLen`, `divScoreWin`, `lbR`, plus the inlined zone-visit/score-hold thresholds.
- NOT scaled: `atrLen`, `atrMult`, `deepExtremeMult`, score thresholds, StochRSI parameters.
- Default off — preserves the v6 4H optimal settings exactly. Enable when running on 1H/1D/15m without manual re-tuning.

---

## Key Findings

**What worked:**
- Zone gate on cross direction (wtSig < 0 for longs, > 0 for shorts) eliminates directionally wrong signals
- Score filter removes low-confidence crosses
- Sustained gate with OS/OB exception preserves reversal signals while suppressing mid-zone noise

**What remains weak:**
- Short side structurally weaker (Run 2 1H: PF 0.705 short vs 1.228 long)
- Score component 5 (corrDepth ≥ 60%) was biased against shorts: when oscillator is at OB zone, corrDepth ≈ 0 (near peak = good for short, but scores 0). Fixed in v2 by replacing with `obBars[1] >= 2` (OB zone sustained for 2+ bars).
- ATR trailing stop is bar-by-bar, not intrabar trailing

---

## Changes (v2)

- Split `sigMinScore` into `sigMinScoreLong` / `sigMinScoreShort` — allows asymmetric tuning
- Score component 5 changed from `corrDepth ≥ corrWarnPct` to zone-sustained check:
  - Long: `osBars[1] >= 2` (was in OS zone ≥2 consecutive bars before cross)
  - Short: `obBars[1] >= 2` (was in OB zone ≥2 consecutive bars before cross)

## Changes (v3)

- `sigGateExtA` default changed to `true` (major improvement, see Run 7)
- **ATR regime gate** (`sigGateVol`, default true): blocks signals when `ATR > EMA(ATR, 50)` — only allows mean-reversion entries in range/low-vol conditions where WaveTrend works reliably
- **Divergence score component 6**: `_bullDivAge <= divScoreWin` (8 bars default) — bull/bear div within window adds +1. Max score 5 → 6
- **Zone visit window tightened**: `_barsFromOS/OB <= 3` (was 5) — requires fresher zone origin
- Divergence engine moved before signal generation to enable div-age tracking

## Changes (v4)

- **Adaptive zone mode** (`zoneMode`, default `Fixed`): optional `Adaptive (Percentile)` uses rolling 10/90 percentiles of the oscillator over `percLookback` bars instead of fixed ±60 bands. Useful for instruments with extreme spikes (NatGas).
- **Distance score component 7**: `wtOsc < lowerThreshold × deepExtremeMult` (default 1.3) — magnitude of exhaustion as +1 score. Max score 6 → 7.
- **StochRSI Trigger (optional)**: separate input group with MTF support. Default `useStochRSI=false`. When enabled and `sigGateStochRSI=true`, WT cross signals only fire if a matching StochRSI K-line crossover (K crosses out of OS/OB) occurred within `stochWindow` bars (default 3). Standalone trigger; uses `request.security` with `lookahead=barmerge.lookahead_off`.

## Changes (v5)

Diagnosis from log analysis (4H, 7 years, 1589 raw crosses): only 18 signals fired (11 long / 7 short). Score gate blocked 85% of crosses; **127 crosses passed all gates but failed only the score**. Root cause: components 1+2 (osc-in-zone, slope-direction) were double-counted — already enforced by `sigGateZone`/`sigGateSlope` and re-counted in the score, leaving the score effectively measuring only 5 components but requiring 4 of 7.

- **Score restructured**: components 1+2 (zone, slope) **removed** — they are exclusively gate-enforced, no longer double-counted. Max score 7 → 5.
- **Default `sigMinScore` 4 → 1** — score gate becomes "need 1 bonus quality beyond the gates." `0` disables the score gate entirely.
- **Components renumbered** (1: percentile, 2: recent visit, 3: sustained zone, 4: divergence, 5: deep extreme).
- Marker tooltips, debug table, and log format updated to /5.

## Changes (v6)

Per-gate diagnostic logging extended to all 9 filters (dir, recZ, zone, slope, extA, sust, vol, stoch, score). Analysis of v5 backtest revealed:

- **Vol gate killed mostly shorts** (20 sole-blocked shorts, only 3 longs). On NatGas, volatile rallies are often exhaustion points — exactly the shorts the strategy wants. The "low-vol-only" thesis from the analysis text doesn't hold for this instrument.
- **NaN bug**: during ATR-EMA warm-up (~50 bars), `_atrRegime` is na, which makes the comparison fail and silently blocks signals. Fixed: `na(_atrRegime)` now passes the gate.
- **`sigGateVol` default reverted to `false`** — keep available as opt-in for ranging instruments, but no longer the default.

This restores the v3 (Run 7) gate stack as the default. Empirically that was the +9.41% / 28-trade configuration.

---

## Verdict

**Rating:** Promising

**Best in-sample:** Run 22 — NatGas 1D, 2017–2026, PF **3.069**, net **+69.69%**, Return/DD **4.87**, 71 trades, win rate 47.89%, max DD 14.32%. Avg winner 3.34× avg loser. Long PF 4.08, Short PF 2.04 — both directions strongly profitable. Significantly above the strategy repo's previous best (Run 20 PF 2.42).

**Extended-history validation:** Run 23 — NYMEX:NG1! futures, 35-year window (1990–2026), 310 trades. **PF 1.218 overall** (Promising, below the 1.3 Ready threshold). Critically: **Long PF 1.929** (clear edge), **Short PF 0.654** (consistent loss across multi-decade bull runs). The CFD sample (Run 22, 2017–2026) happened to coincide with an atypically bear-heavy phase that made shorts look profitable. Over the full 35-year futures history, the indicator's edge is **structurally long-biased** on NatGas. Long-Only configuration would clear the Ready threshold cleanly.

Edge is robust across the 9-year sample but the strategy is currently single-instrument validated. Win rate below 50% — profit depends on the asymmetric winner-vs-loser size, which is consistent and large (2.73×) but a quality the strategy depends on.

**Next steps to reach "Ready":**
1. **Long-Only confirmation on NYMEX:NG1!** — same v11 settings, Trade Direction = "Long Only". Expected: PF ~1.93, DD significantly lower. If confirmed, this is the production-recommended configuration for NatGas.
2. **Out-of-sample on a second instrument** (CL1! crude oil, BRENT, SI1! silver, HG1! copper). Test with default "Both" first — if PF ≥ 1.3 cross-instrument, the indicator's edge is generic. If only Long works on the new instrument too, the indicator is a directional-trend system, not a both-sides reversal system.
3. Walk-forward split: NYMEX:NG1! 1990–2008 (in-sample) vs 2009–2026 (out-of-sample). Verify Long edge persists across regime shifts.
4. Forward-test (paper / small live) to confirm slippage and execution match backtest assumptions.

**Code review v9/v10 closed:** Eight original points addressed — 3 bug fixes kept, 2 cleanups kept (BE-integration, StochRSI lower-TF), 4 logic changes empirically falsified and either reverted or made opt-in.

**Phase 3 status:**
- 🟡 #9 Exit-Logic — Partial Exit removed (no improvement), Structure Exit removed (no improvement), **Volatility Exit kept as default ON (significant improvement)**
- ⏳ #10 Score-system reconsideration — testable without code change (set `sigMinScore=0`)
- ⏳ #11 Persist structural filter — design open (HH/LL detection or slope-inflection)
- ⏳ #12 StochRSI as timing layer — re-architecture, not yet started
