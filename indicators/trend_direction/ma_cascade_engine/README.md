# MA Cascade Engine

Moving averages are treated as a layered system rather than an isolated crossover signal. A Fast/Base/Anchor triplet cascades through four analytical layers — visual, feature, state, and decision — to classify the current market regime and gate entries/exits accordingly.

## Features

- Fast/Base/Anchor moving average triplet with selectable type per line (JMA, EMA, SMA, RMA, WMA, HMA, DEMA, KAMA) and three built-in presets (Responsive, Balanced, Structural) plus Custom
- Open Jurik-style (JMA) approximation — not the proprietary original
- ATR-normalised slope and curvature per MA
- Fast/Base and Base/Anchor separation tracking (expansion vs. compression) and entanglement detection (flat/overlapping MAs)
- Price extension gate to block entries after an overextended move
- MA Respect statistics — historical win rate of price bouncing off the Base MA vs. breaking through it, tracked separately for the Anchor MA
- Confirmed Anchor Rejection markers/alerts — fires when price touches the Anchor MA and holds a reaction move away from it
- Seven-state market classification: Bull/Bear Expansion, Bull/Bear Pullback, Overextended, Transition, Neutral Compression — any active Bull/Bear Expansion/Pullback state also carries a Fading attribute (Fast MA momentum decelerating + Fast/Base compressing)
- Signed −100..+100 score combining direction, slope, expansion, curvature, Base/Anchor MA respect, and cross-frequency quality
- Permission / Setup / Trigger / Exit signal layers with independent visibility toggles
- Small right-side status marker, offset from the current candle, muted when the active state is fading, with the full state/bias/score/permission/setup/MA-respect readout on hover

## Architecture

1. **Visual Layer** — Fast, Base, and Anchor curves plotted on the chart, optionally colour-coded by slope direction.
2. **Feature Layer** — Direction (MA stacking order), ATR-normalised slope, curvature (slope-of-slope), separation/expansion between MA pairs, price extension from the Fast MA, cross frequency (churn detection), and MA Respect (historical Base *and* Anchor MA reaction quality — same touch+reaction mechanic run against both lines independently).
3. **State Layer** — Combines the feature layer into one of seven mutually exclusive states: Bull/Bear Expansion (trending with confirmed slope + expansion), Bull/Bear Pullback (regime intact, price/Fast MA compressed toward Base), Overextended (regime intact but price stretched too far from Fast MA), Transition (no regime, but MAs are moving), Neutral Compression (everything else, including entangled MAs). Any active Bull/Bear Expansion/Pullback state additionally carries a **Fading** attribute — price closing back through the Fast MA while its curvature turns against the regime and the Fast/Base spread compresses — shown as a " (Fading)" suffix on the state readout, a muted status-marker colour, and a dedicated Bull/Bear Regime Fading alert on entry.
4. **Decision Layer** — Permission (directional regime is active, not entangled, not overextended), Setup (regime + proximity/compression near the Base MA), Trigger (Fast MA reclaim with rising/falling slope and curvature confirmation), and Exit (close through the Base MA against a flattening/reversing slope).

## Scoring

The score sums four core components before penalties: Direction (±30, MA stacking + price vs. Base), Slope (±25, Fast/Base/Anchor slope normalised against their minimum-slope thresholds), Expansion (±20, change in Fast/Base and Base/Anchor separation), and Curvature (±10, slope-of-slope on Fast and Base). Base Respect (±8), Anchor Respect (±5), and cross-frequency quality (±7, scaled by the sign of the pre-quality score so it reinforces rather than creates bias) are added on top. Overextension, entanglement, and extreme-volatility penalties then scale the raw score toward zero rather than flipping its sign.

## MA Respect vs. Anchor Rejection

The Anchor MA feeds the regime classification (Base vs. Anchor stacking) but has no reactive behaviour of its own by default — a price bounce off the Anchor line is otherwise invisible to the engine. Anchor Respect closes that gap with the same touch+reaction mechanic already used for the Base MA: a touch is logged, and `Reaction Horizon` bars later the engine checks whether price moved `Required Reaction Move` ATR away and held (no more than `Respect Invalidation` ATR of adverse penetration in between). A confirmed reaction fires a Bullish/Bearish Anchor Rejection marker and alert, and feeds both the Anchor Respect score component and the hover tooltip's "Anchor respected bullish/bearish" line.

The marker is drawn at the historical touch bar (`offset = -Reaction Horizon`), not the later confirmation bar, so it visually sits at the actual bounce. It is still a **retrospective confirmation**, not a forecast: it only asserts that *this specific past touch* held — it says nothing about what price does from the current bar forward. Its real value is statistical, feeding the Anchor Respect rate over the full `Respect Statistics Lookback` window, not as a standalone entry trigger.
