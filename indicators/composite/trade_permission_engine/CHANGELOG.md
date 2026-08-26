# Changelog

## v1.3.0 — 2026-08-20
- Reverted the v1.2.0 "Decision Timeline" (three fixed-height lanes, height carries no information)
  back to plain value curves - real chart feedback, after the state-lifecycle bugs in that version
  were fixed (see v1.2.1), was blunt: "mit den Kurven konnte ich was anfangen, hiermit nicht" ("I
  could work with the curves, not with this"). The lane concept matched the engine's actual
  situation → entry → position sequence on paper, but flat bands at a constant height turned out not
  to be interpretable the way a moving curve is - no amount of debugging the underlying state logic
  fixes a wrong visualization idea. `longPermission`/`shortPermission` are now a plain mirrored
  0–100 line pair (no display stretch, no debounce - a continuous value has nothing to flicker the
  way a boolean-gated flat line did), with `permissionThresholdInput` drawn as a reference line.
  Position Health is a second `style_circles` curve, still gated to one side via
  `healthDisplayModeInput` (kept from v1.2.0 - showing both sides at once was still the wrong idea,
  independent of the lane-vs-curve question). Entry is now a lean marker
  (`newLongTrigger`/`newShortTrigger`, fires once) placed directly on the Permission curve, not a
  separate series with its own display-duration window.
- Removed `laneStabilityBarsInput` and `entryDisplayBarsInput` - both existed only to manage the
  lane display's on/off flicker and duration, which curves don't have.
- Dropped the now-redundant `longPermission`/`shortPermission`/`longPositionHealth`/
  `shortPositionHealth` data-window-only diagnostics - the pane curves above already carry their
  values into the data window automatically, so a second copy under a "Diagnostic:" label was the
  same number twice. `longScore`/`shortScore` (Active Permission, which has no pane plot of its own)
  stay.
- The entry marker started as `shape.triangleup`/`shape.triangledown` - a real chart showed them
  visibly off the Permission curve ("die Position der Pfeile ist nicht gut") even though
  `location.absolute` centers a shape's anchor exactly on the given value. Root cause: a triangle
  is asymmetric (apex at one end, wide base at the other), so its visual weight reads as offset from
  its true anchor point even when correctly centered. Switched to `shape.circle`, which is
  symmetric and sits cleanly on the curve.

## v1.2.0 — 2026-08-19
- Reworked the pane display from a multi-line oscillator into a "Decision Timeline": three
  fixed-height lanes (**Market** = Permission/Continuation-Reversal, **Entry** = Trigger state
  Watch/Broken/Confirmed/Accepted, **Health** = Position Health Hold/Protect/Reduce/Exit) instead
  of a shared 0-100-ish axis. The old display packed several different semantic levels onto one
  axis — a raw 0-100 Permission score, a further-chained Active Permission score, a state-classified
  Position Health score, and their derivatives (velocity, balance) — so the pane read as a pile of
  scores instead of the sequence of decisions the engine actually reasons through (is there a
  situation → has it become an entry → if I'm in it, is it still healthy). Lane height now carries
  no information by itself; only which lane, which side (color) and color transparency
  (strength/state — a Reversal reading additionally fades further than an equally strong
  Continuation one on the Market lane) do — matching how the engine actually works instead of how
  an oscillator conventionally looks.
- Removed the Permission histogram (light/solid columns), the duplicate Permission line, both
  Velocity lines, the Directional Balance line, the six Position Health threshold reference lines,
  and both backgrounds (Permission confidence band, Position Health deterioration warning) — all
  superseded by the lane display above. Removed their now-dead inputs: `highlightRegimesInput`,
  `permissionDisplayStretchInput`, `extensionShadingInput`, `showPositionHealthBackgroundInput`.
  Permission's fade-in-by-strength behavior is kept but now driven directly by the raw Permission
  value (via a new `permissionThresholdInput`-anchored transparency curve) instead of the old
  ATR-move-extension proxy, which answered "how far has price run", not "how permitted is this".
- Position Health's pane display no longer shows Long and Short simultaneously — replaced
  `showPositionHealthInput` with `healthDisplayModeInput` (Auto/Long/Short/Off, default Auto). Auto
  shows only whichever side currently has a TPE-tracked trade open (the Health lane is empty when
  neither does); Long/Short is a manual override to watch a position TPE itself never triggered.
  Showing both sides at once answered a question nobody has ("what's the hypothetical health of a
  position I'm not in"). The price-chart downgrade/upgrade/divergence markers are unaffected by
  which side the lane shows — only by the master Off switch.
- Added a small price-chart marker (`▵`/`▿`) on `newLongSetup`/`newShortSetup` - a permission phase
  beginning is now visible directly on price, not only as a lane color change or an alert.
- Every raw score the old display plotted directly (Permission, Active Permission, Position Health)
  is now in the data window instead, since the new lanes deliberately don't encode magnitude as
  height.
- First pass at the lane display used a separate plot per side per scenario (Continuation/Reversal
  as line vs. dots) and a separate Watch-state dot alongside the Armed-state line — hit `RE10140`
  ("script creates too many plots (65)") on compile. Collapsed both lanes to one plot per side:
  Market's Continuation/Reversal distinction and Entry's Watch/Broken/Confirmed/Accepted distinction
  both now read through color transparency alone (already the mechanism used for strength/state
  elsewhere in this display), not a second plot. Also dropped 5 data-window diagnostics that had
  become redundant with the new lanes or with other diagnostics already there (`longStaleBars`/
  `shortStaleBars` - `longDecayFactor`/`shortDecayFactor` already carry the same information as an
  actual factor; `referenceEpoch` - internal bookkeeping; the dominant-scenario 1/0 flags - the
  Market lane's saturation now shows this) to make room for the 6 new raw-value diagnostics with
  margin to spare.

## v1.2.1 — 2026-08-19
- Fixed the Market/Entry lanes reading as scattered dashes instead of coherent bands on a real
  chart (user report: "nicht brauchbar") - `longSetup`/`shortSetup` toggle on the raw
  `longPermission > shortPermission` comparison, which crosses narrowly and often, so plotting them
  directly turned every brief single-bar cross into a visible gap. Added `laneStabilityBarsInput`
  (default 3, new "Lane stability (bars)" input) - a display-only debounce (`longSetupDisplay`/
  `shortSetupDisplay`) that keeps a lane showing for this many bars after its side last actually
  dominated, bridging brief flips. Purely a display smoothing layer: `longSetup`/`shortSetup`
  themselves, and everything downstream of them (alerts, Trigger eligibility, `newLongTrigger`/
  `newShortTrigger` arbitration), are untouched.
- The debounce fix above wasn't enough - a follow-up real chart report ("die vielen roten Punkte auf
  einer Linie... noch schlechter als die zu Beginn") showed the Entry lane specifically was still
  unreadable, for a different reason than the Market lane's flicker: WATCH and BROKEN were folded
  into the same alpha-ramped line as CONFIRMED/ACCEPTED. WATCH (Trigger state 0, permission
  qualifies) is exactly `longSetupDisplay`/`shortSetupDisplay` - the same condition the Market lane
  already draws, so a second, fainter copy of it on the Entry lane added no information, just a
  permanent pale baseline. BROKEN (state 1) reverts to `UNTRIGGERED` within a bar or two often
  enough in normal price action that drawing it as part of a continuous line made every attempt look
  like an isolated dot on an otherwise-uniform thick band. Fixed by removing WATCH from the Entry
  lane entirely and moving BROKEN out of the continuous plot into a small discrete `◇` price-chart
  marker (same bounded-history-array pattern as the Setup markers) - the Entry lane itself now only
  draws a band from CONFIRMED onward, a real held trigger instead of every attempt.
- Still not fixed - a third real chart report showed the Entry lane still reading as scattered dots,
  now on BOTH sides simultaneously, most of the visible chart. Root cause: `longTriggerState`/
  `shortTriggerState` reverting from CONFIRMED to UNTRIGGERED the moment `close` crosses back over
  `breakLevel` is exactly the same kind of narrow, frequent flip the Market lane's debounce already
  fixes for `longSetup`/`shortSetup` - the Entry lane change above dropped WATCH/BROKEN correctly but
  never applied the same debounce to CONFIRMED/ACCEPTED itself. Fixed by extending
  `laneStabilityBarsInput` to the Entry lane too (`longConfirmedOffStreak`/`shortConfirmedOffStreak`,
  same pattern as `longSetupOffStreak`/`shortSetupOffStreak`) - `longTriggerState`/`shortTriggerState`
  themselves are untouched. Separately flagged, not fixed here since it's a signal-logic question, not
  a display one: both sides showing CONFIRMED near-simultaneously across most of the chart is likely a
  real property of this Trigger design on short timeframes, where `microPivotLen` can be as small as 2
  bars (Scalping/Intraday presets) - a micro-pivot that short reforms constantly, so "closed beyond
  the last micro-swing" stops being a meaningful discriminator. This was already true before the
  Decision Timeline rework; it was just never visible outside the data window before.
- Found the actual bug behind the last three fixes not helping (user diagnosis, confirmed against a
  real screenshot): the Entry lane was reading `longTriggerState`/`shortTriggerState` >= CONFIRMED
  directly, but that state does NOT mean "there was recently an entry" - once ACCEPTED, it stays >= 2
  for as long as `close` doesn't cross back below `longBreakLevel`/`shortBreakLevel`, which can be an
  arbitrarily old micro-pivot. On a real chart this produced ±40 bands lasting weeks or months,
  answering "has this historical break-level not been violated yet", not "was there an entry" -
  `longTriggerState` was conflating two different lifecycles (how far the CURRENT entry attempt has
  progressed, vs. whether a past trigger's level is still intact), a question Position
  Health/`longTradeOpen` already own. No debounce could have fixed this - it wasn't flicker, it was
  the wrong variable. Replaced with the actual entry EVENT: `newLongTrigger`/`newShortTrigger` (fires
  once, on the bar entry is granted) tracked via `lastLongEntryBar`/`lastShortEntryBar`, shown for a
  short fixed window (`entryDisplayBarsInput`, default 5 bars, new "Entry lane display bars" input,
  replaces the Entry-lane use of `laneStabilityBarsInput` - that input now only affects the Market
  lane, renamed to "Market lane stability (bars)"). Separately noted, not fixed here per the
  established rule of not mixing display and calibration changes in one pass: the Market lane (±80)
  likely appears far less often than expected too, since Permission is a product of several gated
  0-1 factors and a 55 threshold is comparatively high for that shape - worth checking against the
  real `longPermission`/`shortPermission` distribution (now in the data window) before touching
  `permissionThresholdInput`'s default.
- The Entry-lane fix above still left every lane empty over 1-2 years of real history on every
  instrument tested, ruling out "just a quiet period". Temporarily surfaced `longPermission`/
  `shortPermission` directly on the pane (not just the data window) to check at a glance - both
  peaked around 10-15 over the sample checked, nowhere near the 55 threshold. Confirms the deferred
  calibration question from the previous entry, with real numbers: `permissionThresholdInput` gates
  not just the Market/Entry lanes but `longTriggerEligible`/`shortTriggerEligible` themselves, so a
  threshold this far out of reach means `newLongTrigger`/`newShortTrigger` (and so the Setup/Trigger/
  Signal alerts) may never have fired in practice, on any instrument, since this existed - the
  Decision Timeline rework didn't create this gap, it just made it visible for the first time.
  Lowered the default from 55.0 to 12.0. Provisional, not a validated figure - one instrument, a few
  days of data - revisit against a wider sample before trusting it long-term. Reverted the temporary
  pane-visible Permission plots back to data-window-only once diagnosed.

## v1.1.2 — 2026-08-01
- Added move-extension shading to the Permission histogram bars (`extensionShadingInput`, default
  on): Permission's floored-multiplicative gates saturate once a trend is established, so the bars
  can look flat even while price keeps extending in the same direction. The fill now fades toward
  full color as the dominant side's live move since its last opposite pivot grows, normalized
  against the existing "Impulse overextension threshold (ATR)" input. Reuses the
  `highSinceLastLow`/`lowSinceLastHigh` trackers fixed in v1.1.1. Display only — bar height, the
  underlying Permission value, Trigger eligibility, CRV and alerts are all untouched.
- Fixed `RE10140` ("script creates too many plots (65), limit is 64") on compile — the script was
  already at/near Pine's 64-cap on combined plot+alertcondition+hline+bgcolor calls before this
  release (see in-file comments near Position Health); dropped 3 of the least load-bearing
  data-window diagnostics (legQualityHistory array-size sanity check, T2 Long/Short — the latter
  still visible as the dashed price-chart target lines) to get back under the limit with margin.
- Fixed the confidence-band background reading as a constant colored wash (user report: "Hintergrund
  ist durchgezogen rot") — its "stagnant" state was a faint tint of the dominant side's color, and
  since Permission rarely moves fast enough bar-to-bar to clear the rising/declining velocity
  threshold, most bars landed in "stagnant" and painted the same tint continuously. Dropped that
  state: the background now stays fully transparent unless there's a real rising (color) or
  declining (gray) move, so shading only appears when it means something.
- Relabeled `highlightRegimesInput` from "Highlight confirmed triggers" (stale, from before the
  confidence-band-background rework) to "Confidence-band background (Permission rising/declining)",
  and removed the same stale "gates ... the background highlight" claim from
  `confirmationThresholdInput`'s tooltip (it never did — the background reads
  longPermission/shortPermission, not confirmationThresholdInput).
- Same fix applied to the separate Position Health background, which had the identical issue: an
  unconditional `else` branch tinted the pane by dominant side whenever health was NOT
  deteriorating, so it painted almost every bar. Now grays only on real deterioration
  (`dominantHealthVelocity < -0.3`), transparent otherwise — the side info stays visible via the
  Position Health lines' own color. Also removed `dominantHealthStateCode` and
  `healthStateBaseColor`, both dead code left over once the state-tint branch was dropped (the
  former was never read anywhere, the latter only fed that branch).
- Refined the move-extension shading curve: was a linear 25-70 transparency ramp, which bunched
  most of the visible color change up near the overextension threshold (bars rarely get that far).
  Now `norm^0.6` over a wider 15-70 range, so the first ATR or so of movement already reads as a
  clear step instead of needing to approach the full threshold before the bars visibly change.

## v1.1.1 — 2026-08-01
- Fixed `lowSinceLastHigh`/`highSinceLastLow`/`lowSinceLastLow`/`highSinceLastHigh` starting at
  the pivot confirmation bar instead of the true pivot bar, silently dropping up to `pivotLen`
  bars of already-known price movement from the plotted T2/Invalidation levels and from
  `longCrvFactor`/`shortCrvFactor`, which can feed into whether a Trigger signal fires at all. Now
  seeded via `ta.lowest`/`ta.highest` over the true pivot-to-confirmation window.
- Fixed the "Directional Balance" plot still reading `longScore`/`shortScore` (compressed near
  zero except around a confirmed trigger) instead of `longPermission`/`shortPermission` — the same
  fix v1.0.1 already applied to the Permission line/velocity/background, missed here.
- Raised `maxLegHistoryInput`'s minimum from 2 to 4 — below 4, the recent-half-vs-older-half trend
  split silently stayed neutral instead of reflecting a real trend read.
- README now documents that reference-impulse exhaustion gets imprecise deep into a counter-move
  (the code already knew this; the caveat wasn't surfaced to users).
- Removed a `math.max` floor on `htfScale` that could never trigger (the other branch is always
  larger by construction) — simplification only, no behavior change.

## v1.1.0 — 2026-08-01
- Added Position Health (Long/Short) — a second, fully decoupled score answering "is an
  already-open position still structurally healthy", not "is a new entry attractive here". Never
  reads CRV, Trigger state or the trade-lifecycle machinery; combined as a weighted average (not
  the multiplicative floored gate used for Permission), so a single weak dimension can't crash a
  hold decision.
- Six components per direction: Live Quality (blends the existing leg-boundary-gated Live Trend
  Quality with a new genuinely continuous per-bar read), Pullback Health (reuses Continuation
  Maturity while the held direction's own leg is active, reuses the existing Reversal Maturity read
  while the opposite leg is active - not a hard 0, avoiding the same pivot-confirmation lag TPE's
  own README flags for Permission), Trend Progress (net directional movement over a lookback,
  scaled by ATR), Trend Fatigue (shrinking recent leg size as a relative ratio, exposed as its own
  score), Structure Intact (graded ramp toward the same 0.90 retracement threshold that governs
  reference-leg flips; reads a continuous recovery ratio rather than a hard 0 while the opposite leg
  is active, meeting Pullback Health's same-lag fix so both branches reach 100 exactly at the
  leg-flip moment, no cliff), and Regime/Sideways-Risk (a net-movement/path-length efficiency
  ratio).
- Fixed Trend Progress and Trend Fatigue after backtested Pine Logs analysis (34,776 logged bars
  across 4 test sessions) showed the score compressed into roughly 15-80 with Long health never
  reaching HOLD (max 81.8) - Trend Progress's original "break beyond the last confirmed swing
  point, then 20-bar decay" model measured exactly 0.0 on 90-98% of bars (a rare pulse spending
  most of its time at the floor); Trend Fatigue's original absolute ATR-multiple difference
  saturated its clamp on ~70% of bars (bimodal 50/100, no gradient). Both replaced with continuous,
  scale-appropriate measures (net ATR-scaled move for Progress, relative ratio for Fatigue) without
  touching the pre-existing `legRangeTrend`/`liveTrendQuality` formula those were derived from.
- A second Pine Logs pass on the fixed version (another 34,776 bars, 0 NaN) showed Trend Progress
  now varying meaningfully (0.0 dropped to ~50% of bars, ≥99.9 rose to ~26%) but Trend Fatigue's
  symmetric ratio clamp still saturated on 61.5% of bars, and Long health's ceiling barely moved
  (80.2). Root cause: the recent-vs-older leg-range ratio is naturally asymmetric - shrinking is
  bounded at -100% (already handled correctly), growing is not (legs commonly more-than-double
  between regimes) - so a symmetric +/-100% clamp saturated the growth side constantly. Only the
  growth side is now compressed by a configurable `trendFatigueGrowthScaleInput` (default 3.0x)
  before the final clamp.
- Classified into four states via configurable thresholds: HOLD / PROTECT / REDUCE / EXIT —
  PROTECT is new: a state between "fine" and "get out" for a healthy-but-cooling trend.
- A third Pine Logs pass (another 34,776 bars) confirmed Trend Fatigue's saturation was fixed
  (0.0% at >=99.9, was 61.5%) but HOLD was still never reached - the score's ceiling barely moved
  (76.3). Root cause this time: Live Quality (25% weight, the single largest) empirically caps
  around 75-85 regardless of trend strength, since real efficiency (net move / path length) rarely
  approaches 1.0 in noisy price action - looks like a genuine property of real market data, not a
  formula defect. Recalibrated the default thresholds against the actual observed distribution
  instead of chasing an unreachable ceiling: HOLD 85→68, PROTECT 65→54, REDUCE 40→36 (roughly
  top-2%/next-16%/next-50%/bottom-32% of the empirical distribution).
- Added a Position Health background (independent toggle, blends with the existing Permission
  confidence band) and downgrade markers - a real chart review showed the two continuous circles
  lines are hard to read as "when did this transition happen" or "is it about to get worse" across
  a wide, multi-month view. The background colors the pane by whichever side currently has the
  healthier reading and its state, overriding to gray whenever that side's smoothed health velocity
  is negative - a weakness signal visible before a state threshold is actually crossed. The markers
  mark every state downgrade directly on the price chart (`force_overlay`, bounded rolling history
  of 30 per side).
- Reworked the downgrade markers twice after real chart review. First pass: full-text labels
  (`Long ⚠ REDUCE`) in the directional `label_up`/`label_down` style (matching the Trigger labels,
  which legitimately ARE directional) crowded and overlapped on a busy chart, and wrongly implied a
  downgrade is a directional trade signal - moved detail into the hover `tooltip`, switched to a
  neutral `label.style_circle` marker. Second pass: `style_circle` still rendered as a large,
  fixed-size disc regardless of `size=` - switched to `label.style_none` (a floating `●` glyph, no
  background bubble) and dropped the flat warning-orange for this file's existing side convention
  (green = long, red = short, matching the Permission histogram/lines), with brightness scaled by
  how severe the downgrade is. Third pass: markers still sat directly on the wick (hard to see) and
  fired on every REDUCE<->EXIT flicker for whichever side was chronically weak (noise, not signal -
  a marker on "Short: REDUCE, score 47.9" during a long-favorable pullback was uninterpretable
  without more context). Offset half an ATR from the wick; only mark downgrades starting from
  PROTECT or HOLD (the meaningful "was fine, now isn't" case); tooltip now also shows the other
  side's current reading for comparison. Fourth pass: the tooltip's bare state-code arrow
  ("PROTECT → REDUCE") assumed the reader already had the HOLD/PROTECT/REDUCE/EXIT ladder memorized
  - each state now carries a short plain-language gloss (e.g. "REDUCE (weakening, cut size)"), and
  the sentence structure spells out "was X, now Y" instead of a bare arrow.
- Displayed as two additional circles-style series in the existing pane, colored
  blue/purple/orange/fuchsia for HOLD/PROTECT/REDUCE/EXIT - deliberately not the pane's existing
  green/teal/red/maroon (Permission/Velocity), which made an early version visually indistinguishable
  from those lines. Neither sub-components nor state codes are individually plotted to the data
  window (`plot()`/`alertcondition()` combined count against Pine's 64-output cap, empirically
  confirmed via RE10140, and this script was already close to it). Added a PROTECT-entry alert per
  side (2 total) — the state this feature actually closes a gap on; HOLD/REDUCE/EXIT stay visible
  via the series color only. Added a "Debug: log Position Health components" toggle (off by
  default) logging all six sub-components plus the final score/state per bar via `log.info()`,
  which does not count against the plot/alertcondition output cap - read via TradingView's Pine
  Logs panel.
- Reworked the Position Health line and background colors after chart review: coloring both lines
  by state alone (blue/purple/orange/fuchsia) made it impossible to tell Long from Short by color -
  only by which half of the pane (upper/lower) they sat in. Hue now encodes side instead (green =
  long, red = short, matching the Permission histogram/lines and the downgrade markers), and
  brightness encodes state (vivid/opaque when healthy, fading toward gray-transparent toward EXIT -
  the same "fading = weakening" language the background's gray override already used). The
  background's own hue was updated to match (side-based, not state-based).
- Added six dotted threshold reference lines (HOLD/PROTECT/REDUCE boundaries, mirrored for Short)
  after chart review confirmed color/brightness alone still didn't answer "where exactly does
  PROTECT start" - Permission already has this for its own thresholds, Position Health didn't.
  Drawn once via `line.new(..., extend=extend.right)`, not `plot()`/`hline()` - free against the
  output cap.
- Added divergence warning markers - reuses this file's existing divergence detection
  (`regularBearDiv`/`hiddenBearDiv`/`regularBullDiv`/`hiddenBullDiv`, already computed for
  Permission's Exhaustion) rather than adding new detection logic. Bearish divergence warns an
  existing Long, bullish divergence warns an existing Short, both leading signals ahead of any
  state change. Deliberately purely visual (a `◇` glyph, same pattern as the downgrade markers) -
  does not feed the Position Health score, so the just-calibrated thresholds don't need re-tuning.
- Two further readability fixes after real chart feedback. Downgrade-marker tooltips still read as
  dense jargon ("was PROTECT (cooling, protect gains), now REDUCE (weakening, cut size), score
  47.4 - for comparison Long is EXIT, score 17.3") - dropped state names, scores, and the
  other-side comparison entirely, down to a single action clause ("Short position weak - consider
  a smaller position"). Divergence markers were scaled by regular-vs-hidden strength (20-55%
  transparency), which read as barely visible on a real chart - switched to full opacity, no
  transparency scaling.
- Fixed divergence markers still reading as too weak and too numerous even after the opacity fix.
  Two causes: the `◇` glyph is outline-only (no fill), nearly invisible at `size.tiny`; and
  `regularBearDiv`/`hiddenBearDiv` (and the bull versions) stay true for every bar between one
  pivot confirmation and the next, not just the bar the divergence was actually confirmed on, so a
  single real event produced a dense cluster of markers instead of one. Switched to filled `◆`;
  gated marker creation to `newPivotHigh`/`newPivotLow` (the exact bar the underlying pivot, and so
  the divergence read, actually changed).
- Added upgrade markers (hollow `○`, mirror of the downgrade markers' filled `●`) after a chart
  question surfaced that a side chronically stuck in REDUCE/EXIT (e.g. Long during a sustained
  downtrend) never shows any downgrade marker at all during pullbacks, since there's nothing above
  PROTECT/HOLD to drop FROM. Applies the identical PROTECT/HOLD-only filter symmetrically (a rise
  INTO PROTECT or HOLD, not every REDUCE<->EXIT tick) - deliberately excludes the plain
  EXIT→REDUCE case even though it's the most obvious first example, since that boundary is exactly
  where the chronic flickering the filter exists to suppress happens.
- Clamped the (pre-existing, not Position-Health-specific) Permission Velocity lines to +/-60,
  fixing a scale problem a real chart showed: unclamped, a single sharp Permission jump (up to
  +/-100 x5 = +/-500 in the extreme) forced the whole pane's autoscale to stretch to accommodate
  that one spike, compressing the histogram, Permission line, Position Health lines, and the new
  threshold reference lines into an unreadable thin band near zero. Purely visual - Velocity feeds
  nothing else (the confidence background uses its own independently-computed smoothed velocity).
- The Velocity clamp alone wasn't enough - real chart feedback confirmed the deeper issue: Permission's
  floored-multiplicative gate design keeps it naturally compressed into a small sub-range (rarely
  much above ~40), while sharing one pane axis with Position Health (full 0-100 range) squashes it
  regardless of any one outlier. Added `permissionDisplayStretchInput` (default 1.6x, new "08 ·
  Display" group input) - stretches the Permission histogram, Permission line, Directional Balance
  line, and Permission's own threshold lines by this factor before plotting (clamped back to
  ±100 so the stretched threshold lines don't exceed the shared axis). Display only - every
  non-plot use of Permission (Trigger eligibility, CRV, alerts, data-window diagnostics) still
  reads the real, unstretched 0-100 value.

## v1.0.1 — 2026-07-31
- Fixed the Permission line, velocity line and confidence-band background driving off
  `longScore`/`shortScore` instead of `longPermission`/`shortPermission`. `longScore`/`shortScore`
  is Permission chained through confirmation × CRV × decay (up to 7 multiplicative gated factors),
  which compresses it near zero almost everywhere except a brief spike at an actual confirmed
  trigger — on a live chart this made the pane look flat/unreadable and made the background's
  dominant-side comparison decide on near-zero noise instead of the actual trend/structure reading.
  Now wired to `longPermission`/`shortPermission` — the same pre-confirmation read the histogram's
  light bars and `permissionThresholdInput` already use.

## v1.0.0 — 2026-07-31
- Initial release. Renamed and reconceptualized from Directional Probability Engine v3.5
  (archived, see `archive/indicators/directional_probability_engine/`) — same architecture
  (alternating confirmed swing reference leg, unified Continuation/Reversal Maturity, split
  Exhaustion, Trigger state machine, scenario-aware Target/Invalidation), reframed from "how
  probable is this setup" to "does the market currently permit trading this direction".
- Added Live Trend Quality — a continuously-updated read of whether the last few legs' efficiency
  and range are trending stronger or weaker, alongside the existing quality frozen at the reference
  leg's formation.
- Added Permission Decay — the final score fades a configurable percent per bar when there's no
  fresh extreme, accelerating momentum or ATR expansion in the relevant direction, instead of
  sitting at a stale high value once the move that earned it has gone quiet.
- Reworked the display: histogram retained (light = Permission, solid = Active Permission), added a
  thicker Permission line, a velocity line (Δ Active Permission), and a rising/falling confidence-
  band background replacing the old confirmed-trigger background.
- Renamed terminology throughout: Readiness → Permission, Score → Active Permission.
