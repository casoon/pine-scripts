# Vein Reversal System — Visual Guide

## Overview

The system consists of 3 indicators. Vein Reversal Score and Vein Execution work together on a NatGas chart; Vein Pullback is self-contained and runs on any timeframe.

| Script | Type | Timeframe | File |
|--------|------|-----------|------|
| Vein Reversal Score | Panel | 4H | `vein_reversal_score.pine` |
| Vein Execution 15m | Overlay | 15m | `vein_execution.pine` |
| Vein Pullback | Overlay | any TF | `vein_pullback.pine` |

**Core principle:** 4H = Context (where to look). 15m = Timing (when to act).

The former Vein scripts (Labeler, Structure & Zones, Feature Exporter, Accumulation Phase, Trend, Exhaustion, Spread Context) are archived; reasons and replacements are listed in [`archive/README.md`](../../../archive/README.md).

## Data Validity

`vein_reversal_score`, `vein_pullback` and `vein_execution` all read `syminfo.volumetype` at runtime
(real = the feed delivers volume and does not report `tick`; most non-crypto feeds report `n/a`). On instruments without real trade volume, MFI
and relative-volume components degrade to neutral — their score weight is dropped, not moved to a price component
(moving it to RSI would count RSI twice). Scores therefore have a lower maximum on such symbols while the absolute
thresholds stay the same.
Climax detection in `vein_reversal_score` falls back to a range-only extreme-bar proxy. `vein_execution`'s `relVol`
degrades to a neutral 1.0. The Reversal Score and Pullback tables show a
"Volume" row when running degraded. See
[`DATA_VALIDITY.md`](../../../DATA_VALIDITY.md) for the full policy.

---

## 1. Vein Reversal Score (Panel, 4H)

Two-layer scoring with regime filter, level context, follow-through, and conflict detection.

### Core Principle

Oscillators alone are not enough. Only Setup + Structure confirmation + Follow-through = take seriously.

### Two Layers

**Layer A — Setup Score (bars in panel):** one input per information family — momentum (RSI), volume (MFI, only with real volume), stretch (EMA20 distance in ATR), candle (wick). Stoch RSI, MACD, the Bollinger touch and the efficiency bonus are not scored, because each repeats a family already counted. Without real volume the MFI points are absent and the thresholds stay as they are.

| Component | Points |
|-----------|--------|
| RSI in extreme zone | +1 |
| RSI turning | +0.5 |
| MFI in extreme zone | +1 |
| MFI turning | +0.5 |
| Price far from EMA20 | +1 to +1.5 |
| Strong wick | +1 |
| Trend against setup | -1 |
| Relative volume < 0.6 (real volume only) | -0.5 |

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

## 2. Vein Execution 15m (Overlay, 15m)

Lean execution/timing module. Only activates when the connected setup source says "interesting".

**Core rule:** 15m does NOT decide direction. It confirms or destroys what the setup source suggests.

### Setup context (external sources) and 4H reference levels

The setup scores are **external sources** ("Vein Module Inputs"), not a 4H request: connect Vein Reversal Score's `Bull Setup [dw]` / `Bear Setup [dw]` plots on the same chart. They are therefore computed on the chart timeframe. The two optional trend sources take any plot that is > 0 while the trend is up / down (no remaining Vein script provides one); they only feed the status-table hint.

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
| 4H Zone | Distance to the 4H swing level in ATR — the swing low when the bias is up, the swing high when it is down; green within "Zone Proximity (ATR)" |

### Alerts

| Alert | Trigger |
|-------|---------|
| Bull/Bear Entry | Entry signal fired |
| Bull/Bear Invalidation | Entry invalidated |

The QUIET/WATCH/SETUP/TRIGGER status is display only and has no alerts.

---

## Display Modes

Vein Reversal Score has two modes (Input "Display Mode"):

| Mode | What it shows |
|------|--------------|
| Light | Compact score table |
| Debug | Extended score table with all component rows |

Vein Execution has Light and Debug modes (Debug shows the micro SWP / BOS labels). Vein Pullback has no display modes.

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
| Score | Spring/Upthrust Detected | Heuristic triggered |
| Score | Major Bull/Bear BOS | Major Break of Structure |
| Score | Bull/Bear CHoCH | Change of Character |
| Score | Bull/Bear Trap Hint | Failed reversal → opposite continuation |
| Execution | Bull/Bear Entry | Entry signal confirmed |
| Execution | Bull/Bear Invalidation | Entry invalidated |
| Pullback | Bull/Bear Entry | Pullback end signal |
| Pullback | Bull/Bear Structure Break | Pullback became reversal |
| Pullback | Bull/Bear Signal Invalidated | Close beyond the frozen stop |

---

## Workflow

### Daily Use (4H)

1. Load **Vein Reversal Score** on 4H NatGas
2. Score table tells you: is anything building? Why or why not?
3. Wait for CANDIDATE or at minimum SETUP + structure event

### Timing (15m)

4. When 4H shows active setup, switch to 15m with **Vein Execution** loaded and its setup sources connected to Vein Reversal Score
5. Wait for micro structure: sweep, BOS, rejection
6. TRIGGER status + ENTRY label = consider acting
7. INVAL label = abort, setup failed on micro level

### Trend Continuation (any TF)

8. Load **Vein Pullback** when the question is not a reversal but whether a counter-move in an existing trend is a pullback or a reversal

---

## Vein Pullback (adaptive, any TF)

Vein Pullback is self-contained and timeframe-agnostic: its EMAs and scoring adapt automatically to the active timeframe, and the table position is configurable. It can be used standalone or next to Vein Reversal Score.

---

## 3. Vein Pullback (Overlay, any TF)

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

## Layered Reading

The three scripts answer different questions:

| Script | Question |
|--------|----------|
| Vein Reversal Score | Is a reversal building — setup, structure event, follow-through? |
| Vein Pullback | Is this counter-move a pullback (reentry) or a reversal (exit)? |
| Vein Execution | Does the 15m confirm or destroy what the setup source suggests? |

**Reading order:** Reversal Score and Pullback give the context (reversal vs. continuation). Execution only adds timing once a setup is active.
