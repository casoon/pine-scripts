# Wyckoff Schematics

Volume/spread-based Wyckoff schematic detector. Identifies accumulation and distribution trading ranges in real time, tracks their A–E sub-phases, and labels the structural events that define each phase (PS/PSY, SC, BC, AR, ST, Spring, Test, SOS, LPS, UTAD, SOW, LPSY). A dashboard summarizes phase state, scores and context.

## Features

- Phases A–E within Accumulation and Distribution, plus Markup/Markdown tracking
- Schematic #1 (Spring/UTAD) and Schematic #2 (no Spring/UTAD, direct SOS/SOW)
- Full event set: PS/PSY, SC, BC, AR, ST, Spring, Test, SOS, LPS, UTAD, SOW, LPSY
- Pivot-confirmed LPS and LPSY detection (volume checked on the pivot bar)
- Setup confidence score (0–100) and range quality score (0–100) with quality labels
- Phase-anchored VWAP (AVWAP) as value-area proxy
- Multi-timeframe bias via configurable HTF (EMA level + slope, computed inside `request.security`)
- No Supply / No Demand / Volume Dry-Up markers
- Effort vs Result analysis (Wyckoff's 3rd Law) with climax/divergence markers
- P&F-approximate Cause & Effect price target
- Optional relative strength vs configurable benchmark
- Signal mode: entry events (TEST/SOS/SOW/LPS/LPSY) can be gated by minimum setup score

## Phase lifecycle

1. **Phase A** — Selling/Buying Climax starts the range; AR and ST are detected within it.
2. **Phase B** — range freezes after `Range Establish Bars`; STs repeat with a 10-bar cooldown.
3. **Phase C** — Spring (accumulation) or UTAD (distribution) breaks the range edge and fails; a low-volume Test confirms it.
4. **Phase D** — SOS/SOW on volume, LPS/LPSY as pivot-confirmed low-volume retests.
5. **Phase E** — confirmed close beyond the range transitions to Markup/Markdown; a close beyond the opposite edge plus invalidation buffer marks the range as failed.

## Alerts

- Phase transitions: Accumulation / Distribution / Markup / Markdown started
- Events: Spring, UTAD, Test, SOS, SOW, LPS, LPSY, Climax (Effort vs Result)
- Combined quality: Spring + Test confirmed, UTAD + Test confirmed, setup score ≥ 75, HTF/LTF aligned
