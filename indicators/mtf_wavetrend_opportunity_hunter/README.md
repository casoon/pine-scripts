# MTF WaveTrend Opportunity Hunter

Three-tier multi-timeframe scoring system that gates entry signals through four independent layers — Regime, Opportunity, Timing, and Quality — and fires only when all four pass their configured thresholds. Signals are accompanied by ATR-based TP1/TP2/TP3 levels, an invalidation line, and exit warnings when trend health deteriorates.

## Features

- **Three-tier MTF framework**: Regime TF (default Daily) → Setup TF (default 4H) → Trigger TF (default 1H); all timeframes configurable
- **Regime score (0–100)**: WT above signal + rising + EMA50/200 stack + ADX minimum + histogram momentum — maximum 100 points
- **Opportunity score (0–100)**: Setup-TF pullback depth vs. JMA (45%) + WT extreme proximity (35%) + WT direction (20%)
- **Timing score (0–100)**: Trigger-TF WT cross (35%) + WT momentum (30%) + JMA structure (25%) + Setup WT confirmation (10%)
- **Quality score (0–100)**: Efficiency Ratio (35%) + ATR volatility band (25%) + optional Relative Strength vs. benchmark (20%) + JMA acceleration (20%)
- **Configurable thresholds**: independent minimum per layer plus a minimum for the weighted final score (weights: Regime 35%, Opportunity 30%, Timing 25%, Quality 10%)
- **TP / Invalidation levels**: drawn at signal bars using ATR multiples (TP1 1.5×, TP2 2.5×, TP3 4.0×, SL 1.2× below/above)
- **Exit warnings**: orange × marks when trend health drops below 45 or WT crosses back against the trade
- **Dashboard**: live component scores, dominant side, and status label (LONG SIGNAL / SHORT SIGNAL / WAIT: … / WATCH)
- **Alerts**: Long signal, Short signal, Long exit warning, Short exit warning

## Scoring

### Regime (35% of final)

| Component | Points |
|---|---|
| WT1 above signal line | 25 |
| WT1 rising (> previous bar) | 20 |
| Close > EMA50 > EMA200 (bull) | 30 |
| ADX ≥ minimum threshold | 15 |
| Histogram rising | 10 |

### Opportunity (30% of final)

Measures how far price has pulled back toward the JMA on the Setup TF and how close WT is to the extreme level.

- Pullback score: normalized from ATR-distance to JMA — higher when price is near or below JMA
- WT extreme score: higher when WT1 is deeply negative (long) or deeply positive (short)
- +20 flat when WT1 is turning in the signal direction

### Timing (25% of final)

Point-based on the Trigger TF:

| Component | Points |
|---|---|
| WT crossover / crossunder | 35 |
| WT momentum (value + histogram both rising) | 30 |
| Close above/below JMA and JMA sloping | 25 |
| Setup TF WT turning in direction | 10 |

### Quality (10% of final)

| Component | Weight |
|---|---|
| Efficiency Ratio (directional movement / total path) | 35% |
| ATR within 0.7×–2.2× of its 20-bar SMA | 25% |
| RS slope vs. benchmark (optional, default off) | 20% |
| JMA short-term acceleration vs. long-term | 20% |

## Modes

- **Allow Long / Allow Short**: independently disable one side
- **Use Relative Strength Filter**: when enabled, uses the configured benchmark symbol (default SPY) to compute a RS slope and scores it in the Quality layer; when disabled, Quality gets a fixed 70/100 for the RS component
- **Show Regime Background**: green/red tint when regime score passes the minimum
- **Show TP / Invalidation Levels**: ATR-based levels drawn only at signal bars
