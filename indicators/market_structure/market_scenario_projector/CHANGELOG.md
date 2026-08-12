# Changelog

## v0.6.7 — in progress
- Do not visually elevate a near-tie: `Minimum Dominance Gap %` (default: 8 pp) now requires a meaningful lead before a scenario branch is thick and opaque; the summary reports `Mixed` or `Clear edge` with the actual gap.
- Fixed rejection body-compression contamination: only barrier-touch candles now contribute, consistent with wick and failed-close evidence.
- Summary wording now distinguishes the raw upward/downward impulse from a bullish/bearish directional conclusion and labels the aggregate as context rather than setup quality.
- Recorder opening and resolution now run only on confirmed bars. Logs additionally include dominance gap and path geometry (target, failure, pullback and pullback-zone width in ATR) for later calibration.

## v0.6.6 — 2026-08-11
- Code audit (`indicator-code-audit` skill) after user asked to search for similar leftover inconsistencies to the Failure color/width issue. Three findings, all fixed:
  - Failure line color was still plain `color.gray` while its label had already moved to a warning-toned dark amber background (v0.6.5) — line now uses `#ff6f00` (repo warning accent), consistent with the label
  - Failure's dominant-state width/transparency (3 / 15%) topped out weaker than Direct/Pullback's (4 / 8%) — a leftover from the pre-v1.0 design where Failure was always the flat, de-emphasized scenario; a dominant Failure read is exactly as actionable as a dominant Direct/Pullback read, so all three now share identical tiers (4/2 width, 8%/45% transparency)
  - `recencyHalfLife` (Level Recency Influence) was documented as a "half-life" in the code comment, tooltip and README, but the formula used `math.exp(-age/recencyHalfLife)`, which reaches ~37% (1/e) at that age, not 50% — replaced with `math.pow(0.5, age/recencyHalfLife)`, a true half-life, so the code now matches what was already documented rather than the other way around

## v0.6.5 — 2026-08-11
- Reversed the v0.6.2/v0.6.4 approach after user report that green Direct text was still hard to read despite measuring 9.39:1 (well past AA): colored text at small sizes reads worse than its raw WCAG number suggests (anti-aliased colored glyphs look fuzzy, and green/red text is a known problem for red-green color blindness, which WCAG's luminance-only contrast formula doesn't account for). All three scenario chip labels (Direct/Pullback/Failure) now use white text (colorblind-safe, matches the summary box that was already confirmed very readable) on a solid scenario-tinted dark background instead of black background + colored text — measured 12.9–16.3:1 across all four combinations, comfortably past AAA

## v0.6.4 — 2026-08-11
- Measured actual WCAG contrast ratios for every label text/background combo (relative-luminance formula) instead of eyeballing screenshots: everything passes AA (4.5:1) except bearish Direct text — `#d50000` on the black chip measured 3.83:1, a real fail invisible in prior bullish-only screenshots. Replaced with `#ff5252` (6.58:1, comfortably past AA). All other combos: bullish `#00c853` 9.39:1, Pullback `#2979ff` 5.27:1, Failure `#b0bec5` 11.02:1, summary white-on-gradient-bg 12.9–16.3:1 across the full setup-quality range — all pass without changes.

## v0.6.3 — 2026-08-11
- Fixed the actual root cause of the label contrast complaint: Pine's built-in `color.green` (HTML "green", `#008000`) and `color.blue` (`#0000FF`) are both low-luminance colors — fine for a thick opaque line, but poor contrast as small text on the new dark label backgrounds. `directColor`/`pullbackColor` now use brighter accents (`#00c853`/`#d50000` bullish/bearish, matching the repo's established dashboard accent colors, and `#2979ff` for pullback) instead of the Pine built-ins, fixing text contrast for the lines/boxes/labels that all share these variables

## v0.6.2 — 2026-08-11
- Scenario label contrast + symbolism, per user report ("Direct 32.4%" chip was barely readable at low dominance-fade transparency): Direct/Pullback/Failure labels now use a dark, fully opaque background (independent of the line's dominance-based fade) with bright accent-colored text instead of a tinted translucent background with white text; added a Failure label (previously line-only) for symmetry with Direct/Pullback
- Added direction (▲/▼) and scenario (↩ Pullback, ✕ Failure) symbols to labels and the summary text for faster at-a-glance reading, replacing plain text-only lines
- Setup Quality now shown as a 10-segment block-character bar (`▰▰▰▰▰▰▱▱▱▱ 57%`) instead of `Setup: 57/100`
- Summary label background now blends from neutral dark gray to a saturated dark green/red (via `color.from_gradient`) based on Setup Quality and direction — color itself now signals strong vs. weak long/short, staying dark throughout so white text keeps full contrast

## v0.6.1 — 2026-08-11
- Summary label contrast fix: background changed from 15%-transparent to fully opaque black (was letting gridlines/dashed reference lines bleed through and wash out the text), text size bumped from `size.small` to `size.normal` for readability, per user report from a real chart screenshot

## v0.6.0 — 2026-08-11
- Objective outcome definition (roadmap v0.5) + historical scenario recorder (roadmap v0.6): new `ScenarioCase` type tracks each fresh setup bar-by-bar from the bar after it forms, resolving as Direct / Pullback / Failure / Unresolved (window = `Projection Bars`) using only each bar's own OHLC — no lookahead; resolution priority within a single bar is Failure > Pullback-touch > Target (documented pessimistic approximation, Pine has no intrabar sequencing)
- New `Enable Outcome Recorder` toggle (off by default) logs entry feature scores + outcome via `log.info()` on resolution, for offline calibration analysis; no effect on scoring or display when off

## v0.5.0 — 2026-08-11
- Scenario tree display (roadmap v1.0): replaced independent per-scenario width thresholds with relative dominance ranking — the single highest-weight scenario of the three now draws thick and opaque, the other two thin and faded, instead of each scaling its own width against separate fixed thresholds; Failure legs now also scale with dominance instead of a hardcoded width of 1

## v0.4.0 — 2026-08-11
- Pullback zone: `projectedPullback` is no longer a single price — structural support/resistance, ATR-expected retracement (`Fallback Pullback ATR`) and impulse Fib retracement (new `Impulse Retracement Ratio` input, default 0.382) now converge on a zone drawn as a shaded box; the anchor price for target/failure search still prefers the structural candidate when available

## v0.3.0 — 2026-08-11
- Level clustering (v0.2): unified level-quality function now clusters nearby pivots into a zone (`zoneLow`/`zoneHigh`) instead of scoring a single price, with recency-weighted touch quality (`Level Recency Influence` input) so old repeated touches count less than fresh ones; barrier zone drawn as a shaded box (`max_boxes_count` added), dashed line kept for the exact anchor price
- Rejection/exhaustion evidence (v0.3): new candle-based rejection score (wick rejection, failed closes, body compression) at bars that actually touched the barrier within the last `Rejection Lookback Bars`, feeding into all three scenario weights with rebalanced weights (`Rejection Touch Distance ATR` / `Rejection Lookback Bars` inputs); added to the internal metrics debug readout
- Fixed CE10156 compile error hit on first TradingView paste of v0.1.0 (~25 sites): outside enclosing parentheses, Pine v6 rejects continuation lines indented by a multiple of 4 spaces — opening brackets moved onto the initiating `=`/`:=` line throughout

## v0.1.0 — 2026-08-11
- Initial release: impulse strength/efficiency/acceleration scoring, HH/HL vs. LH/LL structure bias, lookback-bounded support/resistance search with touch-count quality, three heuristic scenario weights (Direct Continuation / Pullback Continuation / Failure) normalized to 100%, projected two-leg scenario lines + decision levels + summary label, setup quality gate, optional internal metrics debug readout
