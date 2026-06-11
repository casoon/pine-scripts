# SMC Structure & Expectation

Four-layer Smart Money Concepts indicator. Builds context bottom-up: objective swing structure first, then a logical expectation derived from it, then BOS + Order Block confirmation, and finally optional subtle warnings. Each layer acts as a filter for the next — Order Blocks only form after a qualifying BOS, bias only updates after a valid structural move.

## Features

- Layer 1 — Market structure: HH/HL/LH/LL from confirmed pivots, dual external/internal structure with alignment/conflict detection
- Layer 2 — Expectation/bias: "Expect HL", "Expect LH", "Expect Continuation", "Expect Failure" with expiry and invalidation
- Layer 3 — Confirmation: BOS (Close-cross or High/Low-cross with optional close confirmation window) plus a professional Order Block cascade
- Layer 4 — Warnings: swing level breaks, early top/bottom (wick + RSI), visual only, no alerts
- OB filter cascade: range-mismatch guard, segment extraction, displacement (timeframe-adaptive window and threshold), premium/discount location, size (hard limit or score penalty), optional volume and FVG filters
- OB lifecycle: max one OB per direction, mitigation (penetration %), full invalidation, TTL, reaction-type tracking (Tap/Deep/Failure)
- Priority scoring (0–100) from displacement, FVG, volume, location, structure alignment and leg strength
- Bar coloring modes: Structure, Expectation, BOS + OB Priority, Multi-Layer, Alignment
- JMA overlay (3 configurable lengths)
- Debug logging with priority-based filtering and an OB rejection heatmap table
- Alerts: HIGH-priority and standard bull/bear BOS+OB setups, OB mitigation

## Layers

1. **Structure** — external pivots (default 5/5) define the major HH/HL/LH/LL sequence; internal pivots (default 3/3) provide timing and alignment checks.
2. **Expectation** — HH in bullish structure → expect HL; LL in bearish structure → expect LH; HL/LH in trend → expect continuation. Expectations expire after a configurable number of bars and fail when the reference level breaks.
3. **Confirmation** — a BOS only counts when it agrees with the active expectation and passes the range-mismatch guard; the OB is extracted from the impulse segment between swing and BOS and must pass the filter cascade.
4. **Warnings** — passive context flags; they never change the expectation and never fire alerts.
