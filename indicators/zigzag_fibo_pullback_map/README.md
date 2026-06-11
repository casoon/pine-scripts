# ZigZag Fibo Pullback Map

Confirmed ZigZag pivots with pullback-to-fibo labeling and a live fib fan on the current unfinished leg. The indicator labels every completed pullback at its turning point with the matched (or deepest reached) standard fibonacci ratio and tracks how the market reacted afterwards.

## Features

- Confirmed ZigZag pivot engine based on symmetric pivot detection (`ta.pivothigh`/`ta.pivotlow`)
- Pullback labels directly at completed turning points with standard-fibo color coding (0.236 / 0.382 / 0.500 / 0.618 / 0.786)
- Depth regime (Shallow / Normal / Deep / Extreme), pullback duration, efficiency and reaction tracking (HH/LL, Weak, Break)
- Live active-leg projection with fib fan, current-zone box and live retracement label
- Pullback zone engine: confluence zone from recent qualified pullbacks plus continuation/failure outlook
- Zone memory boxes for historical supportive / fragile / risk levels
- Pullback summary table (compact 5-column or full 7-column layout)

## Display presets

| Preset | Behavior |
|---|---|
| Minimal | ZigZag + compact labels only, no table, no zone boxes |
| Balanced | Compact labels with depth/cluster tags, key fan levels, 5-column table |
| Full | All label details, full fib ladder, reaction markers, zone memory, 7-column table |

## Pullback logic

A pullback is measured as leg C against the preceding impulse A→B. It is only labeled once the **next opposite pivot is confirmed**, so provisional pullback ends that later extend deeper are never labeled. Legs must pass a minimum size filter (ATR multiple and percent of price). Label modes: All, Standard + Reached, Standard Only.

## Outlook scoring

Each pullback receives a score from retracement depth, pullback duration, efficiency (impulse speed vs. pullback speed) and the subsequent reaction. The score maps to: Continuation Likely / Balanced Continuation / Fragile Continuation / Failure Risk. Qualified pullbacks feed the confluence zone (average level of recent candidates within an ATR tolerance).
