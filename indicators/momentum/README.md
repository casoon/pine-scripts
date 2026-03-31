# Momentum Indicators

This group covers oscillators and panel indicators focused on momentum, market exhaustion, candle-level pressure dynamics, and composite flow bias. The scripts surface conditions where price moves are losing energy, stress is building, or directional conviction is shifting — useful for timing entries, exits, and reversals within a broader trend framework.

## Scripts

| Script | Type | What it does |
|---|---|---|
| `market_exhaustion.pine` | Panel | Fuses MFI and StochRSI to detect exhaustion conditions, with HTF context and divergence detection. |
| `market_stress_oscillator.pine` | Panel | Bi-directional Williams VIX Fix (WVF) stress oscillator with peak-hold event markers to flag stress spikes. |
| `candle_pressure_response_jma.pine` | Panel | Measures bidirectional candle pressure, rejection, efficiency, and expansion, smoothed with JMA. |
| `flow_bias.pine` | Panel | Composite bias engine combining CMF, volume delta, Stoch, and Ultimate Oscillator to track trend pullbacks and exhaustion. |

---

### Market Exhaustion

- MFI + StochRSI fusion with optional JMA smoothing
- Adaptive MFI zones with optional background highlights
- Auto-HTF MFI context with a bias label
- Regular divergence detection on MFI

### MSO - Market Stress Oscillator

- Bi-directional WVF stress oscillator
- JMA and ADX filters for noise reduction
- Peak-hold event markers to highlight stress extremes

### Candle Pressure & Response (JMA)

- Bidirectional pressure, rejection, efficiency, and expansion metrics per candle
- JMA smoothing for all output series
- ATR-based normalization with configurable efficiency lookback
- Threshold-based visual alerts on the panel

### FlowBias

- Composite bias derived from CMF, volume delta, Stoch, and Ultimate Oscillator
- Dedicated exhaustion/reversal detection group
- Optional multi-timeframe (MTF) overlay input
- Signal and label rendering for pullback and exhaustion conditions
