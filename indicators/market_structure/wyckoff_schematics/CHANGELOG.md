# Changelog

## v4.8.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v4.8.1 — 2026-06-29
- Alerts: messages standardized to `WYS · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v4.8.0 — 2026-06-28
- Stricter breakout release — Markup/Markdown now require Phase D **plus** a confirmed internal structure (Spring/UTAD test, in-range SOS/SOW, or pivot-confirmed LPS/LPSY) **and** a minimum setup score, instead of any Phase-D state. The floor is a new input, **Min Breakout Score (Markup/Markdown)** (default 50)
- Sequence validation in the setup score: Test is only credited when it follows its Spring/UTAD, and in-range SOS/SOW only when it follows the Test (Schematic #1); a clean Spring → Test → SOS order earns an extra structure bonus
- Confirmed breakout/breakdown events (SOSB/SOWB) now contribute to the setup score; the score keeps updating through Markup/Markdown (scored against the originating schematic) so the breakout is credited
- New alerts: SOSB Breakout and SOWB Breakdown (Phase E) — the breakout is exposed as its own subphase
- "Old Phase Ranges → Hide Labels" replaced by a dedicated **Show Current Phase Label** toggle and a clearer **Keep** mode (boxes retained at full color)

## v4.7.0 — 2026-06-28
- Stricter confirmation — addresses the schematic being confirmed too early:
- Prior-trend context for climaxes: a Selling Climax no longer fires inside a clear uptrend, a Buying Climax no longer fires inside a clear downtrend
- Automatic Rally/Reaction now requires the swing to travel ≥ 1 ATR away from the climax extreme, instead of accepting the first counter-candle
- Markup/Markdown require Phase D **and** a confirmed close beyond the range edge on expanding volume (≥ 1.2× avg) — a bare range probe no longer flips the phase
- The breakout is emitted as a distinct event (SOSB / SOWB), visually separating the decisive break from in-range SOS/SOW strength
- Range Invalidation Factor default lowered 0.5 → 0.33 so broken schematics are dropped sooner
- "Old Phase Ranges → Hide Labels" now implemented: schematic boxes render without the phase text overlay
- Event labels are tracked and capped (60) so the chart never sits near TradingView's drawing limit

## v4.5.0 — 2026-06-11
- Fix: 4H lookback input was never used — every intraday timeframe above 30 minutes fell into the 1H branch; 2H/4H charts now use the 4H lookback
- Fix: trend EMA, volume SMAs and range-score pivots are now computed at global scope — previously they ran inside conditionally-executed functions, which skews `ta.*` rolling state (e.g. on bars with `high == low` or outside active phases) and could distort Prior Trend and Range Score
- Fix: phase box/label left edge clamped to ~9000 bars back — prevents a runtime error when a long Markup/Markdown phase starts further back than TradingView's drawing limit
- New alerts: SOS, SOW, LPS and LPSY detected — the Phase D entry events are now alertable like Spring/UTAD/Test

## v4.4.0 — 2026-05-15
- SC/BC spread check now ATR-based (`high - low > ATR × 1.5`) instead of `/ close > 2%` — correct for all instruments and timeframes
- Spring/UTAD threshold hybrid: fires when depth > `ATR × 0.25` OR ≥ configured % — less misses on low-volatility instruments
- HTF Bias slope computed inside `request.security` — now reflects true HTF EMA bar-to-bar change, not chart-bar snapshot comparison
- PS/PSY backfill: volume compared against `volumeAvg[j]` (historical average at that bar), not current average — bug fix
- Effort vs Result: close position within bar (0 = low, 1 = high) now informs classification; wide-spread bar closing near low on high volume classified as bearish CLIMAX
- P&F Target renamed to "Cause Target (~)" in dashboard to signal approximate nature

## v4.3.1
- Add Signal Mode for entry-event filtering (Spring, LPS, UTAD, LPSY toggles)

## v4.3.0
- Phase D/E validation improvements

## v4.2.0
- Phase B Secondary Test hardening — multi-ST with 10-bar cooldown
- LPS/LPSY volume detection with contemporaneous volume logic
- Phase A snapshot, AVWAP rename, confirmed breakout logic
- Remove volumeProfile dependency

## v4.1.0
- Phase scoring system
- Pivot-bar volume fix
- AVWAP overlay
- HTF slope filter

## v4.0.0
- Phase lifecycle detection
- Range freeze and breakout/invalidation logic
- Spring and UTAD event detection
