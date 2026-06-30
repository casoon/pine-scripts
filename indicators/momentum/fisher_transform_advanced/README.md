# Fisher Transform Advanced

Fisher Transform Advanced ports the CCI Advanced context view onto a zero-centered Fisher Transform core. It is designed for clear turning-point and extreme reads, with trend context and conviction layers to make aggressive reversal behavior easier to judge.

## Features

- **Fisher core:** normalized source range → recursive Fisher Transform → averaged main line → signal line
- **Zero-centered scale:** 0 midline with configurable ±1.5 default extreme levels and ±3 zone boundaries
- **Signals on raw Fisher values:** crossover detection uses Fisher and its signal directly
- **4-state histogram:** rising/falling × positive/negative drives four opacity states
- **Gradient line:** `color.from_gradient()` from bull teal to bear pink based on Fisher extreme level
- **Shadow fills:** gradient shadows between Fisher and zero
- **OB/OS zone fills:** configurable upper/lower Fisher extreme bands
- **Signal markers:** configurable extreme-zone filter for Fisher/signal crosses; optional zero-cross dots
- **Stall/absorption layer:** flags bars where Fisher cools/heats sharply while price barely moves
- **Trend context line:** a slow Fisher Transform plotted faint behind the fast line; a cross against its side of zero is marked counter-trend
- **Divergence wedge:** fills the area between fast Fisher and the trend context only when they move in opposite directions
- **Alert conditions:** bull/bear cross from extreme zone; zero-cross up/down

## Scoring

The optional extreme filter requires the Fisher line to have visited the lower or upper extreme zone within the last N bars before a signal-line cross qualifies as a triangle signal.

## Reversal Bias

Fisher Transform is intentionally reversal-heavy. It can make turns and extremes clearer than RSI-style oscillators, but it can also react aggressively in noisy markets. The stall and trend-context layers are visual conviction tools; they do not suppress the base cross.

## Trend Context

The trend context line is a slower Fisher Transform. Above zero it supports long-side pullbacks; below zero it supports short-side bounces. Crosses against that side render as weak/faded triangles.
