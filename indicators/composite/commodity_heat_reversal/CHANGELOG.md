# Changelog

## v1.4.5 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.4.4 — 2026-06-30
- Alerts: messages standardized to `<KÜRZEL> · EVENT · {{ticker}} {{interval}}` for a uniform format across the library (titles unchanged)

## v1.4.3 — 2026-06-11
- Change weak countertrend reversal display default from Mark to Hide for a cleaner chart

## v1.4.2 — 2026-06-11
- Tighten pullback-continuation signals to require local MA20/MA50 trend alignment
- Add separate PB cooldown to avoid repeated continuation markers from one pullback
- Remove `PB` text from continuation markers to reduce chart clutter

## v1.4.1 — 2026-06-11
- Narrow CT classification to weak countertrend cases instead of normal exhaustion reversals
- Remove `CT` text from chart markers to reduce clutter
- Keep spike-fade shorts as normal reversal signals when they are not weak below-trend shorts

## v1.4 — 2026-06-11
- Add Counter-Trend Reversals display mode: Show / Mark / Hide
- Mark non-extreme countertrend reversals as `CT` by default instead of normal long/short triangles
- Add separate countertrend reversal alerts

## v1.3.3 — 2026-06-11
- Replace the too-strict counter-trend toggle with Early / Balanced / Strict confirmation modes
- Default to Balanced confirmation so signals remain visible while filtering weak counter-trend bounces
- Reduce same-direction cooldown default from 5 to 3 bars

## v1.3.2 — 2026-06-11
- Add strict counter-trend confirmation to avoid early bounce signals in local trends
- Add same-direction signal cooldown to reduce clustered repeated reversal markers
- Keep original heat scoring but require stronger structure reclaim/break when fading local MA context

## v1.3.1 — 2026-06-11
- Restore trend filter default to off so existing reversal signals remain visible by default
- Loosen pullback-continuation setup for normal MA20/MA50 trend pullbacks with RSI reset
- Loosen HTF bias from strict close-and-slope alignment to close-or-slope alignment

## v1.3 — 2026-06-11
- Enable trend filter by default to reduce lower-timeframe counter-trend reversals
- Add optional higher-timeframe EMA bias for trend context
- Add separate pullback-continuation signals (`PB`) after heat pullbacks in the HTF trend direction
- Add continuation alerts and HTF bias row in the dashboard

## v1.2 — 2026-06-11
- Fix: Long SL/TP line colors were swapped (SL was green, TP red) — SL is now red and TP green for both directions
- Alert conditions added for long, short, and any signal

## v1.1
- Initial release
