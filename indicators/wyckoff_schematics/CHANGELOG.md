# Changelog

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
