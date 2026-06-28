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
