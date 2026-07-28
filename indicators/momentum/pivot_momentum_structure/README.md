# Pivot Momentum Structure

**TradingView:** https://de.tradingview.com/script/eWSJ4MNi/

Structure-oriented oscillator that uses confirmed price pivots as the authoritative anchor for both price and oscillator structure. Instead of hunting for oscillator-side pivots independently, the indicator classifies HH/HL/LH/LL on the price pivot bar, then evaluates divergences and momentum alignment against the highest-scoring pivot from a short recent history — not blindly against whichever pivot happened to come immediately before.

## Features

- **Oscillator selector**: RSI (default), WaveTrend, Stochastic RSI, CCI, Fisher Transform, TSI, Williams %R, or CMO — one dropdown
- **HH / HL / LH / LL classification**: price structure uses an ATR tolerance band (so the label and the divergence logic can never disagree); oscillator structure stays an exact comparison
- **Best-of-window anchor search**: each new pivot is compared against up to the last 8 same-type pivots (subject to Min/Max Pivot Distance); every candidate that clears the price- and oscillator-difference gates is scored (recency, oscillator rate-of-change, extreme-zone context, price distinctness) and the highest-scoring one is used — not just the immediately preceding pivot, and not just the nearest qualifying one either. The HH/HL/LH/LL *label* still always reflects the immediately preceding pivot (standard swing terminology); only the divergence/confirmation math uses the searched anchor.
- **Optional local-oscillator-extreme anchor**: instead of reading the oscillator exactly on the price-pivot bar (default), optionally use the oscillator's own local high/low within a small radius around it, so oscillator-pane labels/lines land on a real peak/trough. Currently experimental — see the note below and the debug log before relying on it.
- **Regular divergence**: price makes a HH while momentum makes a LH (bearish), or price makes a LL while momentum makes a HL (bullish). Near-equal price pivots (double top/bottom, opt-in) can *only* feed a regular divergence — never a hidden divergence or momentum alignment, since those require the price to have genuinely moved beyond tolerance.
- **Hidden divergence**: price/oscillator diverge in the trend-continuation direction (LH price / HH momentum, or HL price / LL momentum). Optional Trend Context Filter (off by default) requires the pivot to actually sit on the correct side of a Trend EMA — hidden bullish only above it, hidden bearish only below it — since hidden divergence is a continuation signal and is otherwise prone to firing during chop or against the prevailing trend.
- **Momentum alignment**: price and momentum structure agree (both HH, both HL, both LH, or both LL) — a distinct signal type from divergence (structure agreement, not a trade trigger)
- **Divergence Quality Score (0-100)**: informational only, never gates a signal — averages pivot spacing, oscillator-difference magnitude (relative to the oscillator's own rolling StDev), extremity past the OB/OS boundary, and trend context (overextension for regular divergence, alignment for hidden divergence). Shown as a suffix on the divergence label and dashboard status.
- **Structure presets**: Scalping / Intraday / Swing / Position / Major Structure set Pivot Left/Right, Min/Max Pivot Distance, and the ATR price filter together, based on the swing size you want to detect — or Custom for manual control
- **Oscillator-difference filter modes**: Reference Range % (default, comparable across oscillator types), Standard Deviation (adapts to the oscillator's own recent volatility), or Off
- **Quality filters**: minimum/maximum pivot distance, minimum price difference (ATR-relative), optional extreme-zone requirement for regular divergences, optional near-equal-pivot (double top/bottom) handling
- **Optional visuals**: signal line, oscillator/price divergence connector lines (drawn between the actual anchor pivot and the current one, not just the previous pivot), pivot guide lines between consecutive same-type pivots, chart-overlay pivot labels and divergence lines at actual price levels (via `force_overlay`, on by default — see note below)
- **Status dashboard**: split into a "Latest Pivot" block (oscillator type, last pivot type, current price/momentum structure, pivot age in bars) and a "Latest Event" block (latest divergence/alignment status, event age in bars, how many bars back the event's anchor pivot was) — kept visually separate because the two can reflect different points in time (see Anchor Selection)
- **Drawing retention limit**: oldest lines/labels are pruned once the configured maximum is reached (tracked separately per type)
- **Alerts**: regular bullish/bearish divergence, hidden bullish/bearish divergence, bullish/bearish momentum alignment, and a combined "any divergence" condition

## Structure Matrix

| Price | Momentum | Result |
|---|---|---|
| HH | LH | Regular bearish divergence |
| LL | HL | Regular bullish divergence |
| HL | LL | Hidden bullish |
| LH | HH | Hidden bearish |
| HH | HH | Bullish momentum alignment |
| HL | HL | Bullish momentum alignment |
| LH | LH | Bearish momentum alignment |
| LL | LL | Bearish momentum alignment |

## Pivot Confirmation Delay

Pivots require `Pivot Right` bars of confirmation before `ta.pivothigh`/`ta.pivotlow` returns a value. Every label, line, and alert therefore fires with that many bars of delay relative to the pivot bar itself, but is drawn back on the actual pivot bar (`bar_index - pivotRight`) rather than on the confirmation bar — so the chart shows the correct historical position, while alerts fire in real time on confirmation.

The same delay applies on every timeframe in bar terms, but not in real time: 7 bars is ~1h45m on a 15m chart, ~7 trading days on Daily. Structure Presets set a swing size, not a fixed real-time delay — pick the preset that matches the swing size you actually want to trade, not the chart you happen to have open.

## Structure Presets

| Preset | Pivot L/R | Min/Max Pivot Distance | Price Filter |
|---|---|---|---|
| Scalping | 5/5 | 8–60 | 0.15 ATR |
| Intraday | 7/7 | 10–100 | 0.15 ATR |
| Swing (default) | 8/8 | 12–120 | 0.10 ATR |
| Position | 10/10 | 15–160 | 0.10 ATR |
| Major Structure | 14/14 | 20–250 | 0.15 ATR |
| Custom | manual | manual | manual |

Presets are chart-relative, not timeframe-aware — the same preset detects a smaller real-time swing on a 5m chart than on Daily. That's intentional (it matches what's visibly happening on the chart you're looking at), but it means "Swing" on a 5m chart and "Swing" on Daily are not measuring the same real-world move.

## Oscillator Settings

| Oscillator | OB | OS | Midline | Notes |
|---|---|---|---|---|
| RSI (default) | 70 | 30 | 50 | uses **Source** input |
| WaveTrend | 60 | −60 | 0 | fixed hlc3 |
| Stochastic RSI | 80 | 20 | 50 | uses **Source** input |
| CCI | 100 | −100 | 0 | fixed hlc3 |
| Fisher | 1.5 | −1.5 | 0 | fixed hl2; signal = prior-bar value (Ehlers trigger) |
| TSI | 25 | −25 | 0 | uses **Source** input; long/short = TSI Long/Short Length |
| Williams %R | −20 | −80 | −50 | native −100..0 range; fixed high/low/close |
| CMO | 50 | −50 | 0 | uses **Source** input; `100 * (SumUp - SumDown) / (SumUp + SumDown)` |

The **Source** input only affects RSI, Stochastic RSI, TSI, and CMO — the others use their own conventional price inputs regardless of it (matching standard definitions for those oscillators).

ROC was deliberately left out: it is unbounded (no fixed OB/OS), and this indicator has no adaptive-band system like `oscillator_divergence_zones`'s Dynamic Zones — adding it without one would give the extreme-zone plot and the `requireExtremeZone` filter meaningless fixed thresholds.

MFI was also considered and rejected: it needs real volume, and CFD/index feeds (Capital.com, FOREX.com — the exact kind used to test this indicator) report `volume=0` throughout, which produces no signal at all rather than a merely degraded one.

## Oscillator Difference Filter

`Oscillator Difference Mode` controls how the minimum required oscillator-value difference between two pivots is computed:

- **Reference Range %** (default) — a percentage of the oscillator's fixed OB-OS reference range (e.g. 5% of RSI's 40-point range = 2.0). Comparable across oscillator types, but the "range" is a chosen reference zone, not the oscillator's actual measured value range.
- **Standard Deviation** — a multiple of the oscillator's own rolling standard deviation (`StDev Lookback` bars). Adapts to the current market and timeframe instead of using a fixed reference.
- **Off** — no minimum oscillator difference filter.

## Anchor Selection

Two independent anchor concepts are at play, deliberately kept separate:

1. **Structure label anchor** (HH/HL/LH/LL) — always the immediately preceding same-type pivot. This is standard swing terminology and stays intuitive regardless of what the divergence engine picks.
2. **Divergence/confirmation anchor** — the *highest-scoring* qualifying match from the last 8 same-type pivots (within Min/Max Pivot Distance). Every candidate that clears the price- and oscillator-difference gates is scored on four components, and the best-scoring one wins:
   - **Recency (40%)** — closer scores higher. This is deliberately the dominant weight: it keeps the result close to "nearest qualifying" as a baseline, so a distant candidate can only win by being clearly better on the other components.
   - **Oscillator rate-of-change (30%)** — the anchor/current oscillator difference *per bar* (not raw magnitude), relative to the oscillator's own rolling standard deviation. A sharp divergence over a few bars scores higher than the same magnitude stretched over many.
   - **Extreme-zone context (20%)** — whether the candidate pivot's own oscillator value sat in the OB/OS zone, a structurally significant point regardless of distance.
   - **Price distinctness (10%)** — the price difference relative to ATR tolerance; a minor tie-breaker.

   (An earlier version picked the *largest* oscillator-difference match with no distance weighting at all — that systematically favored distant pivots, since oscillators mechanically have more room to diverge over more bars, and could anchor a "divergence" 100+ bars back. Fixed in v2.4.0 by switching to nearest-qualifying. The scoring model above reintroduces a best-match search but keeps recency dominant and uses per-bar rate instead of raw magnitude specifically to avoid reintroducing that bias.)

Divergence/price connector lines are drawn between the actual anchor pivot and the current one — not the immediately preceding pivot — so the visual always matches what triggered the signal. The optional "Connect Oscillator Pivots" guide lines are a separate, purely visual feature that always connects consecutive pivots, regardless of the divergence anchor.

Because these two anchors can differ, the Price/Momentum structure shown for the current pivot and the fired event (e.g. "Hidden Bearish") can look inconsistent at a glance — e.g. the label says "EH" (near-unchanged vs. the immediately preceding pivot) while the status says "Hidden Bearish" (genuinely different vs. the older anchor pivot the search picked). This isn't a bug: it's why the dashboard splits "Latest Pivot" from "Latest Event" into separate blocks. The **Anchor** row and every pivot label's tooltip show how many bars back the anchor was and flag it explicitly when it isn't the immediately preceding pivot.

`Oscillator Anchor: Local Extreme` (opt-in, not default) lets the oscillator *value* used in all of the above come from its own local high/low within a small radius of the price-pivot bar, instead of the oscillator's exact value on that bar. Oscillator-pane labels and lines (structure label, oscillator divergence line, guide line) are drawn at the bar the local extreme actually occurred on, so they land on a real peak/trough of the plotted curve rather than mid-slope — mirroring how price pivots already work (`ta.pivothigh`/`ta.pivotlow` search the price series for its own local extreme; Local Extreme mode does the equivalent search on the oscillator series). Price-chart labels/lines are unaffected — they always use the true price-pivot bar.

**This changes the calculation, not just the drawing — verify before relying on it.** Local Extreme feeds a different oscillator value into the divergence math itself (not only into where things are drawn), and it always picks the most favorable reading within the search window. An early test switching the default to Local Extreme produced visibly fewer divergence signals; whether that's the mode correctly filtering out noise-driven false divergences from "Exact Pivot Bar," or the search window suppressing real ones, hasn't been verified yet. Default stays "Exact Pivot Bar" (the value read exactly on the price-pivot bar, no search involved) until that's settled — use `Enable Debug Logging` (see below) to compare both modes on the same data before switching.

**Why a divergence line can look like it doesn't touch a peak in "Exact Pivot Bar" mode:** the line endpoint sits exactly on the oscillator's value on the price-pivot bar — correct and exactly on the plotted curve, but that bar isn't necessarily where the oscillator itself peaked or troughed, since price and momentum don't always turn on the same candle. A fast oscillator (Stochastic RSI especially) can be mid-swing on the exact bar where price made its pivot. That's expected in this mode, not a bug — `Oscillator Anchor: Local Extreme` is the (currently unverified) fix if this matters more to you than exact-bar timing.

**Why oscillator-pane labels can look "wrong":** a label's Y-position in the oscillator pane is always the oscillator's value on the pivot bar — never a visual indicator of a high/low. An "LL" (price structure) can therefore sit right next to the top of the oscillator curve if momentum happened to be strong on that exact bar; that's not a bug, it's the whole point of a divergence. `Pivot Markers on Main Chart` and `Divergence Lines on Main Chart` (both on by default) show the same structure at actual price levels instead, which is the more intuitive read — the oscillator-pane versions (`Price Structure in Oscillator`, `Divergence Lines in Oscillator`) stay on independently and can be turned off if the duplication feels like clutter.

## Divergence Quality Score

Every fired divergence gets an optional 0-100 score (average of four 0-100 components), shown as a suffix on the label and dashboard status (e.g. "Bearish Divergence 78"). It never gates or filters a signal — informational only.

- **Pivot spacing** — 0 at Minimum Pivot Distance, 100 at Maximum Pivot Distance
- **Oscillator-difference magnitude** — the anchor/current oscillator difference relative to the oscillator's own rolling standard deviation (2× StDev = 100)
- **Extremity** — how far past the active OB/OS boundary the current oscillator value sits, as a percentage of the reference range
- **Trend context** — distance from the Trend EMA in ATR units; regular divergences score higher when they occur against an overextended trend (reversal setup), hidden divergences score higher when aligned with the trend (continuation setup)

## Debug Logging

`Enable Debug Logging` (off by default, Debug input group) logs a `PMS PIVOT` line to the Pine Logs panel on every confirmed pivot: price/oscillator values and structure classification, the anchor found (if any) with its distance/price/oscillator value/score (`anchorScore`), the oscillator's rolling standard deviation at that bar (`oscStDev`, used by the anchor score's rate-of-change component), every raw boolean the divergence/confirmation math is built from (`priceMadeHigherHigh`/`priceMadeLowerHigh`/`priceMadeEqualHigh`, `oscMadeHigherHigh`/`oscMadeLowerHigh`, the extreme-zone and trend-context gates), the final signal flags, the ATR-based price tolerance, the immediately-preceding same-type pivot's price/oscillator, the relevant gate thresholds (`allowEqual`, `minOscDiff`, `minPivotDist`, `maxPivotDist`), and the full same-type pivot history window the anchor search considered (`histIdx`/`histPrice`/`histOsc`, `|`-separated). Export it via the Logs panel (three-dot menu → Export logs) for offline verification.

`scripts/verify_pms_logs.py` in the repo consumes these exports and independently recomputes: the HH/HL/LH/LL price-structure classification, the highest-scoring anchor search (including the `anchorScore` value itself), and every implication between the logged booleans and the final divergence/confirmation flags — not just that a row is internally consistent, but that the anchor actually chosen is the one the algorithm should have picked given the logged history window. Run it with `python3 scripts/verify_pms_logs.py "path/to/pine-logs-PMS_*.csv"`.

## Relationship to Oscillator Divergence Zones

`oscillator_divergence_zones` covers regular/hidden divergence across nine oscillators with ATR zones, a quality score, and a retest counter. This indicator is narrower and structure-first: it adds WaveTrend, Stochastic RSI and Williams %R as sources (CCI/Fisher/TSI overlap with ODZ), explicitly labels HH/HL/LH/LL on both price and oscillator, and treats "structure agreement" (momentum alignment) as its own signal rather than only detecting disagreement (divergence). The two are being evaluated side by side; one may be archived depending on which structure model proves more useful in practice.

## Known Limitations (not yet implemented)

- No setup → trigger → invalidation lifecycle — a divergence/alignment is a structural read, not a staged signal with its own confirmation or invalidation condition.
- The best-of-window anchor search picks one highest-scoring anchor per pivot, not separately per divergence type — in principle a different (unpicked) candidate in the window could better satisfy a specific divergence type than the one chosen. In practice the four types are largely mutually exclusive for a given anchor, so this is a minor theoretical gap, not a common failure mode.
