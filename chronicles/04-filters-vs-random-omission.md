# A filter must beat random omission

A filter that removes trades almost always improves profit factor and drawdown: fewer trades mean
fewer costs and less variance. That improvement says nothing about whether the filter knows which
trades to remove.

## What was seen

Several filters looked convincing, and their whole improvement was matched by removing **the same
number of trades at random**. In other cases most of the benefit of a learned filter came from
trading less, not from trading better.

The most fragile kind: filters derived from the outcomes of the strategy's own trades ("trades in
zone X fail, so block zone X") and then judged on the same trades. Such a filter always looks good
where it was found. In the period after, the difference it was built on usually disappeared.

## What follows

- Every filter gets a control: drop the same number of trades at random, many times, and compare.
  The filter counts only if it is clearly better than that.
- Filters are chosen on one period and judged on a later one, never on the period they came from.
- Ten stacked filters, each found on the same data, are ten chances to fit noise. See
  [12](12-the-iteration-spiral.md).
