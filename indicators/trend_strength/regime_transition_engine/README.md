# Regime Transition Engine

Regime Transition Engine classifies the current market into one of seven regime states — Noise, Compression, Expansion, Trend Up, Trend Down, Exhaustion, Reversion — and derives a directional transition-pressure oscillator that reads how close the market is to flipping into the next expected state.

## Features

- Seven-state regime classifier (Noise / Compression / Expansion / Trend Up / Trend Down / Exhaustion / Reversion)
- Minimum dwell + hysteresis debouncing so the state doesn't flicker on score noise
- Directional Transition Pressure oscillator (−100..+100) reading how close the active state is to flipping
- State-change events plotted at the moment of transition: Compression→Expansion, Expansion→Trend, Trend→Exhaustion, Exhaustion→Reversion
- Optional internal role-score plots (Compression, Expansion, Trend Up/Down, Exhaustion, Reversion) for diagnostics
- Dashboard with current state, next-bias label, transition %, state age, and the underlying volatility/efficiency/variance-ratio readouts

## Regime Model

Each bar computes a score (0..1) for all seven candidate states from a shared feature set (volatility percentile, path efficiency, choppiness, linear-regression slope, return z-score, variance ratio, autocorrelation). The state with the highest score becomes the *candidate* state; the *active* state only switches to the candidate once it has held for at least the configured dwell period **and** the candidate score exceeds the active state's score by more than the hysteresis margin. This keeps the state track stable instead of oscillating bar-to-bar.

## Transition Pressure

Once a state is active, a state-specific sub-score estimates how close the market is to moving into its natural successor state (Compression → Expansion, Expansion → Trend, Trend → Exhaustion, Exhaustion → Reversion). This raw pressure is smoothed and signed by trend direction to produce the main oscillator plot — positive values lean bullish/forming, negative values lean bearish/unwinding, depending on the active state.

## Dashboard

Top-right table showing: active State (color-coded), Next Bias (plain-language description of the expected transition), Transition % (smoothed pressure), State Age (bars since last switch), and the three core diagnostic readouts (VolPct, Efficiency, Variance Ratio).
