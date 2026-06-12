# VWAP Cross Visuals

VWAP cross detection at its core, with optional advanced layers. Session VWAP and two pivot-anchored VWAPs feed a cross signal engine; the **Price × VWAP cross** is the headline signal (shown as hover-tooltip labels). Optional layers — structure crosses, VWAP cluster, ranked S/R zones, rolling volume profile, HTF trend-stack — are off or hidden by default to keep the chart clean.

**Out of the box:** VWAP lines + Price×VWAP cross markers only. Set **Signal Scope → All signals** to surface the secondary systems, and enable the **Zone / Volume / HTF** modules individually when you want those layers.

## Features

- **Session VWAP** plus **anchored VWAP high/low** (anchored at the latest confirmed pivot high/low)
- **Price × VWAP cross signals** with ATR-based strength scoring and throttling
- **Structure crosses** — session VWAP crossing the anchored VWAP levels
- **Multi-VWAP cluster detection** — confluence zones when VWAPs converge within a tolerance
- **Zone Management (Pro)** — orderblock/pivot/cluster/FVG zone creation, scoring (HTF, FVG overlap, freshness, distance, touches), ranking, trimming, and break detection on current and higher timeframe
- **Bias engine** — VWAP band regime (BULL/BEAR/NEUTRAL) used as confirmation gate
- **Target levels** — ATR or sigma multiples from the nearest active zone, drawn as extendable lines
- **Entry signals** — VWAP/zone retest-and-reject logic (Conservative/Aggressive) with cooldown
- **Volume Profile (Pro)** — POC, value area, HVN/LVN nodes, LVN break-and-retest and VA re-entry signals, EMA/Supertrend/MOST trend filters, optional auto-tuning by market regime
- **HTF Stack Panel (Pro)** — weighted trend confluence across four auto-selected higher timeframes with stack alignment/break signals and choppiness index
- **Display modes** — Smart / Price Only / Cluster Only
- **Alerts** — granular `alertcondition`s plus dynamic `alert()` messages, including multi-system confluence alerts
- **Hidden export plots** — signals, VWAP levels, zone/volume/HTF metrics for use in other scripts (`display.none`)

## Signal markers

| Marker | Meaning |
|---|---|
| `▲/▼ P` | Price crosses session VWAP |
| `◆ S` | VWAP structure cross (session vs anchored) |
| `● C` | Multi-VWAP cluster |
| `ZL / ZS` | Zone-based long/short |
| `L / S` | Entry signal (retest + reject, bias-gated) |
| `VL / VS` | Volume profile signal (LVN break & retest, VA re-entry) |
| `HTF↑ / HTF↓ / BREAK` | HTF stack alignment / break |

## Notes

- Pro modules (zones, volume profile, HTF stack) can be toggled independently; the legend table grows accordingly.
- The volume profile recomputes its histogram per bar over the configured window — on very long histories this is the heaviest part of the script.
- Target mode "LIQUIDITY" is exposed in the inputs but currently falls back to sigma targets.
