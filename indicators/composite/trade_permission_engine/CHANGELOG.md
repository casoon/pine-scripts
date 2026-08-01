# Changelog

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
