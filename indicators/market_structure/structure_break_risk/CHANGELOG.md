## v2.0 — 2026-06-28
- **Rebuilt as a chart overlay** (`overlay=true`) — the primary read now lives on the price chart instead of a separate oscillator pane
- New **break-level line** drawn in price: the decisive swing the prevailing trend must hold, coloured by the current risk band
- New **risk zone** shading the cushion between price and the break level; the fill intensifies as risk rises (shown from Watch upward)
- Event labels are now **words** — Watch / Break Pressure / Structure Broken / Pressure Faded — replacing the W/P/X/R single-letter markers; each is **anchored to the break-level line** it concerns (pressure-building below the line, the relief event above) so the pointer touches the structure instead of floating; threshold crossings now respect the cooldown so a High+Critical pair no longer prints two stacked labels
- Kept a single **compact, mobile-friendly info label** (text, not a table): score, state, direction, break level, distance-in-ATR, reason and a **mini-bar per sensor**; BOS shown separately as a confirmed event
- Colour now encodes the **risk band** (neutral → orange → red → dark red), never the trade direction, so it no longer reads as buy/sell; direction is stated in words ("Uptrend / Downtrend Break Risk")
- Cleaner plain-language wording: direction reads "Uptrend at risk" / "Downtrend at risk"; states No trend / Quiet / Watch / Break Pressure / Critical / Structure Broken; reasons Approaching break level / Failed breakout / Structure eroding / Momentum divergence / Break confirmed
- Note: a single Pine indicator cannot host both a price overlay and a sub-pane, so the risk magnitude moved into the info label; the sensor/scoring logic is unchanged

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
