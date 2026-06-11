# Changelog

## v2.0 — 2026-06-11
- Intrabar delta (optional, off by default): the bull/bear split per bar can now come from real lower-timeframe volume direction (`request.security_lower_tf`, chart TF ÷ granularity, clamped to 1 minute) instead of the close-location approximation — falls back automatically on 1-minute/seconds charts or missing LTF data
- Absorption profile (optional): wick-volume per price row — flow at prices the bar visited but closed away from — drawn as a mirror profile left of the anchor line
- Absorption peak zones (optional): rows whose absorption exceeds both neighbors and ≥ 50% of the absorption maximum are projected as S/R zones across the lookback window

## v1.6 — 2026-06-11
- LVN zones: new "Min Zone Rows" input (default 1 = off) — zones built from fewer adjacent LVN rows than the minimum are skipped
- LVN zones: new "Extend Zones Right" input (default off) — projects zone boxes forward to the right edge of the chart
- Internal: multi-line ternaries rewritten as if/else for Pine v6 compatibility

## v1.5 — 2026-05-15
- HVN / LVN / AVN node classification: reference bars now colored by relative flow density (warm orange = HVN, faded gray = LVN, neutral gray = AVN) — immediately shows which price rows were densely vs thinly traded
- Configurable HVN/LVN thresholds (default 80%/20% of row maximum)
- LVN Supply/Demand Zone Overlay: adjacent Low Volume Node rows are merged into zone boxes projected across the lookback period, colored by position relative to POC (red = supply above POC, green = demand below)

## v1.4 — 2026-05-15
- Row spacing: 8% gap between bars for visual separation
- Delta bar gradient: 2-stop fade from anchor (solid) to tip (translucent)
- Total flow reference bar now bordered ("Rahmen" style)
- Bull% label inside each significant row (>4% of max flow): buying share at that price level, color-coded green/red/gray — independent of bar width
- Anchor line widened to 2px
- Price range (`pLo`/`pHi`) computed on every bar to fix height = 0 on some charts

## v1.3 — 2026-05-15
- MF Price Mode input: Row Mid / HL2 / Typical / Close — controls price multiplier for Money Flow source
- Binary "Close Location" mode now uses proportional (c−l)/(h−l) ratio instead of binary threshold — consistent with Proportional mode, less noise
- Renamed "Buying/Selling Pressure" → "Close Location" (more accurate description)
- pLo/pHi range now computed with ta.lowest/ta.highest (simpler, equivalent result)

## v1.2 — 2026-05-15
- Visualization fix: bear overhangs now extend LEFT of anchor, bull overhangs RIGHT — matches center-out intent
- Anchor shifted right by maxOH bars so bear bars have clearance and don't clip into chart

## v1.1
- Initial release
