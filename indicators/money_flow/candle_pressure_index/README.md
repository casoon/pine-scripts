# Candle Pressure Index

Measures buying vs. selling pressure purely from candle microstructure — no derived oscillators, no smoothed indicators. Each bar contributes a raw pressure value: `(2 × close_location − 1) × body_ratio × volume_rank`, where close location encodes where price settled in the bar's range, body ratio encodes decisiveness, and volume rank normalizes against recent volume. The CPI oscillator is an EMA of this raw pressure, ranging from −1 (sustained bear pressure) to +1 (sustained bull pressure). This makes it distinct from oscillator composites like WaveTrend or StochRSI — it reflects what the candles themselves say, not a momentum derivative.

## Features

- **Per-bar raw pressure**: close location × body ratio × relative volume rank
- **CPI oscillator**: EMA of raw pressure (−1 to +1), color-coded by direction
- **Momentum line**: 1st derivative of CPI — shows acceleration/deceleration
- **Spike markers**: circles on bars where raw pressure exceeds the spike threshold — initiation candles (strong bull close) or absorption candles (strong bear close)
- **Zero-cross signals**: long/short signals when CPI crosses zero with momentum confirmation (cpiAcc in cross direction)
- **Dashboard**: state (Strong Bull / Bull / Neutral / Bear / Strong Bear), CPI value, momentum direction, raw bar pressure
- **Alerts**: long/short zero-cross, initiation/absorption spike

## Settings

| Group | Setting | Default | Purpose |
|---|---|---|---|
| CPI | Smoothing Length | 20 | EMA period for the pressure oscillator |
| CPI | Volume Rank Lookback | 20 | Bars used to find the recent volume maximum |
| CPI | Spike Threshold | 0.60 | Min \|raw pressure\| to mark an initiation/absorption candle |
| Signals | Show Zero-Cross Signals | On | Enable long/short markers on CPI zero-crosses |
| Display | Show Dashboard | On | Toggle the info table |
