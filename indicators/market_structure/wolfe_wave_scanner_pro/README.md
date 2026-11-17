# Wolfe Wave Scanner Pro

Searches a depth window of confirmed swings for non-overlapping 5-point Wolfe Wave wedges — a contracting, alternating channel where point 5 tests the 1-3 trendline — that pass every hard geometry rule. Each pattern found projects its own EPA (Estimated Price at Arrival) level from line 1-4 at the time lines 1-3 and 2-4 converge, and is tracked live independently through its own lifecycle until price reaches the EPA, the pattern invalidates, or it expires.

Wolfe Waves are strongly interpretation-dependent — small changes in swing strength or search window shift which geometry gets found. It is a **display of Wolfe geometry**, not a signal machine: there is no quality grade and no trade metric, and "pattern detected" means "a Wolfe-shaped geometry exists here," not "enter now."

**Detection lags point 5.** Swings are confirmed `Swing-Stärke` bars after the extreme, and point 5 can sit several swings back in the search window — so a pattern is often detected well after point 5 formed. The chart label and the dashboard state how many bars P5 lies back.

## Features

- Alternating swing engine (`ta.pivothigh`/`ta.pivotlow`) with bounded history
- Best-of-window search: every valid point-5 anchor within `Suchbereich letzte Swings` is tried (a Wolfe wave is often already several swings old by the time it completes), and for each, points 1-4 are chosen combinatorially from all valid non-consecutive swings — a wave spanning e.g. swings 1,3,5,7,9 is evaluated too, not just the literal last 5 swings
- Tracks up to `Max. gleichzeitige Patterns` (default 1 = only the single highest-ranked pattern) distinct, non-overlapping valid patterns at once, each with its own drawings and invalidation state. An overlapping candidate only replaces an already-tracked pattern at that spot if it ranks higher
- Validity from explicit hard rules only: structure, contraction, channel, boundary hold (swings and bars), leg purity, P5 zone and apex convergence. An internal geometric rank decides between candidates; it is never shown as a grade
- EPA target is the price on line 1-4 at the apex time (where lines 1-3 and 2-4 converge, both drawn bold and stopping exactly there — no dangling infinite extension). The 1-4 line itself is drawn visibly through points 1 and 4 up to that same apex bar, and the vertical apex marker drops from that exact point to point 5 — one shared point everywhere, label/dashboard/drawing included
- Live pattern lifecycle: each tracked pattern runs `ACTIVE` → `50% EPA` → `EPA reached` / `EXPIRED` / `INVALIDATED`, with a live-updating EPA level (recomputed from line 1-4 every bar), a one-time halfway-to-EPA marker, an `Ablaufpuffer nach ETA (Bars)` expiry cutoff, and a dynamic invalidation level that tracks the live 1-3 line for `Dynamische 1-3-Invalidierung (Bars)` bars before freezing — `Invalidierung nur per Close` (default on) chooses between a confirmed close beyond the level or an intrabar high/low breach
- Chart label per pattern: direction, `P5 n bars before detection`, EPA@ETA
- Rule-breakdown debug table for tuning thresholds
- Light-theme dashboard (status, active pattern count, bars since P5, pattern direction, live EPA, EPA @ ETA, invalidation level) — taken from the highest-ranked currently *tracked* pattern; `SCAN` when none is tracked
- `Invalidierung anzeigen` (default off) draws the invalidation level line itself; invalidation *tracking* (the pattern still gets removed/alerted when the level breaks) always runs regardless of this toggle

## Rules and rank

A pattern is valid only when every hard rule passes — there is no score threshold:

| Rule | What it checks |
|---|---|
| Structure | Sequence alternates high/low, point 3 undercuts/exceeds point 1, point 5 extends beyond point 3 (lows declining for a bull pattern, highs rising for bear) |
| Contraction | Channel (line 2-4 vs. points 1/5) narrows by at least 30% end-to-start *and* monotonically through the midpoint; the 1-3 and 2-4 boundaries trend the same direction and their slope magnitudes are within a 3x ratio |
| Channel | Point 4 sits at least 0.5 ATR off the 1-3 line, and the point-4-to-point-5 leg crosses at least 60% of the remaining channel width (`traversal45`) |
| Convergence (apex) | Lines 1-3 and 2-4 converge ahead of point 5, within `2×` the pattern's own width |
| P5-Zone | Point 5's directional offset from the 1-3 line stays within `P5 max. Overshoot ATR` (default 1.0) beyond it or `P5 max. innerhalb ATR` (default 0.75) inside the wedge |
| Leg Purity | No skipped swing deviates from its enclosing leg's straight path by more than `Max. Zwischen-Swing / Leg` (default 50%) of that leg's amplitude |
| Boundary Hold | See below — swings and bars between points 1 and 5 |

**Internal rank.** Several valid combinations can exist per point-5 anchor, and tracked patterns can overlap. To choose between them the scanner sums geometric points — contraction 15, channel 10, apex 10, P5 zone 15, timing 5, symmetry 5, leg purity 5 (max 65). The rank only orders candidates; it is not a quality grade, not a gate and not shown on the chart or dashboard. The debug table shows it with its components.

**Boundary Hold.** A real Wolfe wave only tests the 1-3 trendline once, at point 5 — but the channel has to hold on *both* sides, not just that one. The scanner checks every swing strictly between points 1 and 5 — including ones the combinatorial search skipped when picking a non-consecutive point selection — against both the 1-3 *and* the 2-4 boundary, using `Swing-Boundary-Toleranz ATR` (default 0.35). If price already broke through either boundary earlier (e.g. a sharp plunge-and-recovery between points 3 and 4 on the 1-3 side, or a breach of the 2-4 side that never gets its own dedicated "test" the way point 5 tests 1-3), the pattern is rejected outright: the five chosen points can look clean on their own while the actual price path between them already violated the channel the wave depends on.

**Bar Boundary.** A separate, finer check (`Bar-Boundary-Toleranz ATR`, default 0.25) scans every single *bar* — not just the registered swings — between points 1 and 5 against both boundaries, catching a poke through the channel that never formed its own swing. Point 5's own bar is exempt from the 1-3 side of this check (it's checked by `P5-Zone` instead, which allows a deliberate overshoot); the 2-4 wall still applies to it like any other bar.

**P5-Zone is directional.** Overshooting beyond the 1-3 line and staying inside the wedge are tolerated differently, via separate `P5 max. Overshoot ATR` and `P5 max. innerhalb ATR` inputs. A point 5 outside either tolerance isn't testing the trendline, it's blowing through it (or never reaching it) — the same class of violation as a mid-pattern boundary break, just at the last point instead of an earlier one.

**Channel.** Point 4 must be a meaningful opposite-boundary excursion (≥0.5 ATR off the 1-3 line) and the point-4-to-point-5 leg must cross most (≥60%) of the remaining channel — a point 5 that ends up deep inside the channel instead of completing the traversal to the opposite wall isn't a finished wedge.

**Leg Purity.** The combinatorial search can select a "clean" chain of 5 points while skipping an intermediate swing that moved almost as far as the leg it's nested inside — effectively hiding a real countermove. `Leg Purity` rejects any selection where a skipped swing's deviation from its enclosing leg's straight path exceeds `Max. Zwischen-Swing / Leg` (default 50%) of that leg's own amplitude.

**Convergence (apex).** If the 1-3/2-4 wedge has already converged at or before point 5 (`etaOk` false), the pattern isn't a completed Wolfe wave — and drawing it anyway is actively misleading, since the fallback apex projection extrapolates the same already-converged slopes further out and can go wildly, even negatively, off in price.

## Pattern Lifecycle

A valid candidate is only drawn if it is still open on the bar it is found: one that is already past its expiry, or that the current bar already invalidates or carries to its EPA, is skipped instead of being drawn and closed on the same bar. Detection fires `WWSP · BULL WOLFE DETECTED` / `WWSP · BEAR WOLFE DETECTED`. Once drawn, a pattern enters state `ACTIVE` and is tracked, every bar, independently of every other tracked pattern. Its own creation bar is a one-bar grace period with no lifecycle event; from the next bar on it's checked against three mutually exclusive terminal states, in this order, plus one interim marker:

- **INVALIDATED** — the invalidation level breaks. For the first `Dynamische 1-3-Invalidierung (Bars)` bars (default 10) after point 5, that level tracks `min/max(point 5, the live 1-3 line) ± Invalidierungs-Puffer ATR` (default 0.5 ATR) bar by bar; afterwards it freezes at its last value. Depending on `Invalidierung nur per Close` (default on), either a confirmed close beyond the level or an intrabar high/low breach triggers this. Fires `WWSP · INVALIDATED`.
- **EPA reached** — price reaches the *live* EPA level, recomputed from line 1-4 every bar (not the frozen apex projection used for drawing). Fires `WWSP · EPA REACHED`.
- **EXPIRED** — price hasn't reached the EPA within `Ablaufpuffer nach ETA (Bars)` (default 10) bars past the pattern's computed apex bar. Fires `WWSP · EXPIRED`.
- **50% EPA** — a one-time interim marker that does *not* remove the pattern from tracking: fires once price reaches the halfway point between point 5 and the live EPA, on any bar that didn't already exit into one of the three states above. Fires `WWSP · HALF WAY TO EPA`.

Any of the three terminal states draws a label, removes the pattern from tracking (freeing a slot for a new one), and fires its alert; `Abgeschlossene/ersetzte Patterns behalten` controls whether that pattern's drawings are deleted at that point or kept on the chart as history.

## Multiple patterns

`Max. gleichzeitige Patterns` (default 1, capped at 8) caps how many valid patterns are tracked and drawn at once — each owns up to ~9 lines and 6 labels, so the cap also bounds drawing-object growth (`Suchbereich letzte Swings` is similarly capped at 24 to bound the combinatorial search cost). Each search pass finds the highest-ranked valid combination *per point-5 anchor* in the window, not just the single overall best — so with a cap above 1, two non-overlapping Wolfe waves elsewhere on the chart can both surface. Overlap is checked on the [point 4, point 5] completion leg only, not the full [point 1, point 5] span — since point 1 can sit anywhere within `Suchbereich letzte Swings`, two well-separated completions often still share the same early swings for points 1-2, and comparing the full range would let one wide pattern block every other candidate in that stretch. A margin — a third of the larger pattern's own total width — is added to both patterns' ranges before comparing, so two same-direction patterns crammed a few bars apart still count as overlapping even if their exact completion legs don't literally touch. Overlap only ever competes patterns of the *same direction* for a slot — a bull and a bear pattern occupying the same bars are two different scenarios, not rivals. If a new candidate's completion leg overlaps an already-tracked, same-direction pattern's, it only replaces it when it ranks higher (and isn't the exact same pattern already tracked); otherwise it's skipped. After every search, a cleanup pass checks all tracked patterns pairwise and removes the lower-ranked one of any same-direction, overlapping pair still left over — this catches overlap chains (A overlaps B, B overlaps C, but A and C don't directly overlap) that the one-at-a-time insertion check alone can miss.

Once all `Max. gleichzeitige Patterns` slots are full, a new non-overlapping candidate evicts the currently lowest-ranked tracked pattern if it ranks higher — otherwise the first patterns to fire that happen not to invalidate for a while would permanently occupy every slot and silently block every later candidate. `Abgeschlossene/ersetzte Patterns behalten` controls whether a pattern's drawings are deleted once it's invalidated, hits target, expires, is replaced, or is evicted, or kept on the chart as history.

## Debug

Enabling `Regel-Breakdown Debug-Tabelle` shows a table with the current best-in-depth candidate's pass/fail state per rule, its rank components and the measured values behind each rule — useful for tuning thresholds without guessing why a candidate wasn't drawn.

Enabling `Pine-Logs aktivieren (Fehlersuche)` (off by default) emits `WWSP SWING`/`WWSP SEARCH`/`WWSP PATTERN FIRED`/`WWSP PATTERN REPLACED`/`WWSP PATTERN EVICTED`/`WWSP INVALIDATED`/`WWSP EPA REACHED`/`WWSP EXPIRED`/`WWSP HALF EPA` lines to the Pine Logs pane, including how many 5-point combinations were evaluated per search and the full per-criterion breakdown (including `boundaryHold`) of the single best-in-window candidate — useful when a symbol/timeframe combination seems to produce no patterns at all, or to check why a specific candidate wasn't tracked (a rule failed, boundary broken prematurely, replaced by/skipped in favor of an overlapping higher-ranked one, or skipped because the cap was full and it didn't outrank the lowest-ranked tracked pattern).
