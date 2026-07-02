# Changelog

## v1.2.5 — 2026-06-30
- Alerts: renamed duplicate "Signal: Breakout Watch" (sigIgnit) to "Signal: Ignition" / `MPS · IGNITION` to distinguish it from the state-level "Breakout Watch" alert

## v1.2.4 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.2.3 — 2026-06-29
- Alerts: messages standardized to `MPS · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.2.2 — 2026-06-27
- Fix: Setup Pressure now rises when volume is drying up (inverted volume term), matching genuine squeeze logic — previously high volume wrongly increased Setup Pressure and blurred the separation from Impulse Pressure

## v1.2.1 — 2026-06-11
- Fix: all multi-line ternaries with series types (regime/character/phase colors and texts) rewritten to if/else (Pine v6 compile error CE10156)
- Bias row now shows "Flat" when fast and slow MA are exactly equal (previously fell back to "Bearish")

## v1.2 — 2026-05-15
- Momentum Regime Map: optional background overlay classifying the combined WT + StochRSI + MFI state into Euphoric (extreme overbought/oversold, reversal risk), Distribution (WT bullish but MFI fading), Accumulation (WT bearish but MFI recovering), Energy Build-up (all three near midpoint); replaces phase background when enabled; also shown as colored dashboard row
- Market Character Score: inter-indicator divergence diagnosis in dashboard — Conviction (all three aligned), Artificial Push (WT moves without MFI confirmation), Div. Bull/Bear (StochRSI leads opposite to WT), Mixed

## v1.1 — 2026-05-15
- WaveTrend oscillator overlay (default off): osc + signal line, divergences, zone crosses on price chart
- Same structure as StochRSI overlay — divergences reuse pivot lookback from Divergence group

## v1.0
- Initial release
