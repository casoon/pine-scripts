# Exits that never fire

In the WaveTrend strategy, a trailing exit and a structural exit were tested and rejected: one
"changed nothing", the other "failed". Later it turned out that neither could fire at all.

## What happened

- The take-profit limit was placed at a distance the trailing stop and the structural exit could
  never reach first. On some timeframes the structural exit required more distance than the target
  itself. The limit always filled first.
- The trailing stop was not latched. When price fell back below the trigger, the stop fell back to the
  initial stop or break-even.

The tests measured the take-profit, three times, under three names.

## What follows

- Every exit test reports the **distribution of exit reasons** (target, stop, break-even, trail,
  structure, time). An exit that never appears in that distribution was not tested.
- Exits that compete for the same trade are checked for reachability before they are compared.
- State that must persist across bars (trail level, entry stop, armed signal) is latched explicitly
  and tested for the case where price moves back.
