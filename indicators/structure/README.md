# Structure Indicators

This group covers market structure analysis and related concepts — including Smart Money Concepts (SMC) such as Break of Structure, Order Blocks, and sweeps; multi-timeframe support and resistance zones; candlestick pattern-based supply/demand zones; Wyckoff accumulation/distribution schematics; and hybrid approaches that combine JMA cluster scoring with structure detection. A separate panel indicator measures how quickly price reacts to key structure events relative to volatility.

| Script | Type | What it does |
|---|---|---|
| `smc_structure_expectation.pine` | Overlay | 4-layer SMC framework: labels objective swing structure (HH/HL/LH/LL), derives logical bias/expectation, confirms with BOS and Order Blocks, and optionally warns of trendline breaks and early reversals. |
| `sr_zones_mtf_v2.pine` | Overlay | Builds multi-timeframe support/resistance zones from ATR-reversal structure swings with zone scoring and merging across up to two higher timeframes plus the chart timeframe. |
| `tweezer_kangaroo_zones.pine` | Overlay | Detects tweezer and kangaroo-tail (pin bar) patterns, creates dynamic supply/demand zones from them, and scores each zone using a 5-component system with freshness decay and confluence analysis. |
| `wyckoff_schematics.pine` | Overlay | Automatic Wyckoff accumulation/distribution phase detection with key event labeling (SC, Spring, SOS, BC, UTAD, SOW), Composite Operator tracking, and a real-time dashboard. |
| `jma_struct.pine` | Overlay | Multi-timeframe JMA cluster scoring combined with market structure detection (Wyckoff phases, SMC order blocks) and a data-driven quality scoring system derived from signal analysis. |
| `time_to_react_volatility_time.pine` | Panel | Scores how price reacts to BOS, sweep, and Order Block events against a volatility activity score, with timeframe auto-presets and optional candle coloring. |

---

### SMC Structure & Expectation (`smc_structure_expectation.pine`)

- Detects objective swing structure (HH/HL/LH/LL) as a foundation layer with no predictions, only descriptions.
- Derives a logical expectation/bias from that structure ("Expect HL", "Expect LH", "Continuation", "Failure").
- Confirms setups via BOS and a professional Order Block system with displacement (1.2 ATR), premium/discount location filtering, TTL, and mitigation tracking.
- Optional warnings layer for trendline breaks and early top/bottom signals; designed to minimize signal spam.

### S/R Zones MTF (`sr_zones_mtf_v2.pine`)

- Constructs zones from ATR-reversal structure swings on up to two configurable higher timeframes plus the chart timeframe.
- Merges overlapping zones and limits display to a configurable maximum (up to 50 zones).
- Scores zones to reflect strength and prioritizes the most relevant levels.

### Tweezer & Kangaroo Zones (`tweezer_kangaroo_zones.pine`)

- Detects tweezer patterns and kangaroo tail (pin bar) patterns with timeframe-sensitive sensitivity settings.
- Creates dynamic supply/demand zones from detected patterns with 5-component scoring (0-100), freshness decay, and Top-N filtering.
- Provides structure context via HH/HL/LH/LL swing detection and merges overlapping zones.
- Includes an 8-component confluence scoring system, session-aware profiles (RTH/ETH), and an HTF stack panel for up to 3 timeframes.

### Wyckoff Schematics (`wyckoff_schematics.pine`)

- Automatically identifies accumulation and distribution phases and sub-phases in real time.
- Labels key Wyckoff events: Selling Climax (SC), Spring, Sign of Strength (SOS), Buying Climax (BC), UTAD, and Sign of Weakness (SOW).
- Applies Wyckoff's 2nd Law (Cause and Effect) and 3rd Law (Effort vs Result) analytically.
- Visualizes phase ranges with color-coded boxes and provides alerts for phase transitions.

### JMA Cluster Entries with Market Structure (`jma_struct.pine`)

- Scores JMA cluster alignment across 10 JMAs (0-100) and combines it with momentum, exhaustion, and structure signals in a multi-signal entry matrix.
- Integrates Wyckoff phase/event detection and a professional Order Block system (BOS, displacement, scoring, mitigation).
- Uses timeframe-optimized lookbacks (15M/1H/4H/Daily/Weekly) and a dual-pivot system for both live-ready and confirmed entries.
- Quality scoring is data-driven, derived from analysis of 12,648 historical signals.

### Time-to-React + Volatility-Time (`time_to_react_volatility_time.pine`)

- Scores price reaction speed and validation quality after BOS, liquidity sweep, and Order Block events.
- Calculates a separate volatility activity score to contextualize reaction scores.
- Auto-selects parameter presets by timeframe with optional manual overrides.
- Displays results as a panel with optional chart labels and candle coloring.
