# CFD costs are spread and financing

The strategies in this repository use `commission_value = 0.02 %` and one tick of slippage. For
CFDs that models almost nothing.

## What the costs actually are

- Many CFD brokers charge **no commission**. The cost of entering and leaving is the **spread**,
  paid once per trade.
- Every night a position is held costs **financing**. Beyond roughly a week of holding, financing is
  the larger part of the cost.
- Commodity CFDs carry an additional daily adjustment for the roll of the underlying future. It is not
  in the chart price, and it can be a credit or a charge.
- Many brokers charge triple financing on one weekday to cover the weekend. A rate read off on that
  day overstates all other days. A rate read off on any other day understates that one.
- Historical financing rates differ from today's. Periods with near-zero interest rates had near-zero
  financing.

## What was seen

- On 1h and below, spread and slippage consume nearly every approach. Short holding periods with
  tight stops were net negative throughout.
- Several setups with a small positive edge before costs were flat or negative after costs. Results
  that only survive with optimistic costs do not survive.

## What follows

- Spread as an input in price points, not commission in percent.
- Financing per night as an input, long and short separately, deducted per held night in the result
  table, even though the TradingView tester cannot book it.
- A cost stress factor (for example ×1.5 on all costs) as a switch. A strategy that flips under that
  stress does not pay.
- Position size by risk at the stop, not a fixed share of equity. With "10 % of equity", trades with
  different stop distances risk different amounts and strategies cannot be compared.
