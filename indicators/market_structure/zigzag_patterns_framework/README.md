# ZigZag Patterns

ZigZag pivot engine with pattern detection on confirmed pivots: simple ABC corrections, triangle formations (symmetrical / rising / falling), a basic Wolfe wave heuristic, and a 1-2-3 reversal (Sperandeo) detector, plus smart pivot labels combining structure tags with confirmation signals.

## Features

- Configurable ZigZag pivot engine (`ta.pivothigh`/`ta.pivotlow`, enforced high/low alternation, bounded pivot history)
- Smart pivot labels: HH/LH/HL/LL structure tag, leg strength (Impulse/Correction), wick rejection, RSI divergence — with a minimum-signal threshold
- ABC correction detection with retracement filter (min/max retrace of BC vs. AB)
- Triangle detection on the last 5 alternating pivots: symmetrical (highs down + lows up), rising (highs flat + lows up), falling (lows flat + highs down)
- Wolfe wedge heuristic: contracting alternating 5-pivot sequence with point-5 overshoot and time spacing, EPA projection line (1→4)
- 1-2-3 reversal (Sperandeo) detection: Point 1 (trend extreme) → Point 2 (retracement) → Point 3 (failed continuation), gated by a mandatory prior-trend precondition; confirmed by a later close-through of Point 2's level with a 0–100 quality score
- Alert on every newly confirmed pivot, plus 1-2-3 Long/Short reversal alerts
- Drawing object caps to stay within TradingView limits

## 1-2-3 Reversal (Sperandeo)

Unlike the other patterns, this one is a two-stage signal, since the actual reversal trigger is a price break, not a pivot event:

1. **Setup** — on a new pivot, the last 3 pivots are checked for a valid Point 1 → Point 2 → Point 3 structure: Point 3 must fail to exceed Point 1 (same type, e.g. a higher low after a low Point 1), and the retracement of Point 3 back toward Point 1 (relative to the Point 1→2 leg) must fall within the ABC retrace filter (`minRetr`/`maxRetr`). A prior trend into Point 1 is mandatory — the pivot at Point 1 and the pivot before it must both carry trend-continuation tags (LL+LH for a bullish setup, HH+HL for a bearish one). Without this, a valid setup is drawn (dotted P1-P2-P3 lines, dashed break level at Point 2, "1-2-3 Bull/Bear" label).
2. **Confirmation** — checked every confirmed bar afterwards: if price closes through Point 2's level in the reversal direction, the setup fires a Long/Short signal with a 0–100 quality score (retracement quality, Point-3 failure clarity, ATR-normalized break strength). If price instead closes back beyond Point 1 first, the setup is invalidated silently.

Only one 1-2-3 setup is tracked at a time; a new valid setup replaces a still-pending one.

## Notes

- All detection runs only on the bar where a new pivot is confirmed (pivot length bars after the actual extreme) — no repainting of confirmed patterns, but confirmation is delayed by the pivot length.
- When a same-type pivot is replaced by a more extreme one, stored history is updated; already drawn segments are not redrawn.
