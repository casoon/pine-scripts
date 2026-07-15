## v2.0.0 — 2026-07-15
- Replaced fixed `if/else` state priority with complete candidate scores, best/second-best arbitration, a minimum score, and a configurable dominance margin
- Added orthogonal Structure Regime and Energy Phase axes while retaining the nine familiar visible states; Transition now carries explicit no-data, conflict, trend-forming, structure-break, or chaotic reason codes
- Reworked state confidence, hysteresis, and emergency switching around the same candidate scores; emergency bypass is limited to high-confidence opposite Expansion
- Bound Pullback candidates to a prior active or recent efficient impulse and changed readiness to require a directional reaction rather than merely an active Pullback state
- Rebuilt impulse memory around directed net progress, gross range, efficiency, and close/wick hybrid correction depth
- Replaced binary Long/Short compatibility with `Unfavorable`, `Neutral`, `Compatible`, and `Preferred` context levels
- Renamed visible Accumulation/Distribution or Market Pressure language to the more conservative `Auction Pressure` and separated its volume switch from Box Volume/Box VWAP
- Preserved raw zones across configurable short interruptions or shock bars unless a buffered geometric break occurs
- Added maximum zone width, confirmed-state grace, Balance→Compression history, and compression share to the zone model and hover
- Replaced immediate zone breaks with `BOX?` attempts requiring configurable consecutive closes and minimum breakout quality
- Added post-breakout hover follow-up (`Breakout held`, `Retest passed`, `Back inside the box`) over a configurable observation window
- Renamed visible quality to `State Quality` and exposed separate Trend/Balance quality, axes, candidate dominance, context levels, transition reason, and impulse-efficiency outputs in the Data Window

## v1.3.3 — 2026-07-15
- Restricted the confirmed-state machine and its counters to confirmed bar closes, eliminating intrabar state changes in downstream context
- Fixed the zone creation bar being accumulated twice in quality, ATR, volume, volume baseline, bar count, and Box VWAP
- Split expansion into direction-specific Bull/Bear scores with directional candle body, close location, ATR-normalized progress, and signed-efficiency gates
- Required a measurable deceleration, failed-progress, or effort/result trigger before classifying Exhaustion; persistent directional expansion now reduces the Exhaustion score
- Replaced the fixed three-percentage-point ROC deceleration scale with normalization against the momentum delta's own rolling deviation
- Added an explicit `Initializing` dashboard state and `Engine Ready` Data Window output until all required local and enabled HTF inputs are available

## v1.3.2 — 2026-07-15
- Changed all user-facing script text to English, including settings, tooltips, state descriptions, dashboard values, validation errors, and alert messages

## v1.3.1 — 2026-07-15
- Added total box volume to active, completed, and breakout-source zone hovers using compact number formatting
- Added average volume per box bar relative to the rolling normal volume; symbols without usable volume data are marked as unavailable

## v1.3.0 — 2026-07-15
- Added a Box Profile to zone and breakout hovers: width in average ATR, debounced upper/lower edge tests, and Spring-/Upthrust-like failed-break counts
- Added volume-anchored Box VWAP from the tracked zone onset; its optional evolving line defaults to off while the value remains available in hover text
- Added descriptive breakout quality (`Schwach`/`Sauber`/`Stark`) from buffered ATR distance, candle body, close quality, expansion, and optional volume confirmation

## v1.2.4 — 2026-07-15
- Changed `Strukturlinien` to off by default; the selected structure smoothing remains active in all calculations

## v1.2.3 — 2026-07-15
- Changed the default structure smoothing from EMA to JMA Approx; the selection continues to drive local and confirmed HTF structure consistently

## v1.2.2 — 2026-07-15
- Reworked zone context wording into a non-redundant sequence: previous impulse, phase after impulse, counter-move depth, preferred direction, and concrete rejection reason
- Replaced `Anstieg/Rückgang gefährdet` with `Keine klare Fortsetzung`; the hover now distinguishes a 75% retracement, opposite structure, lost local structure, and opposing HTF
- Replaced the vague final result `Zustand gewechselt` with the actual new state and renamed expiry to `Maximale Zonendauer erreicht`

## v1.2.1 — 2026-07-15
- Separated zone and breakout tooltips: `BAL`/`COMP` describe the source zone, while `BOX ↑/↓` starts with the confirmed breakout direction and then lists clearly marked source-zone values
- Replaced ambiguous visible `Bias` wording with `Marktdruck`/`Zonendruck`; Kauf-/Verkaufsdruck is explicitly distinct from Long/Short direction
- Replaced predictive breakout claims with the descriptive terms `gleichgerichtet` and `gegenläufig`
- Kept directionless zone labels gray; green/red now means an intact impulse direction or confirmed breakout
- Clear remembered zone direction once its impulse context expires, preventing stale arrows and colors
- Corrected active-zone duration to count the current zone bar and seeded quality from the tracked pre-confirmation zone

## v1.2.0 — 2026-07-15
- Added a `Struktur-Glättung` selector with EMA, DEMA, KAMA, and JMA Approx; EMA remains the default and the selected method is also used for confirmed HTF structure
- Colored intact Long/Short zone labels green/red and made the original `BAL`/`COMP` label inherit the direction of a confirmed zone breakout
- Kept HMA out of the selector because its overshoot can produce misleading structure crosses

## v1.1.4 — 2026-07-15
- Removed the orange Compression square and purple Transition diamond from the bottom of the chart; expansion, readiness, zone, and breakout markers remain unchanged

## v1.1.3 — 2026-07-15
- Made impulse-direction labels conservative: arrows now require the parent EMA structure to remain intact and the confirmed HTF not to oppose the remembered impulse
- Correction depth now uses the maximum counter-move since the impulse ended instead of only the current close
- Replaced misleading endangered arrows with directionless `BAL ?` / `COMP ?` labels

## v1.1.2 — 2026-07-15
- Added the remembered impulse direction directly to visible zone labels (`BAL ↑/↓`, `COMP ↑/↓`); a trailing `?` indicates that the prior trend is at risk

## v1.1.1 — 2026-07-15
- Changed the context dashboard to opt-in (`Kontexttabelle` now defaults to off); states, zones, hover labels, Data Window outputs, and alerts remain active independently

## v1.1.0 — 2026-07-15
- Added sequence-aware impulse memory using the last confirmed expansion's direction, ATR-normalized size, duration, and average quality
- Added simple Balance/Compression classifications: Pause/Korrektur nach Anstieg oder Rückgang, plus Anstieg/Rückgang gefährdet
- Added an `Einordnung` dashboard row and suppress the context direction against an intact prior impulse
- Extended zone and breakout hover text with impulse size, correction depth, and continuation/failure outcome
- Added Data Window outputs for prior impulse direction and correction depth, plus a correction-context alert

## v1.0.5 — 2026-07-15
- Positioned bullish `BOX`/`EXP` labels below their bars and bearish labels above them so markers no longer cover candle bodies or wicks

## v1.0.4 — 2026-07-15
- Replaced the non-hoverable `EXP` shapes with labels whose tooltips show direction, confidence, expansion score, market quality, value location, directional bias, and HTF context

## v1.0.3 — 2026-07-15
- Replaced the non-hoverable `BOX ↑/↓` breakout shapes with labels whose tooltips show zone state, bias, quality, duration, range, and breakout direction

## v1.0.2 — 2026-07-15
- Replaced the fatal HTF timeframe validation error with a safe fallback: equal or lower context timeframes disable only the HTF layer and display `TF ≤ Chart` in the dashboard

## v1.0.1 — 2026-07-14
- Fixed zone breakouts being absorbed into the box before the breakout test; confirmed closes are now checked against the prior zone boundaries
- Extended the shock-bar guard to active zones and freeze geometry whenever the raw Balance/Compression state no longer survives
- Stabilized HTF context with completed HTF bars and calculated slow-structure slope inside the HTF series
- Made state-change, readiness, and zone-breakout events bar-close confirmed
- Fixed conditional zone-bias EMA evaluation and directionalized the exhaustion extension component
- Added validation for contradictory structure, ADX, value-location, zone-duration, and timeframe settings
- Clarified raw versus confirmed state outputs in the Data Window

## v1.0.0 — 2026-07-14
- Initial release: nine-state market classifier (Balance, Compression, Bull/Bear Expansion, Bull/Bear Pullback, Bull/Bear Exhaustion, Transition)
- Adaptive value zone with Discount/Value/Premium location classes
- Accumulation/distribution bias from close-position, failed auctions, absorption, and value-extreme reaction
- Compression/expansion/exhaustion energy scoring
- Confirmation-bar state machine with emergency opposite-state override
- Optional higher-timeframe structural context (advisory, with optional strict gate)
- Balance/compression zone boxes anchored to the true undebounced regime onset and grown from real highs/lows (not a fixed lookback window), closed on breakout, expiry, or state exit
- Shock-bar guard: a bar with range beyond `shockBarAtrMult` × ATR can't start, extend, or grow an already-open zone, preventing a single violent bar (before or during an active zone) from inflating box height
- Zone quality encoded via border thickness (running average of market quality across the zone's life)
- Zone hover labels (state, bias, quality, duration, range, and outcome) in the style of Wyckoff Schematics' event tooltips
- Long/short context-compatibility and readiness markers for grading external signals
- Context dashboard and alerts for state changes, zone breakouts, and readiness
