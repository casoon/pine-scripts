# Kestrel Adaptive Smoother

A moving line built from three exponential stages that share one gain per bar. The gain follows how directed and how unusual the recent movement is: while closes go back and forth the line nearly rests, and when they move one way by more than this market usually does it follows, up to passing the close through. The formula, parameters and defaults are those of `kestrel_adaptive_smoother` (alias `kas`) in kestrel-chartkit; Kestrel defines the formula, this script follows it.

## Features

- Three-stage exponential cascade with one adaptive gain per bar
- Gain from the geometric mean of a standard score and an efficiency ratio — no unit, no sign, so price level and direction do not enter
- Phase control: `0` cannot overshoot, `2` follows a straight trend without lag
- Optional hysteresis band (line ± ATR multiple) that turns price-versus-line into a state with memory, with line colour and state markers
- Line, band ATR and state in the data window (`kas_value`, `band_atr`, `band_state`)

## How it works

With `n = (period + 1) / 2`, the base gain `k0 = 2 / (n + 1)`, `a = 2 / (max(n, 2) + 1)`, `b = 2 / (max(4n, 20) + 1)` and the change `d = close − close[1]`:

```text
v  = v + a (d  − v)                 smoothed change
q  = q + a (d² − q)                 its mean square over the same window
Q  = Q + b (d² − Q)                 the long-run mean square
z² = v² / (c · sqrt(Q[1] · q))      c = a / (2 − a)
S  = k0² / (1 − k0) · (z²)^adapt
k  = (sqrt(S² + 4S) − S) / 2
s1, s2, s3 = exponential stages with gain k
KAS = s2 + phase · (s2 − s3)
```

`v / sqrt(c·Q)` is the standard score of the smoothed change; `v / sqrt(c·q)` is the same change against the volatility of its own window, an efficiency ratio. `z` is their geometric mean: it rises with a directed move and rises further when that move is large for this market. `k² / (1 − k) = S` is the steady-state gain of a filter tracking a random walk in noise at signal-to-noise ratio `S`, so `k` stays in `0…1` without clamping and equals `k0` at `z = 1`. `adapt = 0` leaves a fixed three-stage filter.

At a constant gain the line lags a straight trend by `(2 − phase)(period − 1) / 4` bars and overshoots a step by `(1 + 2·phase)·exp(−2(1 + phase)/phase)` of it: none at phase 0, about 0.5 % at 0.5, 5.5 % at 1, 25 % at 2.

## Hysteresis band

The band is a Schmitt trigger around the line, not part of the engine:

- **Up** starts with a close above `KAS + width × ATR` and ends when a close reaches the line again.
- **Down** starts with a close below `KAS − width × ATR` and ends when a close reaches the line again.

Entering at the edge and releasing at the line keeps the state from flipping on every small crossing. Long and short use the same rule mirrored.

## Purpose, use and guardrails

- **Why it exists.** A fixed average sits at one point of the trade-off between lag and noise. This line moves that point bar by bar: it holds still in back-and-forth movement and catches up with a real move.
- **What it is for.** A reference line for the price path — context for which side of a swing price is on, a trailing reference, or the anchor of the band state above.
- **What it is not.** A forecast. Its advantage — staying closer to price at turns than a fixed average with the same number of direction changes — comes from the construction and appears on random series as well; it says nothing about the next direction.
- **Crossings.** Like any line that stays close to price it is crossed often in sideways markets. A bare price/line crossover is no entry rule; the band reduces the flips, it does not remove them.
- **Comparing smoothers.** Compare lines at equal smoothness (equal number of direction changes), not at equal nominal period — a shorter or more adaptive line always looks "faster".

## Kestrel parity

- Engine: kestrel-chartkit, catalog `kestrel_adaptive_smoother`, `src/indicator/kas.rs` (`Kas::update`); defaults `period 20`, `phase 0.5`, `adapt 0.5`.
- The first value is the first close with all three stages on it; a move out of a perfectly flat series passes through.
- Checked by a line-by-line transliteration of this script against the independent reference implementation of kestrel-chartkit on synthetic series (several parameter sets, including `period 1` and `adapt 0`): identical values.
- The `Source` input is an addition; the engine definition uses the close. The band is an addition on top of the engine line.
