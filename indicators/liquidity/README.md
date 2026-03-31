# Liquidity Indicators

These indicators focus on institutional liquidity, smart money concepts (SMC), and VWAP-based analysis. They are designed to surface where large orders cluster, how price interacts with institutional entry zones and fair value gaps, and when price crosses key volume-weighted levels — giving traders a structural edge aligned with how institutions move markets.

## Scripts

| Script | Type | What it does |
|---|---|---|
| `liquidity_hunter.pine` | Overlay | Maps institutional liquidity zones including equal highs/lows, unfilled gaps, and round number levels; detects stop hunts (liquidity grabs) in real time. |
| `smart_money_dashboard.pine` | Overlay | Combines order flow imbalances, order blocks, fair value gaps, and liquidity pools into a unified dashboard with confluence scoring. |
| `vwap_cross_visuals.pine` | Overlay | Detects price crosses against session and anchored VWAPs, identifies multi-VWAP cluster zones, and ranks confluence signals across timeframes. |

---

### liquidity_hunter.pine

- Detects **equal highs/lows** (liquidity pools) with configurable lookback, tolerance, and minimum touch count
- Identifies **unfilled gaps** (magnet zones) and **round number levels** (psychological zones)
- Flags **stop hunts** — candles that sweep a liquidity level and reverse
- Provides **real-time proximity alerts** when price approaches a mapped liquidity zone

### smart_money_dashboard.pine

- Measures **order flow imbalances** (buying vs. selling pressure) with a configurable threshold
- Plots **order blocks** (institutional entry zones) and **fair value gaps** (price inefficiencies)
- Tracks **equal highs/lows** as liquidity pool targets alongside SMC pattern data
- Surfaces a **real-time confluence score** aggregating all active signals into a single dashboard view

### vwap_cross_visuals.pine

- Plots **session VWAP** (daily reset) alongside **anchored VWAP High and Low** (pivot-anchored)
- Fires signals on **price × VWAP crosses** and **VWAP structure crosses** (session vs. anchored)
- Detects **multi-VWAP clusters** to highlight high-confluence price zones
- Offers three display modes (**Smart / Price Only / Cluster Only**) with smart throttling to prevent signal spam
