# Anchored VWAP

Volume-weighted average price anchored to a selectable origin, with volume-weighted standard-deviation bands. It is a display tool: it shows *where the fair-value reference sits* and *how far price is from it* (distance in σ). It produces no long/short triggers; alerts describe events (a cross, a close beyond the stretch level).

Anchoring a VWAP to a meaningful event (a swing pivot, a session/period start, an earnings gap) gives the average price paid since that event, rather than over an arbitrary rolling window.

## Features

- Anchor at an **auto swing pivot** (re-seeded from the real pivot bar, not the confirmation bar), a **period start** (session / week / month / year), or a **manual timestamp**
- **Volume-weighted σ bands** at two configurable multiples, drawn only once the anchor window holds `Min bars since anchor` bars
- **Distance-from-value in σ** as a symmetric output (positive = above the AVWAP, negative = below)
- Stretched and anchor markers (where price stands, not entries)
- Light-theme dashboard and event alerts

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
- **Distance (σ)** — `(close − AVWAP) / σ`. `|distance| ≥ Stretched at (σ)` flags price as stretched above or below the AVWAP.

## Minimum anchor window

Right after a re-anchor σ comes from only a few bars (in the auto-swing modes `Swing Right Bars + 1`), so band levels and distances in σ are not yet meaningful. Until `Min bars since anchor` (default 20) bars lie in the anchor window, the σ bands are not drawn, the dashboard shows σ as "not yet valid" and Distance (σ) / Location as "—", and no stretched marker or stretch alert fires. The AVWAP line itself is drawn from the anchor bar on.

## Dashboard

| Row | Content |
|---|---|
| AVWAP | current anchored VWAP |
| σ | volume-weighted σ, or "not yet valid" |
| Distance (σ) | `(close − AVWAP) / σ` |
| Location | Stretched above / Stretched below / Within ±Xσ |
| Anchor | anchor mode and bars since the anchor |

## Alerts

All alerts fire on the confirmed bar only.

| Alert | Event |
|---|---|
| Close Crossed Above AVWAP | close crossed above the AVWAP (not on a re-anchor bar) |
| Close Crossed Below AVWAP | close crossed below the AVWAP (not on a re-anchor bar) |
| Close Beyond Upper Stretch | distance first reaches `+Stretched at (σ)` |
| Close Beyond Lower Stretch | distance first reaches `−Stretched at (σ)` |

## Notes

- Bands use the cumulative volume-weighted variance `ΣpV·p / ΣV − VWAP²` since the anchor.
- The VWAP line jumps at each re-anchor (session/pivot modes) — that is expected; each segment is an independent anchored series.
- In Manual Date mode nothing is drawn before the anchor timestamp.

## Instrumente

VWAP is fundamentally a volume-weighted average price — there is no meaningful VWAP without real trade volume feeding the weighting.

- **Valid:** any symbol whose feed delivers volume and does not declare it as `tick`. Most feeds outside crypto report `syminfo.volumetype = n/a` ("not specified"), futures with real contract volume included, so `n/a` with volume present counts as valid.
- **Proxy:** where that volume is a broker's own share of the market (a CFD feed with its own volume), the resulting levels sit where *that broker's* volume traded, which need not be where the exchange's did. Read them as approximate, not as the levels other participants watch.
- **Invalid:** any symbol reporting `tick` (a number of transactions, not a quantity) or no volume at all — there is nothing to weight.

On an invalid instrument the running VWAP/σ sums never accumulate real volume, so the AVWAP line, bands, anchor markers, stretched markers, and dashboard all go blank (`na`/`—`), and a short "AVWAP · not available" notice appears in the bottom-right corner.

**Reference-market variant (documented, not implemented):** unlike a pure oscillator, an anchored VWAP is an absolute price level. Computing it from a different market's volume+price (e.g. `NYMEX:NG1!` while charting `CAPITALCOM:NATURALGAS`) would mix two feeds' price levels onto one chart — exactly what `DATA_VALIDITY.md` §4.2 discourages: intraday reference-market price comparison ranks as "schwach" (Stufe 3) due to latency, session, and settlement mismatch between the two feeds. A dedicated single context module could carry a reference-market VWAP as its own series, but grafting a foreign price level onto the CFD chart inside this indicator is not sound. Not implemented here.
