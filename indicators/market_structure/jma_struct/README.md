# JMA Cluster Entries with Market Structure

Multi-timeframe JMA cluster analysis with market structure detection. Combines a 10-JMA cluster scoring system (0–100 alignment score) with Wyckoff phase/event detection, an SMC Order Block system, and a multi-signal entry matrix that produces quality-scored entry signals.

## Features

- JMA cluster scoring (0–100) across 10 Jurik Moving Averages (20–600)
- Multi-signal entry matrix: Momentum (score reversal), Exhaustion (efficiency falling + divergence), Structure (Spring, Absorption, Wyckoff patterns)
- Data-driven quality scoring with feature flags for A/B testing (based on 12,648 signal analysis)
- Wyckoff detection: SC, BC, Spring, UT, AR, ST, LPS/LPSY, SOS/SOW, BU with phase state machine
- Professional Order Block system: BOS validation, displacement, confluence scoring, mitigation tracking, top-3 ranking per direction
- Fair Value Gaps and Breaker Blocks
- Dual-pivot system: live-ready entries (no repainting) + Historical Perfect ZigZag for visualization
- Timeframe-optimized lookbacks (15M/1H/4H/Daily/Weekly)
- Reversion zone with deviation bands and Z-score candle heatmap
- Entry cooldown and anti-spam guardrails (alert cooldown, entry cooldown, pivot reset modes)
- Comprehensive signal logging for offline optimization
- Separate alert conditions for early-warning alerts and confirmed entries

## Signal types

| Label | Class | Trigger |
|---|---|---|
| A (yellow) | Alert | Buildup detected (score extreme + oscillator confirmation) — early warning |
| M (green/red) | Momentum | Score reversal from alert level inside the entry window |
| E (green/red) | Exhaustion | Efficiency falling + rejection, 2-bar confirmation |
| S (green/red) | Structure | Spring/Absorption/Wyckoff pattern, 2-bar confirmation |

## Quality scoring

Two modes, controlled by the "Use Data-Driven Quality Scoring" switch:

- **Original** (default): slope-based quality relative to the selected Slow/Trend JMA
- **Data-driven**: base 50 plus bonuses (efficiency falling, structure class, absorption, rejection wicks, score delta) and penalties (momentum-only, shock regime, impatience, Wyckoff conflict), each individually toggleable. `Min Quality for Entry` gates final signals.

## Alerts

- Entry Long / Entry Short — confirmed entry signals
- Alert Long / Alert Short — early-warning buildup alerts
