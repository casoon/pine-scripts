# Changelog

## v1.1.0 — 2026-10-02
- Fixed: path efficiency compared the wick-to-wick pivot distance against the Path Source (default hlc3) travel between the same bars — the air distance was larger than the path it was divided by, so PE was inflated and often pinned at 1.0 even with clearly choppy legs. Air and path are now measured on the same Path Source; PE and RLE scores of choppy legs come out lower
## v1.0.2 — 2026-06-29
- Alerts: messages standardized to `RLE · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.0.1 — 2026-06-11
- Fixed `ta.atr()` being called inside conditional pivot-state branches (inconsistent series) — ATR is now computed once per bar in global scope and reused everywhere
- Fixed spike-guard max-body lookup: `ta.highest()` with dynamic length could fail with length 0 before the first pivot and produced unreliable history when called conditionally — replaced with explicit loops over the leg window (only evaluated when Spike Guard is enabled)

## v1.0.0
- Initial release
