# TSI Advanced

TSI Advanced ports the CCI Advanced context view onto a True Strength Index core. It uses TSI's natural main/signal structure for cleaner cross and conviction reads, then adds trend context, stall/absorption, divergence wedges, and separate level-vs-direction color language.

## Features

- **TSI core:** double-smoothed momentum divided by double-smoothed absolute momentum, scaled to ±100
- **Zero-centered scale:** 0 midline with configurable ±25 default stretch levels
- **Native signal structure:** TSI main line plus pluggable smoothed signal line
- **4-state histogram:** rising/falling × positive/negative drives four opacity states
- **Gradient line:** `color.from_gradient()` from bull teal to bear pink based on TSI stretch level
- **Shadow fills:** gradient shadows between TSI and zero
- **OB/OS zone fills:** configurable positive/negative stretch bands
- **Signal markers:** configurable stretch-zone filter for TSI/signal crosses; optional zero-cross dots
- **Stall/absorption layer:** flags bars where TSI cools/heats sharply while price barely moves
- **Trend context line:** a slow TSI plotted faint behind the fast line; a cross against its side of zero is marked counter-trend
- **Divergence wedge:** fills the area between fast TSI and the trend context only when they move in opposite directions
- **Sentiment Bar:** optional live label at the panel's right edge — a signed ±100 score for how far TSI sits inside its own stretch zone, plus a mini bar
- **Signal Quality:** optional 0-100 score next to each Bull/Bear Extreme marker — stretch-zone depth (50%) + context agreement (25%) + stall-free (25%)
- **Alert conditions:** bull/bear cross from stretch zone; zero-cross up/down

## Scoring

The optional extreme filter requires the TSI line to have visited the negative or positive stretch zone within the last N bars before a signal-line cross qualifies as a triangle signal.

## Cross Conviction

TSI is slower and smoother than RSI or Williams %R, so this variant is aimed less at raw overbought/oversold reversal and more at cross quality. A cross contradicted by flat price or the slow TSI context remains visible, but renders weak/faded.

## Trend Context

The trend context line is a slower TSI using longer smoothing lengths. Above zero it supports long-side pullbacks; below zero it supports short-side bounces.
