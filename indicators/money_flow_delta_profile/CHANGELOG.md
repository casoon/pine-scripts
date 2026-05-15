# Changelog

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
