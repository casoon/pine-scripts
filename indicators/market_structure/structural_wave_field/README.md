# Structural Wave Field

A chart-native market-structure visualization. It does not draw a classical oscillator — instead it converts structural flow, internal wave energy, correction pressure, maturity, re-synchronization and exhaustion into an adaptive gradient field on a shared Flow Axis below price.

## Features

- Multi-horizon Structural Flow Engine (fast/medium/slow) with hysteresis-based direction (entry vs. opposite-direction flip thresholds)
- Internal Wave Engine combining price momentum, EMA slope and candle impulse into momentum / velocity / acceleration
- Wave segmentation state machine that assigns each transition bar to exactly one segment and archives duration, directional displacement, peak, energy integral, quality, efficiency, participation and retracement
- Structural-leg archive (duration, displacement, cycle count) used to normalize maturity/extension against the instrument's own recent history
- Counter Pressure and Structural Integrity — how much of the active leg is being eroded by the counter-wave
- Maturity, Compression, Re-Sync, Exhaustion and Failed Expansion scoring
- Quality-gated Elliott-context sequence recognition (5-segment impulse / 3-segment correction context) without asserting a hard 1-5 wave count
- Price-scaled Gradient Wave Field renderer — aligned energy always grows above a shared Flow Axis and counter pressure below it, independent of bullish/bearish direction
- Fast, Balanced and Structural sensitivity presets plus advanced calibration with validated horizon/threshold relationships
- Compact `RS`, `F`, `WK`, `EX`, `FF`, `I5` and `C3` event labels with metric-rich hover details, dashboard and bar-close-confirmed alerts

## Structural Flow

Three horizon scores (base/medium/slow length, derived from displacement, signed path efficiency, directional persistence and EMA location) are blended into a single `structuralDrive` value and weighted by horizon agreement. Direction (`structDir`) uses separate hold, entry and opposite-direction flip thresholds: weak flow can return to Transition, a new leg needs stronger entry evidence, and a direct flip needs the strongest opposing evidence.

## Internal Wave

A separate, faster engine (momentum/velocity/acceleration) measures the wave currently running inside the active structural leg. `alignedWave` is this internal wave signed against the structural direction, so positive values mean the internal wave is pushing with structure and negative values mean a counter-wave is running against it.

## Wave Segmentation & Elliott Context

Aligned and counter segments are tracked as a small state machine (start/continue/end on opposite-confirmation or energy decay). A transition bar belongs only to the new segment; the completed segment ends on the preceding bar. The rolling memory stores polarity, duration, directional displacement, peak and mean energy, quality, efficiency, optional participation and retracement. Wave decay and Elliott context use multiple archived dimensions rather than peak energy alone. A polarity pattern becomes `I5` or `C3` context only after its combined quality, efficiency, structure and hierarchy/depth score clears the active sensitivity threshold. This remains pattern context, not a formal Elliott wave count.

## Maturity, Compression, Re-Sync, Exhaustion

- **Maturity** — blends leg age, directionally valid maximum extension, completed expansion/correction cycles, multi-metric wave decay, efficiency loss and price/pressure mismatch against the leg's own historical baseline. Adverse movement beyond the leg origin is never counted as positive extension.
- **Compression** — active only during a correction segment; how tightly price is coiling relative to the structural leg's typical duration.
- **Re-Sync** — a progressive four-stage read (counter decay → neutralizing → acceleration/velocity recovery → aligned-energy confirmation) of the internal wave re-aligning with structure after a correction. Confirmation must own one completed, sensitivity-qualified counter segment and consumes it permanently; duration, depth, quality, structural strength/confidence and an adaptive cooldown remain additional gates. Directional `RS↑`/`RS↓` labels make the continuation direction explicit.
- **Exhaustion** — gated by minimum maturity, combining decay evidence (wave-strength decay, efficiency loss, price/pressure-efficiency loss, optional participation loss) with continuation-failure evidence (price/pressure mismatch, failed expansion, repeated weak peaks).

## Phase Engine

Everything above resolves into one of nine named phases, each with an approximate confidence read: Initiation, Acceleration, Expansion, Correction, Compression, Re-Sync, Late Expansion, Exhaustion, Structural Flow Flip (plus a neutral Transition state when direction, strength or confidence are too weak to classify). Ordinary phase changes need short persistence, preventing a single noisy bar from relabeling the field. “Flow Flip” deliberately names a reversal of the multi-horizon flow model; it does not claim a pivot-based BOS/CHoCH.

## Realtime behavior and settings

The gradient field and dashboard update live on the open realtime bar. Compact event labels and alerts are confirmed on bar close by default so transient intrabar states do not create disappearing events; this can be disabled explicitly. Labels sit in collision-aware lanes outside the corresponding wave-body contour and point back to the event location; their ATR-normalized distance is adjustable. Hover details explain directional `RS↑`/`RS↓` Re-Sync confirmation, `F` Failed Expansion, `WK` Weakening Wave Sequence, `EX` Exhaustion and `FF` Structural Flow Flip. Optional quality-gated `I5` and `C3` events own non-overlapping five- and three-segment windows, preventing rolling patterns from relabeling the same waves. Fast, Balanced and Structural presets scale relative windows, Re-Sync cooldown and transition-memory duration without timeframe-specific direction rules. Structural, wave and scoring parameters remain available behind **Enable advanced calibration**.

## Visual Field

The field follows a short rolling price envelope and sits below it at an ATR-normalized clearance. It participates in chart price scaling, so it remains visible instead of silently falling outside the viewport. The price-following anchor is deliberately thin and neutral: its slope is placement, not a trend signal, and it disappears when neither active structure nor transition memory exists. A colored structural backbone carries direction and confidence. Aligned energy always grows upward from the anchor; counter pressure always grows downward, giving bullish and bearish markets identical geometry. A continuous vertical gradient uses a denser inner glow for energy build/fade and a soft outer contour. Early deterioration progressively ambers the edge before the stronger Exhaustion state. When structure exits into neutral, the completed leg's body and diagnostic context fade for a sensitivity-scaled duration instead of resetting on the exit bar. The candles themselves are never colored or overdrawn.
