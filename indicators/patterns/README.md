# Pattern Indicators

This group covers chart pattern recognition, wave analysis, and Fibonacci-based structure validation. The scripts identify classical price patterns (triangles, wedges, channels), ZigZag-derived pivot structures (ABC corrections, Wolfe waves), and Elliott Wave sequences, using Fibonacci retracements and extensions throughout for target projection and wave validation.

## Scripts

| Script | Type | What it does |
|---|---|---|
| `pattern_recognition.pine` | Overlay | Detects triangles, wedges, and parallel channels in real time, with volume-confirmed breakouts and Fibonacci target projection. |
| `zigzag_patterns_framework.pine` | Overlay | Builds a ZigZag pivot engine and uses it to detect ABC corrections, triangles, and Wolfe waves, with smart pivot labeling. |
| `rj_wave.pine` | Overlay | Validates impulse-pullback wave structure by requiring pullbacks to land on a Fibonacci level before confirming the next wave leg. |
| `wave_navigator.pine` | Overlay | Multi-timeframe Elliott Wave detector with a rule engine, weighted scoring, and persistent visualization of the top-ranked wave counts. |

---

### Pattern Recognition

- Detects Ascending, Descending, and Symmetrical Triangles; Rising and Falling Wedges; and Parallel Channels
- Multi-point pivot validation with volume-confirmed breakouts
- RSI divergence and Stochastic RSI filtering for signal quality
- Fibonacci target projection and smart breakout alerts; real-time pattern status table

### ZigZag Patterns Framework

- Configurable ZigZag pivot engine with adjustable pivot length and stored pivot history
- Detects ABC corrections, triangle formations, and Wolfe wave patterns from pivot sequences
- Smart pivot labels (HH / LH / HL / LL) drawn on confirmed swing points
- Modular build: inputs, core logic, and visualization are separate compiled modules

### RJ-Wave Fibonacci Validator

- Tracks impulse waves (AnchorA → AnchorB) and monitors up to three concurrent pullback candidates
- Confirms a wave only when the pullback touches a valid Fibonacci level within a configurable tolerance
- Requires a subsequent break of AnchorB before committing the wave and updating anchors
- Projects price targets after each confirmed wave commitment

### Wave Navigator

- ZigZag-based pivot detection feeding an Elliott Wave rule engine (Impulse, Diagonal, Flat, Triangle patterns)
- Advanced scoring system weighted by momentum, volume, and time ratios; top-N patterns ranked and displayed
- RSI and MACD momentum confirmation alongside volume-based wave strength validation
- Fibonacci retracement and extension zones drawn with persistent, dynamically updated visualization
