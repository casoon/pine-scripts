# MFI Advanced

MFI Advanced ports the CCI Advanced context view onto a Money Flow Index core. It keeps MFI as a bounded 0-100 money-flow oscillator, then adds a smoothed signal line, trend context, stall/absorption, cross conviction, divergence wedges, and separate level-vs-direction color language.

## Features

- **MFI core:** manual MFI calculation → averaged main line → signal line via the shared smoothing kernel
- **No-volume fallback:** symbols with no usable volume return a neutral 50 MFI and suppress signal/alert conditions instead of crashing or producing false crosses
- **Bounded scale:** fixed 0-100 panel with 50 midline and configurable 80/20 OB/OS levels
- **Signals on raw bounded values:** crossover detection uses MFI and its signal directly, so display toggles never affect signal logic
- **4-state histogram:** rising/falling × positive/negative drives four opacity states
- **Gradient line:** `color.from_gradient()` from bull teal to bear pink based on oscillator level
- **Shadow fills:** gradient shadows between MFI and the 50 midline
- **OB/OS zone fills:** configurable overbought and oversold bands
- **Signal markers:** configurable OB/OS-zone filter for MFI/signal crosses; optional 50-cross dots
- **Stall/absorption layer:** flags bars where MFI cools/heats sharply while price barely moves; renders contradicted crosses as small/faded triangles and fades the histogram without touching cross logic
- **Trend context line:** a slow MFI plotted faint behind the fast line; a cross against its side of 50 is marked counter-trend
- **Divergence wedge:** fills the area between fast MFI and the trend context only when they move in opposite directions
- **Sentiment Bar:** optional live label at the panel's right edge — a signed ±100 score for how far MFI sits inside its own OB/OS zone, plus a mini bar
- **Signal Quality:** optional 0-100 score next to each Bull/Bear Extreme marker — OB/OS-zone depth (50%) + context agreement (25%) + stall-free (25%)
- **Alert conditions:** bull/bear cross from extreme zone; 50-cross up/down

## Scoring

The optional extreme filter requires the MFI line to have visited the oversold or overbought zone within the last N bars before a signal-line cross qualifies as a signal. This keeps mid-range noise out of the main triangle markers.

## Volume Handling

MFI requires volume. On instruments where `volume` is missing or zero across the MFI lookback, the indicator pins the raw MFI calculation to a neutral 50 and disables signal/alert conditions until volume becomes available. The panel remains usable as a visual placeholder, but no money-flow signal should be interpreted on no-volume symbols. The Sentiment Bar naturally reads 0 (balanced) in this state, since a neutral 50 MFI sits exactly on the midline.

## Stall / Absorption

The stall layer compares MFI's change to price's ATR-normalized change over a short lookback. If MFI cools or heats by at least `Min MFI Move` while price moves less than `Max Price Move (ATR)`, money-flow momentum has decoupled from price. A contradicted cross still fires, but renders as a small faded triangle.

## Trend Context

The trend context line is a slower MFI using a longer length. It is single-timeframe and serves two visual roles:

- **Support:** while the slow line holds above 50, a fast pullback can be read as a supported dip; while it holds below 50, a fast bounce can be read as unsupported.
- **Counter-indication:** a fast extreme cross against the slow line's side of 50 renders weak.
- **Divergence wedge:** the area between fast MFI and slow context fills only when they move in opposite directions, using long color for a supported dip and short color for an unsupported bounce.

The panel uses two color languages: teal/pink encodes oscillator level, while green/red Long/Short colors drive the trend context line, histogram, and divergence wedge.
