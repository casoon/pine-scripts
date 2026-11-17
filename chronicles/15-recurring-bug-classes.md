# Recurring bug classes

A review of all scripts found the same five kinds of mistakes again and again. None of them shows up
as a compile error, and most of them make a script look better or more decisive than it is.

## The classes

1. **A latch or condition that contradicts its own gate.** A state is set and checked on the same
   bar, so the gate is always passed, or a condition is provably always true or never true. Example:
   a "range respected" check that is always true in the neutral state and hands out score points for
   free.
2. **A contaminated reference.** The trigger bar counts towards its own reference, the anchor is the
   wrong bar, a window includes the current bar, or a `ta.*` function runs inside an `if` and skips
   bars. Example: a touch count that includes the extreme bar, so two of four required touches are
   free.
3. **Dead components with documented effect.** An input or a sub-score that is computed but never
   used, while the README describes what it does.
4. **Unreachable thresholds.** A documented level ("Break", "A-setup", "high quality") that the score
   scale can practically never reach.
5. **Double counting, self-inclusion, monotonic scores.** The same wick counted as test and as sweep,
   a pattern matched against itself, a score that only ever adds and never decays.

## Two testing lessons

- **Symmetric test data hides asymmetric bugs.** A test case with the close exactly in the middle of
  the range makes every long/short check pass. Test data must be asymmetric.
- **Long and short must mirror.** A mirror test (invert the price series, swap long and short) catches
  a whole family of sign and index errors.

## What follows

Every score and every gate gets a quick check on these five questions before it is tuned. Tuning on
top of one of these bugs fits the bug.
