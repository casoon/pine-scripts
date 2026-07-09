# Williams %R Advanced

Williams %R Advanced ports the CCI Advanced context view onto a Williams %R core. The native Williams %R scale is inverted (`-100` to `0`), so this script normalizes it to a readable `0-100` panel where `0` is oversold and `100` is overbought.

## Features

- **Williams %R core:** high/low range position normalized to `0-100` → averaged main line → signal line via the shared smoothing kernel
- **Bounded scale:** fixed 0-100 panel with 50 midline and configurable 80/20 OB/OS defaults
- **Signals on normalized values:** crossover detection uses normalized %R and its signal directly
- **4-state histogram:** rising/falling × positive/negative drives four opacity states
- **Gradient line:** `color.from_gradient()` from bull teal to bear pink based on oscillator level
- **Shadow fills:** gradient shadows between %R and the 50 midline
- **OB/OS zone fills:** configurable overbought and oversold bands
- **Signal markers:** configurable OB/OS-zone filter for %R/signal crosses; optional 50-cross dots
- **Stall/absorption layer:** flags bars where %R cools/heats sharply while price barely moves
- **Trend context line:** a slow Williams %R plotted faint behind the fast line; a cross against its side of 50 is marked counter-trend
- **Divergence wedge:** fills the area between fast %R and the trend context only when they move in opposite directions
- **Sentiment Bar:** optional live label at the panel's right edge — a signed ±100 score for how far %R sits inside its own OB/OS zone, plus a mini bar
- **Signal Quality:** optional 0-100 score next to each Bull/Bear Extreme marker — OB/OS-zone depth (50%) + context agreement (25%) + stall-free (25%)
- **Alert conditions:** bull/bear cross from extreme zone; 50-cross up/down

## Scale

Native Williams %R reads `0` at the top and `-100` at the bottom. This implementation uses the equivalent normalized range position:

```text
normalized %R = 100 * (source - lowest low) / (highest high - lowest low)
```

That keeps this tool consistent with the RSI/Stoch RSI/MFI advanced ports: 80 is overbought, 20 is oversold, and 50 is the long/short midline.

## Behavior

Williams %R is fast and extreme-driven. It is useful for quick mean-reversion reads, but can be noisier than RSI or TSI. The stall and trend-context layers are visual conviction tools; they do not suppress the base cross.
