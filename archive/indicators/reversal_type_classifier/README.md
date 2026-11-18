# Reversal Type Classifier

Ex-post diagnostic indicator that classifies every confirmed pivot reversal into one of four outcome types. Intended for research and gate-design work, not real-time trading entries — all labels are painted retroactively at the pivot bar once the evaluation window has closed.

## Features

- **Four reversal types:** A Snapback (fast hit of target within N bars), B Grind (slow follow-through), C Fake/Pullback (failed, stopped out), D Chop/Unclear (no decisive outcome)
- **WaveTrend context:** WT value at the pivot bar, divergence vs. prior pivot, extreme-level flag
- **ATR-based R-outcome:** MFE and MAE in R units over the configurable evaluation window
- **Trend and chop flags:** EMA direction + ADX trend strength, ADX chop threshold
- **Quality score (0–100):** Composite score per pivot shown in label tooltip
- **Background coloring:** Optional chart background colored by latest classified type
- **Statistics table:** Count by type over the visible history

## Reversal Types

| Label | Condition |
|-------|-----------|
| **A Snapback** | Hits `snapTargetR` within `snapBars` bars, before hitting the fail threshold |
| **B Grind** | Hits `grindTargetR` before fail, or reaches `minFollowR` MFE without stopping out |
| **C Fake/Pullback** | Hits fail threshold first, or MFE < `minFollowR` |
| **D Chop/Unclear** | Sufficient impulse but none of the above criteria met |

Pivots below `minMoveAtr × ATR` in follow-through are excluded entirely.

## Inputs

### 1) Pivot / Evaluation
- **Pivot length left/right** — confirmation lag on both sides (matches `pivLen` in WaveTrend strategy)
- **Evaluation window** — bars after pivot confirmation to assess the outcome
- **Minimum pivot impulse ATR×** — filters micro-pivots with no meaningful excursion

### 2) WaveTrend
Standard WT parameters (channel length, average length, signal length, OS/OB levels).

### 3) Outcome in R
Defines what counts as Snapback, Grind, Fake, and the minimum follow-through to escape the D bucket.

### 4) Context / Quality
EMA length for trend direction, ADX settings for trend strength and chop detection, ATR rank lookback.

### 5) Display
Toggle individual type labels, background zones, and the statistics table.
