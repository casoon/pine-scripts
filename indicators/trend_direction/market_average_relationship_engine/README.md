# Market–Average Relationship Engine

Evaluates the relationship between price and one consistently selected moving-average family — the MA is treated as a market reference, not as a standalone crossover signal. Six diagnostic dimensions (Trend, Respect, Extension, Compression, Acceleration, Exhaustion) feed a bounded relationship oscillator and a set of confirmed events (pullback, momentum release, do-not-chase, exhaustion, relationship break, divergence, turn from extreme).

## Features

- One MA family at a time (EMA, SMA, WMA, HMA, VWMA, RMA, DEMA, TEMA, ALMA), freely settable length and source — no JMA, since an unlicensed approximation would misrepresent the proprietary Jurik implementation
- Six diagnostic scores, each 0–100: **Trend** (MA slope + price side + persistence of both + price efficiency + direction agreement), **Respect** (historical hit rate of price reactions around the MA, confidence-weighted by sample count), **Extension** (ATR distance from the MA blended with statistical rarity vs. its own history), **Compression** (share of recent bars near the MA + ATR contraction), **Acceleration** (separation velocity + MA-slope acceleration + return acceleration), **Exhaustion** (extension gated by efficiency decay, opposing wicks, stalled progress, and fading acceleration)
- Relationship oscillator (−100..+100): signed Trend quality reduced by an Extension/Exhaustion quality penalty — extension and exhaustion degrade relationship quality but do not flip its sign
- Twelve-state classification: MA Compression, Healthy/Developing Bullish/Bearish, Bullish/Bearish Acceleration, Bullish/Bearish Do Not Chase, Bullish/Bearish Exhaustion Risk, Neutral/Unstructured
- Confirmed event engine: Pullback (PB — trend + respect + prior extension + reaction candle + bounded exhaustion), Momentum Release (M — compression release with slope/acceleration/efficiency agreement), Do Not Chase (! — extension crosses the risk threshold, not a reversal signal), Relationship Broken (BR — sustained opposite-side acceptance + fading MA slope, not a single MA cross), per-family signal cooldown
- Divergence (D): regular bullish/bearish divergence between confirmed price pivots and the relationship oscillator at the matching prior pivot (price lower low vs. relationship higher low, or the mirror on highs) — an informational event, never a gate on the events above
- Turn From Extreme (T): fires when the relationship line has recently touched a deep low/high and is now confirmed rising/falling off it, pivot-free — reads as a new trend starting or an existing extended trend recognizably losing steam, depending on what preceded it
- Optional MA line and event markers on the price chart (`force_overlay`) alongside the oscillator pane, all at `size.tiny`
- Hover tooltips on every event marker with the full six-score readout, ATR distance, MA slope, and Respect sample count/hit rate; the tooltip carrier itself is fully transparent so it never draws a second, larger shape on top of the visible marker; all diagnostics additionally routed to the Data Window
- Alerts for each event direction plus a combined "any MARE event" alert
- `@strategy-config` block for `scripts/build_strategies.py`, generating [`strategies/market_average_relationship_engine/market_average_relationship_engine_strategy.pine`](../../../strategies/market_average_relationship_engine/market_average_relationship_engine_strategy.pine) — see Strategy below

## Strategy

The generated strategy enters long/short on Pullback or Momentum Release only — both are continuation setups already gated on an established, quality-checked trend. Divergence and Turn From Extreme are deliberately excluded from entries: mixing those reversal-style, early signals into the same OR'd trigger as the continuation setups would blend two different market models into one signal, which this repo's indicator-design rules treat as an anti-pattern. The stop is a plain per-bar trailing envelope anchored to the reference MA itself (`ma ∓ stopAtrMultInput × ATR`), matching the indicator's own "MA as market reference" framing rather than a generic chandelier/highest-lowest stop. Not yet backtested — see `strategies/market_average_relationship_engine_strategy_assessment.md`.

## Design rules

- Extension is not treated as trend strength — a far-extended price can remain fully directional while being a poor new entry (Do Not Chase vs. reversal are kept separate)
- All events confirm on closed bars by default (`confirmedOnlyInput`); no future bars or lookahead are used anywhere in the score model
- Respect scores regress toward neutral (50) when the historical sample count is low, instead of reporting a misleadingly confident hit rate
- Price pivots are used for exactly one purpose — detecting the Divergence event itself — and stay a diagnostic reference there; they never gate, grade, or dedup the Pullback/Momentum/Do Not Chase/Exhaustion/Relationship Broken events, which stay pivot-free. Turn From Extreme is likewise pivot-free by design (rolling extreme + confirmed `ta.rising`/`ta.falling` turn, not a swing pivot)

## Status

v1.2.0 is a complete build with plausible starting thresholds, not an empirically calibrated model. Defaults should be validated across instruments, timeframes, and market phases before relying on the event signals. The generated strategy has not been backtested yet.
