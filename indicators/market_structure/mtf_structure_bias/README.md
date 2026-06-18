# MTF Structure Bias

Classifies market structure across four timeframes using pure price geometry — no oscillators, no momentum indicators. For each timeframe, it compares the current highest high and lowest low against the same values `N` bars ago: both rising = bullish structure (+1), both falling = bearish structure (−1), otherwise mixed (0). A weighted sum of all four TF states produces a confluence score from −100 to +100, with higher timeframes weighted more. The result is structural alignment, not oscillator alignment — a different layer of confluence than `mtf_stochrsi_pair_score`.

## Features

- **Structural state per TF**: Bull (HH+HL), Bear (LH+LL), Mixed — no smoothing, no oscillators
- **Four timeframes**: current chart + three configurable HTFs (defaults: 60m, 240m, Daily)
- **Weighted score**: −100 to +100, HTF3 = 2.0×, HTF2 = 1.5×, HTF1 = 1.0×, current = 0.5×
- **Score plot**: color-coded line with bull/bear zone hlines at ±60
- **Dashboard**: per-TF state and weight column, overall score row

## Settings

| Group | Setting | Default | Purpose |
|---|---|---|---|
| Timeframes | HTF 1 | 60 | First higher timeframe |
| Timeframes | HTF 2 | 240 | Second higher timeframe |
| Timeframes | HTF 3 | D | Third higher timeframe |
| Structure | Lookback Period | 20 | Bars for highest/lowest; also the comparison offset |
| Display | Show Dashboard | On | Toggle the info table |

## Scoring

The lookback period serves a dual purpose: it defines the window for `ta.highest(high, N)` and `ta.lowest(low, N)`, and it sets the comparison offset (`hh > hh[N]`). A longer period produces fewer structure state changes — more suitable for HTF bias; a shorter period tracks structure more responsively.
