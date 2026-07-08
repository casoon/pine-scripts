# Changelog

## v2.4.0 — 2026-07-07
- Move Strength: replaced the full-pane background with blue columns (same 5-band coloring) plotted behind Setup/Impulse Pressure, so it adds information without washing out the two curves. Input renamed "Show Columns" (was "Show Background")
- Failed Coil now additionally requires price to have actually fallen back toward the middle of the range (`rangePosition` between 25–75), not just that Setup Pressure dropped — confirms the "range continues" hypothesis with real price behavior instead of Setup Pressure alone
- Naked Impulse now additionally requires ADX < 25 — a strong, ADX-confirmed trend running with low Setup Pressure is normal, not "naked"; this keeps the signal for genuinely fragile, unconfirmed moves
- Reversal now additionally requires the trigger candle itself to close in the reversal's direction (not just show a rejection wick) — a big wick that closes back toward the extreme no longer counts
- Dashboard: new "Action" row — a plain-language read (Ignore/Chop, Watch Setup, Trend Running, Long/Short Reversal, Wait) using the same priority order as the underlying signals, so the table answers "what should I do" directly instead of only showing raw values
- Not implemented: a "directional" variant of Move Strength (tagging it Up/Down Potential purely from which side of the range price sits on) — that's restating range location, not adding real directional information, and would blur the deliberate split between Move Strength (magnitude only) and Reversal (the actual scored directional signal)

## v2.3.0 — 2026-07-07
- Removed Coiling and Breakout Watch entirely: their markers, toggles, phase states, and alerts are gone. Both had known reliability issues discussed at length (Breakout Watch's DMI-based direction lags at turning points; Coiling over-triggered in chop before the Range Chop Filter existed) and are effectively superseded by the DMI-free Reversal signal and the Move Strength gauge
- Phase is now just Sideways/Chop → Impulse Running → Sideways/Quiet → Neutral
- `breakoutBull`/`breakoutBear` (DMI direction) removed — they existed only to serve Breakout Watch and had no other consumer
- Failed Coil is unaffected: it still uses the internal coil-tracking state (`coilEntry`/`inCoil`), just without the "Coiling Start" marker ever being shown

## v2.2.2 — 2026-07-07
- Fix: the v2.2.1 volume guard only caught a volume SMA of exactly `0`; a feed reporting volume as `na` outright (rather than `0`) slipped through (`na == 0` is `false` in Pine), so `volRel` stayed `na` — SPX500 via FOREX.com still came back `na` on every bar after the previous fix while NATGAS via Capital.com was fixed. `volRel` now also treats `na`/negative volume SMA as "no data", not just exactly zero
- New debug output: whenever Setup or Impulse Pressure is `na`, logs every raw ingredient (atr, volume, volSma, volRel, atrPct, bbWidth, compression, srProximity, volQuiet, rangeExpansion, bodyPressure, volumePressure) to Pine Logs, so a still-broken feed can be diagnosed from evidence instead of another guess

## v2.2.1 — 2026-07-07
- Fix: Setup Pressure and Impulse Pressure came back `na` on every single bar on CFD feeds that report zero volume (Capital.com/FOREX.com NATGAS, SPX500, etc.) — `volRel = volume / ta.sma(volume, volLen)` divided by zero, and that `na` fed straight into both pressures with no recovery. `volRel` now falls back to a neutral 1.0 when the volume SMA is 0, instead of letting a single unavailable sensor null out the entire indicator
- Hardened two more unguarded ATR divisions (`nearHigh`/`nearLow` in Setup Pressure, `rangeExpansion` in Impulse Pressure) against the same zero-division risk during flat/zero-range bars, matching the floor already used for `bodyRatio`

## v2.2.0 — 2026-07-07
- New debug input "Log Reversal Context (Pine Logs)" (default off): on every confirmed bar at a range extreme (`validSetupZone`), writes rangePos/chop/setup/impulse/impulseHigh10/exhaustion/both wick ratios/both reversal scores to Pine Logs — lets you check exactly why `sigReversalLong`/`sigReversalShort` did or didn't fire at any specific historical bar, instead of only seeing the current-bar snapshot in the dashboard table

## v2.1.0 — 2026-07-07
- New Reversal signal (`◆` marker, green long / red short): flags exhaustion of the move that got price here (Impulse fading from its own 10-bar high) combined with a rejection wick at a range extreme, weighted by Setup compression — combined as one score per direction (`crossover(score, 60)`), not an AND-chain of hard gates. Gated only by the existing range-extreme + chop veto (`reversalActive`). Deliberately does not use DMI, so it isn't subject to the same lag at turning points as Breakout Watch's directional read
- New alerts: "Signal: Reversal Long" / "Signal: Reversal Short"

## v2.0.0 — 2026-07-07
- Fix: Coiling and Breakout Watch signals (and their markers) fired constantly inside dead sideways ranges, since compression + range-edge proximity happen there all the time — added a Range Chop Filter (ADX < 16, |DI+ − DI−| < 5, price mid-range) and now require price to be near a range extreme (top/bottom 20%) before either signal can fire
- New phase state "Sideways / Chop" takes priority over all other phases while the chop filter is active
- Breakout Watch now has a direction: DMI (DI+ vs DI−) tags the phase text ("Breakout Watch ↑/↓"); the marker becomes a green ▲ (bullish) or red ▼ (bearish) triangle positioned on Impulse Pressure instead of a fixed orange `ℹ` sitting at the arbitrary Setup/Impulse midpoint; falls back to the plain orange `ℹ` while DMI hasn't resolved a direction yet
- Removed StochRSI, MFI and WaveTrend overlays, their cross/price-chart markers, and all four divergence engines (Impulse/StochRSI/WaveTrend/MFI) — none of them ever fed a signal, phase, or alert; they were purely decorative and only bloated the input list
- Removed Momentum Regime Map and Market Character Score dashboard rows — both depended entirely on the now-removed oscillators
- Removed the Double Peak (`DP`) and Dual Fade (`DF`) signal markers and their alerts — they overlapped with what Coiling/Breakout Watch already communicate and tended to fire in confusing back-to-back clusters
- New Move Strength gauge: a blue background (and dashboard row) tracking the expected magnitude of the eventual move — compression depth + range-edge proximity + ADX trend confirmation, suppressed to a third of its value during chop; quantized into 5 opacity bands (invisible/faint/medium/strong/near-solid) instead of a continuous gradient, which read as near-uniform since most bars land in a similar mid-range
- Dashboard table now defaults to off (Show Table toggle); row count reduced from 8 to 7 (Regime/Character rows replaced by Move Str.)

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
