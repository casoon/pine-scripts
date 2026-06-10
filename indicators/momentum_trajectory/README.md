# Momentum Trajectory

Treats WaveTrend, StochRSI, and MFI as movement vectors and decomposes each into direction, velocity (1st derivative), and acceleration (2nd derivative). The key insight is that momentum can still be rising while acceleration is already falling — the trend is dying slowly before the oscillator itself turns. An acceleration zero-cross while velocity is still positive is an early exhaustion warning; a zero-cross while velocity is negative signals a potential recovery — both events fire before the oscillator reversal becomes visible.

## Features

- WaveTrend velocity (1-bar rate of change) and acceleration (2nd derivative)
- StochRSI velocity and acceleration
- MFI velocity and acceleration
- Smoothed velocity lines to reduce tick noise (configurable smoothing length)
- State classification per oscillator: Building / Peaking / Collapsing / Recovering
- Background highlight on critical transitions where WT acceleration crosses zero
- Dashboard showing the current state for each oscillator

## Settings

| Group | Setting | Default | Notes |
|---|---|---|---|
| WaveTrend | Show WaveTrend Trajectory | on | Toggle WT velocity/acceleration plots |
| WaveTrend | Channel Length | 10 | WT channel EMA length |
| WaveTrend | Average Length | 21 | WT smoothing EMA length |
| StochRSI | Show StochRSI Trajectory | on | Toggle StochRSI plots |
| StochRSI | RSI Length | 14 | |
| StochRSI | Stoch Length | 14 | |
| StochRSI | K Smoothing | 3 | |
| MFI | Show MFI Trajectory | on | Toggle MFI plots |
| MFI | MFI Length | 14 | |
| Display | Velocity Smoothing | 3 | 1 = raw, higher = smoother velocity lines |
| Display | Acceleration Zero-Cross Background | on | Highlight bars with WT acceleration zero-cross |
| Display | Show Dashboard | on | |
