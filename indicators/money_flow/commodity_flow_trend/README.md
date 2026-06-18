# Commodity FlowTrend

MFI + CCI composite oscillator designed for commodity markets. Combines directional money-flow momentum (MFI) with a CCI-based trend context layer to identify four distinct flow regimes: bull/bear expansion and accumulation/distribution. Signals fire on MFI/signal-line crosses from extreme zones, optionally gated by CCI direction.

## Features

- **Manual MFI** — computed from source × volume, smoothed and differenced against a signal line; pluggable kernel (EMA, SMA, RMA, WMA)
- **CCI confirmation layer** — normalized to 0–100 for visual alignment with MFI; acts as directional gate for signals and as a trend overlay
- **4-state flow background** — bull expansion (MFI > 50 + CCI > 0 + MFI rising), bull accumulation (MFI < 50 + MFI rising + CCI improving), bear expansion, bear distribution
- **Gradient MFI line** — transitions from bull color near OS to bear color near OB
- **4-state histogram** — rising/falling × positive/negative, matching the WaveTrend Advanced Smoothing convention
- **Extreme-zone reversal signals** — MFI/signal cross after MFI visited OB or OS within the lookback window; optional CCI gate
- **Midline confirmation dots** — MFI crosses the 50 midline with aligned CCI direction
- **Alerts** — bull/bear signal + bull/bear midline confirmation

## Flow State Definitions

| State | MFI | CCI | MFI direction |
|---|---|---|---|
| Bull Expansion | > 50 | > 0 | Rising |
| Bull Accumulation | ≤ 50 | improving | Rising |
| Bear Expansion | < 50 | < 0 | Falling |
| Bear Distribution | ≥ 50 | deteriorating | Falling |

## Signal Logic

Reversal signals require:
1. MFI/signal crossover (or crossunder)
2. CCI confirmation (optional gate): CCI aligned or improving toward signal direction
3. Extreme-zone gate (optional): MFI visited OB or OS within the last N bars

Midline dots fire only when MFI crosses the 50 level with CCI already on the same side — a continuation confirmation rather than a reversal.
