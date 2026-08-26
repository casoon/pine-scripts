# Elder Ray Pressure Engine

A research framework built on Alexander Elder's Bull Power / Bear Power concept — maximum buyer/seller excursion against a consensus-of-value line. Rather than committing to one "improved" formula, it exposes four distinct pressure engines, six consensus types, and five normalization modes as independent switches, so the definitions can be compared against each other on real data instead of assumed correct by design.

## Features

- Four pressure engines: **Classic Elder** (High/Low vs. consensus, can be simultaneously positive/negative), **Directional Elder** (excursion clamped to its own side only), **True Range Elder** (gap-aware, includes previous close), **Close-Weighted Elder** (directional excursion scaled by where the bar closed within its range)
- Selectable consensus line: EMA / RMA / SMA / WMA / HMA / VWMA, on any source
- Normalization: Raw, ATR, Average Range, Percent of consensus, or RMS — makes pressure comparable across instruments and volatility regimes
- Net pressure, gross pressure, and signed dominance (-1..+1, consistent across all four engines)
- Separately toggleable pressure impulse and acceleration (first and second change of net pressure)
- Percentile-based extreme detection, kept separate from exhaustion
- Exhaustion: extreme pressure fading while price still pushes further, with independent extreme-recency and price-push windows; simultaneous bull/bear exhaustion is reported as Dual Exhaustion
- Bar-close-confirmed pivot divergences between price and Bull/Bear Power, plotted on the confirmation bar rather than backdated to the pivot
- Whole-bar position relative to consensus (Above / Below / Straddle) — restores the information Directional and Close-Weighted Elder deliberately strip out of the pressure values themselves

## Why not just the classic formula?

In a strong trend, classic Elder Ray lets Bull Power and Bear Power both be positive (or both negative) at once — the whole bar traded on one side of the EMA. That's correct information about the bar's *position*, but it muddies a pure buyer-vs-seller pressure reading. Directional Elder removes that ambiguity by clamping each side to its own sign; the position information it discards is restored separately via the Position row instead of being silently lost.

## Engines vs. consensus vs. normalization

These three axes are deliberately orthogonal inputs, not a single fixed formula, so a pressure definition, its reference line, and its scaling can each be tested independently:

| Axis | Options |
|---|---|
| Engine | Classic Elder · Directional Elder · True Range Elder · Close-Weighted Elder |
| Consensus | EMA · RMA · SMA · WMA · HMA · VWMA |
| Normalization | Raw · ATR · Average Range · Percent · RMS |

## Exhaustion vs. extreme

Extreme pressure (top/bottom percentile over the lookback window) is not treated as a signal by itself — it usually just means a strong, healthy move. Exhaustion additionally requires the pressure to already be fading (Bull Power falling / Bear Power recovering) while price is still making new highs/lows. Extreme recency and the price-push comparison use independent windows. Signals are emitted only when the current bar closes; an outside bar satisfying both directions is classified as Dual Exhaustion rather than receiving an arbitrary directional priority.

## Signal timing

Exhaustion and divergence markers are confirmed at bar close. Pivot divergences become knowable `Pivot Right` bars after the actual pivot and are drawn on that confirmation bar, not retrospectively on the earlier pivot bar.

## Dashboard

Top-right table (toggle, default on): calculation model, regime (consensus slope vs. net pressure), bar position vs. consensus, pressure state (Expansion / Deceleration / Exhaustion / Balanced), Bull, Bear, Net, Gross pressure, dominance, and both percentile ranks.

## Scope

This indicator deliberately stops at pressure, exhaustion, and divergence — no composite score and no long/short signal. The goal is to first establish which engine/consensus/normalization combination actually discriminates on real instruments before building a decision layer on top of it.
