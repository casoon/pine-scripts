# Changelog

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
