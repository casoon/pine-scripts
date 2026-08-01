# Changelog

## v1.3.1 — 2026-08-01
- Fix: Bullish/Bearish Anchor Rejection markers were drawn on the confirmation bar (`Reaction Horizon` bars, default 5, after the actual touch), landing visually inside the following move instead of at the real bounce — added `offset = -reactionBarsInput` (same idiom already used for pivot markers elsewhere in this repo, e.g. `mtf_wavetrend_opportunity_hunter.pine`, `cvd_bias.pine`) so the marker now draws at the historical touch bar; the underlying confirmation logic and non-repainting behaviour are unchanged

## v1.3.0 — 2026-08-01
- Redesigned Weakness: the old Long/Short Weakness markers (`plotshape`, "LW"/"SW") fired every bar their condition held, stacking overlapping duplicate labels through an entire fade episode with no incremental information after the first bar. Weakness is now a **Fading attribute of the active State Layer state** instead of a separate marker stream: any active Bull/Bear Expansion/Pullback state can additionally carry Fading, surfaced as a " (Fading)" tooltip suffix and a muted status-marker colour, plus edge-triggered Bull/Bear Regime Fading alerts (fire once per episode, not per bar)
- Removed a redundancy in the underlying condition: `fastSlope < fastSlope[1]` (1-bar comparison) and `fastCurvature < 0.0` (already the multi-bar-smoothed slope delta) measured essentially the same deceleration twice; the 1-bar comparison was dropped, `longRegime`/`shortRegime` were replaced by the already-computed `bullExpansionState`/`bullPullbackState`/`bearExpansionState`/`bearPullbackState` booleans (4 conditions instead of 5, no double-counted evidence)
- Removed the now-unnecessary "Show Weakness Signals" toggle — Fading is always part of the existing status marker/tooltip, no separate on/off surface needed
- Added `State Fading` to the data window for debugging

## v1.2.0 — 2026-08-01
- Added Anchor Respect: the same touch+reaction statistics previously tracked only for the Base MA now also run against the Anchor MA (`useAnchorRespectInput`, ±5 score component, "Anchor respected bullish/bearish" tooltip line, Bullish/Bearish Anchor Respect Rate in the data window)
- Added confirmed Bullish/Bearish Anchor Rejection markers (`showAnchorRejectionSignalsInput`) and matching alerts — fires when price touches the Anchor MA and holds a reaction move away from it over the Reaction Horizon; previously a rejection off the Anchor was invisible to the script (Anchor only fed regime/direction, never a live signal)
- Base respect tooltip line reworded "No clear MA respect" → "No clear base respect" to disambiguate from the new Anchor respect line

## v1.1.0 — 2026-08-01
- Status readout: replaced the always-visible multi-line text label with a small state-coloured circle marker; the full readout (state, bias, score, permission, setup, MA respect, preset) now shows on hover via `tooltip`, and the default horizontal offset moved further from the current candle (3 → 10 bars)

## v1.0.2 — 2026-08-01
- Fix: `ta.sum` is not a Pine v6 built-in either — all rolling-sum calls (cross frequency counters, MA-respect touch/success counters, KAMA volatility) now use the `ta.sma(x, n) * n` idiom instead

## v1.0.1 — 2026-08-01
- Fix: `ta.kama` is not a Pine v6 built-in — replaced with a self-contained Kaufman Adaptive MA implementation (efficiency ratio + fast/slow smoothing constant)

## v1.0.0 — 2026-08-01
- Initial version: Fast/Base/Anchor MA cascade with Visual/Feature/State/Decision layer architecture
- Seven-state classification (Bull/Bear Expansion, Bull/Bear Pullback, Overextended, Transition, Neutral Compression)
- Signed −100..+100 score from direction, slope, expansion, curvature, MA respect, and cross-frequency quality
- Permission/Setup/Trigger/Weakness/Exit signals with alerts and right-side status label
