# Changelog

## v2.4.0 — 2026-07-09
- New **Anchor Display** mode (Backpainted / Confirmed): auto-swing anchors previously always re-seeded the curve from the real pivot bar and drew the marker backdated, which looks cleaner historically but the anchor isn't knowable live until `Anchor Swing Right` bars later. **Confirmed** now starts the curve and marks the anchor only at the bar it's actually known live; **Backpainted** (default) keeps the previous behaviour
- Dashboard: **Anchor** row now notes `(drawn Xb back)` when Backpainted is active, so the delay between the drawn anchor and its live confirmation is explicit
- Dashboard: new **Volume** row — flags when `volume` is missing/zero and the curve is falling back to equal-weighted price instead of true volume-weighting
- **Reclaim Quality Score** (0–5): reclaim markers/alerts are unchanged (still fire on stretch + MIDAS crossover), but now carry an annotation score built from stretch beforehand, candle close strength, volume above average, a small structure break, and a TBF late/expired bonus. Shown as marker text and a new dashboard **Reclaim Q** row — context only, does not gate the marker
- Auto EMA bias now holds its side until price closes on the new side for `Auto EMA: min hold bars` (default 3) consecutive bars, reducing whipsaw flips of the context markers in choppy phases (set to 1 for the old immediate-flip behaviour)
- Wording: TBF description softened from "forecasts trend exhaustion" to "accelerated exhaustion estimate" — it projects, it doesn't predict

## v2.3.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v2.3.1 — 2026-06-29
- Alerts: messages standardized to `MIDAS · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v2.3 — 2026-06-28
- Dashboard rebuilt as **Element | Value | Read** — every row carries a plain-language interpretation, plus a synthesised TF-aware **Read** headline (e.g. "Overextended from value → mean-reversion to MIDAS likely")
- Stretch thresholds and the Read conclusion are **timeframe-aware**: intraday uses a wider σ bar (noisier) and softer reversion language than Swing/Position
- Readout is verbalisation of the existing role outputs only — no new signal
- Fix: TBF fit eligibility now requires `age ≥ fitRight + 1` (was `age[fitRight] ≥ 1`), so a fit right after a re-anchor can no longer mix the previous episode's cumulative sums into the projection

## v2.2 — 2026-06-28
- TBF curve now forces a clean one-bar break on every re-anchor, so separate projection episodes no longer bridge into a straight diagonal on long-history views

## v2.1 — 2026-06-28
- New **Auto Last Swing** anchor mode (default) — anchors on the most recent significant swing of either side and sets the TBF direction from it (low → topfinder, high → bottomfinder)
- Anchor marker now plots at the real price (and offset back to the pivot bar in auto modes)
- **Hybrid** band mode (average of VW σ and ATR) — ATR stays reactive while the anchored σ widens in long trends
- Reclaim markers/alerts only fire **after a genuine stretch** past the inner band within a configurable lookback (no longer on small dips)
- TBF exhaustion reframed into a 4-stage state (**no fit / running / late / expired**); "late" = advanced move, not a confirmed turn (marker text `LATE`)
- Alerts de-directionalised: `MIDAS bullish/bearish reclaim`, `TBF late move` (no long/short wording)

## v2.0 — 2026-06-28
- Initial repo release: anchored MIDAS support/resistance curve (manual time / daily open / auto swing pivot)
- Volume-weighted σ bands or ATR bands at two configurable multiples
- True topfinder / bottomfinder accelerated curve with closed-form auto-fit to the most recent same-direction swing (a fit is accepted only if its projected end still lies ahead of the current bar)
- Exhaustion forecast as cumulative-volume progress d/D, with warn threshold + EXH marker
- Stretched-from-value and MIDAS-reclaim context markers (Setup-level, no hard entries)
- Light-theme dashboard, alerts, debug log