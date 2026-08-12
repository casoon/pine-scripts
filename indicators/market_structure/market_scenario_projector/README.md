# Market Scenario Projector

Splits "what happens next" into three explicit forward scenarios instead of a single directional call. From the currently active impulse it measures strength, path efficiency and acceleration, checks whether swing structure (HH/HL vs. LH/LL) agrees with that impulse, clusters nearby pivots into a support/resistance zone, and scores candle-based rejection/exhaustion evidence at that zone. Those readings are combined into three scenario scores — direct continuation/breakout, pullback-then-continuation, and structural failure — normalized to percentages and drawn as projected paths into the future.

## Features

- Impulse Strength — current move size relative to ATR
- Efficiency — how directly price traveled (net displacement vs. total path)
- Acceleration — recent vs. prior half-impulse velocity (speeding up or slowing down)
- Swing Structure Bias — HH/HL vs. LH/LL alignment from stored pivots, checked against the current move direction
- Level Zone / Proximity — nearby pivots within `Level Cluster Width ATR` of the nearest barrier are merged into a zone, scored by recency-weighted touch count (`Level Recency Influence`) instead of a flat count, bounded by `Structure Lookback` and `Maximum Level Distance ATR`
- Rejection / Exhaustion Evidence — over the last `Rejection Lookback Bars`, scores wick rejection, failed closes and body compression at bars that actually touched the barrier (within `Rejection Touch Distance ATR`)
- Pullback Zone — structural support/resistance, ATR-expected retracement (`Fallback Pullback ATR`) and impulse Fib retracement (`Impulse Retracement Ratio`) converge on one zone instead of a single price
- Three scenario scores normalized to 100%, each drawn as a two-leg projected line (now → decision point → target) from a single shared origin, forming a scenario tree
- Dominance-ranked display — the single highest-weight scenario draws thick and opaque, the other two thin and faded, so the chart doesn't read as three equally-weighted lines
- Barrier and pullback zones drawn as shaded boxes (zone bounds) with a reference line at the anchor price, not just a single line
- Context gate — no projection is drawn until the combined score clears `Minimum Context Quality`; it is not a trade-quality or probability measure
- Optional internal metrics readout (`Show Internal Metrics`) for reading the raw component scores behind a projection
- Optional outcome recorder (`Enable Outcome Recorder`) — tracks each fresh setup forward bar-by-bar to resolution and logs entry features + outcome via `log.info()`, for offline calibration of the currently heuristic weights

## Scoring

| Component | Feeds |
|---|---|
| Impulse Strength | Direct (+), Pullback (+), Failure (as 1−Impulse) |
| Efficiency | Direct (+), Pullback (+), Failure (as 1−Efficiency) |
| Acceleration | Direct (+), Pullback (as 1−Acceleration), Failure (as 1−Acceleration) |
| Structure Alignment | Direct (+), Pullback (+), Failure (as 1−Structure) |
| Level Quality | Direct (as 1−Quality, weak barrier favors breakout), Pullback (+), Failure (+, strong opposing barrier) |
| Level Proximity | Direct (+), Pullback (+) |
| Rejection Evidence | Direct (as 1−Rejection), Pullback (+), Failure (+) |

`directScore`, `pullbackScore` and `failureScore` are each a fixed weighted sum of the components above (weights sum to 1.0 per scenario), then normalized against their own total to produce the three percentages shown on the chart.

**These percentages are heuristic evidence weights, not historically calibrated probabilities.** "Direct 61%" means 61% of the current scenario evidence favors that path — it does not mean 61% of comparable historical setups resolved that way. See `todo.md` for the roadmap toward actual calibration.

## Level zones

Instead of scoring a single pivot price, the barrier's quality function clusters every stored pivot within `Level Cluster Width ATR` of the anchor level into one zone (`zoneLow`/`zoneHigh`) and weights each touch by recency — a touch from `Level Recency Influence` × the decay curve (half-life ≈ half of `Structure Lookback`) ago counts less than a fresh one, so a level tested repeatedly long ago doesn't score the same as one tested repeatedly right now. The zone is drawn as a shaded box; the dashed line still marks the exact anchor price used for target search. Additional level sources beyond pivots (breakout level, role reversal, gap, previous day/week high/low) and freshness-as-"used up" (rather than recency) are deliberately deferred — see `todo.md`.

## Rejection / exhaustion evidence

At bars whose high/low actually came within `Rejection Touch Distance ATR` of the barrier during the last `Rejection Lookback Bars`, the engine scores: how much of the bar's range was upper/lower wick beyond the body, how often the close failed to hold beyond the barrier, and how compressed the bodies of those *touching* bars are (exhaustion). This is a same-bar-reactive signal — two weak rejection candles at the barrier visibly shift weight from Direct toward Pullback/Failure, not just the slower-moving impulse/structure/level scores. Close location, engulfing and inside-bar detection are deliberately deferred — see `todo.md`.

## Pullback zone

The pullback reference is no longer a single price. Three candidates are computed — the structural support/resistance on the opposite side of the barrier (when one exists nearby), an ATR-based fallback (`Fallback Pullback ATR`), and a Fib-style retracement of the current impulse move (`Impulse Retracement Ratio`, default 0.382) — and their min/max span becomes the pullback zone (drawn as a shaded box). The anchor price used for target/failure search still prefers the structural candidate when available, falling back to the midpoint of the two estimates otherwise.

## Outcome recorder

When `Enable Outcome Recorder` is on, every fresh setup (a confirmed bar where `validSetup` turns true, or the direction flips while it is already true) opens a tracked case. Resolution also runs only on confirmed bars. From the *next* confirmed bar onward, that case is checked against its own target/failure/pullback-zone levels using only each new bar's OHLC — no lookahead, exactly like watching a setup play out live. It resolves as:

- **Direct** — target reached without the pullback zone ever being touched first
- **Pullback** — pullback zone touched at some point, then target reached
- **Failure** — the failure/invalidation level is touched before the target
- **Unresolved** — none of the above within `Projection Bars`

Within a single bar, if more than one of these could apply at once (Pine has no intrabar sequencing — a bar's high and low happened in some order the OHLC data doesn't reveal), Failure takes priority over a pullback-zone touch, which takes priority over Target. This is a documented pessimistic approximation, not a precise reconstruction.

On resolution, one `log.info()` line is emitted with the six entry component scores (impulse, efficiency, acceleration, structure, level quality, rejection), Context Quality, all three entry weights, dominance gap, target/failure/pullback distances and pullback-zone width in ATR, bars-to-resolve, symbol and timeframe — export via the Pine Logs panel for offline analysis. This is a data-collection tool only; nothing about scoring or display changes when it's on. See `todo.md` for what happens with the collected data (feature-bucketed conditional probabilities, confidence, regime split) once enough cases exist.

## Reading the chart

Three projected paths run from the current bar through a decision point (`Decision Point Bars`) to a target (`Projection Bars`):

- **Direct** (green/red, solid + arrow) — impulse carries through the nearest barrier toward the next level
- **Pullback** (blue, solid + arrow) — price retraces to the nearest support/resistance on the opposite side before resuming
- **Failure** (warning-orange, dashed) — retraces past the pullback level toward the next level in the opposite direction

All three legs share the same origin point (`xNow`, current close) — the tree branches from there. All scenarios use identical width/transparency tiers. A leading scenario is drawn thick (width 4) and at low transparency (8%) only when its lead over the runner-up clears `Minimum Dominance Gap %` (default: 8 pp); otherwise every shown path remains thin (width 2) and noticeably faded (45%) as a mixed state. A dominant Failure read gets the same visual weight as a dominant Direct or Pullback read. Scenarios below `Minimum Scenario Weight %` are not drawn at all. The shaded boxes mark the barrier and pullback zones; the dashed/dotted lines mark their anchor prices.

Every text label (Direct/Pullback/Failure chips and the summary box) uses white text on a solid, scenario-tinted dark background (dark green/red for Direct depending on direction, dark blue for Pullback, dark amber for Failure) — all measured 12.9–16.3:1 WCAG contrast, past AAA. An earlier version tried colored text on a black background instead; that measured "fine" by the raw contrast ratio too, but colored text at small sizes reads worse in practice than its number suggests (anti-aliased colored glyphs look fuzzy, and green/red is a known problem for red-green color blindness, which contrast-ratio math doesn't account for) — white text is used everywhere for that reason. Each chip still carries a symbol for fast, color-independent recognition: ▲/▼ for Direct (direction-aware), ↩ for Pullback, ✕ for Failure — the same symbols appear in the summary text. Context is shown as a 10-segment block bar (`▰▰▰▰▰▰▱▱▱▱ 57%`) instead of "57/100"; the summary calls the raw direction an upward/downward impulse rather than a bullish/bearish conclusion. The summary box's background itself blends from neutral dark gray to a saturated dark green/red as Context rises; it remains dark so white text keeps full contrast.

## What this is not

A directional signal or an entry trigger — it does not fire alerts, gate entries, or claim a single "correct" outcome. It's a scenario-weighting overlay meant to be read alongside the rest of the chart. See `todo.md` for what's still deliberately left out (additional level sources, close-location/engulfing/inside-bar rejection signals, historical outcome calibration).
