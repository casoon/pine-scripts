# Changelog

## v1.1.0 — 2026-06-11
- Fixed: per-event state (reaction, validation, scores) was never reset when a new event fired — the speed score from the first event survived forever and was never recomputed for later events
- Fixed: invalid Pine constructs that prevented compilation (nested function definitions in the event picker, a reset function assigning to global variables, comma-separated statements, untyped na declaration for the candle color)
- Event picker rewritten with explicit priority flags; behavior is unchanged

## v1.0.0
- Initial release
