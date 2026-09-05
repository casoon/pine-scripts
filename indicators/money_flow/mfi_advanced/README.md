# MFI Advanced

MFI Advanced ports the CCI Advanced context view onto a Money Flow Index core. It keeps MFI as a bounded 0-100 money-flow oscillator, then adds a smoothed signal line, trend context, stall/absorption, cross conviction, divergence wedges, and separate level-vs-direction color language.

## Features

- **MFI core:** manual MFI calculation → averaged main line → signal line via the shared smoothing kernel
- **Exchange-only volume gate:** symbols without real trade volume (`syminfo.volumetype` is not `base`/`quote`) get no MFI output at all — no neutral placeholder, no fallback computation
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

## Instrumente

MFI is inherently volume-weighted (typical-price × volume flow ratio) — there is no meaningful MFI without real trade volume.

- **Valid:** Futures, stocks, and crypto exchanges — instruments where `syminfo.volumetype` reports `base` or `quote` (real trade volume)
- **Invalid:** CFDs (including `CAPITALCOM:NATURALGAS`), Forex, and most Indices — these report `tick`/`n/a` volume, which is not a real flow measure

On an invalid instrument the indicator produces no MFI line, no signal/alert conditions, and no scores — every volume-dependent value gates to `na` and the panel goes blank except for a one-time "benötigt echtes Handelsvolumen" warning label on the last bar showing the detected `syminfo.volumetype`.

**Reference-market variant (documented, not implemented):** MFI is a pure oscillator with no absolute price level, so a reference-market MFI (e.g. computed from `NYMEX:NG1!` volume while charting `CAPITALCOM:NATURALGAS`) would at least avoid the price-mixing problem that an anchored VWAP would have. But per `DATA_VALIDITY.md` §4.1, a cross-symbol `request.security()` call inside a single indicator is the exception, not the default — the added latency, session-mismatch, and request-budget cost of a per-indicator reference request isn't justified when the framework's own guidance is to route any reference-market context through one shared context module rather than duplicating it per script. Not implemented here.

## Stall / Absorption

The stall layer compares MFI's change to price's ATR-normalized change over a short lookback. If MFI cools or heats by at least `Min MFI Move` while price moves less than `Max Price Move (ATR)`, money-flow momentum has decoupled from price. A contradicted cross still fires, but renders as a small faded triangle.

## Trend Context

The trend context line is a slower MFI using a longer length. It is single-timeframe and serves two visual roles:

- **Support:** while the slow line holds above 50, a fast pullback can be read as a supported dip; while it holds below 50, a fast bounce can be read as unsupported.
- **Counter-indication:** a fast extreme cross against the slow line's side of 50 renders weak.
- **Divergence wedge:** the area between fast MFI and slow context fills only when they move in opposite directions, using long color for a supported dip and short color for an unsupported bounce.

The panel uses two color languages: teal/pink encodes oscillator level, while green/red Long/Short colors drive the trend context line, histogram, and divergence wedge.
