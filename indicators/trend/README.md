# Trend Indicators

This group covers the core aspects of trend analysis: detecting the current market regime via moving average alignment, measuring trend direction and strength across multiple timeframes, and quantifying how efficiently price moves from pivot to pivot. Together these scripts support entry filtering, confluence confirmation, and leg quality assessment.

## Scripts

| Script | Type | What it does |
|---|---|---|
| `ma_regime_bands.pine` | Overlay | Classifies regime using multi-MA alignment and renders ATR-based stop bands with normalized trend strength. |
| `regime_detector.pine` | Overlay | Detects regime via MA zones with an adaptive engine, multi-timeframe gate, and advanced signal management. |
| `mtf_trend_alignment.pine` | Panel | Scores trend alignment across up to four timeframes using Supertrend and volatility regime classification, outputting a 0–100 confluence score. |
| `relative_leg_efficiency.pine` | Overlay | Scores each pivot-to-pivot leg 0–100 based on path, time, and counter-pressure efficiency; draws leg lines and labels on the chart. |
| `relative_leg_efficiency_panel_chart.pine` | Panel | Companion panel to the RLE overlay; plots live and confirmed RLE scores in a separate pane alongside chart leg lines. |

---

### MA Regime Bands

- Three configurable MAs (default 21 / 55 / 89) with type options: SMA, EMA, DEMA, TEMA, JMA
- ATR-based stop bands rendered as a regime overlay
- Normalized trend strength output
- Overlay indicator; no separate pane required

### Regime Detector

- Adaptive core engine with dedicated regime detection module
- Multi-timeframe gate filters signals by higher-timeframe context
- Advanced filters and signal management (labels, lines, boxes)
- Overlay with up to 500 lines and 100 boxes for zone visualization

### MTF Trend Alignment Dashboard

- Analyzes four timeframes: current plus three configurable HTFs (default 1H / 4H / Daily)
- Per-timeframe Supertrend direction, strength, and volatility regime classification
- Overall alignment score (0–100) with visual trend matrix
- Entry quality signals derived from cross-timeframe confluence

### Relative Leg Efficiency

- Live 0–100 RLE scoring from the current pivot to the active bar
- Path efficiency: straight-line (air) distance vs. actual path distance
- Time efficiency: speed normalization or time penalty, user-selectable
- Counter-pressure measured by candle count or body-weighted pressure, or both

### Relative Leg Efficiency — Panel + Chart

- Panel pane showing both live (in-progress) and confirmed (closed) RLE scores
- Chart-side leg lines and pivot labels with ATR-based label offsets
- Counter-pressure via body-weighted or count mode
- Companion to `relative_leg_efficiency.pine`; extends visualization into a dedicated panel
