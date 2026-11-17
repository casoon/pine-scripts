# Wyckoff Schematics

Volume/spread-based Wyckoff schematic detector. Identifies accumulation and distribution trading ranges in real time, tracks their A–E sub-phases, and labels the structural events that define each phase (PS/PSY, SC, BC, AR, ST, Spring, Test, SOS, LPS, UTAD, SOW, LPSY). A dashboard summarizes phase state, range score and context.

## Features

- Phases A–E within Accumulation and Distribution, plus Markup/Markdown tracking
- Schematic #1 (Spring/UTAD) and Schematic #2 (no Spring/UTAD, direct SOS/SOW)
- Full event set: PS/PSY, SC, BC, AR, ST, Spring, Test, SOS, LPS, UTAD, SOW, LPSY
- Pivot-confirmed LPS and LPSY structure markers (volume checked on the pivot bar; confirmed `Pivot Length` bars after the pivot)
- Range quality score (0–100) with label
- Phase-anchored VWAP (AVWAP) as value-area proxy
- Multi-timeframe bias via configurable HTF (EMA level + slope, computed inside `request.security`)
- No Supply / No Demand / Volume Dry-Up markers
- Effort vs Result analysis (Wyckoff's 3rd Law) with climax/divergence markers
- P&F-approximate Cause & Effect price projection (dashboard "Cause Projection (~)")
- Optional relative strength vs configurable benchmark

## Phase lifecycle

1. **Phase A** — Selling/Buying Climax starts the range. The climax is only accepted when prior trend agrees (an SC will not fire inside a clear uptrend, a BC not inside a clear downtrend). AR requires the swing to travel ≥ 1 ATR away from the climax and to clear the climax bar's own range (above the SC bar's high, below the BC bar's low); ST is detected within the range.
2. **Phase B** — range freezes after `Range Establish Bars`; STs repeat with a 10-bar cooldown.
3. **Phase C** — Spring (accumulation) or UTAD (distribution) breaks the range edge and fails; a low-volume Test confirms it. A Test is only accepted after price has first left the Spring/UTAD level — a close beyond the Spring low + test band (UTAD: below the UTAD high − test band) on an earlier bar.
4. **Phase D** — in-range SOS/SOW on volume, LPS/LPSY as pivot-confirmed low-volume retests.
5. **Phase E** — Markup/Markdown require Phase D, a confirmed internal structure (Spring/UTAD test, in-range SOS/SOW, or pivot-confirmed LPS/LPSY) **and** a confirmed close beyond the range edge on expanding volume (≥ 1.2× avg). That decisive break is emitted as a distinct SOSB/SOWB breakout event. A close beyond the opposite edge plus the invalidation buffer marks the range as failed.

## LPS / LPSY

LPS and LPSY are pivot-confirmed: the label sits on the pivot bar, but the event (and its alert, "LPS CONFIRMED" / "LPSY CONFIRMED") only exists `Pivot Length` bars later. They are structure markers inside the range, not entries.

## Alerts

- Phase transitions: Accumulation / Distribution / Markup / Markdown started
- Events: Spring, UTAD, Test, SOS, SOW, SOSB breakout, SOWB breakdown, LPS, LPSY, Climax (Effort vs Result)
- Combined events: Spring + Test confirmed, UTAD + Test confirmed, HTF/LTF aligned
