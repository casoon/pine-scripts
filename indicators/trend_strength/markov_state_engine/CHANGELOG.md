# Changelog

## v1.4.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.4.1 — 2026-06-29
- Alerts: messages standardized to `MSE · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.4 — 2026-06-28
- **Maturity / coiled-spring gauge**: surfaces the well-sampled TIMING axis the indicator was hiding. Typical dwell = `1/(1−Persistence)`; current dwell ÷ typical → Fresh / Mature / Extended / Overdue (with a ⚠). "Overdue" is descriptive (unusually long vs history), not a claim an exit is due. New "Markov State Extended" alert.
- **Timing vs direction split**: the readout now separates the robust TIMING signal (Maturity, from every in-state bar) from the thin DIRECTION signal (exit distribution, from few exits). The thin flag is relabelled `dir thin/ok`.
- **Edge typing adds Breakout**: an edge out of a neutral state (Compression / Chaos) is now `Breakout` (B↑/B↓) rather than mislabelled "Continuation"; Continuation is reserved for same-side weak states. Reversal unchanged.
- **Honest readout colour**: the label lights up only when something is actionable — green/red for a reliable directional bias, amber for a coiled (extended) state, grey otherwise. Replaces the always-coloured bias text that looked confident even at ~3 % reliability.

## v1.3 — 2026-06-28
- State classification priority fixed: extreme regimes (Chaos, Compression) are now tested **before** trend/weak, so a low-volatility / inefficient bar above the EMA is classified as Compression instead of a weak up-context.
- State is **debounced** (Min State Dwell, default 2): a raw classification must persist N bars before it is committed, removing the 1–2 bar flicker that previously inflated the Markov exit counts with noise.
- Renamed `Up Pullback` / `Down Pullback` → `Up Weak` / `Down Weak` — the bucket is "bullish/bearish context without a confirmed trend" (pullback, weak trend or drift), not a verified pullback.
- Edge typing: edges are now classified as **Reversal** (out of an opposing state) or **Continuation** (R↑/C↑ · R↓/C↓ markers + the readout `leanType`), so the signal says what it means.
- Readout adds a **thin-sample flag** (`Exits N (thin/ok)`) and reframes the tooltip: the percentages are how similar past states historically resolved, not a price prediction.
- `barsInState` guarded with `nz(...)`.

## v1.2 — 2026-06-28
- Readout is now an in-pane label at the last bar instead of a floating table — keeps the oscillator unobstructed (consistent with the other panel indicators); a tooltip explains each field.

## v1.1 — 2026-06-28
- Forecast is now **exit-conditional**: self-transitions (state→same state) are excluded from the Markov count, so the forecast answers "when this regime breaks, where does it go?" instead of restating the current state (first-order chains on sticky regimes are diagonal-dominant).
- New **Persistence** readout (share of self-transitions) — how sticky the current state is; pairs with Dwell time.
- Visual declutter: the three probability lines + reliability stepline are replaced by a single net forecast line `P(Bull) − P(Bear)` centred at 0, whose fill density encodes Reliability.
- Reliability now uses **directional (3-way) predictability** (Bull/Bear/Neutral, normalised over log 3) instead of the 5-bucket raw entropy — the raw entropy was structurally high (Up Trend vs Up Pullback never matters for direction) and pegged reliability near zero so no Edge ever fired.
- Watch markers are **off by default** and now fire only on a fresh lean (the net forecast line already shows the continuous lean) — removes the marker spam.
- Defaults retuned so Edges are reachable per state: Transition Lookback 300 → 500, Reliable Sample Count 40 → 20, Reliability threshold 45 → 40.
- Dashboard relabelled (Exit → Bull/Bear/Neutral, Exit destination, Persistence, Exits sampled).

## v1.0 — 2026-06-28
- Initial release: six-state regime classifier (Up Trend / Up Pullback / Compression / Down Trend / Down Pullback / Expansion-Chaos) driven by EMA context, ADX strength, path efficiency and ATR rank.
- First-order Markov next-state forecast for the current state with Laplace smoothing; aggregated into Bull / Bear / Neutral probabilities and an expected-next-state.
- Reliability gauge = sample adequacy × predictability (normalized entropy) — an Edge requires both directional confidence and reliability.
- Signal separation: stable hysteresis Bias, anticipated-transition Edge markers (windowed), visual-only Watch markers.
- Light-theme dashboard, state background coloring, forecast lines, edge / regime-change alerts and a debug log.
