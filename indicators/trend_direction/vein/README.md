# Vein Reversal System — Visual Guide

## Overview

The system consists of 6 indicators that work together on a NatGas chart.

| Script | Type | Timeframe | File |
|--------|------|-----------|------|
| Vein Reversal Labeler | Overlay | 4H | `vein_reversal_labeler_4h.pine` |
| Vein Structure & Zones | Overlay | 4H | `vein_structure_zones_4h.pine` |
| Vein Feature Exporter | Panel | 4H | `vein_feature_exporter_core_4h.pine` |
| Vein Reversal Score | Panel | 4H | `vein_reversal_score_4h.pine` |
| Vein Accumulation Phase | Overlay | 4H | `vein_accumulation_phase_4h.pine` |
| Vein Execution 15m | Overlay | 15m | `vein_execution_15m.pine` |

**Core principle:** 4H = Context (where to look). 15m = Timing (when to act). Accumulation = Patience (is a base forming?).

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
- **MAE** — Max Adverse Excursion (largest adverse move in ATR)
- **Bars** — bars to target
- **Timing** — Fast / Normal / Slow

### Table (Research mode only, default off)

Two sections:
- **Quality:** Bull Strong / Bull Weak / Bear Strong / Bear Weak — Count + Percent
- **Timing:** Fast / Normal / Slow — Count + Percent

---

## 2. Vein Structure & Zones (Overlay, 4H)

Combined structural event detection AND automatic S/R zones with integrated zone assessment.

### Event Labels

#### Micro vs Major

All swing and BOS events are detected on two levels:
- **Micro** (Pivot 3/3) — local structure, shorter swings
- **Major** (Pivot 7/7) — significant structure, longer swings

#### Tier 1 — Most Important Events (large, prominent)

| Label | Meaning |
|-------|---------|
| ★ SPRING | Major Spring — fake breakdown below significant swing low |
| spring | Micro Spring — fake breakdown below local swing low |
| ★ UPTHRUST | Major Upthrust — fake breakout above significant swing high |
| upthrust | Micro Upthrust — fake breakout above local swing high |
| ★ BOS ↑↑ / ★ BOS ↓↓ | Major Break of Structure |
| bos ↑ / bos ↓ | Micro Break of Structure |

#### Event Quality

Each event gets a quality grade based on 4 factors:
- Wick size (≥ 55% = strong)
- Candle range (≥ 0.8× ATR = strong)
- Volume (≥ 1.3× average = strong)
- Sweep depth (≥ 0.15× ATR = strong)

| Prefix | Quality | Color | Criterion |
|--------|---------|-------|-----------|
| ★ | **Strong** | bold | 3–4 factors above threshold |
| (none) | Normal | medium | 1–2 factors |
| ~ | Weak | faded | Barely qualified |

#### Climax Sequence

| Label | Color | Meaning |
|-------|-------|---------|
| Selling CLX / Buying CLX | fuchsia | Climax detected, sequence started |
| TST ↑ / TST ↓ | purple | Test validated |
| **CLX→TST→BOS ↑ / ↓** | **green/red, large** | **Full sequence — strongest signal** |

Internally 5 stages: CLX → Reacting → Test Pending → Test Valid → Confirmed (after BOS).

#### Other Events

| Label | Meaning |
|-------|---------|
| FB | Fake Break — breakout above/below swing level, close back inside |
| ★rej / rej / ~rej | Rejection (with quality) |
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
- Only the top N zones are shown (default: 8), prioritized by type, quality, status, touches and age

### Zone Assessment (integrated)

For the nearest active Support and Resistance zone, the script calculates:

| Metric | Range | Meaning |
|--------|-------|---------|
| **Reach** | 0–100 | How likely is it that price reaches this zone? |
| **Hold** | 0–100 | If reached, how likely is a meaningful reaction? |
| **Break** | 0–100 | How likely is the zone to fail? |
| **State** | text | stable / holding / under_pressure / weakening / likely_reaction / likely_break |

Based on 4 sub-scores:
- **Structure** — zone origin and quality (spring > swing, major > micro)
- **Respect** — how well was the zone historically respected?
- **Approach** — how is price currently approaching? (decelerating = good for hold)
- **Context** — regime, trend, volatility alignment

**Labels at zones:** `H62 B41 R74` = Hold 62, Break 41, Reach 74. Color: green if hold > break, red if break > hold, amber if mixed.

**Assessment table:** Default off. Enable via input "Show Assessment Table". Shows full breakdown for nearest support and resistance.

### Key Purpose

**"Here is a zone where the reversal system should be taken seriously."**

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

### Follow-Through

After an event, checked within 2–4 bars:
- Is there a higher/lower close?
- Does price hold above/below trigger level?
- No opposing BOS?

### Status Logic

| Status | Meaning |
|--------|---------|
| — | Nothing active |
| WATCH | Setup building |
| SETUP | Setup strong, waiting for confirmation |
| ALERT | Structure event, but setup too weak |
| PENDING | Setup + Conf, follow-through pending |
| **CANDIDATE** | **Setup + Conf + Follow-through — take seriously** |
| **CONFLICTED** | **Contradictory — do not act** |
| EXPIRED | Event too old |
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

### Three Alert Types

| Alert | Condition | Purpose |
|-------|-----------|---------|
| **REVIEW** | Setup ≥ 4, Conf ≥ 1.5, no strong conflict | "Look at this" |
| **ACTION** | Setup ≥ 5, Conf ≥ 3, Follow-through ✓, no conflict | "Consider acting" |
| **INVALIDATION** | Previously Candidate, now Failed | "Signal is dead" |

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

Detects bottom formation (accumulation) and top formation (distribution) as process states over time — not point signals.

### Core Idea

**"Is this just a bounce, or is a base actually forming?"**

A bottom/top is not an event but a phase: trend weakens → range forms → volatility compresses → liquidity gets swept → structure shifts.

### 5 Components (0–2 each, max 10)

| Component | What it measures | Score 0 | Score 1 | Score 2 |
|-----------|-----------------|---------|---------|---------|
| **Trend Loss** | Downtrend/uptrend weakening | Still trending | Flattening | Clear loss |
| **Range Formation** | Sideways consolidation | Trending (high ER) | Transitioning | Clear range (low ER) |
| **Vol Compression** | Candles/BB/ATR shrinking | Volatile | Declining | Compressed |
| **Liquidity** | Sweeps, springs, upthrusts | None | Single events | Multiple/repeated |
| **Early Structure** | First HL/LH, micro BOS | Nothing | First hints | Repeated |

### States

| State | Score | Meaning |
|-------|-------|---------|
| none | < 3 | No phase detected |
| transition | ≥ 3 | First signs, minimum duration not yet met |
| early | ≥ 3 | Phase beginning after min duration met |
| developing | ≥ 5 | Clear phase with multiple components |
| mature | ≥ 6 | Strong phase, liquidity + range confirmed |
| breakout_ready / breakdown_ready | ≥ 8 | Structure actively shifting |

**Minimum duration:** 10 bars (configurable). Filters out V-reversals.

### Both Directions

The script detects both:
- **Accumulation** (bottom) — after downtrend, bullish structure emerging
- **Distribution** (top) — after uptrend, bearish structure emerging

### Visualization

| Element | Description |
|---------|-------------|
| **Background shading** | Gray → orange → green(accum)/red(distrib) → blue(breakout ready) |
| **Phase label** | On chart: "ACCUMULATION (developing) Score: 6.8 \| 14 bars" |
| **Tooltip on label** | Full component breakdown + metrics |

### Status Table (top right)

| Row | Content |
|-----|---------|
| Header | Vein Accum + phase type (ACCUM/DISTRIB/NONE) + state |
| Score | X / 10 + duration in bars + range width |
| Interpretation | Plain-language: "Accumulation building — watch sweeps" |
| Components | T:2 R:1 V:2 L:1 S:1 (hover for details) |
| Context | ER, BBW ratio, ATR ratio values |

Debug mode adds: separate Accum/Distrib scores, sweep/spring counts, HL/LL/LH flags.

### Alerts

| Alert | Trigger |
|-------|---------|
| Accum Developing | Phase enters "developing" |
| Accum Mature | Phase enters "mature" |
| Breakout Ready | Accumulation with bull structure shifting |
| Distrib Developing | Distribution enters "developing" |
| Distrib Mature | Distribution enters "mature" |
| Breakdown Ready | Distribution with bear structure shifting |

### Integration with Other Scripts

The Accumulation Phase answers: **"Should I even be watching for a reversal here?"**

| Accum State | Reversal Score says... | Action |
|-------------|----------------------|--------|
| none | CANDIDATE | Probably just a bounce — be cautious |
| developing | SETUP | Building — patience, wait for confirmation |
| mature | CANDIDATE | **High confidence** — structure + base align |
| breakout_ready | TRIGGER (15m) | **Best case** — base formed, now timing the entry |

---

## 6. Vein Execution 15m (Overlay, 15m)

Lean execution/timing module. Only activates when 4H says "interesting".

**Core rule:** 15m does NOT decide direction. It confirms or destroys what 4H suggests.

### 4H Context (via request.security)

The script pulls simplified 4H data:
- Trend direction (EMA20 vs EMA50)
- RSI / MFI levels
- Simplified setup score
- Last swing high/low as reference levels

**Activation:** 15m only works when 4H setup score ≥ threshold (default: 2.0). Otherwise shows "QUIET".

### Bias

| Bias | Meaning |
|------|---------|
| BULL | 4H has active bull setup, no bear |
| BEAR | 4H has active bear setup, no bull |
| MIXED | Both sides active — 15m dampened |
| QUIET | 4H below threshold — 15m inactive |

### Micro Score (0–10)

| Component | Max | Source |
|-----------|-----|--------|
| **Setup** | 3 | 4H context: setup active (+1), setup strong (+1), near 4H zone (+1) |
| **Structure** | 4 | 15m events: sweep (+1), sweep confirmed (+1), micro BOS (+1), HL/LH shift (+1) |
| **Behaviour** | 2 | Candle: rejection/engulfing (+1), range expansion + volume (+1) |
| **Tempo** | 1 | Follow-through within 4 bars (+1) |

### Status

| Status | Score | Meaning |
|--------|-------|---------|
| QUIET | — | 4H not active, nothing to do |
| WATCH | ≥ 3 | 4H active, watching for 15m structure |
| SETUP | ≥ 5 | Micro structure forming |
| **TRIGGER** | **≥ 7** | **Structure + behaviour confirmed — entry zone** |

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
| 4H Bias | BULL/BEAR/MIXED/QUIET + setup score |
| Micro Score | X / 10 with color coding |
| Components | Set \| Str \| Beh \| Tmp breakdown |
| Interpretation | Plain-language explanation of current state |
| Signal | BULL ENTRY active / BEAR ENTRY active / — |
| 4H Zone | Distance to nearest relevant 4H zone in ATR |

### Alerts

| Alert | Trigger |
|-------|---------|
| Bull/Bear Trigger | Micro status = TRIGGER |
| Bull/Bear Entry | Entry signal fired |
| Bull/Bear Invalidation | Entry invalidated |
| Micro Setup | Status changes to SETUP |

---

## Display Modes

Each 4H script has three modes (Input "Display Mode"):

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

### Recommended Alert Setup (3 alerts cover 90% of use)

| Alert | Source | Purpose |
|-------|--------|---------|
| **Bull/Bear Review** | Vein Score (4H) | "Something is building — look at chart" |
| **Bull/Bear Trigger** | Vein Execution (15m) | "Now it's getting concrete" |
| **Bull/Bear Invalidation** | Vein Score (4H) | "Cancel — signal failed" |

### Full Alert List

| Source | Alert | Condition |
|--------|-------|-----------|
| Score | Bull/Bear Review | Setup ≥ 4 + Conf ≥ 1.5 |
| Score | Bull/Bear Action | Setup ≥ 5 + Conf ≥ 3 + FT |
| Score | Bull/Bear Invalidation | Candidate → Failed |
| Score | Bull/Bear Candidate | Status = CANDIDATE |
| Score | Conflict | Significant conflict detected |
| Score | Spring/Upthrust | Heuristic triggered |
| Score | Major BOS | Major Break of Structure |
| Score | Bull/Bear Trap | Failed reversal → opposite continuation |
| Zones | Support/Resist Relevant | Zone within 1 ATR, Reach ≥ 60 |
| Zones | Likely Hold/Break | Hold or Break ≥ 60 |
| Execution | Bull/Bear Trigger | 15m status = TRIGGER |
| Execution | Bull/Bear Entry | Entry signal confirmed |
| Execution | Bull/Bear Invalidation | Entry invalidated |
| Execution | Micro Setup | 15m status = SETUP |
| Accum | Developing/Mature | Phase state change |
| Accum | Breakout/Breakdown Ready | Structure shifting |

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
| Vein Trend | Composite reversal signal | `vein_trend.pine` |
| Vein Pullback | Pullback vs. reversal detection | `vein_pullback.pine` |
| Vein Exhaustion | Temporal + emotional overextension | `vein_exhaustion.pine` |

**Three perspectives on the same question:**
- **Trend** → "Is there a structural reversal signal right now?"
- **Pullback** → "Is this counter-move a pullback (reentry) or a reversal (exit)?"
- **Exhaustion** → "Is this move overextended emotionally, before structure confirms anything?"

EMAs and scoring adapt automatically to the active timeframe. All three scripts are configurable as overlays with table position inputs.

---

## 7. Vein Trend (Overlay, any TF)

Multi-layer composite score detecting high-probability reversal signals. Filters with structure gate, conflict detection, cooldown, and trend filter.

### AutoTF Parameters

| Timeframe | Threshold | Cooldown | Structure Gate | Delta |
|-----------|-----------|----------|----------------|-------|
| Daily | 5.5 | 7 bars | 2.0 (conf required) | 1.5 |
| 4H | 5.0 | 5 bars | off | 1.5 |
| 1H | 6.0 | 8 bars | off | 1.5 |
| <1H | 7.5 | 25 bars | off | 2.0 |

### Three Score Layers

**Layer A — Setup Score:** Momentum signals (RSI, MFI, price distance from EMA, wick rejections). Fires early, before structure events.

**Layer B — Confirmation Score:** Structure events with volume weighting: Springs, Upthrusts, BOS. Highest weight (1.5×) — signal requires structural evidence.

**Layer C — Phase Score (0–5):** Accumulation/Distribution context. EMA slope loss, volume compression, range formation. Bonus weight (0.5×) for market context.

**Composite = 1.0 × Setup + 1.5 × Confirm + 0.5 × Phase**

The score bar in the table fills to threshold — full bar = signal condition met.

### Guards

| Guard | Purpose |
|-------|---------|
| **Threshold** | Composite must exceed effThresh |
| **Delta** | Bull and bear scores must differ by ≥ effDelta (prevents ambiguous signals) |
| **Structure Gate** | On Daily: Confirm score ≥ 2.0 required (zone alone not enough) |
| **Cooldown** | Minimum bars between signals in same direction |
| **Trend Filter** | On sub-1H: requires follow-through confirmation |
| **Conflict** | Suppresses signal when both sides near threshold |

### Debug Markers

Colored dots when composite ≥ threshold but a guard blocks the signal:

| Color | Blocking Guard |
|-------|---------------|
| 🟠 Orange | Conflict (both sides near threshold) |
| 🟡 Yellow | Cooldown |
| 🔵 Blue | Structure Gate |
| 🟣 Purple | Trend Filter |
| 🩵 Teal | Follow-Through |
| ⚫ Gray | Delta |

### Table (top right, configurable)

Shows Composite (with progress bar to threshold), Threshold, Setup, Confirm, Phase, Status, Candle State, and Regime.

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
| **Move Weakness** | 3 | RSI stays in safe zone + volume stays low + small candles |
| **Structure Intact** | 2 | No break of frozen swing low/high reference |
| **Fib Depth** | 1 | Retracement in 25–68% range (both references frozen at PB start) |

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
| **Time** | 3 | Consecutive directional closes (grace: 1 bar tolerance before reset) |
| **Overextension** | 3 | EMA distance in ATR units + RSI extreme + MFI extreme |
| **Orderflow Proxy** | 2 | Directional absorption and capitulation/distribution |
| **Volatility** | 2 | Directional ATR spike + climax bar (bull or bear only) |

### Orderflow Events

| Event | Side | Detection |
|-------|------|-----------|
| **Bear Absorption** | Bear exhaustion | Bearish bar + high vol + small range = buyers absorbing |
| **Bull Absorption** | Bull exhaustion | Bullish bar + high vol + small range = sellers absorbing |
| **Capitulation** | Bear exhaustion | Bearish bar + very high vol + large range + close near low |
| **Distribution** | Bull exhaustion | Bearish close after up move + upper wick dominates + overextended |

### Signals

| Signal | Shape | Meaning |
|--------|-------|---------|
| `▼ 7.8` | Label above bar | Upward move exhausted — potential top |
| `▲ 6.2` | Label below bar | Downward move exhausted — potential bottom |
| ● cyan | Dot below bar | Bear absorption — buyers stepping in |
| ● orange | Dot above bar | Bull absorption — sellers stepping in |
| ★ | Cross below bar | Capitulation — panic low |

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
| Trend: WATCH | Composite 5.8 | Approaching threshold but no signal yet |
| → Combined | | High confidence: pullback ending soon, exhaustion at extremes, trend signal building |

**Key rule:** Exhaustion fires first (leading). Pullback identifies context (reentry vs exit). Trend fires last (structural confirmation). All three together = highest confluence.
