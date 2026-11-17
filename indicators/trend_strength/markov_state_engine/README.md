# Markov State Engine

Markov State Engine classifies every bar into one of six market states and then treats those states as a first-order Markov chain. Over a lookback window it measures where the *current* state historically resolved **when it ended**, and turns that into a distribution over exit destinations. It is a **regime resolution map, not a price forecast** — the percentages describe how similar past states resolved, not a prediction of this instance. It is a display of where the market stands: it issues no entry signals or directional verdicts, and its alerts fire only on state-change events.

## States

| # | State | Condition |
|---|---|---|
| 5 | Expansion/Chaos | high ATR rank but low efficiency |
| 2 | Compression | low ATR rank AND low BB width rank + low efficiency |
| 0 | Up Trend | up context + high trend (ADX & efficiency above threshold) |
| 3 | Down Trend | down context + high trend |
| 1 | Up Weak | up context, trend not confirmed (pullback, weak trend or drift) |
| 4 | Down Weak | down context, trend not confirmed |

Up/down context = close vs EMA plus EMA slope, normalized by ATR (`(ema − ema[5]) / ATR` against an ATR-multiple threshold) so the test is scale-free across instruments and price levels. "High trend" combines ADX strength and path efficiency, so ADX is used only as a strength sensor — never as direction. Compression requires ATR Rank **and** an independent BB Width Rank to both be low, so a slow drift with normal bar-to-bar range but still-wide multi-bar bands no longer misclassifies as Compression. The table is ordered by **classification priority**: extreme regimes (Chaos, Compression) are tested first, so a low-volatility / inefficient bar above the EMA is Compression rather than a weak up-context. `Up Weak` / `Down Weak` is deliberately broad — directional context without a confirmed trend — rather than claiming a verified pullback.

The state is **debounced** (Min State Dwell): a raw classification must persist a few bars before it is committed, so 1–2 bar flutter does not inflate the Markov exit counts with noise.

## Exit distribution — exit-conditional

A first-order Markov chain on sticky regime states is diagonal-dominant: the most likely "next" state is almost always the *current* one, so a naive count just restates the present. To avoid that, the distribution is **exit-conditional** — self-transitions (state → same state) are excluded from the count and reported separately as **Persistence**. The remaining (exit) transitions over the lookback are Laplace-smoothed into destination probabilities, aggregated into:

- **Exit → Bull** = Up Trend + Up Weak
- **Exit → Bear** = Down Trend + Down Weak
- **Exit → Neutral** = Compression + Expansion/Chaos

So the read is "*when* this regime breaks, where does it go?" — the current state is not a valid destination (its bucket is forced to 0). **Persistence** (= share of self-transitions) tells you how sticky the state is and pairs naturally with the Dwell counter: high persistence + long dwell = the regime is holding, no exit imminent.

**Laplace smoothing (α)** adds a pseudo-count to each of the 5 valid destinations so a thin sample never reads a misleading 0% / 100%; with few exits the distribution stays closer to even.

**Context-conditioned matching for Compression.** Compression is not directionally uniform — a squeeze under a rising EMA and one under a falling EMA are different setups. The historical match that builds the row above is keyed on a `contextState` that splits Compression into bullish / bearish / neutral flavors (the same up/down context test used for state classification), so exit history is drawn only from analogous squeeze setups. Destination buckets, the visible state, and its label are unchanged — still the plain six-state model; only *which past bars count as a match* got more specific. This trades sample size for relevance: Compression's exit count is now smaller (split three ways), so its distribution is more often below the minimum exit sample than for the other five states.

## Two axes — timing vs exit direction

The indicator shows **two axes**, and they rest on very different sample sizes:

- **Timing (robust)** — Persistence and **Maturity** are computed from *every* in-state bar, so they are well-sampled even when exits are rare.
- **Exit direction (usually thin)** — the exit distribution (Bull/Bear/Neutral) hangs on the handful of times the state actually ended, so on sticky states it is statistically weak. The readout shows the exit count n; below the Minimum Exit Sample (default 40) the distribution is not shown, only n. Next to it stands the base rate: where the exits of all states went over the same lookback — a state's distribution only says something where it differs from that.

**Maturity** is the coiled-spring gauge. Under a geometric dwell model the typical dwell of a state is `1 / (1 − Persistence)`; the current dwell divided by that typical value says how stretched the state is versus its own history:

| Ratio | Maturity |
|---|---|
| < 0.75× | Fresh |
| 0.75–1.5× | Mature |
| 1.5–2.5× | Extended ⚠ |
| ≥ 2.5× | Overdue ⚠ |

"Overdue" is **descriptive** — unusually long versus history — not a claim that an exit is mechanically due (pure Markov dwell is memoryless; real regimes are semi-Markov, so an empirically stretched dwell is informative). Entering Extended/Overdue fires the **MSE State Extended** alert.

## Alerts

All alerts respect the "Alerts only on bar close (confirmed)" toggle (default on). They describe events, not trade calls:

- **MSE State Changed** — the debounced state changed
- **MSE State → Up Trend / Up Weak / Compression / Down Trend / Down Weak / Expansion/Chaos** — the state changed to that state
- **MSE State Extended** — the current state's dwell entered Extended/Overdue

## Plot

The **Resolution Bias** line — `P(Bull) − P(Bear)`, centred at 0 — is drawn as a **stepline**: it only changes value when the state exits, so it visibly holds flat rather than reading as a continuously evolving curve. It is the historical exit statistic for whichever regime is active right now, computed from past data only. Line colour follows the sign (green above zero, red below); the line is not drawn while the current state has fewer past exits than the Minimum Exit Sample.

The pane **background** tints only Compression and Chaos — the two neutral/extreme states — not all six, so trend/weak changes no longer flicker the pane. Its intensity scales with **Maturity** (`dwellRatio`): a fresh squeeze is barely tinted, an overdue one reads clearly more saturated, making the "how stretched is this regime" statement visible on its own.

## Features

- Six-state regime classifier — extremes (Chaos/Compression) first, then trend/weak; debounced to kill flicker
- Compression requires ATR Rank AND BB Width Rank agreement (dual squeeze check)
- EMA slope normalized by ATR — scale-free up/down context across instruments
- Exit-conditional transition counts, source-matched on a Compression-flavor context state, with Laplace smoothing
- Persistence + Maturity gauge — the timing axis, separate from the thin exit-direction axis
- Resolution Bias stepline, coloured by sign and hidden while the exit sample is below the minimum
- In-pane readout, Compression/Chaos background tinted by Maturity, state-change and extended-state alerts, debug log on state changes

## Readout

In-pane label at the last bar: a headline with the current state and bars in state, a **Timing** line (Maturity rating · ratio · typical dwell), a **Past exits** line (Bull/Bear/Neutral distribution with n and the most frequent exit destination, or only n below the minimum), an **Any state** line (base rate of all exits in the lookback, with n) and Persistence. The text turns amber only for an Extended/Overdue state. A tooltip explains each field and the resolution-not-forecast framing.
