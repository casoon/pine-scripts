# Market Memory & Decay Oscillator

A signed oscillator that scores how much "memory" the current price impulse carries versus how fast that memory is decaying back toward random-walk noise. It combines four independent statistical reads on the same lookback window — return autocorrelation half-life, a Hurst exponent approximation, path efficiency, and range expansion/contraction — into one Carry/Decay axis, rather than treating momentum and mean-reversion as separate indicators.

## Features

- Autocorrelation-derived half-life: how many bars a directional impulse statistically persists before its serial correlation decays to half
- Hurst exponent approximation (rescaled-range over the memory window) to separate persistent (trending) from mean-reverting (anti-persistent) regimes
- Path efficiency: net displacement vs. total distance travelled, rewarding clean directional moves over choppy ones
- Range expansion/decay via fast-vs-slow ATR ratio, feeding both the Memory Strength and Decay Pressure components
- Composite **Memory Strength** (persistence-favoring) vs. **Decay Pressure** (reversion-favoring) blend into the main `MMDO` score
- Regime states — **Bullish Carry**, **Bearish Carry**, **Decay**, **No Edge** — with background shading
- Impulse markers where the return Z-score crosses the configurable threshold
- Light-theme dashboard: score, state, half-life, impulse age, Hurst, efficiency, range ratio
- Bullish/Bearish Carry and Impulse Decay alerts

## Scoring

1. **Impulse** — EMA of the Z-scored log return; its sign sets `impulseDir`, its magnitude sets `impulseStrength`.
2. **Memory Strength** — weighted blend of half-life score (35%), positive Hurst memory (25%), path efficiency (25%), and range expansion (15%). High values mean the current impulse has statistical persistence.
3. **Decay Pressure** — weighted blend of range contraction (35%), impulse age since the last Z-threshold breach (25%), negative Hurst memory (25%), and low path efficiency (15%). High values mean the impulse is losing coherence and reverting toward noise.
4. **MMDO** = EMA of `carryRaw − decayRaw × 0.55`, where `carryRaw = impulseDir × impulseStrength × memoryStrength × decayCurve × 100` and `decayRaw = impulseDir × decayPressure × impulseStrength × 100`. `decayCurve` is the exponential half-life decay evaluated at the current impulse age.
5. **State** — Bullish/Bearish Carry above/below ±25 on MMDO (unless Decay dominates); Decay when the decay line exceeds 65% of the memory line while MMDO itself stays below the memory line; otherwise No Edge.
