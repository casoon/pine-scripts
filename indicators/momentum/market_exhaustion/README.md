# Market Exhaustion

MFI + StochRSI fusion in a single exhaustion panel. The MFI (optionally JMA-smoothed) provides volume-weighted flow context with adaptive or static OB/OS zones; the StochRSI K line provides timing. Long/short signals require both: MFI confirmed in (or crossing out of) its extreme zone plus a StochRSI cross of the OS/OB level. A higher-timeframe MFI adds bias context and can optionally gate signals. Regular divergences on the active oscillator are scored and drawn directly in the panel.

## Features

- Adaptive MFI zones: dynamic OB/OS levels from a rolling lookback (fractions of the observed range) or static 80/20, with optional background highlights and band fill
- Oscillator modes: MFI (default), CCI (tanh-mapped to 0–100), or MFI+CCI with selectable engine for divergence/score logic
- StochRSI timing overlay with configurable OS/OB levels
- Context + timing signals: MFI zone confirmation (configurable confirm bars) + StochRSI cross, optional HTF filter
- Auto-HTF MFI context: automatic higher-timeframe selection (5m→15m, 15m→1H, 1H→4H, intraday→D, daily→M) or manual TF; bias label at the top of the panel
- JMA smoothing: optional Jurik-style smoothing for MFI, StochRSI K, and HTF MFI
- Regular divergences on the active oscillator, anchored on price pivots, with OS/OB area check, ATR swing filter, and direction tolerances
- Divergence quality score (0–100) from ΔMFI, swing size, time span, fatigue, reaction, and sequence count — strong divergences drawn with thicker lines
- Timeframe presets for divergence parameters (5m / 15m / 1H / 4H / 1D) with "More Signals" and "Conservative" profiles, or fully manual values
- Optional candle coloring by HTF bias or signals
- Alert conditions for long/short signals
- Debug log output for divergence diagnostics (Pine logs)

## Signals

| Signal | Condition |
|---|---|
| Long `L` | MFI oversold confirmed (or crossing back above the lower zone) AND StochRSI K crosses above the OS level, HTF filter permitting |
| Short `S` | MFI overbought confirmed (or crossing back below the upper zone) AND StochRSI K crosses below the OB level, HTF filter permitting |

## Divergence Scoring

Score (0–100) is a weighted blend of six normalized components: MFI delta, swing size vs ATR, bars between pivots, fatigue (distance from the recent oscillator extreme), price reaction after the pivot, and consecutive-divergence sequence — plus an optional HTF bias bonus. Lines with score ≥ the strong threshold are drawn thicker; the mid label shows the score (or "Bull/Bear Div" text).
