# Stoch RSI Advanced

Stoch RSI Advanced ports the CCI Advanced context view onto a bounded Stoch RSI K/D core. It keeps the fast K line and D signal readable as a standard 0-100 oscillator, then adds trend context, stall/absorption, cross conviction, divergence wedges, and separate level-vs-direction color language.

## Features

- **Stoch RSI core:** RSI → stochastic normalization → K smoothing → D signal via the shared smoothing kernel
- **Bounded scale:** fixed 0-100 panel with 50 midline and configurable 80/20 OB/OS levels
- **Signals on raw bounded values:** crossover detection uses K and D directly, so display toggles never affect signal logic
- **4-state histogram:** rising/falling × positive/negative drives four opacity states
- **Gradient line:** `color.from_gradient()` from bull teal to bear pink based on oscillator level
- **Shadow fills:** gradient shadows between K and the 50 midline
- **OB/OS zone fills:** configurable overbought and oversold bands
- **Signal markers:** configurable OB/OS-zone filter for K/D crosses; optional 50-cross dots
- **Stall/absorption layer:** flags bars where Stoch RSI cools/heats sharply while price barely moves; renders contradicted crosses as small/faded triangles and fades the histogram without touching cross logic
- **Trend context line:** a slow Stoch RSI plotted faint behind K; a cross against its side of 50 is marked counter-trend
- **Divergence wedge:** fills the area between K and the trend context only when they move in opposite directions
- **Sentiment Bar:** optional live label at the panel's right edge — a signed ±100 score for how far K sits inside its own OB/OS zone, plus a mini bar
- **Signal Quality:** optional 0-100 score next to each Bull/Bear Extreme marker — OB/OS-zone depth (50%) + context agreement (25%) + stall-free (25%)
- **Alert conditions:** bull/bear cross from extreme zone; 50-cross up/down

## Scoring

The optional extreme filter requires the K line to have visited the oversold or overbought zone within the last N bars before a K/D cross qualifies as a signal. This keeps mid-range noise out of the main triangle markers.

## Stall / Absorption

The stall layer compares K's change to price's ATR-normalized change over a short lookback. If K cools or heats by at least `Min Stoch RSI Move` while price moves less than `Max Price Move (ATR)`, momentum has decoupled from price. A contradicted cross still fires, but renders as a small faded triangle.

## Trend Context

The trend context line is a slower Stoch RSI, using longer RSI and stochastic lengths. It is single-timeframe and serves two visual roles:

- **Support:** while the slow line holds above 50, a fast pullback can be read as a supported dip; while it holds below 50, a fast bounce can be read as unsupported.
- **Counter-indication:** a fast extreme cross against the slow line's side of 50 renders weak.
- **Divergence wedge:** the area between fast K and slow context fills only when they move in opposite directions, using long color for a supported dip and short color for an unsupported bounce.

The panel uses two color languages: teal/pink encodes oscillator level, while green/red Long/Short colors drive the trend context line, histogram, and divergence wedge.
