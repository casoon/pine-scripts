# Changelog

## v3.5.0 — 2026-07-31 — "Structural Core Fix"
- Fix (most consequential since v3.0): a normal, healthy pullback was replacing the reference leg it was a pullback *within*, before Continuation Maturity's own preferred zone (~0.38–0.62) could ever be reached — v3.2's `minLegRetracementInput` default (0.25) sat below that zone, so the leg got promoted away right when the setup should have started scoring well. Renamed to `legInvalidationRetracementInput`, default raised to 0.90 (near-full round-trip back to the leg's own origin) — the formula already measured retracement against the origin correctly, only the threshold was wrong
- Fix: a same-type pivot only extends the reference leg's endpoint if it's an actual new extreme beyond tolerance — a smaller same-type pivot no longer silently shrinks the leg
- Fix: new `bullImpulseExhaustion`/`bearImpulseExhaustion` (reusing the existing divergence-decay state, properly rescaled) replace counter-move exhaustion in the Reversal readiness formulas — Reversal needs "is the original impulse exhausted", not "is the counter-move exhausted" (which is evidence *for* continuation, not reversal — using the same measure for both was backwards)
- Fix: Endpoint Reversal's overextension score now uses ATR frozen at the moment the leg's endpoint was last set, not live ATR during the correction that follows (so later volatility can't re-rate an already-completed leg)
- Fix: T2 is discarded (`na`) unless it actually lies beyond T1 by the minimum distance instead of freezing a nonsensical level
- Fix: CRV switches from T1 to T2 once T1 has already been hit and T2 tracking is active — staying pinned to an already-passed T1 was crushing the score right when the trade was doing well
- Fix: a trade only stays open past T1 for T2 tracking if T2 actually froze as a valid level — otherwise (T2 enabled but no valid T2 target) it would never close on its own
- Fix: a Trigger that never fires within its validity window now resets to UNTRIGGERED instead of indefinitely showing a confirmed score with no way left to signal
- Fix: scenario hysteresis (Continuation vs. Reversal dominance) resets on a new reference leg instead of carrying the old leg's dominant scenario into a brand new one
- Fix: a new Trigger no longer fires while a same-direction trade is already open — it would have silently replaced the open trade's frozen Target/Invalidation
- Reviewed and reaffirmed not a bug (asked again in this review): leg-quality numerator/denominator attribution — see README "Reviewed and not changed"

## v3.4.0 — 2026-07-31
- New: Endpoint Reversal — a second Reversal Maturity component scores the reference leg's own overextension (ATR-relative), independent of how deep it has retraced yet, so a reversal can score right at the impulse's own top instead of only after a ~1.272 round-trip; combines with the existing structural-failure curve via `max()`
- New: a separate, wider/later-centered time-maturity curve for Reversal (structural failure is typically a bigger, slower move than a Continuation pullback)
- New: Trigger validity window (`triggerValidityBarsInput`, default 8) — a confirmed Trigger stays armed for N bars instead of only being usable on the exact bar it reached CONFIRMED, so Readiness clearing its threshold a few bars later doesn't lose the signal
- New: a confirmed opposite-direction Trigger now resets the other side's Trigger state machine instead of leaving a stale Broken/Confirmed state to linger
- New: T1 searches recent confirmed-pivot history (`maxPivotHistoryInput`, default 20) for the nearest qualifying level instead of only ever checking `lastHigh`/`lastLow`; tracks and displays whether it used a real pivot or the ATR fallback
- New: Continuation/Reversal dominance is sticky (`scenarioHysteresisMarginInput`, default 10) instead of flipping every bar the two scores cross, so T2/Invalidation geometry doesn't flicker
- New: HTF influence on Reversal is now asymmetric (`reversalHtfAlignedFactorInput`/`reversalHtfConflictFactorInput`) — conflict with the HTF trend costs a Reversal thesis more than alignment helps it, applied per-scenario before the `max()` combination

## v3.3.0 — 2026-07-30
- Fix: v3.2's leg-significance gate had a bootstrap deadlock — `swingOriginPrice` starts `na`, so the retracement check (`na > EPS`) was always false and the reference leg could never initialize. The check is now skipped (accepted unconditionally) until a first leg exists
- Fix: the counter-move extreme trackers (`lowSinceLastHigh`/`highSinceLastLow`/`lowSinceLastLow`/`highSinceLastHigh`) reset on the raw pivot event even when that pivot was rejected by the significance filter, silently understating the true counter-move depth — they now reset only on an accepted endpoint update
- Fix: T2 could only ever be hit on the exact same bar as T1 — the trade-open lifecycle closed on T1 alone even when T2 tracking was enabled. The trade now stays open until T2 (if enabled), not T1; the "only fire once" guard on the T1-hit event is now explicit instead of relying on that side effect
- Fix: the CRV feasibility factor (and so the displayed Score) kept using the live, still-moving target/invalidation after a trigger had already frozen the actually-tracked ones, so Score and the tracked trade could drift apart — CRV now switches to the frozen values once a trade is open; Trigger arbitration uses a pre-CRV score to avoid a circular dependency
- Renamed `completedLeg*` → `referenceLeg*` for clarity (it always described the newly-active reference leg, never a retired one — the old name implied the opposite)
- Reviewed and did not change two further claims from the same review (numerator/denominator leg-quality mismatch, accumulator "mixing") after tracing them against the actual code with concrete examples — see README "Reviewed and not changed"

## v3.2.0 — 2026-07-30
- Fix: a small opposite-type pivot (e.g. a minor Higher Low inside an uptrend) could still hijack the reference leg away from the larger trend it was actually just a pullback within — v3.1's alternating swing only fixed same-type overwrites, not this. A new pivot now only flips the reference leg if it retraces at least `minLegRetracementInput` (new input, default 0.25) of the current leg's own range; a shallow one is ignored for reference-leg purposes and the leg keeps extending through it
- Found via a live NatGas chart: DPE3 showed a persistent Short reading through a multi-day uptrend, traced back to minor Higher-Low pivots repeatedly flipping the reference leg to tiny bearish corrections

## v3.1.0 — 2026-07-30
- Fix: reference leg now comes from an explicitly alternating confirmed swing (`swingOrigin`/`swingEndpoint`/`referenceEpoch`) instead of two independently-tracked "last high"/"last low" values — a same-type pivot only extends the current endpoint, only an opposite-type pivot confirms a new leg
- Fix: leg-quality accumulator now resets only on a genuine new leg (not every pivot) and is anchored to the true pivot price/bar; documented residual imprecision (path sum still starts at the origin's confirmation bar, not its true bar — deliberately not solved with a series-length `math.sum` or ring buffer, see file comment)
- Fix: rejection-at-extreme now confirms against the rejection candle's opposite extreme (its high, for a bullish rejection) instead of its own low, which was trivially satisfied on the next bar
- Fix: a Trigger can only fire while its direction's Readiness clears the threshold and dominates the other side (previously could fire independent of Readiness entirely)
- Fix: Trigger state resets if the reference leg changes underneath it (`referenceEpoch` mismatch), so a stale Broken/Confirmed state from a superseded leg can no longer complete
- Fix: an explicit trade-open lifecycle now gates all T1/T2/Invalidation hit detection, so a cancelled or already-closed setup can no longer report further hits
- Fix: simultaneous same-bar Long/Short trigger candidates are arbitrated by raw score instead of both firing and immediately cancelling each other
- Fix: micro-swing break is now a crossover/crossunder event, not a persisting level condition
- Fix: HTF trend strength now normalizes by the HTF's own confirmed ATR instead of the chart timeframe's
- Fix: Continuation and Reversal now combine via `max()` (competing explanations of the same retracement) instead of noisy-OR (independent evidence); the dominant scenario now selects which counter-move range feeds T2/Invalidation instead of one formula serving both
- New alerts: Long/Short Signal (Trigger + Score threshold, replaces the previously visual-only threshold)
- Minor: `divergenceDecayBars` no longer leaks the unused `customPivotLen` outside the Custom preset; Target/Invalidation lines dim to gray once a setup closes (hit/invalidated/cancelled); clarified the "freeze scores" input label

## v3.0.0 — 2026-07-30
- Ground-up restructure (new file, `directional_probability_engine_v3.pine`, v1/v2 kept as superseded predecessors): unified Continuation and Reversal as two bell curves on the same retracement ratio against the same reference leg, instead of only modeling continuation
- Leg-scoped accumulators replace the rolling `structureLen` window — efficiency/overlap freeze at each confirmed pivot so the reference leg and its quality score always refer to the same leg
- Maturity gained a time dimension (counter-move duration vs. the reference leg's own duration) alongside the existing price bell curve
- Exhaustion redefined as deterioration (recent-bars efficiency vs. the counter-move's own running average) instead of a static choppiness snapshot
- Trigger rebuilt as an explicit state machine (UNTRIGGERED → BROKEN → CONFIRMED → ACCEPTED) with a new same-bar rejection-at-extreme ingredient (genuinely leading) alongside the existing micro-swing break (relabeled as a faster-confirming, not leading, sensor); Acceptance now derives from the same state instead of a non-consecutive rolling count
- Readiness combination changed from a weighted average to a floored-multiplicative gate across reference-leg quality, Maturity and Exhaustion, combined across Continuation/Reversal via a noisy-OR
- Target model: T1 validated against a minimum ATR distance with a synthetic fallback; new CRV (reward:risk) feasibility factor gates the Score; same-bar Target/Invalidation ambiguity resolves conservatively (invalidation checked first); a fresh opposite-direction trigger now cancels the other side's open setup
- New alerts: per-side Cancelled

## v2.0.0 — 2026-07-30
- Ground-up architecture rebuild (new file, `directional_probability_engine_v2.pine`, v1 kept as predecessor): replaced the flat Structure+Location+Response weighted average with a Readiness/Confirmation split
- Context (Trend, classification only), Correction Maturity (Location, bell-curve retracement of the counter-move), Exhaustion (Momentum, is the counter-move losing steam), and a new Trigger role (fast micro-swing structure-shift + candle strength, independent shorter pivot length)
- Readiness = weighted(Context, Maturity, Exhaustion); Confirmation = weighted(Trigger, Acceptance); Score = Readiness × floor-adjusted Confirmation factor
- Target/Invalidation levels (T1 structural swing, optional T2 extension, ATR-buffered invalidation) frozen at each confirmed Trigger and drawn on the price chart via `force_overlay`
- Display kept to the color-coded histogram only (light = Readiness, solid = confirmed Score) — no table in the oscillator pane; per-role scores moved to the data window instead
- New alert set: Setup, Trigger, T1/T2 hit, Invalidation hit — per side

## v1.0.0 — 2026-07-30
- Initial release: Structure + Fibonacci Location + Momentum & Response, independent Long/Short 0–100 scores, Independent/Relative score modes, timeframe-adaptive presets, optional confirmed HTF context, mirrored histogram/line/balance display modes, regime alerts and regular/hidden divergence alerts
