# Adaptive Cycle Detector

Estimates the dominant market cycle by measuring the average period between WaveTrend zero-crossings over a configurable lookback window. Fast markets — where the oscillator crosses zero frequently — receive shorter recommended indicator lengths; slow swing markets with infrequent crossings receive longer lengths. ATR regime (volatility trend) and ADX (trend clarity) are incorporated as secondary signals to further refine the length recommendations. The approach approximates a Hilbert-Transform cycle estimator using zero-crossing periods, which is accurate enough for practical length adaptation without the complexity of a full spectral transform.

## Features

- Dominant cycle estimation via WT zero-crossing period (average bars between crossings)
- ATR regime detection: rising / falling / flat volatility classification
- Trend clarity via ADX to distinguish trending from choppy markets
- Adaptive length recommendations for WaveTrend, StochRSI, and MFI
- Smoothed cycle period plot with configurable min/max bounds band
- Dashboard with the current period estimate and recommended lengths

## Settings

| Group | Setting | Default | Notes |
|---|---|---|---|
| Cycle Detection | Lookback for Crossing Count | 100 | Bars used to count WT zero crossings |
| Cycle Detection | Period Estimate Smoothing | 5 | EMA smoothing on the raw period estimate |
| Cycle Detection | Minimum Cycle Period | 8 | Output period is clamped to this lower bound |
| Cycle Detection | Maximum Cycle Period | 60 | Output period is clamped to this upper bound |
| Base WaveTrend | Channel Length | 10 | |
| Base WaveTrend | Average Length | 21 | |
| ADX | ADX Length | 14 | |
| ADX | Trend Threshold | 25 | ADX above this value = trending; favor longer lengths |
| Display | Show Min/Max Band | on | Shade the clamped period bounds on the plot |
| Display | Show Dashboard | on | |
