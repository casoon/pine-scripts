# Changelog

## v1.3.0 — 2026-10-02
- Touch structure: the bar that sets each range extreme no longer counts as a touch of that edge — before, 2 of the required touches were free. Each side still needs at least one real retest
- Minimum boundary touches lowered by 2 to match: Strict 5→3, Balanced 4→2, Aggressive 4→2, Custom default 4→2 (provisional defaults, not yet validated on data)

## v1.2.6 — 2026-10-02
- Fixed: Historical S/R Reuse (+10) no longer matches pivots inside the current range window — the range's own extreme was counted as a "historical" level
- README corrected: breakouts are not gated by rising ADX, ADX is not a mandatory zone gate, and bias uses EMA structure instead of DI (matches the behaviour since v1.2.2)

## v1.2.5 — 2026-09-05
- Volume data validity: `volumeAvailable` now also requires `syminfo.volumetype` to be `base` or `quote` — tick-volume instruments no longer treat their tick-count feed as real trade volume. The Volume Dry-Up score module and `breakoutVolumeOk` already degrade to a neutral/pass-through state when volume is unavailable; this only widens that definition to include tick volume. The dashboard's existing "Volume" row already surfaces "Unavailable" in that case. Data Contract added (`CFD-degraded`).

## v1.2.4 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.2.3 — 2026-06-29
- Alerts: messages standardized to `CFZ · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.2.2 — 2026-06-27
- Zone bias direction now derives from price structure (touch pressure + EMA stack) instead of DI+/DI− comparison — ADX/DI is demoted to a strength weight that only tightens the pressure needed, never the direction decider
- Breakout direction is set purely by price closing beyond the zone edge — removed the `adx > 20 or DI` hard direction veto that could suppress valid breakouts
- Zone qualification replaced the hard AND of range-compression and touch-structure with structural evidence scoring (`Minimum Structure Evidence` input) — neither module acts as a lone hard veto

## v1.2.1 — 2026-06-11
- Fixed: sensitivity preset mapping still used multi-line conditional expressions — rewritten to single lines (potential Pine v6 compile failure, would prevent the script from loading at all)
- New: "Table Position" input — the info table no longer has to sit top-right, where it can hide behind other indicators' dashboards

## v1.2 — 2026-06-11
- Fixed: zone high/low were only added to the historical S/R memory when "Show Old Zones" was enabled — historical reuse scoring no longer depends on a visual setting
- Fixed: multi-line conditional expressions on series values (bias, zone colors, table bias) rewritten as if/else — these could fail to compile in Pine v6
- Zone border and breakout marker colors aligned to the standard accent palette (bullish #00c853, bearish #d50000)

## v1.1
- Initial release
