# Directional Probability Engine

Three versions coexist in this directory. **v3** is the current architecture and the one to use;
v1 and v2 are kept as superseded predecessors (see below).

## v3 — Reversal + Continuation Unification (current)

v3 answers: *"what's the most likely next directional leg from here — a continuation of the
current trend, or a reversal of it — and what target can it reach before invalidation?"* v2 only
modeled continuation (a pullback inside an established trend ending and the trend resuming); v3
adds genuine reversal scenarios without duplicating the whole pipeline four times.

### The key idea

Continuation and Reversal are two readings of the *same* retracement ratio against the same
reference leg, not two separate detectors:

- `referenceLeg` = the most recently **confirmed** leg from an explicitly *alternating* swing
  structure (`swingOrigin` → `swingEndpoint`, tagged with a `referenceEpoch`) — a same-type pivot
  only extends the current endpoint (and only if it's an actual new extreme, not just any pivot of
  the same type); an opposite-type pivot only confirms a genuinely new leg once price has retraced
  (near-)fully back to the leg's own origin (`legInvalidationRetracementInput`, default 0.90). An
  ordinary pullback into the Continuation zone (~0.38–0.62) must *not* replace the leg it's a
  pullback within — the counter-move can contain its own internal pivots without ever becoming the
  new reference. `counterMove` = price action since that leg's endpoint (still forming), which by
  construction runs against `referenceLeg`'s direction.
- `r` = the counter-move's retracement ratio against `referenceLeg`'s range.
- **Continuation Maturity** = a bell curve on `r` centered near a typical pullback depth
  (~0.382–0.618, adapting to how clean `referenceLeg` was) → bet `referenceLeg`'s direction
  resumes.
- **Reversal Maturity** = the larger of two readings on the exact same `r`: a *structural-failure*
  bell curve centered near a full round-trip (~1.272, a late signal — most of the reversal move has
  typically already happened by the time it fires) and an *endpoint* reading that scores
  `referenceLeg`'s own overextension (ATR-relative) independent of how much it has retraced yet, so
  a reversal can score right at the impulse's own top. Either way → bet `referenceLeg` is
  invalidated and a fresh opposite leg is starting.
- A bullish `referenceLeg` feeds **Long Continuation** *and* **Short Reversal**. A bearish
  `referenceLeg` feeds **Short Continuation** *and* **Long Reversal**. Only one `referenceLeg`
  type is active at a time, so exactly one continuation/reversal pair is live per bar.
- Exhaustion (of the counter-move) and Trigger/Confirmation (has price actually turned) are
  direction-specific but shared between Continuation and Reversal — not duplicated per scenario.

### Features

- **Reference-leg quality** — efficiency + overlap of the leg accumulated bar-by-bar and frozen
  the instant a new pivot confirms, so the quality score always refers to the *same* leg the
  retracement is measured against (v2 mixed this with a generic rolling window)
- **Maturity** — price bell curve (Continuation *and* Reversal, see above) × a time-maturity
  factor (counter-move duration relative to the reference leg's own duration — too fast or too
  slow both score lower). Reversal uses its own, wider/later-centered duration curve (a structural
  failure is typically a bigger, slower move than a Continuation pullback)
- **Continuation/Reversal dominance is sticky** — the two only swap which one drives Readiness
  once one leads by a margin (hysteresis), so the Target/Invalidation geometry (which depends on
  which scenario is dominant) doesn't flicker when the two scores are close; the hysteresis resets
  on a new reference leg instead of carrying the old leg's dominant scenario into a brand new one
- **Two distinct Exhaustion measures**, not one reused for everything:
  - **Counter-move exhaustion** — *deterioration*: recent-bars efficiency vs. the counter-move's
    own running average, not a static choppiness snapshot — feeds Continuation (a counter-move
    running out of steam is evidence the original leg resumes)
  - **Reference-impulse exhaustion** — divergence at the leg's own endpoint pivot — feeds
    Reversal instead (Reversal needs the *original impulse* to be exhausted, not the counter-move;
    a strong, undeteriorating counter-move is what a reversal thesis actually wants)
- **Endpoint Reversal's overextension** (how many ATRs the reference leg spans) uses ATR frozen at
  the moment the leg's endpoint was last set, not live ATR during the correction that follows — so
  later volatility can't re-rate an already-completed leg's overextension after the fact
- **Trigger** — an explicit state machine (`UNTRIGGERED → BROKEN → CONFIRMED → ACCEPTED`) driven
  by either a same-bar **rejection-at-extreme** (a marginal new extreme that closes back
  in-range — genuinely leading, fires before any pivot confirms) or a micro-swing structure break
  (faster-confirming, still lags `microPivotLen` bars — labeled honestly as such, not as leading)
- **Readiness** = a *floored-multiplicative gate* — `∏(floor + (1−floor)×factor/100)` over
  reference-leg quality, Maturity and Exhaustion. A strong reference leg can no longer
  single-handedly carry a score when Maturity is genuinely zero (the per-factor floor keeps this
  from becoming a brittle AND-chain — see this project's own Gate A/B/C lessons in
  `.claude/CLAUDE.md`). Continuation and Reversal are *competing* explanations of the same
  retracement, not independent evidence, so they combine via `max()`, not noisy-OR — the dominant
  scenario is tracked and used to select scenario-specific T2/Invalidation ranges below. Optional
  confirmed HTF EMA context nudges each scenario *before* that combination, and asymmetrically for
  Reversal: fighting the HTF trend costs a Reversal thesis more than agreeing with it helps,
  since the HTF direction is itself evidence for Continuation and against Reversal
- A Trigger can only fire while its own direction's Readiness actually clears the threshold and
  dominates the other side, doesn't fire while a same-direction trade is already open (it would
  otherwise silently replace the open trade's frozen Target/Invalidation), and resets if the
  reference leg changes underneath it (a Broken/Confirmed state from a superseded leg can't
  complete). Once CONFIRMED, it stays *armed* for `triggerValidityBarsInput` bars — Readiness
  clearing its threshold a few bars later (not the exact same bar) still fires the signal instead
  of losing it — and fires at most once per episode. If it never fires within that window it
  expires back to UNTRIGGERED instead of indefinitely showing a confirmed score with no way left
  to signal. A confirmed Trigger also resets the *opposite* side's Trigger state machine, instead
  of leaving a stale Broken/Confirmed state on the other side to linger
- **Confirmation** = weighted(Trigger state score, Acceptance) — both come from the *same* state
  machine, so they can't disagree the way two independently-computed formulas could
- **Score** = `Readiness × confirmation factor × CRV feasibility factor`. CRV targets T1 until T1
  is hit, then switches to T2 (if tracked) — staying pinned to an already-passed T1 would crush the
  score right when the trade is actually doing well
- **Target / Invalidation**, frozen the instant a Trigger confirms, drawn on the price chart
  (`force_overlay`):
  - **T1** — searches a rolling history of recent confirmed pivots (both types) for the *nearest*
    one that clears a minimum ATR distance from price, instead of only ever checking the single
    most recent swing high/low; falls back to a synthetic ATR projection only if none qualify.
    Whether it used a real pivot or the fallback is tracked and shown on the Trigger label
  - **T2** (optional) and **Invalidation** are *scenario-aware*: Continuation uses the extreme
    reached since the current endpoint; Reversal uses the counter-move's own bounce range and any
    retest depth since that same endpoint — these are different legs of the structure and don't
    share one formula. T2 is discarded (not frozen) unless it actually lies beyond T1 by the
    minimum distance, and a trade only stays open past T1 waiting for T2 if T2 froze as a valid
    level in the first place
  - Same-bar Target/Invalidation ambiguity resolves conservatively: invalidation is checked
    first; both cannot register on the same bar
  - A fresh opposite-direction trigger cancels the other side's still-open setup, and its
    Target/Invalidation lines dim to gray once the setup closes (hit, invalidated or cancelled)
  - Simultaneous same-bar Long/Short trigger candidates are arbitrated by raw score rather than
    both firing and immediately cancelling each other
- No table in the oscillator pane — color-coded histogram only (light = Readiness, solid =
  confirmed Score); every per-role score is in the data window for debugging
- Alerts: Setup, Trigger, **Signal** (Trigger + Score threshold), T1/T2 hit, Invalidation hit,
  Cancelled — per side
- T2 tracking keeps a trade open until T2 (not T1) closes it, and CRV/Score switch from live to
  frozen target geometry once a trade is open, so the displayed Score always matches what's
  actually being tracked (see CHANGELOG v3.3.0)

### Reviewed and not changed

Two claims from the v3.3 review were traced against the actual code with concrete numeric
examples and did not hold up — noted here rather than silently dropped:

- **"Leg quality uses the new leg's distance but the old leg's path sum"** — traced with concrete
  pivot values: the path accumulator resets at the same event that overwrites
  `swingOrigin`/`swingEnd`, so by the time a leg's efficiency is computed, the accumulator has
  been running exactly since *that* leg's origin was set, not since some earlier leg. Numerator
  and denominator refer to the same leg. The variable name (`completedLegEfficiency`, now renamed
  `referenceLegEfficiency`) likely caused the reading — it never described a *retired* leg, always
  the newly-active reference leg, which is what feeds the forward-looking Fibonacci-center and
  Readiness gate correctly.
- **"Reference-leg and counter-move accumulators are dangerously mixed"** — the same running
  accumulator legitimately serves two purposes at two different times: read live (before the next
  pivot), it's the counter-move's own progress (feeds Exhaustion); frozen at the next pivot, it
  becomes that finished leg's quality (feeds the next leg's Fibonacci center). This is by
  construction, not a mixing bug — the counter-move *is* the candidate for the next reference leg.
  Raised again in the v3.5 review with the same reasoning (no new concrete counter-example) —
  reaffirmed after a second trace; still stands.

### Deliberate scope cuts (v3.5)

- **Endpoint and Structural Reversal share one Maturity→Readiness pipeline** (combined via
  `max()`) rather than being two fully independent scenarios with their own tuned formulas end to
  end. They now at least use the correct exhaustion (impulse, not counter-move) and their own
  Maturity curves — a full split (e.g. Structural Reversal using counter-move *strength* instead
  of impulse exhaustion, since a genuine structural failure is characterized by the new move
  accepting new extremes efficiently, not by the old impulse merely fading) is a further
  refinement, not implemented here.
- **Simultaneous same-bar pivot-high-and-pivot-low arbitration** — rare (needs specific
  intrabar structure `ta.pivothigh`/`ta.pivotlow` can't distinguish without lower-timeframe data)
  and not implemented; the two `if` blocks run in a fixed order (high before low).

### Deliberate scope cuts

- **Structural/internal-wave maturity** (ABC-sequence detection, internal swing count) — real
  value, but a distinct sub-system; price+time maturity is the load-bearing fix here.
- **Trendline-break as a Trigger ingredient** — needs a line-fitting subsystem disproportionate to
  the fix; rejection-at-extreme covers the "same-bar leading signal" gap at much lower cost.
- **Calibrated hit-rate probabilities** — same caveat as v1/v2: these stay rule-based 0–100
  evidence scores. A separate outcome/backtest model would be required to turn a score into an
  empirical hit rate.

### Known limitation

Reference-leg quality's path-sum accumulator resets at each new confirmed leg, but only starts
accumulating from that leg's origin's *confirmation* bar (`pivotLen` bars after the origin's true
bar), not the true bar itself — so each leg's measured efficiency is biased slightly high (the
denominator undercounts by up to `pivotLen` bars). Fixing this exactly would need either a
retroactive sum over a series-length window (an unverified compile risk in this codebase) or a
fixed-size ring buffer of recent bar deltas — deliberately not implemented, same cost/benefit
category as the confirmation-lag caveats already disclosed above.

## v2 — Transition Engine (superseded)

v2 introduced the Readiness/Confirmation split but only modeled continuation (no reversal
scenarios), used a rolling-window efficiency/overlap measure that could mix multiple legs, scored
Exhaustion as static choppiness rather than deterioration, combined Readiness as a weighted
average (letting a strong Context partially compensate for a correction that hadn't started), and
froze targets without validating they were still ahead of price. See
`directional_probability_engine_v2.pine` — kept for reference, not recommended for new use.

## v1 — Trend/Momentum Score (predecessor)

v1 scores three components (Structure, Fibonacci Location, Momentum & Response) directly into
independent Long/Short 0–100 scores. It is an honest trend + pullback-quality + momentum
confirmation reading — useful as a "how clean is the current move" gauge — but not a leading
indicator: all three components are derived from recent price action, so the composite tracks
price almost 1:1. See `directional_probability_engine_v1.pine` and its version history in
`CHANGELOG.md`.

## Repainting policy (all versions)

- Confirmed structural pivots only become available after right-side confirmation (delayed by the
  pivot length). v2/v3's Trigger role uses a separate, shorter micro-pivot length — and, in v3,
  a same-bar rejection-at-extreme ingredient — specifically to reduce this lag for timing.
- Optional HTF context uses the previous confirmed HTF bar.
- The live chart bar can naturally fluctuate until it closes; enable "Freeze scores until chart
  bar closes" to suppress this.
