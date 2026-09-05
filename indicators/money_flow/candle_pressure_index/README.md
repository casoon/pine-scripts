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

## Instrumente

**Valid:** Futures, stocks, crypto exchanges — real trade volume via `syminfo.volumetype` (`base`/`quote`).
**Invalid:** CFDs (including the repo's reference instrument `CAPITALCOM:NATURALGAS`), Forex, most Indices — `tick`/`n/a` volume.

On invalid instruments the indicator shows a "benötigt echtes Handelsvolumen" (needs real trade volume) label on the last bar and plots nothing, instead of falling back to a neutral `volume_rank` of 0.5.

A reference-market volume would not save the core idea here: `volume_rank` is meant to measure the relative trading intensity of the exact same candle whose geometry (`close_location`, `body_ratio`) also comes from the chart symbol. Applying another market's volume to the CFD's price geometry would attribute activity that happened on that market to candles that formed on a different one — and per `DATA_VALIDITY.md` §4.1 it would additionally force a price comparison between the CFD and the future that the framework deliberately avoids outside a dedicated context module. Degradation (label + no output) is the right answer, not a reference-market request.

## Settings

| Group | Setting | Default | Purpose |
|---|---|---|---|
| CPI | Smoothing Length | 20 | EMA period for the pressure oscillator |
| CPI | Volume Rank Lookback | 20 | Bars used to find the recent volume maximum |
| CPI | Spike Threshold | 0.60 | Min \|raw pressure\| to mark an initiation/absorption candle |
| Signals | Show Zero-Cross Signals | On | Enable long/short markers on CPI zero-crosses |
| Display | Show Dashboard | On | Toggle the info table |
