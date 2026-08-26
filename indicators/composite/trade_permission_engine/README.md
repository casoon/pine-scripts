# Trade Permission Engine

The successor to `directional_probability_engine` (archived, see
`archive/indicators/directional_probability_engine/`). It answers *"does the market currently
permit trading Long or Short here"*, not *"how probable is this specific setup"* — a reframing
prompted by a live-chart review where a sharp, fresh breakout produced almost no reaction (correctly
diagnosed as inherent pivot-confirmation lag on the reference leg, not a bug: the leg genuinely
hadn't been confirmed yet). Permission carries that same architectural lag; the point of this
version is to stop presenting a stale-but-still-high reading as if it were still earned, and to keep
tracking whether the *current* impulse is still healthy rather than only how good it looked when it
formed.

It keeps the full v3.5 architecture from Directional Probability Engine unchanged (alternating
confirmed swing as the reference leg, unified Continuation/Reversal Maturity on one retracement
ratio, separated impulse-vs-counter-move Exhaustion, a Trigger state machine, scenario-aware
Target/Invalidation) and adds two mechanisms aimed specifically at the permission framing.

## The key idea

Continuation and Reversal are two readings of the *same* retracement ratio against the same
reference leg, not two separate detectors:

- `referenceLeg` = the most recently **confirmed** leg from an explicitly *alternating* swing
  structure (`swingOrigin` → `swingEndpoint`, tagged with a `referenceEpoch`) — a same-type pivot
  only extends the current endpoint on a genuine new extreme; an opposite-type pivot only confirms
  a genuinely new leg once price has retraced (near-)fully back to the leg's own origin
  (`legInvalidationRetracementInput`, default 0.90).
- `r` = the counter-move's retracement ratio against `referenceLeg`'s range.
- **Continuation Maturity** = a bell curve on `r` centered near a typical pullback depth
  (~0.382–0.618) → bet `referenceLeg`'s direction resumes.
- **Reversal Maturity** = the larger of a structural-failure bell curve (near a full round-trip,
  ~1.272) and an endpoint reading of `referenceLeg`'s own overextension → bet `referenceLeg` is
  invalidated and a fresh opposite leg is starting.
- A bullish `referenceLeg` feeds **Long Continuation** *and* **Short Reversal**; a bearish one
  feeds the mirror pair. Only one `referenceLeg` type is active at a time.

## Features

- **Live Trend Quality** — a second, continuously-updated quality read alongside the quality frozen
  the instant the reference leg formed. Answers "is this impulse *still* healthy", not just "was it
  good when it formed": a recency-weighted average of the last `maxLegHistoryInput` completed legs'
  efficiency (more recent legs weighted higher), adjusted by whether that efficiency and the legs'
  ATR-normalized range are trending up or down across the tracked history. Fed into all four
  Permission formulas as an additional gated factor (`liveTrendQualityFloorInput` floor) alongside
  the existing frozen reference-leg quality — a strong leg that formed cleanly three legs ago can no
  longer single-handedly carry a Permission reading if the trend has since gotten choppier.
- **Permission Decay** — Permission fades over bars with no new extreme, no accelerating momentum
  and no ATR expansion in the relevant direction, instead of sitting at a stale high value once the
  move that earned it has gone quiet. Each stale bar fades the final score by
  `decayPerBarInput` percent (default 0.5%/bar, 0 disables decay); the counter resets to zero on any
  bar that shows fresh progress. Decay is applied only to the final displayed/alerted score — not to
  the Permission value used for Trigger eligibility/arbitration — so a fading-but-still-open trade
  doesn't get its Trigger state machine perturbed by decay math.
- **Reference-leg quality** — efficiency + overlap of the leg accumulated bar-by-bar and frozen the
  instant a new pivot confirms.
- **Maturity** — price bell curve (Continuation *and* Reversal) × a time-maturity factor. Reversal
  uses its own, wider/later-centered duration curve.
- **Continuation/Reversal dominance is sticky** (hysteresis), resetting on a new reference leg.
- **Two distinct Exhaustion measures**: counter-move exhaustion (deterioration, feeds Continuation)
  and reference-impulse exhaustion (divergence at the leg's own endpoint, feeds Reversal) — most
  accurate right after the leg completes; it gets imprecise deep into the counter-move, since the
  divergence tracker may by then have moved on to a more recent, smaller pivot.
- **Trigger** — an explicit state machine (`UNTRIGGERED → BROKEN → CONFIRMED → ACCEPTED`) driven by
  either a same-bar rejection-at-extreme or a micro-swing structure break, armed for
  `triggerValidityBarsInput` bars, resetting on a stale reference leg or an opposite confirmed
  trigger, and gated so it can't fire while a same-direction trade is already open. Two price-chart
  markers (`force_overlay`, bounded rolling history like the Position Health markers below): a small
  `▵`/`▿` on `newLongSetup`/`newShortSetup` (a permission phase beginning), and a small `◇` when a
  side enters BROKEN (an attempt happened, without claiming it held - BROKEN reverts to
  `UNTRIGGERED` often enough in normal price action that it's marked as a discrete event, not a
  persisting state).
- **Confirmation** = weighted(Trigger state score, Acceptance).
- **Active Permission** = `Permission × confirmation factor × CRV feasibility factor × decay
  factor`. CRV targets T1 until T1 is hit, then switches to T2 if tracked.
- **Target / Invalidation**, frozen the instant a Trigger confirms, drawn on the price chart
  (`force_overlay`): T1 via a real recent-pivot search (falls back to an ATR projection only if none
  qualify), scenario-aware T2/Invalidation, same-bar ambiguity resolved conservatively
  (invalidation checked first), opposite-trigger cancellation.
- **Display** (no table, standing preference for this lineage): plain value curves - `longPermission`/
  `shortPermission` as a mirrored 0–100 line pair, `permissionThresholdInput` drawn as a reference
  line against it, and Position Health (only the side `healthDisplayModeInput` selects - see
  `## Position Health` below) as a second, `style_circles` curve so it stays visually distinct from
  the Permission line while sharing the axis. Entry gets a lean circle marker (`shape.circle`, not
  a directional triangle - a triangle's apex-vs-base asymmetry visibly sat off the curve at
  `location.absolute` even with a correctly-centered anchor) at the actual entry event
  (`newLongTrigger`/`newShortTrigger`, fires once) placed directly on the Permission curve, not a
  separate series. v1.2.0/v1.2.1 tried a "Decision Timeline" pane instead - three fixed-height
  lanes (Market/Entry/Health) where height carried no information, only lane/side/color transparency
  did, matching the engine's situation → entry → position sequence on paper. Real chart feedback
  after the state-lifecycle bugs in that version were fixed was clear: flat bands at a constant
  height aren't interpretable the way a moving curve is ("mit den Kurven konnte ich was anfangen,
  hiermit nicht") - reverted to curves in v1.3.0. Every other raw score (Active Permission, Live
  Trend Quality, the decay factors, etc.) is in the data window.
- **Alerts**: Setup, Trigger, Signal (Trigger + Permission threshold), T1/T2 hit, Invalidation hit,
  Cancelled — per side.

## Position Health (Long/Short)

A second, fully decoupled score answering a different question than Permission above: not "is a
new entry attractive here", but *"assuming I'm already Long (or Short), is that position still
structurally healthy — should I hold, protect, reduce or exit"*. It never reads CRV, Trigger state,
or the trade-lifecycle machinery (`t1LongFrozen` etc.) — computed and placed earlier in the script
than that machinery so the decoupling is enforced by file position, not just convention. Combined
as a weighted average, not a multiplicative floored gate: a single weak dimension (a choppy regime,
say) must not crash a hold decision the way a weak factor is intentionally allowed to crash a
new-entry Permission score.

Six components, per direction:

- **Live Quality** — blends the leg-boundary-gated Live Trend Quality with a new, genuinely
  continuous per-bar read (`liveLegQuality`, same efficiency/overlap formula as reference-leg
  quality but never reset mid-leg) — reacts within an in-progress pullback instead of only at the
  next confirmed leg.
- **Pullback Health** — reuses Continuation Maturity's depth/duration/exhaustion read, blended
  against a healthy-100 baseline scaled by how much correction is actually present, while the held
  direction's own leg is still the active reference. While the OPPOSITE leg is the active reference
  (`swingDirection` hasn't flipped back yet - which only happens at a conservative 90% retracement),
  this does NOT hard-zero - that would reintroduce the same pivot-confirmation lag TPE's own README
  already flags for Permission (a strong favorable move would read as "unhealthy" for many bars
  while clearly recovering, well before the formal leg-flip). Instead it reuses the already-computed
  Reversal Maturity read, which continuously scores "is the opposite leg being invalidated".
- **Trend Progress** — net directional movement over a configurable lookback, scaled by ATR;
  continuous, not a "break beyond the last confirmed swing point, then decay" pulse model - that
  model measured 0.0 on 90-98% of bars in backtested Pine Logs (a rare threshold event with a decay
  tail spends most of its time at the floor), which is unusable for a 20%-weight component.
- **Trend Fatigue** — shrinking recent leg size, exposed as its own score, but as a *relative*
  ratio rather than the *absolute* ATR-multiple difference Live Trend Quality's own formula uses
  internally (that one stays untouched) - the absolute version saturated its clamp on ~70% of bars
  in backtested Pine Logs given how much leg sizes vary. A first pass to a symmetric ratio clamp
  only dropped that to 61.5% - the ratio is naturally asymmetric (shrinking is bounded at -100%,
  growing is not; legs commonly more-than-double between regimes), so only the growth side is now
  compressed by a configurable factor before the final clamp.
- **Structure Intact** — a graded ramp toward the same 0.90 retracement threshold that governs
  whether the reference leg itself flips direction; an ordinary ≤62% pullback (e.g. a Wave-4-style
  correction) does not erode this the way a genuine structural break does. Same lag fix as Pullback
  Health: while the opposite leg is active, this reads a continuous recovery ratio (how much of that
  leg's range price has already recovered) scaled against the same 0.90 threshold, instead of a hard
  0 - the two branches meet at 100 exactly at the moment the leg would flip, so there's no cliff.
- **Regime/Sideways-Risk** — a Kaufman-style net-movement/path-length efficiency ratio, independent
  of leg structure.

Classified into four states via configurable thresholds: **HOLD** (68+), **PROTECT** (54–68),
**REDUCE** (36–54), **EXIT** (below 36) — PROTECT is the gap this closes: a state between "fine"
and "get out" that lets a healthy-but-cooling trend be managed (tighten stops, take partials)
without forcing an all-or-nothing decision. These are calibrated against 34,776 bars of backtested
Pine Logs, not round numbers - with all six components in their current form, the combined score
empirically tops out around 76 (Live Quality alone rarely exceeds ~75-85 in real, noisy price
action, since its underlying efficiency measure - net move / path length - is rarely close to 1.0;
this looks like a genuine property of real market data, not a formula defect). The original
85/65/40 thresholds made HOLD literally unreachable across the entire backtest.

Displayed as the pane's Position Health curve - a single `style_circles` series, not two.
`healthDisplayModeInput` (Auto/Long/Short/Off, default Auto) picks which side to show: Auto follows
whichever side has a TPE-tracked trade open (empty when neither does), Long/Short shows that side
unconditionally (e.g. to watch a manually-entered position TPE itself never triggered). Showing both
Long and Short Position Health at once answered a question nobody has ("what's the hypothetical
health of a position I'm not in"); only the side actually held matters. Hue still encodes side
(green = Long, red = Short, this file's existing convention); brightness encodes state on top of the
curve's own height - vivid/opaque at HOLD, fading toward gray-transparent toward EXIT. Sub-components
aren't individually plotted to the data window - this script's `plot()`/`alertcondition()` combined
were already close to Pine's 64-output cap before Position Health, so they're only exposed via
`longPositionHealth`/`shortPositionHealth`'s own value (both the pane curve and the data window). A
"Debug: log Position Health components" toggle (off by default) logs all six sub-components plus the
final score/state per bar via `log.info()` instead - this does not count against the same output cap,
so it's available for debugging without touching the plot budget; read it in TradingView's Pine Logs
panel. Only a PROTECT-entry alert is added per side — the state this feature actually closes a gap
on; HOLD/REDUCE/EXIT stay visible via the curve color instead of a dedicated alert, to stay within
the same output budget.

Further additions address transitions and early weakness across a wide chart, not just the
curve color at a single bar:

- **Position Health downgrade markers** — a small `●` text glyph (`label.style_none`, no
  background bubble - `label.style_circle` renders a fixed-size disc regardless of `size=`, too
  large on a busy chart), offset half an ATR from the wick so it doesn't sit on the candle, drawn
  on the price chart (`force_overlay`). Only marks downgrades that started from PROTECT or HOLD -
  a side that spends most of its time in REDUCE/EXIT (e.g. Short during a sustained uptrend)
  constantly flickers across that boundary, and marking every one of those is noise rather than a
  real "this was fine, now it's not" event. Colored by the side it concerns - green for long, red
  for short, this file's existing convention (Permission/Position Health curves) rather than a flat
  warning color - with brightness scaling by severity: a mild HOLD→PROTECT slip is faint, a drop
  into EXIT is much more visible. The hover `tooltip` is deliberately a single short action clause
  ("Short position weak - consider a smaller position") - earlier versions spelling out old/new
  state names plus scores plus a comparison to the other side ("was PROTECT (cooling, protect
  gains), now REDUCE (weakening, cut size), score 47.4 - for comparison Long is EXIT...") were
  still too dense to read at a glance. Bounded rolling history (30 per side, oldest deleted
  first), same pattern as the pivot-history arrays elsewhere in this file.
- **Position Health upgrade markers** — the mirror of the downgrade markers: a hollow `○` (vs.
  the downgrade markers' filled `●`) marking a rise INTO PROTECT or HOLD, same side-color and
  position convention. Deliberately the same PROTECT/HOLD-only filter as downgrades, applied
  symmetrically - a plain EXIT→REDUCE tick is the most obvious first example to want marked, but
  that's exactly the boundary where chronic flickering happens (see downgrade markers above), so
  it's deliberately excluded here too.
- **Divergence warning markers** — a filled `◆` glyph (same minimal style as the downgrade
  markers, distinct shape so the two aren't confused; full opacity - not scaled by
  regular-vs-hidden strength like an earlier version, and not the outline-only `◇`, which read as
  barely visible at `size.tiny`) reusing this file's existing divergence detection
  (`regularBearDiv`/`hiddenBearDiv`/`regularBullDiv`/`hiddenBullDiv`, already computed above for
  Permission's Exhaustion) rather than adding new detection logic. Gated to
  `newPivotHigh`/`newPivotLow` - the divergence booleans themselves stay true for every bar between
  one pivot confirmation and the next, not just the bar the divergence was actually confirmed on;
  without this gate, a single real divergence event produced a dense cluster of markers instead of
  one. Bearish divergence (price makes a new high, momentum doesn't confirm) is a classic leading
  warning for an existing Long - the rally may be losing steam before price itself turns; bullish
  divergence is the mirror warning for an existing Short. Deliberately **purely visual** - it does
  not feed the Position Health score, so the thresholds already calibrated against real backtested
  Pine Logs don't need re-tuning for it.

## Reviewed and not changed

Carried over from Directional Probability Engine v3.3/v3.5 (same accumulators, same reasoning,
traced twice against concrete numeric examples and reaffirmed both times — see the archived
`README.md`'s "Reviewed and not changed" section for the full trace): the leg-quality accumulator
correctly refers to the newly-active reference leg only, and the reference-leg/counter-move dual use
of one running accumulator is intentional, not a mixing bug.

## Deliberate scope cuts

Carried over from Directional Probability Engine v3.5 (unchanged, not revisited in this pass):
Endpoint and Structural Reversal share one Maturity→Readiness pipeline via `max()`; simultaneous
same-bar pivot-high-and-pivot-low arbitration is not implemented; no structural/internal-wave
maturity or trendline-break Trigger ingredient; scores stay rule-based 0–100 evidence, not
calibrated hit-rate probabilities.

New for this version, proposed alongside Live Trend Quality/Permission Decay but deliberately not
implemented in v1:

- **Opportunity Window** lifecycle staging (EARLY → BUILDING → ACTIVE → MATURE → LATE → EXHAUSTED
  modulating the score) — real value, but a distinct state-machine sub-system on top of an already
  large file.
- **Event-based-only score updates** (score only moves on structural events, not every bar) — a
  responsiveness/display-cadence tradeoff worth prototyping on its own, not bundled into this pass.
- **Explicit Trend Fatigue point-schedule** (e.g. HH1=+12/HH2=+10/HH3=+7/HH4=+4) — Position Health
  (v1.1.0) now exposes a Trend Fatigue score derived from Live Trend Quality's existing
  recency-weighted leg-range trend, but as a lighter continuous read, not the originally-floated
  explicit diminishing-schedule model.
- **Full multi-leg trend-development array** (explicit "are impulses lengthening/shortening,
  corrections deepening, volatility declining" breakdown) — Live Trend Quality uses a lighter
  recency-weighted history for the same purpose; a fully separate multi-dimensional breakdown is a
  further refinement, not in v1.

Position Health (v1.1.0) does not add per-timeframe-preset auto-tuning of its own weights/
thresholds (unlike `pivotLen`/`atrLen`/etc.), and does not add a dashboard table — consistent with
this file's standing no-table policy.

## Known limitation

Reference-leg quality's path-sum accumulator resets at each new confirmed leg, but only starts
accumulating from that leg's origin's *confirmation* bar, not the true bar itself — carried over
unchanged from Directional Probability Engine (same cost/benefit tradeoff: fixing it exactly would
need a retroactive series-length sum, an unverified compile risk in this codebase, or a fixed-size
ring buffer, deliberately not implemented).

## Repainting policy

- Confirmed structural pivots only become available after right-side confirmation (delayed by the
  pivot length). The Trigger role uses a separate, shorter micro-pivot length and a same-bar
  rejection-at-extreme ingredient specifically to reduce this lag for timing.
- Optional HTF context uses the previous confirmed HTF bar.
- The live chart bar can naturally fluctuate until it closes; enable "Freeze scores until chart bar
  closes" to suppress this.
