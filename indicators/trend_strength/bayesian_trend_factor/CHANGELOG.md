# Changelog

## v1.7.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.7.1 — 2026-06-29
- Alerts: messages standardized to `BTF · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.7 — 2026-06-28
- Rebuilt the pullback module as an explicit state machine (Idle → Armed → Mature → Triggered / Invalidated) for clear signal attribution
- Maturity now requires the pullback to be both old enough and deep enough (≥ Min Pullback Depth); shallow pullbacks stay Armed and cannot trigger a continuation
- Pullback tracking variables are now fully reset on continuation and on invalidation
- Clamped final Bull/Bear probability to `0..1` so EMA smoothing of the factor cannot push it out of range
- Trend Exit Threshold is now bounded below the main threshold (`maxval=55`, exit level = `min(exit, trend − 1)`) so the hysteresis band is always non-degenerate
- Data Window now exposes the bull/bear pullback state for debugging; dashboard distinguishes Armed / Mature / Cont / Invalidated
- Switched the dashboard to the standard light-theme table style so cell text stays readable over any chart background (the previous transparent dark cells were unreadable)

## v1.6 — 2026-06-28
- Reframed header/docs as "Bayesian-inspired" to avoid implying calibrated Bayesian probabilities
- Added Trend Exit Threshold hysteresis: trend activates at the main threshold and exits only below the lower exit threshold
- Pullback trend gate now uses smoothed/final Bull-Bear probability derived from `factorFinal`
- Dashboard separates final Bull Probability from Raw Bull Probability
- Data Window now exposes both final and raw Bull/Bear probabilities

## v1.5 — 2026-06-28
- Added hover tooltips to BTF score labels, PB setup labels and CONT trigger labels
- Replaced PB `plotshape()` markers with real labels so setup explanations are available on hover
- Tooltips show factor, confidence, probabilities, evidence scores, quality multiplier, trigger reason and pullback context

## v1.4 — 2026-06-28
- Backdated Structure Freshness timestamps by `pivotLen`, so confirmed pivots are not treated as fresher than they are
- Widened Pullback Zone around Fair Path to allow controlled sweeps (`+0.25/-0.75 ATR` bull, mirrored bear)
- Reduced Confidence exhaustion malus from `22` to `16`; Exhaustion still penalizes direction through log-odds
- Added short Factor Smoothing input (default `2`) to reduce state flicker
- Limited Volatility Quality Weight input to `0..1`, matching its quality-multiplier role
- Trend Candles now show lightly transparent wicks and borders instead of hiding them
- Dashboard now includes Vol Quality, Quality Multiplier and Direction Gate status
- Dashboard clear uses explicit coordinates for the full table range

## v1.3 — 2026-06-28
- Removed volatility from directional log-odds; ATR regime now acts only as a quality multiplier
- Added minimum-direction gate before Strength can contribute bullish/bearish evidence
- Added Structure Freshness decay so stale HH/HL or LL/LH readings lose influence over time
- Reworked Exhaustion: acceleration alone no longer counts as risk; exhaustion now requires stretch plus rejection or momentum fade
- Reworked Confidence: low exhaustion no longer grants positive confidence points; exhaustion is a true malus
- Tightened Pullback setup detection: price must return from above/below the Pullback EMA and Fair Path into a stricter zone
- Pullback depth now references a prior impulse high/low lookback instead of only the setup candle
- Added score-label cooldown and clears the dashboard table when disabled

## v1.2 — 2026-06-28
- Added optional HAMA-style smoothed Trend Candles via `plotcandle()`
- Added configurable smoothed Open/High/Low/Close lengths and MA types for Open/Close
- Added BTF-gradient candle coloring and alternative smoothed-candle-direction coloring
- Added optional Trend Candle MA line with advance/decline gradient mode
- Clamped smoothed High/Low so synthetic candles always contain their smoothed Open/Close

## v1.1 — 2026-06-28
- Added optional Pullback / Continuation module gated by BTF trend direction and confidence
- Pullback setup detection marks controlled returns to the Pullback EMA / Fair Path zone
- Continuation trigger fires on EMA reclaim, one-bar micro-BOS or rejection wick while structure holds
- Added `0..10` Continuation Score, PB setup markers, CONT trigger labels, dashboard rows and four alerts
- Hardened confidence gating for `Minimum Confidence = 0` and removed unused intermediate variables

## v1.0 — 2026-06-28
- Initial release — probabilistic trend-quality filter with signed `-100..+100` Trend Factor and separate `0..100` Confidence
- Five evidence blocks: regression direction, ADX/ER/R2 strength, swing structure, ATR-regime volatility and exhaustion penalty
- Bayesian-style log-odds fusion with configurable evidence weights
- Confidence gate scales down weak evidence instead of producing a hard binary veto
- Overlay display with candle coloring, Fair Path / ATR bands, optional score labels and compact dashboard
- Alerts for bull/bear trend activation, strong trend states and neutral transition