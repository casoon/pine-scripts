# Changelog

## v2.7.0 — 2026-07-15
- Manual Time no longer creates a hidden pre-anchor MIDAS episode; a timestamp before loaded history starts honestly on the first available bar
- Reconstructed backpainted cumulative states are now the canonical episode statistics, allowing valid early TBF fits without reading immutable values from a previous episode
- Volume quality is measured across the complete anchor episode and shown as an availability percentage plus weighting quality; added explicit Per-bar fallback and Equal weight modes
- Active redraw remains bounded to 2,500 bars and rebuilds the complete episode on the last bar, preventing Pine realtime rollback from leaving only a one-bar curve/zone fragment
- Added Compact (default), Detailed, and Tooltip-only live badge modes; the full measurements and decision logic remain available on hover
- Dashboard remains off by default and keeps the project-standard light-theme table style

## v2.6.1 — 2026-07-15
- Fixed Backpainted TBF history leakage: fit pivots before the live anchor-confirmation bar are blocked instead of reading prior-episode Series values
- Added **TBF History → From Fit** (default) so Active draws the current TBF only from when its fit became known; Retrospective remains an explicit analysis mode
- A single strongly shifted `D` candidate no longer replaces the active fit. It becomes `candidate 1/2` and requires a second similar candidate before adoption
- Split current-fit and episode reaction memory; stable small refits preserve reactions, while materially new fits reset only current-fit evidence
- Context markers are bar-close confirmed by default; alert confirmation remains independently configurable
- Stretch and reclaim detection no longer use EMA bias as a hard gate. Bias now classifies trend-aligned versus counter-bias events
- Reclaim's fifth quality point is direction-coherent: Bottomfinder for bullish reclaim, Topfinder for bearish reclaim; renamed close-in-body to the correct close-location terminology
- Improved TBF reaction separation with ATR-sized displacement and an inner-band transition; passed fits without current-fit reaction become **Stale Fit** at 150% by default
- Active MIDAS, zones, and TBF history now share a 2,500-bar limit; active marker IDs are capped at 300
- Renamed the normalized distance internally and labels Hybrid distance as `hdev` rather than an ambiguous multiplier

## v2.6.0 — 2026-07-15
- Active mode now redraws the latest topfinder/bottomfinder from the complete current episode and current fitted `D`, so the purple curve is visible without restoring obsolete historical fits
- Added **Minimum Fit Maturity** (default 20% `d/D`): mathematically valid but premature fits are rejected before they can drive exhaustion wording
- Added fit stability: first fit is `provisional`; repeated fits are `stable` or `unstable` according to the change in projected total volume `D` (default tolerance 25%)
- Exhaustion phases are now `developing / mature / late / passed`; hover adds remaining projected volume and a rough bars-remaining translation based on episode-average volume
- Added separate 3-part price-reaction confirmation (rejection candle, one-bar structure break, inner-band return). A 2/3 reaction after `late/passed` creates a purple `EXH n/3` marker and dedicated alert
- Live Read now distinguishes advanced projection, fit confidence, and observed price reaction; `late` or `passed` alone no longer reads like a reversal confirmation
- Increased the right-edge Live Read label text from `tiny` to `small`; event markers remain compact
- Replaced the redundant final `READ` row with `NEXT`, which names the next observable condition: band return/test, MIDAS pullback/reclaim/loss, TBF price reaction, or renewed trend alignment

## v2.5.0 — 2026-07-15
- Reworked the chart hierarchy: MIDAS is now the dominant value line, while the inner value area and outer stretch areas use quiet neutral/amber fills instead of directional green/red band semantics
- New **Band Display** modes (`Zones` default / `Lines` / `Zones + Lines`); bullish and bearish colors are now reserved for directional reclaim events
- TBF now communicates progression by state: in **Full**, the curve strengthens near/inside `late` and marks the projected end; in **Active**, its independent Exhaustion row reports fit availability and progress
- Context markers are easier to distinguish: stretch is a neutral amber dot at the outer band, while reclaim labels read `R n/5`, scale with quality, and explain their score breakdown on hover
- The current anchor is shown as a single subtle `A` in **Active** mode; **Full** can show every anchor, and historical plot episodes use clean one-bar breaks
- Dashboard remains off by default; when enabled it opens as a compact 5-row decision view, while the previous diagnostic table remains available via **Dashboard detail → Detailed**
- New default **Active** visual mode reconstructs the complete current anchor episode with polylines, including the Backpainted pivot-to-confirmation history; previous episode clouds/markers are actually removed instead of arbitrarily cropped by a bar lookback. **Full** restores complete diagnostic history
- The live read now keeps four roles explicit: `TREND`, `LOCATION`, `EXHAUSTION`, and `READ`. A positive trend can therefore appear alongside an extended location and unavailable exhaustion without one state hiding the others; hover retains detailed values, meaning, anchor maturity, and change conditions

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
