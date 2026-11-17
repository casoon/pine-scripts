# Changelog

## [Unreleased]

## v1.7.0 — 2026-11-17

### Added
- **Base rate:** the readout shows where the exits of all states went over the same lookback ("Any state", with n) next to the current state's exit distribution

### Changed
- **Thin samples hidden:** below the Minimum Exit Sample (40) the exit distribution and the Resolution Bias line are not shown at all instead of greyed; the readout shows only n. The separate "Sample" line is gone

## v1.6.0 — 2026-11-17
Rebuilt as a display: the script shows the current state and the historical exit statistic; it no longer issues directional verdicts. **Existing alerts must be recreated** — the alert set changed.

### Removed
- **Edge layer:** Bull/Bear Reversal, Breakout and Continuation Edge markers (`R↑ B↑ C↑ R↓ B↓ C↓`) and the Watch markers. The edge could come from neutral-state confidence through a held bias, and the entropy-based reliability gate made reversal edges practically unreachable, so the layer did not say what its name claimed
- **Alerts:** "Markov Bullish Edge" and "Markov Bearish Edge"
- **Inputs:** whole "4 · Signal" group — "Directional Confidence ≥ (%)", "Reliability ≥ (%)", "Bias Flip Margin (pp)" — and "Show Watch Markers"
- **Reliability gauge** (sample adequacy × entropy predictability) and the stable Bias; the readout headline no longer names a Bullish/Bearish bias or lean type

### Changed
- **Alerts:** "Markov Regime Change" renamed to "MSE State Changed"; new per-state alerts "MSE State → Up Trend / Up Weak / Compression / Down Trend / Down Weak / Expansion/Chaos"; "Markov State Extended" renamed to "MSE State Extended"
- **Resolution Bias line:** coloured by sign, drawn grey while the exit sample is below the minimum; fill has a fixed density instead of encoding reliability
- **Inputs:** "Reliable Sample Count" renamed to "Minimum Exit Sample" (default 40) — it now only flags a thin exit sample; group "3 · Markov Forecast" renamed to "3 · Transition Statistics", "5 · Display" to "4 · Display"
- **Readout:** headline shows state and bars in state; lines for Timing, past exit distribution with the most frequent destination, and sample size with Persistence. Amber only for an Extended/Overdue state
- **Header:** description states the display role; Data Contract block added

## v1.5.1 — 2026-10-02
- Oscillator scale no longer inherits the chart symbol's price precision (values like 80,0000 on 4-decimal symbols such as NATGAS) — shows 2 decimals

## v1.5.0 — 2026-07-08
- **EMA slope normalized by ATR**: `close vs EMA` context now uses `(ema − ema[5]) / ATR` against a new "EMA Slope Threshold (×ATR)" input, instead of a raw price-unit slope — makes up/down context scale-free across instruments and price levels.
- **Compression requires ATR Rank AND BB Width Rank**: a new Bollinger-width rank (independent of ATR) must also be below the Compression threshold, so a slow drift with normal bar-to-bar range but still-wide multi-bar bands no longer misclassifies as Compression.
- **Context-conditioned Compression matching**: the Markov row's historical source match is now keyed on a `contextState` that splits Compression into bullish/bearish/neutral flavors (by the same up/down context test), so exit history is drawn from analogous squeeze setups rather than "any Compression". The visible state and its label are unchanged (still six states) — only which historical bars count as a match got more specific. This further thins an already-thin sample on Compression, so expect Compression's exit count/Reliability to move (and possibly drop) versus v1.4.x.
- **Path efficiency via `ta.cum`**: replaced the per-bar summation loop with a cumulative-sum difference (`ta.cum(...) - ta.cum(...)[n-1]`) — identical result, cheaper per bar.
- **Readout restructured into Timing/Direction/Quality lines**: the headline now reads "No reliable direction" instead of naming a Bias/lean type whenever confidence or reliability falls short, so the text never implies more certainty than the color already shows. `dir thin/ok` relabelled to "below min sample"/"sample OK".
- **Plot renamed "Net Forecast" → "Resolution Bias"** and rendered as a stepline (it only changes value on a state exit, so it should read as holding-then-jumping, not as a continuously evolving curve). Line color is now gated by actionability (confident AND reliable) — bold green/red only when both clear their thresholds, muted grey otherwise, so line color is itself the verdict.
- **Background reworked**: tints only Compression/Chaos (not all six states, which flickered on every trend/weak change) and its intensity now scales with Maturity/`dwellRatio` instead of a fixed transparency — a fresh squeeze is barely tinted, an overdue one reads clearly more saturated.

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
