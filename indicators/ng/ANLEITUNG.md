# NG Reversal System — Visual Guide

## Overview

The system consists of 5 indicators that work together on a NatGas chart.

| Script | Type | Timeframe | File |
|--------|------|-----------|------|
| NG Reversal Labeler | Overlay | 4H | `ng_reversal_labeler_4h.pine` |
| NG Structure & Zones | Overlay | 4H | `ng_structure_zones_4h.pine` |
| NG Feature Exporter | Panel | 4H | `ng_feature_exporter_core_4h.pine` |
| NG Reversal Score | Panel | 4H | `ng_reversal_score_4h.pine` |
| NG Execution 15m | Overlay | 15m | `ng_execution_15m.pine` |

**Core principle:** 4H = Context (where to look). 15m = Timing (when to act).

---

## 1. NG Reversal Labeler (Overlay, 4H)

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

## 2. NG Structure & Zones (Overlay, 4H)

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

## 3. NG Feature Exporter (Panel, 4H)

Shows indicator values as an oscillator panel below the chart.

**Plot group selectable via input "Plot Group":**

| Group | What it shows |
|-------|--------------|
| Momentum | RSI (yellow), Stoch RSI K (cyan), Stoch RSI D (orange) |
| Volume | MFI (teal), Relative Volume (purple) |
| Volatility | BB Width (orange), Candle/ATR (green), BB Distance (cyan) |
| Trend | Price→EMA20 (yellow), EMA20→EMA50 (orange), Slope direction (dots) |
| Candle | Body/Range % (yellow), Upper Wick % (red), Lower Wick % (green) |

### Interpretation Table (top right)

3-column layout showing each feature with current value + plain-language reading:

| Feature | Value | Reading |
|---------|-------|---------|
| RSI | 28.3 | RSI oversold — possible exhaustion |
| StochRSI | K:12 D:18 | StochRSI low, K turns above D — possible reversal up |
| MFI | 24.1 | MFI low — more money flowing out than in |
| Trend | -1.8x | Price below EMA20 — overextended downside |
| Volatility | BB:-2.1 | Price at lower Bollinger extreme |
| Volume | 1.4x | Volume above average — elevated interest |
| | | SUMMARY: Multiple indicators show oversold... |

Color-coded: green at bullish extremes, red at bearish, gray at neutral.

---

## 4. NG Reversal Score (Panel, 4H)

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

### Interpretation (always visible in table, top right)

The table now explains the current state in plain language:

**When a signal is active:**
- "▲ Setup+Structure+FT confirmed"
- "▼ Awaiting follow-through"

**When NO signal is active (the common case):**
- "▲ No bull setup — momentum still bearish"
- "▼ RSI elevated but no overheating in money flow"
- Context: "Downtrend | High volatility | RSI weak"

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

### Momentum Variants (switchable)

| Variant | Components |
|---------|----------|
| **A: RSI+MFI+MACD** (Default) | Cleaner |
| B: RSI+MFI+StochRSI | Faster |
| C: All | For comparison |

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

## 5. NG Execution 15m (Overlay, 15m)

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

### Micro Structure (15m)

Detected with fast pivots (2/2):
- **Micro BOS** — close breaks above last swing high (bull) or below last swing low (bear)
- **Higher Low / Lower High** — structure shift in bias direction
- **Liquidity Sweep** — wick below swing low + close back above (bull spring on 15m)
- **Sweep Confirmed** — price holds above sweep level on following bars

### Entry & Invalidation

**Entry signal fires when:**
- Status = TRIGGER (score ≥ 7)
- Micro BOS or confirmed sweep in bias direction
- Rejection, engulfing, or follow-through present

**Invalidation fires when:**
- Price breaks below sweep low (bull) or above sweep high (bear)
- Opposing micro BOS
- Entry expires after extended time without movement

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

### Status Table (bottom right)

| Row | Content |
|-----|---------|
| Header | NG Exec 15m + Status (QUIET/WATCH/SETUP/TRIGGER) |
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

## Workflow

### Daily Use (4H)

1. Load **NG Structure & Zones** + **NG Reversal Score** on 4H NatGas
2. Score table tells you: is anything building? Why or why not?
3. Zones show: where would a reversal be meaningful?
4. Wait for CANDIDATE or at minimum SETUP + structure event

### Timing (15m)

5. When 4H shows active setup, switch to 15m with **NG Execution** loaded
6. Wait for micro structure: sweep, BOS, rejection
7. TRIGGER status + ENTRY label = consider acting
8. INVAL label = abort, setup failed on micro level

### Research

9. Load **NG Labeler** to see where past reversals were (strong vs weak, fast vs slow)
10. Load **NG Feature Exporter** to compare indicator readings at those points
11. Use Research mode tables for parameter tuning
