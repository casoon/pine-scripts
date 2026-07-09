# ROC Advanced

ROC Advanced ports the CCI Advanced context view onto a classic percentage Rate of Change core. It focuses on momentum acceleration/deceleration and stall detection rather than pure overbought/oversold reversal.

## Features

- **ROC core:** percentage rate of change → averaged main line → signal line via the shared smoothing kernel
- **Zero-centered scale:** 0 midline with configurable positive/negative stretch defaults at ±5%
- **Signals on raw percentage values:** crossover detection uses ROC and its signal directly
- **4-state histogram:** rising/falling × positive/negative drives four opacity states
- **Gradient line:** `color.from_gradient()` from bull teal to bear pink based on positive/negative stretch
- **Shadow fills:** gradient shadows between ROC and zero
- **Signal markers:** configurable stretch-zone filter for ROC/signal crosses; optional zero-cross dots
- **Stall/absorption layer:** central to this variant; flags bars where ROC changes sharply while price barely moves
- **Trend context line:** a slow ROC plotted faint behind the fast line; a cross against its side of zero is marked counter-trend
- **Divergence wedge:** fills the area between fast ROC and the trend context only when they move in opposite directions
- **Sentiment Bar:** optional live label at the panel's right edge — a signed ±100 score for how far ROC sits inside its own stretch zone, plus a mini bar
- **Signal Quality:** optional 0-100 score next to each Bull/Bear Stretch marker — stretch-zone depth (50%) + context agreement (25%) + stall-free (25%)
- **Alert conditions:** bull/bear cross from stretch zone; zero-cross up/down

## Scale

This implementation uses classic percentage ROC:

```text
ROC = 100 * (source - source[length]) / source[length]
```

The default stretch levels are ±5%, intentionally configurable because raw ROC magnitude depends heavily on instrument, timeframe, and volatility. The panel has no fixed outer scale boundary — it autoscales to the actual ROC range so small-magnitude instruments aren't compressed near zero.

## Behavior

ROC is best read as momentum acceleration/deceleration. A large ROC move on flat ATR-normalized price can be a useful stall/absorption clue, while a slow ROC context above or below zero gives the fast cross a directional backdrop.
