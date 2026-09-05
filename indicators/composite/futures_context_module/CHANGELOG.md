# Changelog

## v1.0.0 — 2026-09-05
- Initial release: Daily-only futures context module — Open Interest, ΔOI vs. front-contract
  price change (OI×Price quadrant classification), Front/Next term structure
  (Contango/Backwardation + curve trend), and front-contract real-volume validity check
- Explicit Front/Next `input.symbol()` inputs, default `NYMEX:NG1!` / `NYMEX:NG2!`
- Visible "not configured" / "no data feed" / "daily only" states instead of a silent blank table
- Pure context display — no signals, no alerts
