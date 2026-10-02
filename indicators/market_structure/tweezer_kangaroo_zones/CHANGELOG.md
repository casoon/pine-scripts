# Changelog

## v3.2.0 — 2026-10-02
- Fix: retest signals no longer fire on the bar whose own pattern created or merged into the zone — that bar always lies inside its zone, so it produced a "zone retest" signal/alert on creation and, with "Retest once only" on, used up the zone's single retest before the first real one
- Fix: the per-bar zone score update dropped the pattern weight (Kangaroo/Tweezer), the structure bonus and the creation height factor, so those settings only affected the admission check. They are now stored per zone and kept in every update; only freshness and cleanliness change over time
- Fix: "impulse before" now measures the five bars before the pattern bar instead of including the pattern bar's own wick, which was counted both as rejection and as impulse
- Fix: the pattern-strength confluence component now only enters the score maximum on bars where a pattern actually forms; previously its weight was always in the maximum but could only score on pattern bars, deflating the normalized 0–10 score on ordinary retests
- Fix: the normalized 0–10 score counted the maximum of the structure, zone-thinness, Supertrend and MOST components twice

## v3.1.3 — 2026-09-05
- Fix: Tweezer/Kangaroo pattern detection (`volCheck`) and the confluence score's Relative Volume component used raw `volume` with no check on `syminfo.volumetype` — on feeds that report tick volume, both were gating/scoring against a meaningless tick count. Added a `volumeIsReal` guard (`base`/`quote` only); pattern `volCheck` now passes through neutrally instead of blocking detection, and the Relative Volume component drops out of both the score and its max (same as any other disabled component) instead of lowering the achievable confluence score
- Data Contract header block added (`Volume: OPTIONAL`, `Verdict: CFD-degraded`)

## v3.1.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v3.1.1 — 2026-06-29
- Alerts: messages standardized to `TKZ · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v3.1.0 — 2026-06-11
- HTF Stack panel and Metrics panel restyled to the light-theme table convention (readable on both TradingView themes)
- Metrics panel "Active" zone count now counts only active zones (previously showed the total number of zones ever created)
- Fixed: rolling 5-bar high/low for structure check was computed inside the zone loop, corrupting the series when multiple zones were active
- Fixed: wick-similarity score could divide by zero when "Max wick ratio" was set to 1.0 (input now has a minimum of 1.1)
- Fixed: impulse score returned na on the first bars of the chart
- Choppiness length input now has a minimum of 2 (prevented a division by zero)
