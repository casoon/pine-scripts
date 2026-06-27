# Anchored VWAP

Volume-weighted average price anchored to a selectable origin, with volume-weighted standard-deviation bands. It implements **Stage 4** of the four-stage reversal pipeline (see the `indicator-design` skill, §6.1) — the "fair value zone" / Location sensor. It reports *how stretched price is from value* (distance in σ) and *where the fair-value reference sits*; it deliberately produces **no long/short triggers**.

Anchoring a VWAP to a meaningful event (a swing pivot, a session/period start, an earnings gap) gives a far more honest "fair price since the move began" than a rolling VWAP. Large, sustained deviations from an anchored VWAP tend to revert — which is exactly the Location evidence the reversal pipeline needs.

## Features

- Anchor at an **auto swing pivot** (re-seeded from the real pivot bar, not the confirmation bar), a **period start** (session / week / month / year), or a **manual timestamp**
- **Volume-weighted σ bands** at two configurable multiples
- **Distance-from-value in σ** as a symmetric Location output (positive = above value → short location, negative = below → long location)
- Stretched / anchor / band context markers (Location flags, not entries)
- Light-theme dashboard and alerts

## Anchor modes

| Mode | Origin |
|---|---|
| Auto: Last Swing | most recent confirmed swing high *or* low |
| Auto: Swing High / Low | most recent confirmed swing of that type |
| Session / Week / Month / Year | start of the current period |
| Manual Date | a fixed timestamp input |

Auto modes recompute the running sums from the actual pivot bar (`pivR` bars back) on confirmation, so value accrues from the real swing rather than from the lagging confirmation bar. The pivot only sets the **anchor origin** — it is not used as a trigger, grade gate, or dedup key (design skill §8).

## Outputs

- **AVWAP** — the anchored volume-weighted average price.
- **σ** — volume-weighted standard deviation of the source around the AVWAP since the anchor.
- **Distance (σ)** — `(close − AVWAP) / σ`, the Location measure. `|distance| ≥ Stretched at (σ)` flags a stretched location.

These feed the *Location* role (skill §1) of a downstream reversal module as evidence, not as a blocking gate.

## Notes

- Bands use the cumulative volume-weighted variance `ΣpV·p / ΣV − VWAP²` since the anchor.
- The VWAP line jumps at each re-anchor (session/pivot modes) — that is expected; each segment is an independent anchored series.
- In Manual Date mode nothing is drawn before the anchor timestamp.
