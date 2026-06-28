# Changelog

## v4.0.1 — 2026-06-27
- Final signal gate: the timing trigger (Emit Entry + Entry Direction) is now always required and can no longer be out-voted by context; supporting evidence (Quality Gate / Trend Alignment / Heat) became a graded confidence score with a clamped threshold, and dead-volatility / low-volume remains the only hard structural veto. Replaces the previous 5-point AND-style confluence gate.

## v3.1.2 — 2026-06-27
- Signal model selection (ADX Auto): trend vs reversal model is now chosen by the market-structure regime classifier (trending → trend model, ranging/transitioning → reversal model), making the two mutually exclusive per bar; removed the arbitrary "prefer Mean Reversion" tiebreak.
- Structure filter is now symmetric: longs are vetoed in a confirmed bear trend just as shorts are vetoed in a confirmed bull trend, with the asymmetry driven by the regime rather than hardcoded per direction.

## v4.0
- v4 experimental build

## v3.1.1 — 2026-06-11
- Fix: alert messages referenced plots by index ({{plot_0}}, {{plot_1}}, {{plot_2}}), which pointed at the wrong plots — now referenced by name ({{plot("Consensus Score")}}, {{plot("Signal Confidence")}}, {{plot("Heat Score")}})

## v3.1
- Published release
