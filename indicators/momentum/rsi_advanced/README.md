# RSI Advanced

RSI Advanced ports the CCI Advanced context view onto a bounded RSI core. It keeps RSI as a direct 0-100 momentum oscillator, then adds a smoothed signal line, trend context, stall/absorption, cross conviction, divergence wedges, and separate level-vs-direction color language.

## Features

- **RSI core:** `ta.rsi(src, len)` → averaged main line → signal line via the shared smoothing kernel
- **Bounded scale:** fixed 0-100 panel with 50 midline and configurable 70/30 OB/OS defaults
- **Signals on raw bounded values:** crossover detection uses RSI and its signal directly
- **4-state histogram:** rising/falling × positive/negative drives four opacity states
- **Gradient line:** `color.from_gradient()` from bull teal to bear pink based on oscillator level
- **Shadow fills:** gradient shadows between RSI and the 50 midline
- **OB/OS zone fills:** configurable overbought and oversold bands
- **Signal markers:** configurable OB/OS-zone filter for RSI/signal crosses; optional 50-cross dots
- **Stall/absorption layer:** flags bars where RSI cools/heats sharply while price barely moves
- **Trend context line:** a slow RSI plotted faint behind the fast line; a cross against its side of 50 is marked counter-trend
- **Divergence wedge:** fills the area between fast RSI and the trend context only when they move in opposite directions
- **Sentiment Bar:** optional live label at the panel's right edge — a signed ±100 score for how far RSI sits inside its own OB/OS zone, plus a mini bar
- **Signal Quality:** optional 0-100 score next to each Bull/Bear Extreme marker — OB/OS-zone depth (50%) + context agreement (25%) + stall-free (25%)
- **Alert conditions:** bull/bear cross from extreme zone; 50-cross up/down

## Scoring

The optional extreme filter requires the RSI line to have visited the oversold or overbought zone within the last N bars before a signal-line cross qualifies as a triangle signal.

The Sentiment Bar and Signal Quality score are a separate, optional layer (group 8, ported from Williams VIX Fix Advanced): the Sentiment Bar reads current extremity live, the Signal Quality score grades each individual cross.

## Trend Context

The trend context line is a slower RSI using a longer length. Above 50 it supports long-side pullbacks; below 50 it supports short-side bounces. Crosses against that side render as weak/faded triangles, without changing the underlying cross logic.

## Defaults

RSI uses 70/30 as the default OB/OS pair because this variant is meant to be the clean baseline port. Users who want fewer but more stretched signals can move the levels to 80/20.
