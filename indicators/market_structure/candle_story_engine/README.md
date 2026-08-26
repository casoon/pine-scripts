# Candle Story Engine

Interprets candle behaviour as a weighted multi-candle sequence instead of relying on isolated candlestick patterns. It decomposes each candle quantitatively (pressure, body/wick structure, close position, range vs. ATR) and then reads several candles together — sequence pressure, dominance, close persistence, body/wick evolution, compression and exhaustion — to build a directional evidence score instead of just a pattern name.

## Features

- Candle Pressure (-100..+100) from close position, body size and wick imbalance, with an optional volume adjustment
- Candle Quality — how cleanly a single candle's internal structure supports a bullish or bearish read (not a probability)
- Recency-weighted multi-candle Sequence Engine (configurable length, default 5 candles)
- Buyer / Seller Dominance (candle count + body participation across the entire sequence, including Doji) and Close Persistence across the sequence
- Body Contraction and range-compression tracking (short vs. long range average, inside bars)
- Compression-breakout attempts — an expanded directional exit from a recent compression range; informational, not a BUY/SELL input
- Deceleration Engine — directional close progress relative to each candle's range, compared across balanced older/recent sequence halves and feeding trend fatigue into the Exhaustion Engine
- Trend Context from EMA slope + price distance, contributing as supporting (not primary) evidence
- Bullish / Bearish Exhaustion, deliberately decoupled from BUY/SELL — an existing trend can be flagged as exhausted without generating an opposite-direction signal
- Follow-through and Signal Failure detection on the candle immediately after a signal
- Classic candlestick patterns (Engulfing, Hammer, Shooting Star, Morning/Evening Star) as supporting evidence only, not standalone triggers
- Doji are explicitly separated from Hammer/Shooting-Star detection and exported to the data window
- Liquidity Sweep detection — a wick pierces a recent N-bar high/low and closes back inside it; informational only, not a BUY/SELL input
- Data-window outputs (Bull/Bear Evidence, Pressure, Dominance, Exhaustion, Compression, Trend Context, Range/ATR, Relative Volume) for downstream research/backtesting

## Scoring

Directional evidence (`bullEvidence` / `bearEvidence`, 0-100) is built from two distinct base roles plus two contextual additions:

- Candle Evidence (45%) — current-candle pressure qualified by its same-direction structure; this is the timing/trigger role
- Sequence Evidence (55%) — recency-weighted pressure, directional body participation and close persistence combined into one sequence role
- Trend Context (added, capped by `trendWeight`) — only contributes in the aligned direction
- Classic Pattern Evidence (added, capped by `patternWeight`) — only contributes when the pattern opposes an established EMA trend; it is never a continuation-score boost

The sequence sub-measures are intentionally **not** presented as independent votes. They all describe the same OHLC sequence and are combined before entering the final score, avoiding the prior four-way double-counting of a single momentum move.

A fresh BUY/SELL signal fires when the leading evidence score clears `signalThreshold`, beats the opposite score, improves by at least `minimumSignalChange` since the prior bar, and the trend is not already flagged as exhausted in that direction. With the default setting, signals and alerts are evaluated only after the bar closes; this can be disabled with `Confirm Signals on Bar Close`.

The underlying "in control" state uses hysteresis rather than a single hard threshold: it arms at `signalThreshold` but only disarms once evidence drops `signalExitBuffer` points below it (or the opposite side takes over, or exhaustion trips — both exit immediately). Candle Evidence is ~30% driven by the current single candle, so without this buffer one weak pullback candle mid-trend would drop evidence under the threshold for a bar and re-trigger a "fresh" signal on the next strong candle, producing a signal on almost every bar of an otherwise clean trend leg.

## Deceleration Engine

For each close-to-close interval in the sequence, progress-per-range measures how much of the associated candle range converted into net directional close progress. The available intervals are split as evenly as possible into older and recent halves; `bullDecelerationScore` / `bearDecelerationScore` (0-100) rise as the recent-half average falls short of the older-half average — i.e. the trend keeps producing range but converts a shrinking share of it into forward progress. With a sequence length of two there is no older comparison interval, so deceleration is zero. This replaced an earlier single-candle momentum-delta score and feeds into the Exhaustion Engine.

## Exhaustion vs. Reversal

Exhaustion is a separate concept from a directional signal. `bullExhaustion` / `bearExhaustion` only evaluate while an existing trend is in place (`trendScore` beyond `exhaustionTrendMin`) and combine opposing-wick rejection, body contraction, deceleration and trend-strength context. A high exhaustion score means the prevailing trend is losing force — it does not by itself imply the opposite direction is now in control; that still requires the opposite evidence score to clear its own threshold.

## Follow-through / Failure

Evaluated on the candle immediately after a signal:

- **Follow-through** — breaks the signal candle's extreme in the signal direction and closes convincingly inside that range.
- **Failure** — immediately closes beyond the signal candle's opposite extreme.

These are intended as raw material for later research into which signal properties (pressure, quality, dominance, trend alignment) actually distinguish follow-through from failure.

## Compression Breakout Attempts

A bullish/bearish breakout-attempt flag requires three things on a confirmed bar: compression was active on the prior bar, the current range exceeds the configured ATR expansion threshold, and the close breaks the prior `Compression Short Window` high/low while finishing in the corresponding 40% of its range. It is intentionally not added to `bullEvidence`/`bearEvidence`: whether this feature improves outcomes needs validation before it earns score weight.

## Liquidity Sweep

A bullish sweep requires, on a confirmed bar, that the low pierces the prior `Sweep Lookback` N-bar low, the close recovers back above that level, the lower wick makes up at least `Sweep: Minimum Wick / Range` of the candle's range, and the close finishes in at least `Sweep: Minimum Close-Back Position` of the range (the bearish sweep mirrors this against the prior N-bar high). The referenced high/low is a rolling window, not a confirmed swing pivot — pivots in this codebase are a control/reference overlay only and never feed a trigger. Like the Compression Breakout Attempt, this is intentionally not added to `bullEvidence`/`bearEvidence`: it needs outcome validation before it earns score weight.

## Candle Roles

The engine currently distinguishes directional candles, Doji, and the five supporting classic patterns. It does **not** infer actual buyer/seller identity or order-flow delta from OHLCV. The names Buyer/Seller Dominance refer only to the direction, count and relative body size of visible candles.

## Roadmap

See `todo.md` for the open validation and extension roadmap. The priority is validating the existing evidence model before expanding its pattern library or adding more score inputs.
