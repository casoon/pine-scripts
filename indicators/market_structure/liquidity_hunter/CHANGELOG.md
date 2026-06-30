# Changelog

## v3.2.4 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v3.2.3 — 2026-06-29
- Alerts: messages standardized to `LQH · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v3.2.2 — 2026-06-27
- Decoupled momentum from the sweep/reclaim signal: WaveTrend + MFI exhaustion bonuses in the event score now apply only when the Momentum Hybrid toggle is enabled (default off) — the sweep trigger and reclaim event remain purely structural
- Directional bias is now a dashboard-only summary (computed inside the dashboard block) rather than a standalone aggregator in the main path; it never feeds sweeps, reclaims, hunts, or alerts

## v3.2.1 — 2026-06-11
- Internal: multi-line ternaries (armed-level background, dashboard WT state) rewritten as if/else for Pine v6 compatibility — no behavior change
- Header brought in line with repo convention

## v3.2.0 — 2026-05-15
- Momentum Hybrid: built-in WaveTrend + MFI calculation to qualify sweep/hunt events; Exhaustion Events fire when a BSL sweep/hunt coincides with WT above +threshold (bearish exhaustion) or an SSL sweep/hunt with WT below -threshold (bullish exhaustion)
- Exhaustion markers on chart: large triangles labeled "EX" above/below the triggering bar
- Dashboard extended: WT state (Neutral/Bull/Bear/Extreme) + MFI value row; Exhaustion state row
- 2 new alert conditions: Exhaustion Bear, Exhaustion Bull

## v3.1.0 — 2026-05-14
- Added unfilled gap detection with box visualization (gap magnet zones)
- Added stop hunt detection: same-bar sweep + volume spike + reversal close — distinct from reclaim
- Stop hunts shown with HUNT label; sweeps hidden when hunt fires on same bar
- Dashboard extended: gap count + hunt count row
- 2 new alert conditions: BSL Stop Hunt, SSL Stop Hunt

## v3.0.0 — 2026-02-23
- Full rewrite: BSL/SSL quality scoring, primary/secondary level selection
- ATR-based level tolerance (replaces % tolerance)
- Sweep/reclaim engine with composite event scoring
- Bias output, armed level highlight, dashboard

## v2.2.0
- Equal Highs/Lows with strength scoring and stale cleanup
- Unfilled Gaps, Round Numbers, Stop Hunt detection, Confluence scoring
