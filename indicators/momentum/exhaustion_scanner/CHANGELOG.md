# Changelog

## v2.1 — 2026-06-28
- Added exhaustion zones: each signal draws a box over the overextended price area (band-to-extreme) that keeps extending until price reclaims it or it ages out
- Labels are now bold (▼/▲ headline + score + reason) and carry the full role breakdown — Score/threshold, Stretch/Exhaustion/Reaction, regime+ADX, vol multiplier — on hover instead of crowding the chart

## v2.0 — 2026-06-28
- Restructured the score into three separately-attributable role scores — Stretch (location), Exhaustion (momentum + flow + divergence), Reaction (trigger) — instead of one flat five-component mix
- Added a regime classifier (EMA stack + ADX): signals are now framed as Continuation Risk / Trend Exhaustion / Range Fade rather than blind buy/sell, and countertrend signals require more evidence via a threshold penalty
- Volatility is now a multiplier on the combined score, not a directionless component that inflated both sides equally
- One score drives both the dashboard and the label — removed the Total/Trigger discrepancy
- Reaction trigger hardened: reclaim-fail (poke beyond band/extreme then close back inside) and WT cross only when WT was actually extreme, instead of a bare close < low[1]
- Divergences now invalidate when price breaks beyond the divergence pivot, not just on the validity timer
- Dashboard shows role breakdown, regime + ADX, signal reason (Stretch / Momentum / Rejection / Divergence) and the volatility multiplier
- Replaced "Pivot Confirmed" confirmation mode; custom weights are now per-role with a Money Flow toggle
- Renamed alerts to Top/Bottom/Any Risk to match the risk-context framing

## v1.3 — 2026-06-11
- Added a dedicated trigger score for labels so strong distance/structure/divergence evidence can produce signals even when the weighted total is low
- Recalibrated signal thresholds to Early 30 / Normal 40 / Conservative 50
- Label scores now show trigger strength instead of the weighted dashboard total

## v1.2 — 2026-06-11
- Recalibrated signal thresholds to Early 45 / Normal 55 / Conservative 65 for more practical 4H commodity signals
- Changed default signal mode from Conservative to Normal
- Added divergence-assisted setup labels so visible WT divergences can produce exhaustion signals when price is stretched
- Shortened the dashboard confirmation text for better readability

## v1.1 — 2026-06-11
- Added signal confirmation modes: Score Only, Candle Reaction, Pivot Confirmed
- Added faint candidate dots so raw exhaustion zones remain visible before confirmation
- Added same-side signal spacing to reduce repeated labels in persistent trends
- Hardened Money Flow scoring for feeds with missing or unusable volume data
- Dashboard now shows confirmation mode and current extreme state

## v1.0 — 2026-06-11
- Initial release
- Weighted top/bottom exhaustion scores (0–100) from five components: Distance, Momentum, Money Flow, Volatility, Structure
- Market presets (Stocks / Commodities / Forex-CFD / Crypto / Custom weights)
- Signal modes Early / Normal / Conservative (thresholds 75 / 82 / 88)
- WT divergence detection with validity window as momentum sub-component
- Heatmap background, extreme labels, component breakdown dashboard (light theme)
- Alerts: Top Exhaustion, Bottom Exhaustion, Any
