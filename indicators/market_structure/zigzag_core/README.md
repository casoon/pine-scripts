# ZigZag Core

A configurable ZigZag foundation for structural chart analysis. Instead of a single depth-only pivot connector, it separates pivot detection, reversal significance, minimum bar spacing, and alternation into four independent filters, and supports genuine higher- AND lower-timeframe calculation.

## Features

- Separated Pivot Depth, Reversal Threshold, Backstep, and Alternation filters
- Percent, ATR, and Hybrid (max of both) reversal significance modes
- True higher-timeframe calculation with pivot-time projection onto the chart
- True lower-timeframe calculation via a manual `request.security_lower_tf()` pivot scan
- Confirmed ZigZag structure stays stable; the last leg is shown separately as developing
- HH/HL/LH/LL structure labels, pivot price, and swing-change % labels
- Live Retracement % of the forming reversal vs. the leg that preceded it
- Optional diagnostics marking rejected pivot candidates and why
- Optional recursive Level-2 ZigZag built from confirmed Level-1 pivots
- Optional independent Secondary ZigZag with its own Depth/Backstep/Deviation (Dual ZigZag)

## Pivot Engine

A pivot only becomes a confirmed ZigZag point once it passes all of the following, in order:

1. **Depth** — is this a confirmed local high/low at all?
2. **Alternation** — does it move the ZigZag in the correct HIGH → LOW → HIGH direction? A same-side pivot updates the current extreme instead of creating a duplicate.
3. **Backstep** — is it far enough (in calculation-timeframe bars) from the previous pivot?
4. **Deviation** — is the reversal move large enough per the selected Reversal Mode?

## Reversal Modes

- **Percent** — requires a fixed percentage reversal from the prior pivot. Classic and instrument-agnostic, but the same threshold means very different things on a low-volatility vs. high-volatility instrument.
- **ATR** — requires a reversal of at least N × ATR. Adapts automatically to the instrument's current volatility regime.
- **Hybrid** (default) — requires whichever threshold is larger: Percent or ATR. Prevents tiny absolute moves on low-price instruments while still adapting to volatility regime changes.

## Higher-Timeframe Mode

Setting "Calculation Timeframe" to a timeframe higher than the chart calculates pivots and ATR on that timeframe via `request.security()` + `ta.pivothigh`/`ta.pivotlow`, then projects the actual pivot bar time onto the chart with `xloc.bar_time`. This is a genuine HTF ZigZag, not a depth adjustment on the chart timeframe.

## Lower-Timeframe Mode

Setting "Calculation Timeframe" to a timeframe **lower** than the chart calculates a genuine LTF ZigZag too — but not via `request.security()`, which only returns one value per chart bar and would silently skip every lower-timeframe bar in between. Instead, `request.security_lower_tf()` returns every lower-timeframe bar inside the current chart bar; the script buffers those into persistent arrays and manually scans them for local extrema (`ta.pivothigh`/`ta.pivotlow` can't run over a manually assembled bar sequence, only the engine's own bars). Everything downstream — alternation, backstep, deviation, activePivot, the developing leg, drawing — is identical between the two paths; only the pivot source is swapped in.

Known simplification: at most one new high pivot and one new low pivot surface per chart bar, matching the higher-timeframe path's own grain. An extreme LTF ratio confirming more than one same-type pivot within a single chart bar only surfaces the most recent. The pivot buffers never shrink, bounded by Pine's 100,000-element array cap — an extreme ratio (e.g. 1s under a 1D chart) over a very long chart history could reach it.

## Developing Leg

The confirmed ZigZag never repaints, but pivot confirmation always lags Pivot Depth bars behind the actual extreme — the last confirmed pivot can be stale while price keeps moving. Two unconfirmed states cover that gap, only one active at a time:

- **Extension** — price is still pushing past the active pivot in its own direction (e.g. a new high above a confirmed high that hasn't been replaced yet). Instead of pausing and drawing a separate line, the active leg itself (line + label/dot) grows live to follow price.
- **Reversal** — once that extension stops, a dashed candidate leg is tracked from the active pivot instead of from the (possibly stale) confirmed pivot price.

This makes the inherently repainting nature of a ZigZag's last leg visible instead of indistinguishable from confirmed structure, and avoids the line freezing while price runs on.

### Active vs. confirmed pivot state

The script keeps two separate references for the last pivot, deliberately out of sync with each other:

- `lastPivotPrice`/`lastPivotTime` — the backend reference used only by the alternation/backstep/deviation gating math. Only ever set by an actual confirmed `ta.pivothigh`/`ta.pivotlow` event, so it always lags.
- `activePivotPrice`/`activePivotTime` — the single source of truth for the drawn ZigZag endpoint. Updated monotonically (never regresses) by live extension, by a same-side confirmed replacement, and by a confirmed reversal — so a new leg always starts exactly where the chart last visually ended, instead of snapping back to a stale confirmed price.

## Retracement %

While a reversal candidate is forming, a small label at its far end shows how deep the pullback is relative to the leg that preceded `activePivot` — e.g. `38.2%`. Toggle: "Show Retracement %". Hidden during a same-direction extension (there is no completed leg size to measure against yet).

## Diagnostics

"Show Rejected Pivot Diagnostics" (off by default) marks every confirmed pivot candidate that got rejected by Minimum Pivot Spacing or the Reversal Filter, labeled with which one blocked it. Use it to trace a specific missed swing to its exact blocking filter instead of blindly retuning Depth/ATR. It only covers post-Depth rejections — a candidate that never got confirmed by `ta.pivothigh`/`ta.pivotlow` in the first place produced no event to diagnose.

## Recursive ZigZag (Level 2)

"Show Recursive (Level 2) ZigZag" draws a second, coarser ZigZag built from the CONFIRMED Level-1 pivot stream instead of raw price — macro/subwave structure without a second indicator instance.

Because Level 1 already guarantees every point fed to Level 2 is a genuine local extremum, and the stream already strictly alternates HIGH/LOW, Level 2 skips the Depth step entirely and only re-applies Alternation/Backstep/Deviation:

- **L2 Minimum Pivot Spacing** — counted in confirmed Level-1 pivots, not bars.
- **L2 Deviation Multiplier** — reuses Level 1's Reversal Mode (Percent/ATR/Hybrid) settings, scaled up by this multiplier (default 2.0×), rather than exposing a whole separate set of Percent/ATR inputs.

Level 2 is confirmed-only by design — no live/developing leg the way Level 1 has one. A Level-2 pivot only exists once enough Level-1 pivots have alternated and deviated around it.

## Dual ZigZag (Secondary)

"Show Secondary ZigZag" runs a second, fully independent pivot engine — its own Pivot Depth, Minimum Pivot Spacing, and a Deviation Multiplier on top of the primary Reversal Mode settings — on the same Calculation Timeframe as the primary ZigZag. Typical use: a coarser "Structural" primary (large Depth) alongside a finer "Internal" secondary (small Depth, low multiplier).

Confirmed-only, like Level 2 — no live/developing leg, retracement label, or diagnostics for Secondary; those stay primary-only features. In Lower-Timeframe mode, Secondary reuses the primary engine's already-buffered lower-timeframe bar data with its own scan window, so it doesn't need a second `request.security_lower_tf()` call — only the higher/chart-timeframe path needs its own `request.security()` calls, since `ta.pivothigh`/`ta.pivotlow` are depth-specific and can't be shared between two different Pivot Depth settings.

## Open TODOs

None — the original backlog (see CHANGELOG for the full history) is complete. Further additions here would be new feature requests.
