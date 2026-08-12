# Support & Resistance Zones

A detector-driven support/resistance zone engine. Independent detectors (pivot clusters, multiple tests, base/supply-demand, order blocks, fair value gaps, price gaps, equal-high/low liquidity) each emit `ZoneCandidate` evidence into a central registry, which is the only part of the script allowed to create, merge, score or draw a zone. Detectors never draw directly — detection and rendering are deliberately separated so the registry can be validated, reused by other WavesUnchained indicators, and eventually extracted into a shared library.

## Architecture

```
Detectors -> ZoneCandidate -> candidate validation -> Zone registry ->
clustering/merging -> confluence -> scoring -> lifecycle -> renderer + logs + statistics
```

- **Detectors** only produce `ZoneCandidate` objects (direction, price range, origin bar, source code, initial score, reason string). They hold no drawing logic.
- **Registry** (`f_ingestCandidate`) validates a candidate's width against ATR, then either merges it into the nearest valid overlapping/nearby same-direction zone or creates a new `Zone` with a stable `id`.
- **Confluence** (`f_applyConfluence`) adds score once per source (EMA, VWAP, Fibonacci, psychological level, relative volume) to a zone at the moment it is touched, independent of which detector created it — not continuously, so a wide zone can't accumulate confluence merely by being wide.
- **Lifecycle** mutates only on confirmed bars, advances each zone through age, break, touch and reaction checks, and re-checks each live zone's width against `Maximum Merged Zone Width · ATR` so a zone merged during a high-volatility period doesn't stay frozen that wide once volatility drops. A new zone and a break/flip bar cannot validate themselves as a retest.
- **Renderer** only draws the `Maximum Visible Zones Per Side` zones nearest to price that clear `Minimum Visible Zone Score`, are on their actual side of price (support at/below, resistance at/above), and don't overlap a selected zone of the same direction.

## Features

- Pivot cluster (PC) detector from ATR-tolerant clustering of confirmed pivots retained for the configured history window; MT is normally earned through later real zone tests and falls back to stricter pivot clustering only if PC was not accepted
- Base / Supply & Demand detector — compact range followed by a displacement exit; the shared raw pattern is one source (`SD` when enabled, otherwise `BASE`), never `BASE+SD` double evidence
- Order Block (OB) detector — displacement + prior-structure break + last opposite-color origin candle
- Fair Value Gap (FVG) and residual unfilled classical Price Gap (GAP) detectors, tracked as separate sources
- Equal High / Equal Low Liquidity (LIQ) detector from clusters of same-level confirmed pivots in retained history
- Central zone registry with ATR-based merge distance, merged-width cap and stable `Zxxx` IDs
- Confluence scoring: EMA, VWAP, Fibonacci (rolling high/low), psychological price step, relative volume
- Lifecycle: touch detection with cooldown, reaction validation against a configurable ATR target and horizon, confirmed break detection, optional Support <-> Resistance flip on break (BO source)
- Nearest-to-price renderer — top N zones per side, score-filtered, non-overlapping, on-chart state label, with hover tooltips (state, sources, score, touches, reactions, breaks, origin/created bar)
- Pine Log event logging (`CREATE`/`MERGE`/`REJECT`/`TOUCH`/`REACTION`/`WEAK`/`BREAK`/`FLIP`) and an optional validation statistics table for Validation/Debug operating modes

## Scoring

`score` (0-100, clamped) is a heuristic confluence/quality score, **not** a statistical probability. It accumulates from:

- The initiating detector's configured weight (Pivot Cluster, Multiple Tests, Base, Supply/Demand, Order Block, Fair Value Gap, Price Gap, Liquidity)
- Each additional detector whose evidence merges into the same zone (once per source code, tracked via the `sources` string, e.g. `PC+OB+FIB`)
- Confluence hits (EMA/VWAP/Fib/Psychological/Volume), each awarded once per zone
- A Breakout/Flip bonus (`BO`) the first time a zone is confirmed broken and flips direction

All weights live in the `10 · Scoring` input group so relative detector/confluence importance can be tuned without touching code.

## Lifecycle states

`NEW -> TESTED -> CONFIRMED` on a successful reaction, or `-> WEAK` if the reaction horizon expires without one. A confirmed break either sets `BROKEN` (kept for `Keep Broken Zones` bars, then `INVALID`) or, if `Convert Broken Zones Into Flip Zones` is on, sets `FLIPPED` and reverses `dir`. `INVALID` zones are functionally dead but remain in storage until pruned by `Maximum Stored Zones`. With `Show Zone State` on (default), the current state is appended to the on-chart label, e.g. `OB+FIB+MA · 28 · TESTED` — validity is visible without hovering.

## Zone age vs. provenance

The rendered box's left edge is anchored to `createdBar` (when the Zone entity itself was instantiated) rather than `originBar` (the earliest evidence ever merged into it). `originBar` only ever regresses further into the past as a zone absorbs more evidence over time — anchoring the box to it would make every long-lived, frequently-reinforced zone look equally ancient regardless of how recently it was actually reinforced. `originBar` remains visible in the hover tooltip as "how far back does evidence for this price area go," a genuinely different and still useful question from "how long has this exact zone existed."

## Zone codes

The label on each rendered zone is its `sources` string with `|` replaced by `+` (e.g. `PC+OB+FIB`), optionally followed by ` · <score>`. Codes: `PC` pivot cluster, `MT` multiple tests, `BASE`/`SD` base / supply-demand, `OB` order block, `FVG` fair value gap, `GAP` price gap, `LIQ` liquidity, `BO` breakout/flip, `MA`/`VWAP`/`FIB`/`PSY`/`VOL` confluence.

## Status

This is a `0.1.11` engine-foundation build: the architecture, detectors, merging, lifecycle, confluence, scoring, renderer, logging and validation table exist end-to-end, but no detector threshold or scoring weight has been calibrated against real charts, and the script has not yet been run through the TradingView Pine Editor compiler. The v0.1.6 static-review fixes ensure that lifecycle events occur only after a confirmed bar, fresh zones do not validate themselves, GAP boxes are residual unfilled gaps, reinforcement extends analysis lifetime, and the renderer honours actual price sides. v0.1.7 makes equal-high/low detection robust to intervening pivots, v0.1.8 removes duplicate BASE/SD evidence, v0.1.9 chooses the nearest valid merge target, v0.1.10 retains the configured pivot-history window, and v0.1.11 removes routine PC/MT double scoring. See `CHANGELOG.md` and `todo.md`; the next priority remains compiling and isolating the registry before trusting the speculative detectors (OB, SD, LIQ).

## Known limitation — width re-check can cut off an in-progress touch

The v0.1.1 width re-check re-centers an over-wide zone around its midpoint every bar, including bars where price is actively inside it. If a zone was wide because that width was itself meaningful evidence (e.g. a genuinely broad liquidity pool), shrinking it mid-touch could clip the interaction. Not yet observed on a real chart — flagged here so it's the first thing to check if reaction/touch counts look off after this change.
