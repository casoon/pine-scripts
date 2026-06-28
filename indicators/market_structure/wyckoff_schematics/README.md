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

1. **Phase A** — Selling/Buying Climax starts the range. The climax is only accepted when prior trend agrees (an SC will not fire inside a clear uptrend, a BC not inside a clear downtrend). AR requires the swing to travel ≥ 1 ATR away from the climax; ST is detected within the range.
2. **Phase B** — range freezes after `Range Establish Bars`; STs repeat with a 10-bar cooldown.
3. **Phase C** — Spring (accumulation) or UTAD (distribution) breaks the range edge and fails; a low-volume Test confirms it.
4. **Phase D** — in-range SOS/SOW on volume, LPS/LPSY as pivot-confirmed low-volume retests.
5. **Phase E** — Markup/Markdown require Phase D, a confirmed internal structure (Spring/UTAD test, in-range SOS/SOW, or pivot-confirmed LPS/LPSY), a setup score ≥ 50, **and** a confirmed close beyond the range edge on expanding volume (≥ 1.2× avg). That decisive break is emitted as a distinct SOSB/SOWB breakout event. A close beyond the opposite edge plus the invalidation buffer marks the range as failed.

## Setup score & sequence

The setup score (0–100) sums evidence from the structural events, but it is **order-aware**: a Test only counts when it follows its Spring/UTAD, and an in-range SOS/SOW only when it follows the Test (Schematic #1). A clean `Spring → Test → SOS` order earns an extra structure bonus, and the confirmed breakout (SOSB/SOWB) adds to the score. The score keeps updating through Markup/Markdown — there it is scored against the originating schematic (via the previous phase) so the breakout is credited.

## Alerts

- Phase transitions: Accumulation / Distribution / Markup / Markdown started
- Events: Spring, UTAD, Test, SOS, SOW, SOSB breakout, SOWB breakdown, LPS, LPSY, Climax (Effort vs Result)
- Combined quality: Spring + Test confirmed, UTAD + Test confirmed, setup score ≥ 75, HTF/LTF aligned
