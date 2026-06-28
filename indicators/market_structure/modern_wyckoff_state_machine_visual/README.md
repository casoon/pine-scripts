# Modern Wyckoff State Machine Lite

Lightweight Wyckoff state-machine overlay for identifying accumulation, distribution, markup and markdown context. It tracks A-E phases, labels quality-graded events, scores accumulation vs distribution evidence, and summarizes the current phase in a compact dashboard.

## Features

- Accumulation, Distribution, Markup and Markdown state tracking
- A-E Wyckoff phase model with configurable minimum bars per phase
- Quality-graded Spring, UTAD, SOS, SOW, LPS and LPSY event labels
- Stored Spring/UTAD retest logic using event price and event volume
- Pivot-confirmed LPS and LPSY with pivot-bar volume checks
- Selling Climax / Buying Climax and absorption context
- Range high, midpoint and range low visualization
- Locked trading range after phase start
- Range-bounded phase zones with state/phase labels and configurable old-zone handling
- Phase-track line mapped inside the current trading range
- Cause score for Phase B context
- Accumulation score, distribution score, cause score and range-quality dashboard
- Alerts for key Wyckoff events and Phase E trend release

## Model

The script first qualifies a trading range with ADX and ATR-normalized range width. Once a Wyckoff state starts, the active range is locked so Springs, UTADs, breakouts and phase zones are judged against the same reference. It then scores accumulation and distribution evidence from location inside the range, event memory, absorption, midline reclaim/loss and swing/EMA structure.

The state machine uses those scores plus event sequences to progress through:

1. **Phase A** — stopping action via SC/BC or high-volume edge behavior.
2. **Phase B** — cause-building range behavior with accumulation/distribution bias, compression, dwell time, swings, volume dry-up and range respect.
3. **Phase C** — quality-graded Spring/UTAD or lower-volume test of the stored event price.
4. **Phase D** — SOS/SOW, pivot-confirmed LPS/LPSY or preparation near the opposite range side.
5. **Phase E** — confirmed breakout beyond the locked range in the direction of the dominant score.

## Notes

This is intentionally simpler than `wyckoff_schematics`: it is a visual state/context tool, not a full schematic engine. Phase zones are drawn as price-bounded rectangles inside the detected range, not as full-height chart backgrounds. Old phase zones can be deleted, faded, kept without labels or replaced by the current zone only.

Use this as the lightweight live read. Use `wyckoff_schematics` when you need the full event taxonomy, AR/ST sequencing, AVWAP, relative strength and Cause & Effect targets.

## Alerts

- Wyckoff Spring
- Wyckoff UTAD
- Wyckoff SOS
- Wyckoff SOW
- Wyckoff Markup
- Wyckoff Markdown
