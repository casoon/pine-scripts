# Market Exhaustion

MFI + StochRSI fusion in a single exhaustion panel. The MFI (optionally JMA-smoothed) provides volume-weighted flow context with adaptive or static OB/OS zones; the StochRSI K line provides timing. Long/short signals require both: MFI confirmed in (or crossing out of) its extreme zone plus a StochRSI cross of the OS/OB level. A higher-timeframe MFI adds bias context and can optionally gate signals. Regular divergences on the active oscillator are drawn directly in the panel as markers.

## Features

- Adaptive MFI zones: dynamic OB/OS levels from a rolling lookback (fractions of the observed range) or static 80/20, with optional background highlights and band fill
- Oscillator modes: MFI (default), CCI (tanh-mapped to 0–100), or MFI+CCI with selectable engine for divergence logic
- StochRSI timing overlay with configurable OS/OB levels
- Context + timing signals: MFI zone confirmation (configurable confirm bars) + StochRSI cross, optional HTF filter
- Auto-HTF MFI context: automatic higher-timeframe selection (5m→15m, 15m→1H, 1H→4H, intraday→D, daily→M) or manual TF; bias label at the top of the panel
- JMA smoothing: optional Jurik-style smoothing for MFI, StochRSI K, and HTF MFI
- Regular divergences on the active oscillator, anchored on price pivots, with OS/OB area check, ATR swing filter, and direction tolerances
- Timeframe presets for divergence parameters (5m / 15m / 1H / 4H / 1D) with "More Signals" and "Conservative" profiles, or fully manual values
- Optional candle coloring by HTF bias or signals
- Alert conditions for long/short signals
- Debug log output for divergence diagnostics (Pine logs)

## Signals

| Signal | Condition |
|---|---|
| Long `L` | MFI oversold confirmed (or crossing back above the lower zone) AND StochRSI K crosses above the OS level, HTF filter permitting |
| Short `S` | MFI overbought confirmed (or crossing back below the upper zone) AND StochRSI K crosses below the OB level, HTF filter permitting |

## Divergence Markers

Divergences are a display only: a line between the two oscillator pivots, a "Bull Div" / "Bear Div" mid label and a ▲/▼ at the confirming pivot. They are drawn once, at pivot confirmation, and not changed afterwards. The mid-label tooltip shows the raw values: sequence count (consecutive divergences of the same direction; resets when a confirmed pivot is not one), ΔMFI between the pivots and bars between them. Divergences carry no score, do not feed the long/short signals and have no alerts.

## Data requirements

MFI needs real trade volume (the feed delivers volume and `syminfo.volumetype` is not `tick`). On symbols without it (CFDs, tick volume, no volume) the MFI line, MFI zones, HTF MFI and the MFI-based long/short signals stay empty; the CCI oscillator mode and its divergences keep working.
