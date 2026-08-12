# Market Motion DNA v1.0

Objective movement-character engine. It does not count Elliott waves — it classifies each confirmed and developing pivot-to-pivot leg as primarily impulsive, corrective, or neutral using measurable price-action properties. A green leg means "impulsive", not "bullish"; a red leg means "corrective", not "bearish" — an impulsive downward move is shown green.

## Features

- ✓ Alternating confirmed pivot engine (same-type extremes replace the last pivot instead of adding a new one) with a minimum leg size in ATR and a bounded history of retained legs
- ✓ Live leg: the current leg runs from the last confirmed pivot to the current bar and re-scores every candle
- ✓ 10-feature Leg DNA: Directional Efficiency, Candle Overlap, internal Retracement Depth, Close Commitment, Wick Cleanliness, Momentum Expansion, True-Range Expansion, MA Support, Direction Cleanliness, Directional Acceptance — each feature's weight is configurable
- ✓ Impulse Score (0–100), Correction Score (0–100), Confidence, and Maturity per leg
- ✓ Minimum maturity age and hysteresis so young or borderline legs don't flip character every bar
- ✓ Translucent leg envelopes (historical + live), optional live-candle tint, completed/live labels, live character-change alerts, and full Data Window exposure
- ✓ Segment-level leg coloring — a completed leg's envelope is split into colored segments at each bar where its character changed while still live, instead of one solid color for the whole move
- ✓ Internal sub-swing count, average sub-swing size (ATR multiples), progression-to-rotation ratio, and sub-swing growth ratio per leg, from a smaller, independently-configured pivot pass scoped to each leg — diagnostic only (tooltip + Data Window), does not feed the Impulse/Correction score
- ✓ Minimum label spacing (bars) — skips a completed leg's label if it would land too close to the previous one, so short/frequent legs don't stack overlapping labels; the leg's colored envelope is unaffected
- ✓ Merge consecutive legs into one coherent wave — a classic Zigzag-style rule: a wave tracks new extremes in one direction, absorbing a same-direction leg only if it's an actual new high/low and absorbing an opposite-direction (counter-swing) leg unconditionally without moving that tracked extreme. The wave ends exactly at its last real extreme — never past it — the instant a same-direction leg fails to extend further, and the next wave starts from that exact same point (no time gap). A grinding trend made of small alternating impulsive pushes and corrective pullbacks now draws as one clean pivot-to-pivot box instead of many small, individually-weak ones. Once flushed, the wave's whole span is classified the same way as any leg — a run whose whole-span character is NEUTRAL and reaches at least "Minimum consecutive legs to merge into one wave" legs draws as a "RANGE (Nx)" box instead of a normal leg

## Scoring

Every confirmed and live leg runs through `f_calculateLeg`, which walks the leg's bars (capped at "Maximum bars evaluated per leg") and accumulates the 10 DNA features. Each feature maps to a 0–1 value; Impulse Score and Correction Score are the weighted sum of those features (inverted for Correction) scaled to 0–100 and pulled toward neutral (50) by the leg's Maturity — a leg younger than "Bars until full score maturity" is not yet fully committed to a character. A leg is classified `IMPULSE`/`CORRECTION` only once Maturity reaches 1.0 and the score separation clears "Minimum score separation"; otherwise it stays `NEUTRAL`.

## Modes

There is a single live mode: historical legs are drawn once on confirmation and stay fixed, while the current leg's envelope, label, candle tint, and classification are recalculated on every bar until the next pivot confirms and closes it out.

The pivot engine works strictly swing-to-swing — it has no concept of "this is one flat/ranging zone" or "this is one bigger wave." A genuine consolidation, or a grinding trend made of small alternating impulsive pushes and corrective pullbacks, legitimately decomposes into several small legs, each individually weak or mixed in character. "Merge consecutive legs into one coherent wave" (v1.5.0, refined to a strict Zigzag-extreme rule in v1.5.1) tracks new extremes in one direction: a same-direction leg absorbs only if it's an actual new high/low, a counter-swing leg absorbs unconditionally without moving the tracked extreme. The wave always ends exactly at its last real extreme (never past it, and never with a time gap to the next box) the moment a same-direction leg fails to extend further, at which point its whole span gets classified the same way as any leg. Only a wave whose whole-span character stays NEUTRAL gets the generic "RANGE (Nx)" treatment — any IMPULSE/CORRECTION wave, however many small legs it absorbed, draws as one normal leg.

## Suggested starting presets

| Preset | Pivot L/R | Min leg size (ATR) | Score maturity |
|---|---|---|---|
| Default / general test | 5 / 5 | 0.50 | 8 bars |
| Larger structure | 8–13 / 8–13 | 1.0–1.5 | 12–20 bars |
| Intraday / smaller structure | 3–5 / 3–5 | 0.3–0.7 | 5–10 bars |

Also useful as a starting point: Impulse/Correction threshold 62, Minimum separation 18, Character-change buffer 5, Support MA EMA 34.

## Known limitations

- Not compiled/run in TradingView's Pine compiler yet — minor compiler fixes are possible
- Score formulas are not yet empirically calibrated across asset classes/regimes
- Internal sub-swing tracking (v1.2.0/v1.3.0) covers count, average size, progression-to-rotation, and growth trend — no structural (non-candle-range) overlap between sub-swings yet
- Several DNA features (Commitment, Wick Cleanliness, Momentum/TR Expansion, MA Support, Acceptance) read close to neutral (~50) in both trending and choppy conditions, diluting the score separation the stronger discriminators (Efficiency, Overlap, Retracement, Cleanliness) would otherwise produce — this can leave genuinely decisive legs classified NEUTRAL; tracked for Phase 1.2 calibration, not yet acted on without real per-leg data
- No ABC/WXY detection, Elliott labeling, or Fibonacci targets (roadmap Phase 2+)
- "Wick cleanliness" measures body/range dominance, not which side of the candle the wick is on — a favorable and an unfavorable wick of the same size score identically

See `todo.md` for the full roadmap.
