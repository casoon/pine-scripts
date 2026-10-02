# Changelog

## v1.0.1 — 2026-10-02
- Fix: when the prior Open Interest (or prior front close) for the ΔOI lookback was missing, the change was measured against zero — the ΔOI row showed n/a while the OI x Price row still classified "OI rising + new longs/shorts". A missing prior value now leaves both rows at n/a

## v1.0.0 — 2026-09-05
- Initial release: Daily-only futures context module — Open Interest, ΔOI vs. front-contract
  price change (OI×Price quadrant classification), Front/Next term structure
  (Contango/Backwardation + curve trend), and front-contract real-volume validity check
- Explicit Front/Next `input.symbol()` inputs, default `NYMEX:NG1!` / `NYMEX:NG2!`
- Visible "not configured" / "no data feed" / "daily only" states instead of a silent blank table
- Pure context display — no signals, no alerts
