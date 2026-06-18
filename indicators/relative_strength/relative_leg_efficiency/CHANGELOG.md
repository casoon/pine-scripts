# Changelog

## v1.0.1 — 2026-06-11
- Fixed `ta.atr()` being called inside conditional pivot-state branches (inconsistent series) — ATR is now computed once per bar in global scope and reused everywhere
- Fixed spike-guard max-body lookup: `ta.highest()` with dynamic length could fail with length 0 before the first pivot and produced unreliable history when called conditionally — replaced with explicit loops over the leg window (only evaluated when Spike Guard is enabled)

## v1.0.0
- Initial release
