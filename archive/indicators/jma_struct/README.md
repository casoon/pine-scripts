# JMA Cluster Entries with Market Structure

Multi-timeframe JMA cluster analysis with market structure detection. Combines a 10-JMA cluster scoring system (0–100 alignment score) with Wyckoff phase/event detection, an SMC Order Block system, and trend entries that fire on the JMA cluster flip.

## Features

- JMA cluster scoring (0–100) across 10 Jurik Moving Averages (20–600)
- Trend entries on the JMA cluster flip, filtered by minimum slope, score jump (JMA steps), ATR distance to the slow JMA and optional slope direction
- Wyckoff detection: SC, BC, Spring, UT, AR, ST, LPS/LPSY, SOS/SOW, BU with phase state machine
- Professional Order Block system: BOS validation, displacement, confluence scoring, mitigation tracking, top-3 ranking per direction
- Fair Value Gaps and Breaker Blocks
- Dual-pivot system: live-ready entries (no repainting) + Historical Perfect ZigZag for visualization
- Timeframe-optimized lookbacks (15M/1H/4H/Daily/Weekly)
- Reversion zone with deviation bands and Z-score candle heatmap
- Entry cooldown and anti-spam guardrails (entry cooldown, pivot reset modes)
- Signal logging with bar metrics at entries and pivot coverage
- Alert conditions for entries

## Signal

| Label | Trigger |
|---|---|
| T (green/red) | JMA cluster flip (score crosses the cluster threshold) with slope, score-jump and ATR-distance filters and the entry cooldown |

Wyckoff events, order blocks, FVGs, retests and the reversion zone are context on the chart; they do not trigger entries.

## Alerts

- Entry Long / Entry Short — confirmed entry signals
