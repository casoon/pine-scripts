# Vein Reversal System — Visual Guide

## Overview

The system consists of 6 indicators that work together on a NatGas chart.

| Script | Type | Timeframe | File |
|--------|------|-----------|------|
| Vein Reversal Labeler | Overlay | 4H | `vein_reversal_labeler.pine` |
| Vein Structure & Zones | Overlay | 4H | `vein_structure_zones.pine` |
| Vein Feature Exporter | Panel | 4H | `vein_feature_exporter.pine` |
| Vein Reversal Score | Panel | 4H | `vein_reversal_score.pine` |
| Vein Accumulation Phase | Overlay | 4H | `vein_accumulation_phase.pine` |
| Vein Execution 15m | Overlay | 15m | `vein_execution.pine` |

**Core principle:** 4H = Context (where to look). 15m = Timing (when to act). Accumulation = Patience (is a base forming?).

## Data Validity

`vein_structure_zones`, `vein_exhaustion`, `vein_reversal_score`, `vein_trend`, `vein_pullback`,
`vein_feature_exporter` and `vein_execution` all read `syminfo.volumetype` at runtime
(real = the feed delivers volume and does not report `tick`; most non-crypto feeds report `n/a`). On instruments without real trade volume, MFI
and relative-volume components degrade to neutral — their score weight is dropped, not moved to a price component
(moving it to RSI would count RSI twice). Scores therefore have a lower maximum on such symbols while the absolute
thresholds stay the same.
Climax detection falls back to a range-only extreme-bar proxy. `vein_execution`'s `relVol`
degrades to a neutral 1.0. Dashboard tables show a
"Volume" row (or a one-time chart label) when running degraded. See
[`DATA_VALIDITY.md`](../../../DATA_VALIDITY.md) for the full policy.

---

## 1. Vein Reversal Labeler (Overlay, 4H)

Marks historical reversal points directly on chart — with quality and timing grading.

**Purpose:** Research tool only. Uses intentional lookahead (future data) to label where reversals started in hindsight.

### Labels

| Element | Meaning |
|---------|---------|
| ▲▲ green (large, bold) | **Strong Bull** — large move, reached quickly, low adverse excursion |
| ▲ green (small, faded) | Weak Bull — reversal present, but weaker or slower |
| ▼▼ red (large, bold) | **Strong Bear** — large move, reached quickly, low adverse excursion |
| ▼ red (small, faded) | Weak Bear — reversal present, but weaker or slower |

### Timing Suffixes

| Suffix | Meaning | Criterion |
|--------|---------|-----------|
| ⚡ | **Fast** — signal was early and usable | Target reached in ≤ 4 bars |
| (none) | Normal — solid timing | Target reached in ≤ 8 bars |
| ~ | Slow — signal was late / noisy | Target reached in > 8 bars |

Example: `▲▲ ⚡` = Strong Bull, fast — best case. `▼ ~` = Weak Bear, slow — worst case.

### Quality Criteria

A reversal is **strong** when:
- price reaches the large target (2.5× ATR in 16 bars), OR
- the small target (1.5× ATR) is reached fast (≤ 4 bars) with low adverse excursion (≤ 0.3× ATR)

Everything else is **weak**.

### Tooltips

Hover over each label shows:
- **Move** — achieved move in ATR
- **MAE** — Max Adverse Excursion (largest adverse move in ATR before the target is hit)
- **Bars** — bars to target
- **Timing** — Fast / Normal / Slow

### Table (Research mode only, default off)

Two sections:
- **Quality:** Bull Strong / Bull Weak / Bear Strong / Bear Weak — Count + Percent
- **Timing:** Fast / Normal / Slow — Count + Percent

---

## 2. Vein Structure & Zones (Overlay, 4H)

Combined structural event detection AND automatic S/R zones, with raw facts about the nearest support and resistance zone.

### Event Labels

#### Micro vs Major

All swing and BOS events are detected on two levels:
- **Micro** (Pivot 3/3) — local structure, shorter swings
- **Major** (Pivot 7/7) — significant structure, longer swings

#### Tier 1 — Most Important Events (large, prominent)

| Label | Meaning |
|-------|---------|
| SPRING | Major Spring — fake breakdown below significant swing low |
| spring | Micro Spring — fake breakdown below local swing low |
| UPTHRUST | Major Upthrust — fake breakout above significant swing high |
| upthrust | Micro Upthrust — fake breakout above local swing high |
| BOS ↑↑ / BOS ↓↓ | Major Break of Structure |
| bos ↑ / bos ↓ | Micro Break of Structure |

#### Event Tooltips

Event labels show the plain event name. The tooltip carries the raw measurements of the bar:

| Event | Tooltip facts |
|-------|---------------|
| Spring / Upthrust | Sweep depth beyond the swing level (ATR), wick % of range, candle range (× ATR), volume (× average, only with real volume) |
| BOS / CHoCH | Close beyond the broken swing level (ATR), volume (× average, only with real volume) |
| Rejection | Wick % of range, body % of range, candle range (× ATR), volume (× average, only with real volume) |

#### Climax Sequence

| Label | Color | Meaning |
|-------|-------|---------|
| Selling CLX / Buying CLX | fuchsia | Climax detected, sequence started |
| TST ↑ / TST ↓ | purple | Test validated |
| **CLX→TST→BOS ↑ / ↓** | **green/red, large** | Sequence complete: climax → reaction → test → BOS in the climax direction |

Internally 5 stages: CLX → Reacting → Test Pending → Test Valid → Confirmed (after BOS). The sequence advances at most one stage per bar and resets after 2 × "Test: Lookback Bars".

#### Other Events

| Label | Meaning |
|-------|---------|
| FB | Fake Break — breakout above/below swing level, close back inside |
| rej | Rejection candle |
| · | Swing High/Low (minimal dot) |

### Automatic Zones

Events generate horizontal S/R zones as colored boxes.

#### Zone Sources

| Type | Source | Direction |
|------|--------|-----------|
| Swing Zone | Major Swing High/Low | S/R |
| Spring Zone | Sweep Low → old Swing Low | Support |
| Upthrust Zone | Old Swing High → Sweep High | Resistance |
| BOS Flip | Broken Major Swing level | S↔R |
| Climax Zone | High/Low of climax candle | By direction |

#### Zone Lifecycle

| Status | Meaning |
|--------|---------|
| Fresh | Newly created, untested |
| Tested | Price touched the zone |
| Confirmed | Price reacted at the zone |
| Broken | Zone breached |
| Flipped | Broken zone, role reversed |

#### Zone Display

- **Green boxes** = Support
- **Red boxes** = Resistance
- **Amber boxes** = Flip zones
- Only the top N zones are shown (default: 8), prioritized by type, status, touches, age and the formation of the source bar (wick, range, absorption, climax volume); the ranking only decides what is drawn and is not shown

### Nearest Zone Info

For the nearest active support (below price) and resistance (above price) within "Max Distance (ATR)", the script shows the zone's raw facts — no hold or break probability:

| Fact | Meaning |
|------|---------|
| Zone / Status | Zone source and lifecycle status |
| Distance | Close to zone mid, in ATR |
| Age | Bars since the zone was created |
| Touches | Number of visits (entries into the zone) |
| Bounces ≥ / < 0.5 ATR | Reactions per visit, split by size |
| Max / last bounce | Largest and most recent reaction, in ATR |
| FVG / OB nearby | Unmitigated FVG / order block within 2 ATR of price on that side |
| POC | Zone near POC, inside the value area, or outside (— without real volume) |

**Labels at zones:** `1.2 ATR · T3` = distance 1.2 ATR, 3 touches. Hover for all facts.

**Zone info table:** Default off. Enable via input "Show Zone Info Table" (top left).

### Alerts

| Alert | Trigger |
|-------|---------|
| Price Entered Support Zone | Price enters an active support zone (new visit) |
| Price Entered Resistance Zone | Price enters an active resistance zone (new visit) |
| Support Zone Broken | Close below a support zone |
| Resistance Zone Broken | Close above a resistance zone |
| Zone Flipped | A broken zone is retested from the other side and changes role |

### Key Purpose

**"Where is structure, and how has price treated it so far?"**

---

## 3. Vein Feature Exporter (Panel, 4H)

Shows indicator values as an oscillator panel below the chart. Includes WaveTrend with divergence detection.

**Plot group selectable via input "Plot Group":**

| Group | What it shows |
|-------|--------------|
| Momentum | RSI (yellow), Stoch RSI K (cyan), Stoch RSI D (orange) |
| Volume | MFI (teal), Relative Volume (purple) |
| Volatility | BB Width (orange), Candle/ATR (green), BB Distance (cyan) |
| Trend | Price→EMA20 (yellow), EMA20→EMA50 (orange), Slope direction (dots) |
| Candle | Body/Range % (yellow), Upper Wick % (red), Lower Wick % (green) |
| WaveTrend | WT Oscillator (blue), WT Signal (orange), WT Histogram (green/red bars) |

### Line Labels

Each plot group shows value labels at the right edge of the chart, directly on each line. Toggle via "Show Line Labels" (default: on). Hover shows interpretation tooltip.

### Interpretation Table (top right, toggleable)

Compact 4-column layout — two features per row with values. Hover any cell for full interpretation.

| Left | Value | Right | Value |
|------|-------|-------|-------|
| RSI | 32.0 | Trend | -1.2x |
| StchRSI | 15/22 | Volatil | -1.8 |
| MFI | 28.0 | Volume | 1.1x |
| WT | -45/-38 | WT Bias | ↓57% |

Color logic reflects **current state** (not reversal opportunity):
- Red = bearish pressure (low RSI falling, price below EMA)
- Amber = transitional (turning)
- Green = bullish pressure
- chart.fg_color = neutral

### WaveTrend

WaveTrend momentum oscillator with:
- **Oscillator + Signal** lines with OB/OS levels (±60)
- **Divergence Detection** — Regular + Hidden, Bull + Bear
- **Composite Bias Score** (-7 to +7): Oscillator position + Momentum + Cross (with decay) + Divergence (with decay) + Regime → "S↑/↑/w↑/—/w↓/↓/S↓" with confidence %

### Summary Line

Bottom row shows overall assessment. Hover for full breakdown of all indicators.

---

## 4. Vein Reversal Score (Panel, 4H)

Two-layer scoring with regime filter, level context, follow-through, and conflict detection.

### Core Principle

Oscillators alone are not enough. Only Setup + Structure confirmation + Follow-through = take seriously.

### Two Layers

**Layer A — Setup Score (bars in panel):**

| Component | Points |
|-----------|--------|
| RSI in extreme zone | +1 |
| RSI turning | +0.5 |
| MFI in extreme zone | +1 |
| MFI turning | +0.5 |
| Stoch RSI / MACD (by variant) | +0.5 to +1 |
| Price far from EMA20 | +1 to +1.5 |
| Bollinger band touched | +1 |
| Strong wick | +1 |
| **At meaningful level** | **+1** |
| Trend against setup | -1 |
| No volume | -0.5 |
| Far from any level | -0.5 |

**Layer B — Confirmation Score (circles in panel):**

| Component | Micro weak | Micro strong | Major weak | Major strong |
|-----------|-----------|-------------|-----------|-------------|
| Spring/Upthrust | +1.5 | +3.0 | +3.0 | +4.5 |
| BOS | +0.5 | +2.0 | +2.0 | +3.5 |
| Fake Break | +0.5 | — | +1.0 | — |
| CLX detected | +1.0 | | | |
| Test validated | +1.5 | | | |
| CLX→TST→BOS | +2.5 | | | |

### Event Decay

Confirmation loses weight automatically after the event:

| Bars after event | Effect |
|-----------------|--------|
| 0–3 | 100% |
| 4–6 | Linear decline → 20% |
| >6 | 0% (expired) |

The event bar's confirmation is latched and fades along this curve, so it still counts on the follow-through bars after the event.

### Follow-Through

After an event, checked within 2–4 bars:
- Is there a higher/lower close?
- Does price hold above/below the trigger level (the event bar's close)?
- No opposing BOS?

### Status Logic

| Status | Meaning |
|--------|---------|
| — | Nothing active |
| WATCH | Setup building |
| SETUP | Setup strong, waiting for confirmation |
| ALERT | Structure event, but setup too weak |
| PENDING | Setup + Conf, follow-through not (yet) achieved |
| **CANDIDATE** | **Setup + Conf + Follow-through — take seriously** |
| **CONFLICTED** | **Contradictory — do not act** |
| **FAILED** | **No follow-through or trigger lost** |

### Table (top right)

Compact display with rich hover tooltips on every cell:
- **Vein Score** hover → full system explanation
- **▲ S:3 C:1** hover → all bull setup/confirm components with ✓/·
- **▼ S:2 C:0** hover → all bear components
- **Context** hover → regime, multipliers, conflict details
- **FT ✓/✗** hover → follow-through status, decay, event age

### Conflict Detection

| Conflict Type | Detection |
|--------------|-----------|
| Setup conflict | Bull + Bear setup both active |
| Conf conflict | Both sides confirmed |
| Trend conflict | Setup against strong trend (ER > 0.45) |
| Opposed candidate | Candidate + opposing side confirmed |

### Signal and alerts

The **Reversal Signal** is built from structure and price only: a structure event (Spring/Upthrust,
BOS, confirmed climax) whose own confirmation reaches `Confirmation Required`, followed within 1–4
bars by its first follow-through bar (higher/lower close beyond the trigger level, no counter BOS),
while the opposite side is not confirmed. The Setup score does not gate it, and there is no quality
grade. It is invalidated when price closes back through the trigger level or the event expires
without follow-through.

| Alert | Condition |
|-------|-----------|
| **Reversal Signal** | Structure event + first follow-through bar (triangle marker) |
| **Setup + Structure Event** | Status becomes CANDIDATE (setup and a structure event on the same side) |
| **Invalidation** | A Candidate or Signal, now Failed |

Plus: **Trap Hint** when a failed reversal signals the opposite direction.

### Regime Filter

| Regime | Setup Score | Confirmation Score |
|--------|------------|-------------------|
| RANGE | ×1.2 | ×1.0 |
| TREND | ×0.8 | ×1.3 |
| HIGH VOL | — | ×1.2 |
| LOW VOL | — | ×0.8 |

### Background Color

| Color | Meaning |
|-------|---------|
| Green | Bull CANDIDATE |
| Red | Bear CANDIDATE |
| Gray-blue | CONFLICTED |
| Orange | FAILED |
| Amber | Both sides confirmed |
| Faint green/red | PENDING |

---

## 5. Vein Accumulation Phase (Overlay, 4H)

Shows whether the market is in an accumulation phase (range after a decline) or a distribution phase (range after a rally) — a state over time, not a point signal.

### Core Idea

**"Is this just a bounce, or has a range formed after the move?"**

### Phase Rule

The same rule applies to both sides; neither takes precedence.

| Condition | Accumulation | Distribution |
|-----------|--------------|--------------|
| Prior trend | EMA20 < EMA50, "Phase Lookback Bars" ago | EMA20 > EMA50, "Phase Lookback Bars" ago |
| EMA20/50 flat | gap < 0.5 ATR | gap < 0.5 ATR |
| Ranging | Efficiency Ratio < threshold | Efficiency Ratio < threshold |

### States

| State | Meaning |
|-------|---------|
| NONE | Condition not met |
| ACCUM / DISTRIB forming | Condition met, fewer than "Min Phase Duration" bars in a row |
| ACCUMULATION / DISTRIBUTION | Condition held "Min Phase Duration" bars in a row; the lookback range is latched |
| Range exit | A close above or below the latched range ends the phase (shown as "Last exit") |

Once a phase is set it lasts until the range exit, even if the condition stops holding inside the range.

### Raw Conditions (shown, not scored)

- Prior trend, EMA20/50 flat (gap in ATR), ranging (ER, range width in ATR)
- Compressed: BB width ratio or ATR ratio below its threshold — info only, not part of the rule
- Sweeps below / above the last swing, springs, upthrusts — counted within the lookback
- Bars since the last bull / bear BOS; swing sequence HL / LL / LH / HH

### Visualization

| Element | Description |
|---------|-------------|
| **Background shading** | Green = accumulation, red = distribution, gray = forming |
| **Phase range** | Latched high / low of the active phase |
| **Phase label** | On chart: "ACCUMULATION · 14 bars"; tooltip lists all raw conditions |

### Status Table (top right)

Rows: Phase + duration, Prior trend, EMA20/50 flat, Ranging, Compressed, Sweeps ↓ / springs, Sweeps ↑ / upthrusts, bars since BOS ↑ / ↓ with swing sequence, Last exit.

### Alerts

| Alert | Trigger |
|-------|---------|
| Phase Changed to Accumulation | Phase becomes ACCUMULATION |
| Phase Changed to Distribution | Phase becomes DISTRIBUTION |
| Phase Ended — Close Above Range | Close above the latched phase range |
| Phase Ended — Close Below Range | Close below the latched phase range |

---

## 6. Vein Execution 15m (Overlay, 15m)

Lean execution/timing module. Only activates when the connected setup source says "interesting".

**Core rule:** 15m does NOT decide direction. It confirms or destroys what the setup source suggests.

### Setup context (external sources) and 4H reference levels

The setup scores are **external sources** ("Vein Module Inputs"), not a 4H request: connect Vein Reversal Score's `Bull Setup [dw]` / `Bear Setup [dw]` plots on the same chart. They are therefore computed on the chart timeframe. The two optional trend sources take any plot that is > 0 while the trend is up / down (Vein Trend has no such plot); they only feed the status-table hint.

Only the reference levels come from the 4H timeframe via `request.security`: last swing high/low (pivots), EMA20 and RSI.

**Activation:** 15m only works when the connected setup score ≥ threshold (default: 2.0). Otherwise shows "QUIET".

If both setup sources are left on their default (`close`), they count as not connected: the module stays QUIET and the table shows "Setup sources not connected". The same applies to the two trend sources (treated as neutral).

**Entries** (off by default) need a 15m structure trigger AND an active setup on that side AND (a behaviour candle OR follow-through).

### Bias

| Bias | Meaning |
|------|---------|
| BULL | Setup source has an active bull setup, no bear |
| BEAR | Setup source has an active bear setup, no bull |
| MIXED | Both sides active — 15m dampened |
| QUIET | Setup source below threshold — 15m inactive |

### Roles (on/off, no points)

| Role | On when |
|------|---------|
| **Setup** | Connected setup score for that side ≥ activation threshold |
| **Structure** | 15m event: sweep, sweep confirmed or micro BOS; pivot-order HL/LH shifts are not used |
| **Behaviour** | Rejection or engulfing candle, or a range-expansion bar (with volume) in that direction |
| **Tempo** | Follow-through of at least the minimum move within the follow-through window after a trigger |

### Status (display only, no alerts)

| Status | Meaning |
|--------|---------|
| QUIET | Setup source not active, nothing to do |
| WATCH | Setup active, watching for a 15m structure event |
| SETUP | Structure event, no behaviour or follow-through yet |
| **TRIGGER** | **Structure event + behaviour or follow-through** |

### Visual Elements

| Element | Description |
|---------|-------------|
| **ENTRY ▲ / ENTRY ▼** | Green/red labels at entry signals |
| **INVAL ✗** | Orange labels when entry invalidated |
| Dashed lines | 4H swing high (red), swing low (green), EMA20 (amber) |
| Background tint | Subtle green/red at TRIGGER, amber at SETUP |
| SWP / BOS labels | Debug mode: micro events visible |

### Status Table (top right)

| Row | Content |
|-----|---------|
| Header | Vein Exec + Status (QUIET/WATCH/SETUP/TRIGGER) |
| Setup Bias | BULL/BEAR/MIXED/QUIET + setup score |
| Set \| Str | Setup and structure role on/off (signal direction) |
| Beh \| Tmp | Behaviour and tempo role on/off (signal direction) |
| Interpretation | Plain-language explanation of current state |
| Signal | BULL ENTRY active / BEAR ENTRY active / — |
| 4H Zone | Distance to nearest relevant 4H zone in ATR |

### Alerts

| Alert | Trigger |
|-------|---------|
| Bull/Bear Entry | Entry signal fired |
| Bull/Bear Invalidation | Entry invalidated |

The QUIET/WATCH/SETUP/TRIGGER status is display only and has no alerts.

---

## Display Modes

The 4H scripts except Vein Accumulation Phase have three modes (Input "Display Mode"):

| Mode | What it shows |
|------|--------------|
| Light | Essentials only — markers, score, zones, core plots |
| Debug | Additional values, swing lines, zone scores, status info |
| Research | Everything — tables, statistics, timing, export data |

The 15m script has Light and Debug modes.

**Recommendation:** "Light" for daily use. "Debug" for analysis. "Research" for parameter tuning.

---

## Table Design

All tables follow consistent design:
- **Transparent background** — no dark overlay, adapts to chart theme
- **chart.fg_color** for labels — black on light theme, white on dark
- **Signal colors:** green (#00e676) = bullish, red (#ff1744) = bearish, dark orange (#e65100) = warning/transition
- **Rich tooltips** on all cells — hover for full interpretation, component breakdown, and explanations

---

## Alerts Summary

### Recommended Alert Setup

| Alert | Source | Purpose |
|-------|--------|---------|
| **Bull/Bear Reversal Signal** | Vein Score (4H) | Structure event + follow-through |
| **Bull/Bear Entry** | Vein Execution (15m) | "Now it's getting concrete" (enable entries) |
| **Bull/Bear Invalidation** | Vein Score (4H) | "Cancel — signal failed" |

### Full Alert List

| Source | Alert | Condition |
|--------|-------|-----------|
| Score | Bull/Bear Reversal Signal | Structure event + first follow-through bar |
| Score | Bull/Bear Invalidation | Candidate or Signal → Failed |
| Score | Bull/Bear Setup + Structure Event | Status becomes CANDIDATE |
| Score | Conflict | Significant conflict detected |
| Score | Spring/Upthrust | Heuristic triggered |
| Score | Major BOS | Major Break of Structure |
| Score | Bull/Bear Trap | Failed reversal → opposite continuation |
| Zones | Price Entered Support/Resistance Zone | New visit into an active zone |
| Zones | Support/Resistance Zone Broken, Zone Flipped | Zone lifecycle events |
| Execution | Bull/Bear Entry | Entry signal confirmed |
| Execution | Bull/Bear Invalidation | Entry invalidated |
| Accum | Phase Changed to Accumulation/Distribution | Phase set after min duration |
| Accum | Phase Ended — Close Above/Below Range | Close outside the latched range |
| Trend | Candle State Changed | Heatmap state changes |
| Trend | Major BOS / Major CHoCH Bull/Bear | Major structure events |

---

## Workflow

### Daily Use (4H)

1. Load **Vein Structure & Zones** + **Vein Reversal Score** + **Vein Accumulation Phase** on 4H NatGas
2. Accumulation tells you: is a base forming, or just noise?
3. Score table tells you: is anything building? Why or why not?
4. Zones show: where would a reversal be meaningful?
5. Wait for CANDIDATE or at minimum SETUP + structure event

### Timing (15m)

6. When 4H shows active setup, switch to 15m with **Vein Execution** loaded
7. Wait for micro structure: sweep, BOS, rejection
8. TRIGGER status + ENTRY label = consider acting
9. INVAL label = abort, setup failed on micro level

### Research

10. Load **Vein Labeler** to see where past reversals were (strong vs weak, fast vs slow)
11. Load **Vein Feature Exporter** to compare indicator readings at those points
12. Use Research mode tables for parameter tuning

---

## Vein Adaptive Suite (v2)

Three self-contained, timeframe-agnostic indicators that work on any chart. They can be used standalone or layered together as complementary perspectives.

| Script | Purpose | File |
|--------|---------|------|
| Vein Trend | Trend state and structure events | `vein_trend.pine` |
| Vein Pullback | Pullback vs. reversal detection | `vein_pullback.pine` |
| Vein Exhaustion | Temporal + emotional overextension | `vein_exhaustion.pine` |

**Three perspectives on the same question:**
- **Trend** → "What state is the trend in, and what did the structure last do?"
- **Pullback** → "Is this counter-move a pullback (reentry) or a reversal (exit)?"
- **Exhaustion** → "Is this move overextended emotionally, before structure confirms anything?"

EMAs and scoring adapt automatically to the active timeframe. All three scripts are configurable as overlays with table position inputs.

---

## 7. Vein Trend (Overlay, any TF)

Trend-state display: colors candles by EMA direction and efficiency ratio and marks the structural events that change the swing structure. No buy/sell signals.

### Candle State

| State | Condition |
|-------|-----------|
| CONFLICT | EMA20/50 direction opposite to the direction of the last major BOS |
| RANGE | Efficiency Ratio (20) ≤ 0.35 |
| UP STRONG / DOWN STRONG | EMA20 above / below EMA50, ER ≥ 0.5 |
| UP / DOWN | EMA20 above / below EMA50, ER 0.35–0.5 |
| FLAT | EMAs equal or not enough data |

Priority: Conflict → Range → Strong → Normal → Flat.

### Structure Events

| Marker | Event |
|--------|-------|
| CHoCH | Major BOS against the current major structure |
| BOS | Major BOS in the direction of the current major structure |
| SPR / UT | Spring / Upthrust — wick beyond the last swing, close back inside (major = solid color) |
| CLX | Climax sequence complete: climax → reaction → test → BOS (one stage per bar, 20-bar expiry) |

Micro BOS/CHoCH are tracked for the table's structure row and "Last event".

### Table (top right, configurable)

State, EMA 20/50 (gap in ATR), Efficiency (ER + regime), BB width ratio (volatility), micro/major structure, last structure event with age, position in the major swing range (premium / discount / equilibrium, %), climax sequence stage, volume validity.

### Alerts

| Alert | Trigger |
|-------|---------|
| Candle State Changed | Heatmap state differs from the previous bar |
| Major BOS Bull / Bear | Close beyond the major swing high / low (not a CHoCH) |
| Major CHoCH Bull / Bear | Major BOS against the current major structure |

---

## 8. Vein Pullback (Overlay, any TF)

Answers: "Is this counter-trend move a pullback (continue trend) or a reversal (change direction)?"

### AutoTF EMAs

| Timeframe | Fast EMA | Slow EMA |
|-----------|----------|----------|
| Daily | 50 | 200 |
| 4H | 34 | 100 |
| 1H | 21 | 55 |
| <1H | 20 | 50 |

### Score Layers (0–10)

| Layer | Max | What it measures |
|-------|-----|-----------------|
| **Trend Quality** | 2 | EMA alignment + Efficiency Ratio — weak trend = weak pullback context |
| **Pullback Active** | 2 | Bars elapsed since pullback start — reward pullbacks with some duration |
| **Move Weakness** | 3 | RSI stays in safe zone + volume stays low + small candles (max 2 without real volume) |
| **Structure Intact** | 2 | No break of frozen swing low/high reference |
| **Fib Depth** | 1 | Retracement in 25–68% range (both references frozen at PB start; the origin is the higher of the last swing high and the recent unconfirmed high — mirrored for bear) |

### State Machine

Pullback starts when price crosses EMA Fast against the trend. Active until one of:
- **Reclaim** — price crosses back through EMA Fast (normal end)
- **Structure Break** — close beyond frozen swing reference → signal ◆
- **Timeout** — 40 bars without resolution → invalidated

### End Signal

Fires when score ≥ threshold AND (rejection candle OR micro BOS from pullback zone). Micro BOS requires the previous close to have been below EMA Fast — prevents firing on random up-closes mid-pullback.

### Signals

| Signal | Shape | Meaning |
|--------|-------|---------|
| `▲ 7.2` | Label below bar | Bull pullback ending — entry in trend direction |
| `▼ 6.8` | Label above bar | Bear pullback ending — entry in trend direction |
| ◆ | Diamond | Structure broken — pullback became reversal |
| Stop line | Line | Pullback extreme frozen when the end signal fires |
| ✕ | Cross | Close beyond that stop — end signal invalidated |

### Table (configurable position)

Shows Trend, State (with bar count), Score (with progress bar), Trend Q, Weakness, Structure, Depth.

---

## 9. Vein Exhaustion (Overlay, any TF)

Detects when a move is overextended — temporally, emotionally, and through orderflow — before structure shows it.

### AutoTF EMA

| Timeframe | EMA |
|-----------|-----|
| Daily | 50 |
| 4H | 34 |
| 1H | 21 |
| <1H | 20 |

### Score Layers (0–10, separate for Bull and Bear)

| Layer | Max | What it measures |
|-------|-----|-----------------|
| **Time** | 3 | Consecutive directional closes (grace: 1 bar tolerance before reset; re-arms after ≥ 2 directional bars) |
| **Overextension** | 3 | EMA distance in ATR units + RSI extreme + MFI extreme |
| **Orderflow Proxy** | 2 | Directional absorption, capitulation/blow-off and accumulation/distribution bars |
| **Volatility** | 2 | Directional ATR spike + climax bar (bull or bear only) |

### Orderflow Events

| Event | Side | Detection |
|-------|------|-----------|
| **Bear Absorption** | Bear exhaustion | Bearish bar + high vol + small range = buyers absorbing |
| **Bull Absorption** | Bull exhaustion | Bullish bar + high vol + small range = sellers absorbing |
| **Capitulation** | Bear exhaustion | Bearish bar + very high vol + large range + close near low |
| **Blow-off** | Bull exhaustion | Bullish bar + very high vol + large range + close near high |
| **Distribution** | Bull exhaustion | Bearish close after up move + upper wick dominates + overextended |
| **Accumulation** | Bear exhaustion | Bullish close after down move + lower wick dominates + overextended |

### Signals

| Signal | Shape | Meaning |
|--------|-------|---------|
| `▼ 7.8` | Label above bar | Upward move exhausted — potential top |
| `▲ 6.2` | Label below bar | Downward move exhausted — potential bottom |
| ● cyan | Dot below bar | Bear absorption — buyers stepping in |
| ● orange | Dot above bar | Bull absorption — sellers stepping in |
| ★ | Cross below bar | Capitulation — panic low |
| ★ | Cross above bar | Blow-off — buying climax |

### Score States

| State | Score | Background |
|-------|-------|-----------|
| NORMAL | < 3 | None |
| STRETCHED | ≥ 3 | Faint |
| EXHAUSTED | ≥ threshold | Colored |
| EXTREME | ≥ 8 | Strong |

### Table (configurable position, default bottom right)

Shows Status (color-coded), Score (with progress bar), Time, Overextension, Orderflow, Volatility, and Event for both Bull and Bear sides separately.

---

## Layered Reading

The three v2 indicators answer different questions simultaneously:

| Indicator | Reading | Interpretation |
|-----------|---------|---------------|
| Exhaustion: Bear EXTREME | Score 8.5 | Downmove very overextended, time + orderflow + vol all elevated |
| Pullback: BEAR PB active | Score 6.2 | Counter-move active, structure still intact, weak move |
| Trend: DOWN | ER 0.41 | EMAs still down, last event a major Spring |
| → Combined | | Down move stretched, counter-move active with structure intact, trend state still down |

**Reading order:** Exhaustion reacts first (leading). Pullback identifies context (reentry vs exit). Trend shows the current state and the last structure event.
