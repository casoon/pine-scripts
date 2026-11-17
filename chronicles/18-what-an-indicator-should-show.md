# What an indicator should show

An indicator does not have to prove that it pays over years. It has one job: show honestly, in the
moment, what is there. These rules follow from the notes before.

1. **Facts before verdicts.** Show what can be measured: position relative to the recent extreme,
   distance to the structural stop in ATR, zone, divergence yes or no. No "high-probability" labels
   and no traffic light that recommends an entry while the event type has no shown edge
   ([11](11-event-types-without-edge.md)).
2. **Every figure with its count.** A rate without n cannot be read. Statistics panels show n and
   hide themselves below a minimum count instead of showing a number anyway.
3. **Every rate with its base rate.** Next to the win rate of a signal, the win rate of random bars
   with the same exit, long and short separately ([02](02-win-rate-follows-geometry.md),
   [03](03-drift-and-the-side-baseline.md)).
4. **Make costs visible.** The most useful number for a setup is often: stop distance in ATR, spread
   as a share of it, financing per night as a share of it. That shows at once whether a setup can
   carry its costs ([07](07-cfd-costs.md)).
5. **Range rather than direction.** Volatility can be forecast, direction hardly. An ATR-based range
   estimate is a good display for stop width.
6. **Only compute what the data carries.** When a basis is missing (volume, history, HTF data), the
   indicator reduces its display instead of computing with substitutes
   ([14](14-volume-is-not-always-volume.md)).
7. **One view, not a collection of variants.** An indicator fixes a context and a calculation.
   Switches that only swap the calculation (kernel, source, normalisation) without a shown difference
   go, or move into a group clearly marked as display options ([01](01-smoothing-is-not-an-edge.md)).
8. **No drawing back without marking.** What is known only after `rightbars` is shown at the
   confirmation bar or clearly marked as after the fact ([09](09-hindsight-measures.md)).
9. **Confirmed and forming apart.** Values from a running higher timeframe are shown as provisional
   and never become a stored signal ([13](13-running-htf-values.md)).
