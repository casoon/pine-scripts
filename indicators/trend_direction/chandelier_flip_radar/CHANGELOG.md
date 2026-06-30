# Changelog

## v1.6.1 — 2026-06-30
- Alerts: messages standardized to `<KÜRZEL> · EVENT · {{ticker}} {{interval}}` for a uniform format across the library (titles unchanged)

## v1.6 — 2026-06-28
- Ratchet fix: the active stop now holds until an accepted flip and is no longer loosened by a body-rejected close past the trigger (ratchet keyed to the accepted direction, not raw price)
- New **Conviction** adaptive mode: trend-aware multiplier (ATR rank + EMA-separation trend force + chop penalty) — tightens in strong trends, widens in chop
- K-means performance instances now simulate the real Chandelier stop (HH/LL ± k·ATR) instead of a hl2-Supertrend proxy; renamed "AI (K-means)" → "K-means" / "Performance AMA" (honest naming, no behavior claim of an AI model)
- Directional state model (+3/+2/+1/−1/−2/−3): danger keeps its sign, and the stop line stays green/red even in the danger zone — direction is no longer lost
- Weak-flip markers (×): close broke the trigger but body too weak to confirm — distinct from traps and confirmed flips
- Clarified that **Simple** is a volatility-regime scaler only (not trend strength)

## v1.5 — 2026-06-28
- Optional MTF confluence layer (off by default): HTF Chandelier direction, pullback-zone background, diamond confluence flips, HTF stop step-line — absorbed from the archived Adaptive Supertrend
- Base signal path unchanged when MTF is off

## v1.4 — 2026-04-29
- Initial release
