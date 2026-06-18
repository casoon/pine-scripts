# ZigZag Patterns

ZigZag pivot engine with pattern detection on confirmed pivots: simple ABC corrections, triangle formations (symmetrical / rising / falling) and a basic Wolfe wave heuristic, plus smart pivot labels combining structure tags with confirmation signals.

## Features

- Configurable ZigZag pivot engine (`ta.pivothigh`/`ta.pivotlow`, enforced high/low alternation, bounded pivot history)
- Smart pivot labels: HH/LH/HL/LL structure tag, leg strength (Impulse/Correction), wick rejection, RSI divergence — with a minimum-signal threshold
- ABC correction detection with retracement filter (min/max retrace of BC vs. AB)
- Triangle detection on the last 5 alternating pivots: symmetrical (highs down + lows up), rising (highs flat + lows up), falling (lows flat + highs down)
- Wolfe wedge heuristic: contracting alternating 5-pivot sequence with point-5 overshoot and time spacing, EPA projection line (1→4)
- Alert on every newly confirmed pivot
- Drawing object caps to stay within TradingView limits

## Notes

- All detection runs only on the bar where a new pivot is confirmed (pivot length bars after the actual extreme) — no repainting of confirmed patterns, but confirmation is delayed by the pivot length.
- When a same-type pivot is replaced by a more extreme one, stored history is updated; already drawn segments are not redrawn.
