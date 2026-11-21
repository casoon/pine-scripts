# Changelog

## [Unreleased]

### Added
- **Sub-structure:** the finer degree also recognises a diagonal (overlapping W4, contracting or expanding) and places it by position — "LD" in W1 / A (leading), "ED" in W5 / C (ending). A diagonal W3 rules the count out, as does a diagonal in a B wave, a flat A or a diagonal's W2 / W4; in W1 / A and W5 / C it confirms the wave like a five
- **Diagonal fallback:** a diagonal that starts at the last impulse end opens the next move and is labeled leading
- **Counting:** while an A–B after impulse is active and A is not a clear five on the sub degree, the same two waves run as alt count "W1-W2 (leading diagonal?)" — a new trend starting with a leading diagonal. It breaks with the A–B at the impulse end and takes over, labeled (1)-(2) and provisional, when the A–B breaks without a valid A–B–C
- **Dashboard:** a 1–2 / A–B count whose third wave is under way (price beyond the W1 / A end) reads "… · W3/C developing"
- **Counting:** every possible origin of W1 / A is tested (each pivot more extreme than all later ones, back to a pivot beyond the wave end; of more than eight, the nearest one and the seven with the largest move into them relative to the wave); the complete count decides. Origin guideline: a move into the origin smaller than 38.2 % of the wave costs up to 20 fit points
- **Dashboard:** a count whose waves do not show the sub-structure their type requires (motive waves and zigzag A / C five waves, flat A three, A / W1 of a partial count five or three) reads "unconfirmed" instead of "counted" / "complete"
- **Pivots:** new input `Count on last N bars` (default 5000) — counts are searched only on the last N bars, keeping the all-pivot search within the run-time limit
- **Counting:** provisional fallbacks when no running count and no ordinary interpretation exist — contracting / expanding diagonal searched over all stored pivots like the impulse (overlap, wedge geometry, sub-structure; labeled "Leading diagonal?", "Ending diagonal?" or "Diagonal (L/E)?") and W–X–Y searched over all stored pivots (W, X, Y each a zigzag or flat, their ends picked like wave origins). New inputs `Detect diagonal fallback`, `Detect W-X-Y fallback` and `Fallback plausibility threshold` (default 55); a credible fallback also shows as the alt count
- **Fib fit:** guideline of one extension — after an extended W3 (≥ 1.618 × W1), a W5 longer than W3 lowers the fit by 30 points. Completing an impulse from a running W1–W4 also needs `Min Fibonacci fit`
- **Rules:** a W1–W4 count whose W3 is shorter than W1 draws the W5 limit as "W5 max" (W4 end + length of W3 — beyond it W3 would be the shortest) and breaks when price runs beyond it
- **Counting:** W1–W4 and A–B–C read from the same 1–2 / A–B run in parallel when both hold: the better fit (plus completeness bonus) is the main count, the other is continued as "Alt count (running)" and takes over when the main count breaks (e.g. W4 entering W1 territory) or its correction completes
- **Display:** the last completed impulse stays on the chart (faded) while the next structure develops, instead of disappearing at the next pivot; it is removed once price trades beyond its W5 end
- **Counting:** running count — the active count is continued at every new pivot (W1–W2 → W1–W4 → impulse → A–B after impulse → A–B–C) and is replaced only when it breaks; a new local pattern with a better Fib fit no longer displaces it. A continued count is held to the hard rules only (no Fib fit minimum except for completing an impulse). An A–B after an impulse is dropped once C runs beyond the A end without a valid A–B–C. Dashboard "Checks" shows whether the count was continued, kept or taken from the alternate
- **Counting:** when price trades beyond the W5 end of the active impulse, W5 is extending — the count returns to W1–W4 and the next pivot sets the new W5 end
- **Dashboard:** "Checks" row: rule-valid interpretations at the last pivot and how many fell below the Fib fit
- **Rules:** `Min Fibonacci fit (0-100)` (default 55) — counts that pass the hard rules but fit the Fibonacci guidelines poorly are rejected instead of drawn
- **Rules:** sub-structure check on the finer pivot degree (impulse 5-3-5-3-5, zigzag 5-3-5, flat 3-3-5): internal swings (≥ `Min sub-wave swing (× wave)`, default 0.08) are tested for a 5-wave impulse under the same hard rules. Only clear results reject — exactly three swings rule out W1/W3/W5 and the zigzag A and C (flat C); a 5-wave fit rules out a B wave and the flat A. More swings without a 5-wave fit ("unclear"), a single leg or missing sub pivots leave the count open. The dashboard sub-structure row shows the result per wave. Sub pivots are stored separately (up to 400)
- **Fib fit:** degree guideline — a counter-swing inside a wave larger than the count's own corrective waves (inside W1/W3/W5: the larger of W2 and W4; inside A and C: B) lowers the fit by 20–40 points

### Changed
- **W1 origin:** the 38.2 % rule that picked a single origin is replaced by testing all origins (see Added)
- **Pivots:** `Max pivots stored` default 60 → 200 (max 300); the sub degree keeps five times as many. Counts, sub-wave labels and the zigzag are drawn by bar time, so older wave points do not hit the bar-offset limit
- **Rules:** the diagonal toggle no longer relaxes the W4 overlap rule of an ordinary impulse or W1–W4; it now switches the diagonal fallback (input renamed to `Detect diagonal fallback`, default on)
- **Sub-structure:** three swings count as corrective only in A-B-C shape (B 0.236–1.382 of A, C beyond A); other swings without a 5-wave fit are "unclear"
- **Counting:** all counts (impulse, W1–W4, W1–W2, zigzag, flat, A–B after impulse) pick their wave points from all stored pivots instead of the last consecutive ones — each wave point is the extreme of its segment, so a wave may contain smaller swings (long W3 with internal pullbacks, W2 as an A-B-C)
- **Count selection:** without an active count, rule-valid counts are ranked by Fibonacci guideline fit plus a small bonus for more complete structures; the best interpretation of another type becomes the alternate count
- **Fib fit:** an extended W3 (1.618–4.236 × W1) counts as a full fit, and W5 may also relate to 0.618 × the distance from the W1 start to the W3 end — impulses and W1–W4 counts with a short W1 and an extended W3 are no longer rejected by the minimum fit
- **W1–W2 count:** W1 starts at the most extreme point of the preceding pullback instead of the last pivot — counter-swings smaller than 38.2 % of W1 before it are treated as part of the origin
- **W1–W2 count:** W2 retracement levels (38.2 / 50 / 61.8 / 78.6 %) are drawn with the projections
- **Count selection:** no W1–W2 count whose W1 ends at the last impulse end — the W5 is no longer relabeled as a new W1. A W1 may start at the impulse end
- **Rules:** hard rules and guidelines are separated. Rejected only by rules: W2 beyond the W1 start, W3 the shortest, W4 in W1 territory, no progress beyond W1 / W3, a clearly corrective motive wave; zigzag B ≥ 90 % of A (then it is a flat), flat B < 90 %, C not beyond the A end. Fib ranges (W2 38.2–78.6 %, W3 ≥ 0.8 × W1, zigzag B 0.236–0.886 and C 0.5–2.0 × A, flat B up to 1.38 and C 0.8–1.8 × A, A–B after impulse B 0.236–0.886) no longer reject; they shape the Fib fit, and `Min Fibonacci fit` stays as a separate plausibility filter for fresh counts
- **Counting:** every new W1–W2 is labeled "1-2 / A-B" (labels "1/A", "2/B", W2/B levels, W3/C projections) until the next waves decide: a pullback after W3 / C out of W1 territory with W1 and W3 not corrective makes it W1–W4, otherwise a valid zigzag or flat makes it A–B–C. Alert "EW: W1-W2 count active" fires for it (message "1-2 OR A-B COUNT ACTIVE")
- **Dashboard:** the sub-structure row shows the 5-wave check per wave instead of a pivot count

### Fixed
- **Count selection:** a W1–W2 starting at the last impulse end was excluded, so the count started mid-move at a later pivot; that origin is tested again
- **Running count:** a 1–2 / A–B whose W1 / A is corrective (three swings) and that cannot become W1–W4 or A–B–C is dropped at the next pivot instead of being kept; the fresh search decides
- **Counting:** a long wave could miss its real origin — only the eight nearest candidate origins were tested, on lower timeframes all minor dips inside the wave; candidates are now ranked by the move into them
- **W–X–Y:** the A end of a component must be beyond every pivot between the component start and A — W could skip a higher intermediate high
- **Pivots:** the true-extreme scan of a new pivot starts at the pivot bar instead of the current bar (no change in result — the bars after a confirmed pivot are never more extreme)
- **W1 origin:** no division by zero when the origin candidate equals the wave end
- **Sub-wave labels:** old (i)-(iv) / (a)-(b) labels are now removed when the count is redrawn instead of piling up on the chart

## v1.3.0 — 2026-11-17
Rebuilt as a display of the current wave count: no score, no "setup" calls. **Existing alerts must be recreated** — titles and messages changed.
- New event "Close beyond W1 end" fires on a break observed after the W1-W2 count appears, not on the count bar when the pivot lag already placed the close beyond W1
- Removed: Fibonacci guideline score (0–100, incl. alternation bonus) and its gate input "Min count score (0-100)". The score measured closeness to ideal ratios and read as a quality verdict; the dashboard "Score" row now shows the raw ratios (W2/W1, W3/W1, W4/W3, W5/W1, B/A, C/A)
- Count selection no longer ranks by score + bonus: the most complete rule-valid interpretation wins in a fixed order (impulse, zigzag/flat, A-B after impulse, W1-W4, W1-W2); the next valid one is the alt count. Without the score gate, every count that passes the hard rules can be shown
- Removed alerts: "EW: Wave-3 setup", "EW: Wave-5 setup", "EW: C-wave setup", "EW: Impulse complete", "EW: ABC complete", "EW: Flat complete"
- New event alerts: "EW: Impulse count complete", "EW: Zigzag count complete", "EW: Flat count complete", "EW: A-B count active", "EW: W1-W2 count active", "EW: W1-W4 count active", "EW: Close beyond W1 end" (once per W1-W2 count). "EW: Count invalidated" is unchanged
- Count alerts now also fire when a new count of the same type replaces the previous one (different first point); before, a same-type sequence was suppressed
- Dashboard status reads "<count> ▲/▼ complete" or "… counted" instead of "→ W3/W5/C setup"; post-impulse levels relabelled "Retr 38.2/50/61.8%"
- Header: Data Contract block added

## v1.2.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.2.1 — 2026-06-29
- Alerts: messages standardized to `EWR · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.2 — 2026-06-11
- Fix: wave points now anchor to the TRUE extreme since the previous pivot. Sharp counter-swings that never confirm as pivots (shorter than Pivot Length on either side) were invisible to the engine, so e.g. Wave 2 could land on a later, lower high instead of the strongest pullback. Each accepted pivot now scans the actual high/low of the gap and uses that price/bar.

## v1.1 — 2026-06-11
- Flat correction detection (regular ≈ B 1.0×A, expanded ≈ B 1.05–1.38×A), disjoint from the zigzag eval (B ≤ 0.886)
- C-wave setup: after a completed impulse, a confirmed A-B sequence projects C targets (×1.0 / ×1.618 of A) with the impulse extreme as monitored invalidation level
- New alerts: "Flat complete" and "C-wave setup"
- Candidate selection refactored (array-based ranking with correct runner-up tracking)

## v1.0 — 2026-06-11
- Initial release
- ZigZag pivot engine (two degrees) with ATR noise filter
- Hard-rule validation for impulses (W2/W3/W4 rules, diagonal toggle) and zigzag A-B-C
- Fibonacci guideline scoring 0–100 with alternation bonus, configurable score gate
- Developing counts: W3 setup (after W1-W2) and W5 setup (after W1-W4) with Fib target projections
- Post-impulse correction targets (38.2 / 50 / 61.8 %)
- Invalidation level drawn and monitored; broken level clears the count
- Sub-wave labels (i)-(iv) / (a)-(b) from the sub degree, W1/W3 leg check in dashboard
- Alternate count in dashboard; "No valid count" state instead of forced labels
- Alerts: impulse complete, ABC complete, W3 setup, W5 setup, count invalidated
