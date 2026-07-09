# CCI Advanced

CCI with pluggable smoothing, three scale modes, and rich visualization. The indicator builds a smoothed main line and a signal line from the raw CCI value, producing a histogram and a gradient line that reflects the current extreme level.

## Features

- **CCI core:** `ta.cci(src, len)` → averaged main line → signal line via the shared smoothing kernel
- **Pluggable smoothing:** EMA, SMA, RMA, WMA, SuperSmoother, T3, KAMA, JMA Approx — applied to both main and signal line
- **Three scale modes:** Classic (unbounded raw CCI), Clamp ±200 (hard clip), Adaptive ±100 (shared rescale using recent range)
- **Shared adaptive scale:** both CCI and signal are divided by the same lookback maximum, preventing phantom crossovers
- **Signals on raw values:** crossover detection uses the unscaled CCI so display mode changes never affect signal logic
- **4-state histogram:** rising/falling × positive/negative drives four opacity states
- **Gradient line:** `color.from_gradient()` from bull teal to bear pink based on oscillator level
- **Shadow fills:** 6-argument `fill()` places gradient shadows between the CCI line and zero
- **OB/OS zone fills:** configurable ±100 and ±200 levels with translucent fills
- **Signal markers:** configurable OB/OS-zone filter for crosses; optional zero-line cross dots
- **Stall/absorption layer:** single-timeframe detector for bars where the CCI cools/heats sharply while price barely moves; renders the contradicted cross as a small/faded triangle and fades the histogram, without touching the cross logic
- **Trend context line:** a slow CCI (longer length, same kernel) plotted faint behind the fast line — the price-dependent trend the fast CCI rests on; a cross against its side of zero is marked counter-trend (weak)
- **Sentiment Bar:** optional live label at the panel's right edge — a signed ±100 score for how far CCI sits inside its own OB/OS zone, plus a mini bar
- **Signal Quality:** optional 0-100 score next to each Bull/Bear Extreme marker — OB/OS-zone depth (50%) + context agreement (25%) + stall-free (25%)
- **Alert conditions:** bull/bear cross from extreme zone; zero-line cross up/down

## Scoring

The optional extreme filter requires the main CCI line to have visited the oversold (or overbought) zone within the last N bars before a cross qualifies as a signal. This eliminates mid-range crosses that lack mean-reversion context.

The Sentiment Bar and Signal Quality score (group 10, ported from Williams VIX Fix Advanced) are computed on the raw, unscaled CCI line and Overbought 1 / Oversold 1 levels — like the signal logic above, they stay consistent across all three Scale Modes. Quality labels are positioned on the displayed (scaled) line so they land at the correct screen height regardless of Scale Mode.

## Stall / Absorption

A cross is only as good as the price move behind it. The stall layer compares the CCI's change to the price's change over a short lookback: when the CCI cools (or heats) by at least `Min CCI Move` while price travels less than `Max Price Move (ATR)`, momentum has decoupled from price. The reading is symmetric — direction comes from the situation, not a hardcoded side: a falling CCI on flat price is absorption (bullish-leaning), a rising CCI on flat price is distribution (bearish-leaning). An extreme cross that runs into such a stall is drawn small and faded ("absorbed") instead of solid, and the histogram fades, so a cross that price never confirmed reads as weak at a glance. The cross detection itself is unchanged.

## Trend Context

The fast CCI (length 20) measures short-term deviation; a second, slower CCI (`Trend CCI Length`, default 100, same smoothing kernel) measures the deviation over a longer window and is plotted faint behind the fast line — the trend the fast line rests on. It serves two roles, both price-dependent and single-timeframe:

- **Support:** while the slow line holds its side of zero, a fast-line pullback toward zero is supported — the trend hasn't turned.
- **Counter-indication:** when the fast line fires an extreme cross against the slow line's side (e.g. a bearish cross while the context is still positive), the cross is counter-trend and is drawn as a weak/absorbed triangle.
- **Divergence wedge:** the area between the fast line and the context line stays empty while they travel together and fills only when they move in opposite directions — long color when the fast line cools into a rising trend (a supported dip), short color when it heats into a falling trend (an unsupported bounce). The fast slope is measured over a short lookback with a minimum-slope noise guard (so it stays robust on low timeframes like 15m), while the smooth slow line contributes its direction alone. Annotation only — it never gates a signal.

Stall and trend context are independent toggles (`useStall` / `useCtx`); a cross is weak if either flags it. With both off, every cross renders solid as before.

The panel uses two color languages: the **teal/pink** gradient on the fast CCI line encodes oscillator level (mean reversion — pink stretched up, teal stretched down), while the configurable **green/red Long/Short** colors drive the trend context line (long vs short regime) and the histogram (long vs short momentum), so directional bias reads at a glance independently of the level coloring.
