# Changelog

## v1.4.0 — 2026-11-18
- Fixed: Minimum Zone Bars now counts the bars the zone condition actually held. Before, the age was measured from the back-dated box start, so even a one-bar zone passed the minimum and armed a breakout watch
- Fixed: the bar that ends a zone no longer rewrites the zone's read and touch counts — a breakout bar could shift the read toward its own direction and so pass `Avoid Breakouts Against Box Read`
- Score: missing volume and disabled modules no longer grant their full points; the score is normalized over the measurable modules (scale stays 0–80). On instruments without real volume (CFDs, tick volume) scores are lower than before, so fewer zones qualify at the same preset
- Impulse-In Context now measures the move into the base (before the range window) instead of drift inside it, frozen when the zone starts — scores and continuation reads change
- ATR Compression and ADX Chop give 40% of their points right at their threshold (rising to 100% at zero) instead of 0% — scores are higher on all instruments
- A running zone holds while at least one structure condition (range compression or touch structure) still holds; score and full structure only decide whether a zone starts. Before, a single score dip ended the zone
- Breakout markers and alerts evaluate on confirmed bars only — no marker appears and vanishes on the open bar. The "Alerts only on bar close" toggle is removed
- Breakout markers no longer carry "BO↑/BO↓" text; hovering a marker shows direction, zone range, read and close. Breakout Up/Down appear in the Data Window
- A dotted line inside each zone box marks the bar the zone was detected on; the part of the box left of it is drawn back over the range window

## v1.3.1 — 2026-10-12
- Volume check fixed: only `tick` volume is rejected; `n/a` counts when the feed actually delivers volume. Most non-crypto feeds report `n/a`, so the old `base`/`quote` check treated futures and stocks with real volume (e.g. EUREX:FDAX1!) as volume-less — volume-based parts are active there again, which can change scores, gates and signals on those markets

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
