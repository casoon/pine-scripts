# Trading Range State Machine

Trading Range State Machine detects an active trading range and tracks its maturity through a state machine, from first formation to breakout. The range boundaries come from clustering recent pivot highs/lows (falling back to a simple highest/lowest window when no reliable cluster exists), and an 8-factor weighted score measures how strongly the current price action actually behaves like a range rather than a trend.

## Features

- Pivot-Cluster Range Detection (fallback to highest/lowest window)
- 8-Factor Weighted Range Score (Efficiency Ratio, Candle Overlap, Choppiness, Structure Chaos, Regression Flatness, Boundary Stability, ATR Compression, Mean Reversion)
- Range State Machine: Inactive → Building → Confirmed → Mature → Breaking, with directional (Up/Down) breakout detection
- Position-in-Range readout: % location within the range plus an Upper/Mid/Lower zone label
- Range Lines, Midline, Touch Markers, Continuous Score-Scaled Background Heat, Bottom Ribbon
- Dashboard with score breakdown

## Scoring

Each bar's range score (0–100) is a weighted blend of eight components, each capturing a different aspect of range-bound behavior:

- **Efficiency Ratio** — low net-to-total price movement over the lookback favors a range
- **Candle Overlap** — high bar-to-bar overlap favors a range
- **Choppiness** — high choppiness (price covering little net distance relative to true range) favors a range
- **Structure Chaos** — few breaks of recent structure favors a range
- **Regression Flatness** — a flat linear regression slope with weak trend correlation favors a range
- **Boundary Stability** — repeated, balanced touches of the same upper/lower cluster levels favor a range
- **ATR Compression** — current volatility below its longer-term average favors a range
- **Mean Reversion** — repeated returns to the range midpoint favor a range

Weights are configurable per component (`Weights` group).

## State Machine

The range score drives a five-state machine:

- **Inactive** — score below 75% of the Confirmed threshold
- **Building** — score at or above 75% of the Confirmed threshold
- **Confirmed** — score at or above the Confirmed threshold
- **Mature** — score at or above the Mature threshold
- **Breaking** — score still at or above Confirmed, but price has closed beyond the range boundary (plus an ATR buffer); colored and alerted separately for Up vs Down

Range lines, midline, background heat, and the bottom ribbon are only drawn while the state is Building, Confirmed, or Mature. Background heat alpha scales continuously with the range score within each state, so a strengthening range is visible before the next state boundary is crossed rather than jumping in one step.

## Position in Range

Alongside the state, a Position readout shows where the current close sits between the range boundaries as a percentage, plus a zone label: **Upper** (≥ 80%), **Lower** (≤ 20%), or **Mid**.
