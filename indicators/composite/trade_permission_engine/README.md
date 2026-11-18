# Trade Permission Engine

**Role: signal generator with context.** A Trigger (rejection inside the pullback/reversal zone or
close beyond the last micro swing, on a confirmed bar) becomes a Long/Short signal when Permission
clears its threshold and dominates the other side, and Active Permission still retains
`signalRetentionInput` % of it. Continuation and Reversal signals are tagged and alerted separately.
Pivots are used as known reference levels (leg endpoints, targets); divergence is an optional
marker (off by default) and does not feed Permission.

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
  good when it formed": a recency-weighted average of the `maxLegHistoryInput` completed legs before
  the current reference leg (that one already enters as the frozen quality) — their
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
  and reference-impulse exhaustion (feeds Reversal): how far the oscillator has recovered from its
  recent extreme minus how far price has retraced the leg — momentum turning before price. No
  pivot divergence in either.
- **Permission** = geometric mean of its gated factors, so it stays on a real 0–100 scale:
  Continuation = reference-leg quality × maturity × counter-move exhaustion × HTF alignment
  (4th root); Reversal = maturity × impulse exhaustion × HTF alignment (cube root, no leg-quality
  factor — a clean impulse argues against reversing it). HTF alignment: 1 when aligned, the
  `HTF alignment floor` when against, halfway when neutral or no valid HTF. Default threshold 55.
- **Trigger** — an explicit state machine (`UNTRIGGERED → BROKEN → CONFIRMED → ACCEPTED`) driven by
  either a same-bar rejection-at-extreme or a micro-swing structure break, armed for
  `triggerValidityBarsInput` bars, resetting on a stale reference leg or an opposite confirmed
  trigger, and gated so it can't fire while a same-direction trade is already open. A rejection
  candle only counts while the matching side's Continuation or Reversal Maturity is at least
  `rejectionZoneMinInput` (price is inside the zone) - rejection candles are common on any bar.
- **Confirmation** = weighted(Trigger state score, Acceptance).
- **Active Permission** = `Permission × confirmation factor × CRV feasibility factor × decay
  factor`. CRV targets T1 until T1 is hit, then switches to T2 if tracked.
- **Target / Invalidation**, frozen the instant a Trigger confirms, drawn on the price chart
  (`force_overlay`): T1 via a real recent-pivot search (falls back to an ATR projection only if none
  qualify), scenario-aware T2/Invalidation, same-bar ambiguity resolved conservatively
  (invalidation checked first), opposite-trigger cancellation.
- **Display**: Permission as a mirrored 0–100 line pair with the threshold as reference line; one
  status line right of the last bar (leading side, scenario, the smallest gated factor limiting
  Permission, trigger state); one label per Trigger/Signal on price with side, scenario tag
  (`CONT`/`REV`), entry, invalidation and T1, plus the T1/T2/invalidation lines. Colour means
  direction only (green/red); warnings are orange. Position Health is a state line under (Long) or above (Short) the candles on the price
  chart while a tracked trade is open. Every other raw score is in the data window.
- **Signal log** (opt-in, `showSignalLogInput`, off by default): follows every Signal to its outcome
  and tabulates closed signals by Long/Short × Continuation/Reversal and by Permission band
  ([threshold, +10), [+10, +20), ≥ +20), each row with its sample size `n`. Won = T1 before
  invalidation (same bar: invalidation wins), lost = invalidation first, cancelled by an opposite
  trigger = not counted. R = from the signal bar's close to the invalidation level, exit at T1,
  minus the spread assumption (`spreadTicksInput`, in ticks). It is a measurement of the loaded
  chart history - rows with n < 30 say nothing about the signal. Ablation of single factors uses
  the existing inputs (decay per bar 0, factor floors 1.0) and reads the effect from this table.
- **Alerts**: Setup (permission above threshold), Trigger, Long/Short **Continuation** Signal and
  Long/Short **Reversal** Signal (Trigger whose Active Permission still holds ≥
  `signalRetentionInput` % of its Permission), T1/T2 hit, Invalidation hit, Cancelled — per side.

## Position Health (Long/Short)

A second, fully decoupled score answering a different question than Permission above: not "is a
new entry attractive here", but *"assuming I'm already Long (or Short), is that position still
structurally healthy — should I hold, protect, reduce or exit"*. It never reads CRV, Trigger state,
or the trade-lifecycle machinery (`t1LongFrozen` etc.) — computed and placed earlier in the script
than that machinery so the decoupling is enforced by file position, not just convention. Combined
as a weighted average, not a multiplicative floored gate: a single weak dimension (a choppy regime,
say) must not crash a hold decision the way a weak factor is intentionally allowed to crash a
new-entry Permission score.

Five components, per direction (one trend-efficiency read — Live Quality — rather than a second Kaufman efficiency ratio on top):

- **Live Quality** — blends the leg-boundary-gated Live Trend Quality with a genuinely
  continuous per-bar read of the counter-move since the current endpoint (`liveLegQuality`, same
  efficiency/overlap formula as reference-leg quality, measured from the endpoint's pivot bar) —
  reacts within an in-progress pullback instead of only at the next confirmed leg. A clean
  counter-move lowers the held direction's health, a choppy one keeps it up.
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

Classified into four states via configurable thresholds: **HOLD** (68+), **PROTECT** (54–68),
**REDUCE** (36–54), **EXIT** (below 36) — PROTECT is the gap this closes: a state between "fine"
and "get out" that lets a healthy-but-cooling trend be managed (tighten stops, take partials)
without forcing an all-or-nothing decision. These are calibrated against 34,776 bars of backtested
Pine Logs, not round numbers - with the components in their former six-part form, the combined score
empirically tops out around 76 (Live Quality alone rarely exceeds ~75-85 in real, noisy price
action, since its underlying efficiency measure - net move / path length - is rarely close to 1.0;
this looks like a genuine property of real market data, not a formula defect). The original
85/65/40 thresholds made HOLD literally unreachable across the entire backtest.

Displayed as a state line on the price chart (`plot`, `force_overlay`) - under the candles for
Long, above them for Short - for the side `healthDisplayModeInput` selects: Auto follows whichever
side has a TPE-tracked trade open (nothing when neither does), Long/Short shows that side
unconditionally, Off hides it. The line follows the rolling 20-bar low/high (so it stays near
horizontal) and changes colour with the state: gray HOLD, yellow PROTECT, orange REDUCE, dark
orange EXIT; green/red are reserved for direction. The score of both sides is in the data window.
When a tracked trade's state drops out of PROTECT/HOLD, one orange `Health <state>` label marks it
(bounded history, 30 per side).

**What the bands are.** HOLD/PROTECT/REDUCE/EXIT are a state indicator: the band edges follow how
often the score takes these values on earlier chart logs, not how positions performed afterwards,
so they carry no exit instruction. Testing them against "hold until invalidation/T2" is open.
Sub-components are not plotted individually (output cap); a "Debug: log Position Health components"
toggle logs them via `log.info()`. Only a PROTECT-entry alert exists per side.

**Divergence markers** (`showDivergenceMarkersInput`, off by default): an orange `◆` at the
confirmed pivot where regular/hidden divergence is found - above the high for bearish, below the
low for bullish. They arrive late and feed nothing else.

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
