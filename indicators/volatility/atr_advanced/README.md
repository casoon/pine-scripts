# ATR Advanced

ATR in four display modes with pluggable smoothing and gradient visualization. The indicator is useful both as a standalone volatility pane and as a regime filter for other indicators.

## Features

- **Four display modes:** Raw ATR, ATR% (ATR / close × 100), Normalized (z-score vs N-bar window), Percentile Rank (0–100 vs N-bar window)
- **Pluggable smoothing:** EMA, SMA, RMA, WMA, SuperSmoother, T3, KAMA, JMA Approx — default RMA (matches standard ATR convention)
- **4-state histogram:** ATR minus signal; rising/falling × above/below signal drives four opacity states
- **Gradient line:** maps from low-vol teal to high-vol pink based on the mode's natural range
- **Shadow fill:** between ATR line and signal line
- **Level lines:** for Normalized mode ±1σ lines; for Percentile Rank mode configurable percentile lines — both with a mid-zone fill
- **Signal markers:** expansion cross (ATR crosses above signal) and contraction cross
- **Alert conditions:** expansion and contraction

## Modes

| Mode | What it shows |
|---|---|
| Raw | Plain ATR in price units — not comparable across instruments |
| ATR% | ATR normalized to price — comparable across instruments and timeframes |
| Normalized | Z-score: how many standard deviations above/below recent average — good for expansion detection |
| Percentile Rank | Where current ATR sits in the recent distribution — 80+ = high vol regime, 20− = compression |
