## v1.2 — 2026-06-28
- Replaced the dashboard table with a single compact, mobile-friendly **info label** carrying the same read (risk · state · direction · reason · all five sensor values); size selectable (Small / Normal / Large)

## v1.1 — 2026-06-28
- Trend context now **latches** the last clear direction through transitions, so risk can build before the trend formally flips (no more "No Trend" exactly where the break forms)
- New **Near Break Level** sensor — risk rises as price approaches the decisive break level (distance-to-BOS in ATR), not only after the break is confirmed
- Divergence upgraded to proper **pivot RSI divergence** (price pivot vs. RSI sampled at the pivot bar) instead of a fixed-lookback proxy
- Replaced the "Distribution at Extreme" location sensor with Near Break Level; reweighted (Near 25 / BOS 30 / SFP 20 / Erosion 15 / Divergence 10)
- Added a **Reason** read (Near Break Level / Failed Breakout / Structure Erosion / RSI Divergence / Confirmed BOS) so the score explains itself; state idle name is now "No Context"

## v1.0 — 2026-06-28
- Initial release — forward-looking 0–100 structure-break risk gauge, symmetric (top-break in an uptrend, bottom-break in a downtrend), gated to zero when no trend is active
- Weighted evidence sensors: Break of Structure, Failed Breakout/SFP, Structure Erosion, Momentum Divergence, Distribution at Extreme
- Pivots used as swing-level references only; the break event is the trigger
- Evidence-hold window so transient sensors persist; EMA-smoothed composite
- State read with implied-direction colouring (red top-break, green bottom-break) and heat-column fill
- Optional confirmed-break markers, light-theme dashboard, debug log on state change, and High / Critical / Top-Break / Bottom-Break alerts
