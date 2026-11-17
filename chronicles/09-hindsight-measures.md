# Hindsight measures are ceilings, not results

Some measures need the future to be computed. They are useful as a ceiling, never as evidence of a
tradable edge.

## Examples from this collection

- **Pivot to pivot.** Measuring from the confirmed low to the confirmed high shows how much movement
  there was. Both points are only known afterwards. "The strategy has a pivot-to-pivot potential of
  X" is a statement about the market, not about the strategy.
- **Pivots drawn back.** `ta.pivothigh` and `ta.pivotlow` with `rightbars > 0` confirm a pivot
  several bars later. Drawing the label on the pivot bar makes the indicator look as if it knew the
  turn at the turn. Any signal that depends on such a pivot can only fire at the confirmation bar.
- **Labelers.** Scripts that label historical reversals with forward data (for example a reversal
  labeler) are research tools. Their output must never feed a live signal or a score.
- **Year-wide baselines.** A comparison base that spans the whole year of a signal contains the
  future of that year (see [03](03-drift-and-the-side-baseline.md)).

## What follows

- Separate hindsight measures from tradable measures in name and in display.
- Signals derived from pivots are plotted and counted at the bar where they become known.
