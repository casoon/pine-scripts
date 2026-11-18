# Changelog

## v1.2.1 — 2026-10-02
- Oscillator scale no longer inherits the chart symbol's price precision (values like 80,0000 on 4-decimal symbols such as NATGAS) — shows 2 decimals

## v1.2.0 — 2026-10-02
- Fixed: BOS fired on every bar closing above the prior swing-lookback high (or below the low) — the "first break" check could never fail. BOS now fires only on the bar that first closes beyond the level, so far fewer BOS events
- Fixed: the event bar could count as its own reaction (green BOS bar → speed score 100). The reaction search now starts on the bar after the event; a reaction on that next bar scores 100
- Fixed: validation progress (component B) was measured from the swing/OB level, so the trigger bar's own range already filled most of the ATR target. It is now measured from the event bar's close
## v1.1.0 — 2026-06-11
- Fixed: per-event state (reaction, validation, scores) was never reset when a new event fired — the speed score from the first event survived forever and was never recomputed for later events
- Fixed: invalid Pine constructs that prevented compilation (nested function definitions in the event picker, a reset function assigning to global variables, comma-separated statements, untyped na declaration for the candle color)
- Event picker rewritten with explicit priority flags; behavior is unchanged

## v1.0.0
- Initial release
