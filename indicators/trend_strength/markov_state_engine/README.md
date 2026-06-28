# Markov State Engine

Markov State Engine classifies every bar into one of six market states and then treats those states as a first-order Markov chain. Over a lookback window it measures where the *current* state historically resolved **when it ended**, and turns that into a distribution over exit destinations. It is a **regime resolution map, not a price forecast** — the percentages describe how similar past states resolved, not a prediction of this instance. As a Quality/context layer (reversal-pipeline Stage 1) it never fires a raw trend trigger on its own; its directional output is a contextual bias, not a standalone entry.

## States

| # | State | Condition |
|---|---|---|
| 5 | Expansion/Chaos | high ATR rank but low efficiency |
| 2 | Compression | low ATR rank + low efficiency |
| 0 | Up Trend | up context + high trend (ADX & efficiency above threshold) |
| 3 | Down Trend | down context + high trend |
| 1 | Up Weak | up context, trend not confirmed (pullback, weak trend or drift) |
| 4 | Down Weak | down context, trend not confirmed |

Up/down context = close vs EMA plus EMA slope. "High trend" combines ADX strength and path efficiency, so ADX is used only as a strength sensor — never as direction. The table is ordered by **classification priority**: extreme regimes (Chaos, Compression) are tested first, so a low-volatility / inefficient bar above the EMA is Compression rather than a weak up-context. `Up Weak` / `Down Weak` is deliberately broad — directional context without a confirmed trend — rather than claiming a verified pullback.

The state is **debounced** (Min State Dwell): a raw classification must persist a few bars before it is committed, so 1–2 bar flutter does not inflate the Markov exit counts with noise.

## Forecast — exit-conditional

A first-order Markov chain on sticky regime states is diagonal-dominant: the most likely "next" state is almost always the *current* one, so a naive forecast just restates the present. To avoid that, the forecast is **exit-conditional** — self-transitions (state → same state) are excluded from the count and reported separately as **Persistence**. The remaining (exit) transitions over the lookback are Laplace-smoothed into destination probabilities, aggregated into:

- **Exit → Bull** = Up Trend + Up Weak
- **Exit → Bear** = Down Trend + Down Weak
- **Exit → Neutral** = Compression + Expansion/Chaos

So the read is "*when* this regime breaks, where does it go?" — the current state is not a valid destination (its bucket is forced to 0). **Persistence** (= share of self-transitions) tells you how sticky the state is and pairs naturally with the Dwell counter: high persistence + long dwell = the regime is holding, no exit imminent.

**Laplace smoothing (α)** adds a pseudo-count to each of the 5 valid destinations so a thin sample never reads a misleading 0% / 100%, and confidence degrades gracefully when data is sparse.

## Reliability — forecast quality

A high directional probability is worthless if the sample is tiny or the distribution is near-uniform. **Reliability** combines two factors:

- **Sample adequacy** — `min(1, exit samples / Reliable Sample Count)`
- **Predictability** — `1 − normalized Shannon entropy` of the **directional 3-way** distribution (Bull / Bear / Neutral, normalized over `log 3`); one dominant direction → high predictability, an even split → near zero. It is measured 3-way on purpose: that is what Bias and Edge decide on, and a 6-bucket raw entropy would be structurally high (splitting Up Trend vs Up Weak never matters for direction) and would peg reliability near zero.

Reliability = sample adequacy × predictability. An Edge requires both directional confidence *and* reliability. The reliability stays deliberately strict (entropy-based rather than a looser winner-margin): regime-exit distributions on most instruments are genuinely close to random, and a strict gauge keeps the readout from looking more certain than it is.

## Two axes — timing vs direction

The single most important thing to read off this indicator is that it has **two independent quality axes**, and they are *not* equally trustworthy:

- **Timing (robust)** — Persistence and **Maturity** are computed from *every* in-state bar, so they are well-sampled even when exits are rare.
- **Direction (usually thin)** — the exit distribution (Bull/Bear/Neutral, Reliability) hangs on the handful of times the state actually ended, so on sticky states it is statistically weak. The readout flags this as `dir thin` / `dir ok`.

**Maturity** is the coiled-spring gauge. Under a geometric dwell model the typical dwell of a state is `1 / (1 − Persistence)`; the current dwell divided by that typical value says how stretched the state is versus its own history:

| Ratio | Maturity |
|---|---|
| < 0.75× | Fresh |
| 0.75–1.5× | Mature |
| 1.5–2.5× | Extended ⚠ |
| ≥ 2.5× | Overdue ⚠ |

"Overdue" is **descriptive** — unusually long versus history — not a claim that an exit is mechanically due (pure Markov dwell is memoryless; real regimes are semi-Markov, so an empirically stretched dwell is informative). An Extended/Overdue state fires the **Markov State Extended** alert.

## Signals

Following the repo's signal-type separation:

- **Bias** — a *stable* directional state for the exit. It flips only when the dominant exit probability leads the next-best by the Bias Flip Margin (hysteresis), so it does not flicker on score noise.
- **Edge**, typed — when an exit lean clears both confidence and reliability and we are not already in that trend state. It is classified by the state it comes *out of*: **Reversal** (`R↑`/`R↓`, out of an opposing trend/weak state), **Breakout** (`B↑`/`B↓`, out of a neutral Compression/Chaos state — a resolution, not a continuation) or **Continuation** (`C↑`/`C↓`, out of the same-side weak state).
- **Watch** (gray dots, off by default) — marks a *fresh* low-conviction lean. Off by default because the net line already shows the lean continuously. Visual only, never wired into logic.

The readout `leanType` (Reversal / Breakout / Continuation) is informative even below the edge threshold.

## Plot

A single **net resolution line** `P(Bull) − P(Bear)`, centred at 0 — above zero = exits resolve up, below = down. The fill between the line and zero encodes **Reliability**: faint = thin/uncertain sample, solid = well-sampled and predictable. So direction and quality read at a glance without a second axis. The pane background is tinted by the current state.

## Features

- Six-state regime classifier — extremes (Chaos/Compression) first, then trend/weak; debounced to kill flicker
- Exit-conditional Markov resolution (self-transitions excluded) with Laplace smoothing
- Persistence + Maturity (coiled-spring) gauge — the robust timing axis, separate from the thin direction axis
- Entropy + sample-size Reliability gauge with a `dir thin/ok` flag
- Single net resolution line with reliability-encoded fill density
- Stable Bias with hysteresis; Reversal / Breakout / Continuation edge typing; visual-only Watch markers
- Honest readout colour — green/red reliable direction · amber coiled state · grey otherwise
- In-pane readout, state background coloring, edge / regime-change / extended-state alerts and a debug log

## Readout

In-pane label at the last bar: current state + bias + lean type, a Maturity line (rating · ratio · typical dwell), exit destination with its probability, persistence, dwell time, exits sampled (with `dir thin/ok` flag), the Bull / Bear / Neutral distribution, and Reliability. The label colour lights up only when something is actionable. A tooltip explains each field, the two axes, and the resolution-not-forecast framing.
