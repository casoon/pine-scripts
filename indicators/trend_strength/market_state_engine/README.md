# Market State Engine

A context engine for medium- to long-term discretionary trading. Instead of producing a standalone buy/sell signal, it classifies the market into one of nine states, locates price within an adaptive value zone, estimates which side holds the structural advantage, and scores whether the market is building, releasing, or exhausting energy — so that signals from other indicators can be graded against the surrounding context rather than read in isolation.

## Features

- Orthogonal Structure Regime, Energy Phase, and Auction Location axes combined into nine visible states
- Score arbitration across all non-Transition states; ambiguous reads become Transition
- Adaptive value zone (VWMA / EMA / Hybrid basis) with Discount / Value / Premium / Extreme location classes
- Auction Pressure from close-position, failed breakouts/breakdowns, effort-vs-result absorption, and reaction at value extremes
- Compression plus direction-specific Bull/Bear expansion and exhaustion scores built from ATR, Bollinger width, candle overlap, ADX, efficiency ratio, directional progress, and normalized momentum deceleration
- Bar-close state machine with confirmation bars, minimum state dwell, and an emergency override limited to high-confidence opposite Expansion
- Selectable structure smoothing: JMA Approx (smooth low-lag default), EMA (stable comparison), DEMA (faster), or KAMA (adaptive)
- Sequence-aware Balance/Compression context using directed impulse progress, efficiency, and hybrid close/wick correction depth
- Optional confirmed higher-timeframe structural context (advisory by default; a strict toggle can gate expansions against HTF structure)
- Balance/compression zones with interruption grace, maximum ATR width, confirmed-state grace, and Balance→Compression history
- Acceptance-based `BOX?` attempts requiring consecutive buffered closes and minimum quality; accepted breakouts receive follow-up status
- Zone quality encoded via border thickness (running average State Quality), with fill/border colored by Auction Pressure
- Box profile in every zone hover: ATR-normalized width, debounced upper/lower edge reactions, failed breaks on both sides, total and relative volume, volume-anchored Box VWAP when usable, and scored breakout quality
- `EXP`, zone, and `BOX ↑/↓` breakout hover labels with the relevant state, score, bias, quality, location, duration, range, and outcome context
- Four-level Long/Short context (`Unfavorable`, `Neutral`, `Compatible`, `Preferred`) and reaction-based readiness markers
- Optional context dashboard (off by default) and bar-close alerts for state changes, zone breakouts, and long/short readiness

## State Model

| State | Meaning |
|---|---|
| Balance | Market trades in equilibrium — high candle overlap, low net progress |
| Compression | Balance with additionally falling ATR/BB width — space and movement are contracting |
| Bull/Bear Expansion | Directional move with structural support, matching candle behavior, and efficient signed net progress |
| Bull/Bear Pullback | Retracement inside an intact directional structure |
| Bull/Bear Exhaustion | Extended directional move with a measured deceleration, failed-progress, or effort/result trigger |
| Transition | None of the above states qualifies — no reliable read |

Each non-Transition state receives a complete candidate score. The engine selects the best and second-best candidates, then requires both `Minimum State Score` and `State Dominance Margin`; otherwise the raw result is Transition. States then pass through the bar-close confirmation machine (`confirmBars`, `minimumStateBars`). Only a high-confidence opposite Bull/Bear Expansion can bypass normal dwell. Until every required input is available, the dashboard displays `Initializing` and no state is confirmed.

## Orthogonal Axes

`Structure Regime` reports Bullish, Bearish, Balanced, or Conflicted. `Energy Phase` reports Contracting, Neutral, Expanding, or Exhausting. Auction Location remains the five-part Extreme Discount → Extreme Premium scale. Visible states are the dominant composition of these concurrent properties rather than the first matching boolean rule. The Data Window exposes both axes, candidate scores, best/second-best scores, and dominance. Transition additionally reports whether data is missing, candidates conflict, a trend is forming, structure broke, or conditions are chaotic.

## Value Location

Fair value is a VWMA, EMA, or hybrid of `hlc3`. Zone width scales with the residual standard deviation of price around that basis (floored at 0.6× ATR), producing five location classes from Extreme Discount to Extreme Premium. Location is descriptive, not a signal by itself — its meaning depends on the concurrent market state (e.g. Discount inside a Bull Pullback vs. Discount inside a Bear Expansion).

## Auction Pressure

`directionalBias` is a behavioral proxy—not order flow, accumulation/distribution, or smart-money detection. It combines signed close-position/body-efficiency pressure, failed auctions, effort-vs-result absorption, and reaction at value extremes. Visible text calls it `Auction Pressure`. `Use Volume in Auction Pressure` affects this model; `Use Volume in Box Statistics` independently controls Box Volume, Box VWAP, and breakout-volume confirmation.

## Context Compatibility

Long and Short context each use four levels: `Unfavorable`, `Neutral`, `Compatible`, and `Preferred`. Balance at Value is neutral, ordinary Premium is unfavorable for Long, and ordinary Discount is unfavorable for Short. Pullbacks become Preferred only after a directional reaction candle at structure/value with matching Auction Pressure. Readiness therefore means a reaction or directional auction condition is present—not merely that a Pullback state exists.

## Impulse and Correction Context

The engine remembers the most recent confirmed Bull/Bear Expansion using start/end price, directed net progress in ATR, gross range, efficiency, duration, and average State Quality. A usable impulse requires at least 0.80 ATR net progress and 45% efficiency. Correction depth combines 35% wick retracement with 65% close retracement to reduce single-wick distortion. If Balance or Compression follows while that impulse is still recent and meaningful, the dashboard adds one simple classification:

- `Pause after advance` / `Pause after decline` — shallow compression with no strong opposing bias
- `Correction after advance` / `Correction after decline` — a broader balance or pullback after the move
- `No clear continuation` — the retracement is too deep, opposite/local structure no longer supports the impulse, or the confirmed HTF runs against it
- `No clear impulse` — no sufficiently recent and meaningful impulse is available

The classification is context, not a trade signal. While the prior move remains intact, the Long/Short compatibility rows suppress the direction against that move. Zone labels expose the result directly as `BAL ↑/↓` or `COMP ↑/↓`, where the arrow is the prior impulse and preferred continuation direction; `BAL ?` / `COMP ?` means that direction is no longer trustworthy. A directional label requires the selected parent structure to remain intact, the confirmed HTF not to oppose it, and the maximum counter-move since impulse completion to stay below the invalidation threshold. Intact Long/Short labels are green/red; labels without a reliable direction remain gray. The hover separates the previous impulse, subsequent phase, counter-move depth, preferred direction, and the concrete reason when no direction remains. After a confirmed zone breakout, the original zone label adopts the breakout direction. Tooltips describe breakouts only as `aligned` or `opposing`; they do not claim that a trend must continue or that a correction has definitively failed.

## Structure Smoothing

`Structure Smoothing` changes both structure lines and every rule derived from them, including their cross, slopes, pullback tests, impulse preservation, and confirmed HTF structure. JMA Approx is the default for a smoother low-lag response. EMA remains the stable comparison, DEMA reacts faster but can switch more often, and KAMA adapts its speed to market efficiency. HMA is intentionally excluded because its overshoot can create misleading structure crosses in a regime classifier.

## Higher Timeframe

The higher timeframe does not vote on the current state. It only contributes to `htfAgreementScore` (part of trend quality) and to the long/short context-compatibility gates. With `requireHtfAgreement` enabled, Bull/Bear Expansion additionally requires HTF structural agreement. HTF calculations use the most recently completed context bar, including a slope calculated between two completed HTF bars, so realtime values remain stable. If the selected context timeframe is equal to or below the chart timeframe, the HTF layer safely falls back to off and the dashboard displays `TF ≤ Chart`.

## Zone Geometry

Zone boxes retain the true raw Balance/Compression onset. Shock or ineligible bars pause a young raw zone for `Raw Zone Interruption Bars`; they do not alter geometry, and a buffered close outside still resets it immediately. Active geometry grows only on eligible confirmed bars and closes as `Balance became too broad` before exceeding `Maximum Zone Width in ATR`. Leaving the zone state starts `Zone State Grace Bars`; state alone does not close the box while price remains accepted inside. Zone hover records its start/current type and Compression share. The transferred creation bar is accumulated only once.

A buffered close creates `BOX? ↑/↓`, not an immediate breakout. Acceptance requires `Breakout Confirmation Closes` consecutive closes outside and `Minimum Breakout Quality`. A return inside records a failed attempt and leaves the source zone active. Accepted breakout labels are monitored for `Breakout Follow-up Bars`; their hover is updated with `Breakout held`, `Retest passed`, or `Back inside the box` without rewriting the original breakout decision.

## Box Profile

The hover normalizes box width by the average ATR tracked across the zone, making ranges comparable across symbols and timeframes. After the box becomes confirmed and visible, upper/lower edge reactions are counted only once per continuous contact; a wick must reject the edge rather than merely trade nearby. Failed breaks require a meaningful probe beyond the prior edge and a close back inside, so the counts are Spring-/Upthrust-like observations rather than full Wyckoff phase claims.

With `Use Volume in Box Statistics`, the hover reports total volume, average volume per bar relative to normal, and Box VWAP. The feed may supply tick volume rather than exchange volume. `Show Box VWAP` controls only the line. Breakout quality combines buffered ATR distance, directional candle behavior, directional Expansion, and optional box-volume confirmation; it is now part of acceptance rather than a purely descriptive after-the-fact score.

## Input Validation

The engine rejects contradictory settings instead of silently producing inverted scores: the fast structure length must remain below the slow length, the strong-ADX threshold above the trend threshold, Discount/Premium thresholds inside the Extreme threshold, and the minimum zone duration within the maximum duration. An invalid HTF/chart-timeframe combination does not stop the script; it disables only the HTF layer.
