# Changelog

## v3.4.0 — 2026-07-07
- Fixed a critical Fair Value Gap bug: the fill check compared price against the wrong boundary of the gap (the one derived from the current bar itself), so every FVG was marked filled and removed on the very bar it was created — FVGs now persist correctly until price actually trades back through the far side of the gap
- Fixed level lifecycle: a swept level (sweep or breakout) is now excluded from primary/secondary BSL/SSL scoring immediately, instead of being able to reappear as an "active" level later if price drifts back near it without a qualifying reclaim
- Fixed the Momentum Hybrid event-score bonus to use the "WT Extreme Threshold" input instead of a hardcoded 50.0
- Event priority (Exhaustion > Hunt > Reclaim > Sweep > Breakout) is now resolved globally across both sides instead of separately per direction, so a bar can no longer show a low-priority marker on one side while a higher-priority event fires on the other
- Hunt/Reclaim/Exhaustion labels shortened to `H x<vol>` / `R <score>` / `EX WT <value>` (full detail stays in the hover tooltip)
- Primary/secondary BSL/SSL line labels now show ATR distance directly (`BSL 2x · 64 · 0.8 ATR`) instead of only in the tooltip
- New "Show FVG Labels" toggle (default on) — turn off to keep FVG zones as plain boxes without a text label
- Dashboard now on by default
- Dashboard "Armed" row replaced with a more granular Liquidity State (Idle / Approaching BSL·SSL / BSL·SSL Swept / Bearish·Bullish Reclaim Active / Breakout Accepted)

## v3.3.1 — 2026-07-06
- Removed the live `shape.xcross`/`shape.triangle` + cryptic-text plotshape markers for Hunt, Reclaim and Exhaustion — they were pure duplicate clutter on top of the (better) persistent labels already drawn for the same events, and are exactly what looked cheap/unreadable
- Hunt, Reclaim and Exhaustion now render as a single clean word label ("Hunt" / "Reclaim" / "Exhaustion") with a full hover tooltip (what happened, why, level/score/volume/WT context) — matching this repo's established label style (wyckoff_schematics, bayesian_trend_factor, structure_break_risk)
- Added same-bar/same-direction dedup across Hunt > Reclaim and Exhaustion > Hunt/Reclaim so a strong same-bar event no longer stacks two overlapping labels at the same anchor point
- Sweep and Breakout remain minimal, unlabeled markers (ambient context, not premium events) — unchanged

## v3.3.0 — 2026-07-06
- Sweep vs. breakout: a touch that closes back on its own side is a Sweep; a touch whose close already sits beyond the level is now classified as a Breakout (separate marker/alert) instead of being mislabeled as a sweep
- Stop hunts now require wick-rejection quality (upper/lower wick ratio + close position within the bar) instead of just a red/green candle + volume spike — configurable via "Min Rejection Wick Ratio" / "Max Close Position in Bar"
- Reclaim event score gains a structural bonus (close breaks the prior bar's high/low — a micro-BOS) on top of the existing wick/close-back/volume components
- New optional Regime Context (off by default): range-vs-trend efficiency-ratio regime + premium/discount range location, added as a bounded score bonus to reclaim events and shown on the dashboard — informational, never gates a signal
- New optional Level Lifecycle (off by default): a level that breaks with full acceptance (breakout) is re-tracked on the opposite side instead of discarded (old resistance -> candidate support, and vice versa)
- Gaps replaced with Fair Value Gaps (3-candle imbalance, `low > high[2]` / `high < low[2]`) — more relevant than consecutive-bar gaps for intraday/crypto/forex
- Chart decluttered: one marker per bar per side by priority (Exhaustion > Hunt > Reclaim > Sweep > Breakout); plain sweep/breakout markers no longer carry a text label
- Dashboard rebuilt with a dynamic row count — compact when optional layers are off, with a new Regime row when Regime Context is enabled
- 2 new alert conditions: BSL Breakout, SSL Breakout

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
