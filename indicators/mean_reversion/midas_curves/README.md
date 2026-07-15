# MIDAS 2.0

An anchored **MIDAS support/resistance curve** (Paul Levine's launch-anchored volume-weighted price) with a true **topfinder / bottomfinder** accelerated curve — an accelerated exhaustion *estimate*, not a forecast. It is a **Location + Exhaustion** sensor: it reports *where price sits relative to value* (distance from the curve, band zone) and *how far the launched move has run toward its projected end* (the topfinder d/D progress). Context markers are Setup-level evidence, never hard BUY/SELL triggers.

It is the exhaustion-aware sibling of [`anchored_vwap`](../anchored_vwap/): where Anchored VWAP is a pure Location sensor (distance-in-σ, no triggers), MIDAS 2.0 adds the launch-anchored S/R curve and the accelerated topfinder/bottomfinder that the classic MIDAS methodology is actually known for.

## Features

- MIDAS curve anchored at a **manual time**, **daily open**, or **auto swing** (last / low / high), re-seeded from the real pivot bar, not the lagging confirmation bar
- **Volume-weighted σ bands**, **ATR bands**, or **Hybrid** (average of the two) at two configurable multiples, shown as quiet value/stretch zones or classic lines
- **Topfinder / bottomfinder** accelerated curve with maturity-filtered, candidate-confirmed closed-form fits — live-honest **From Fit** history by default
- **Qualified exhaustion read** (`no fit / developing / mature / late / passed`) from cumulative-volume progress `d/D`, followed by a separate 3-part price-reaction check
- Bias-independent **stretched-from-value** and **reclaim-after-stretch** context markers, classified as trend-aligned or counter-bias; persistent markers are bar-close confirmed by default
- **Backpainted / Confirmed** anchor display mode — trade off a clean historical look against a live-honest anchor
- Manual Time remains inactive before the selected timestamp; if it predates loaded history, the first available bar becomes the visible start
- Episode-wide **volume quality** with an explicit **Per-bar fallback / Equal weight** policy instead of a current-bar-only status
- Auto EMA bias with a configurable **hold-bars** hysteresis to reduce whipsaw flips in choppy phases
- **Compact / Detailed / Tooltip-only live badge** with the complete measurement context retained on hover
- Optional **Compact / Detailed dashboard** — a 5-row decision view plus the full diagnostic **Element | Value | Interpretation** table
- **Active / Full visual modes** — the complete current anchor episode by default, or every historical episode for diagnostic review
- Light-theme dashboard, alerts (de-directionalised wording), optional debug log

## Roles (design skill §1)

| Role | What provides it |
|---|---|
| **Location** | normalized distance from the MIDAS curve (σ / ATR / hybrid deviation), band zone |
| **Exhaustion (Momentum)** | topfinder/bottomfinder `d/D` phase + fit stability |
| **Trend** | price side + MIDAS slope in the live read; bias colours markers and picks top vs bottom only |
| **Trigger / Setup** | stretched-from-value, MIDAS reclaim, and `EXH n/3` price-reaction markers (context, not entries) |
| **Quality / Debug** | dashboard + `log.info` events |

The bias is **not** a hard gate on the curve or the exhaustion read — it only colours markers and (for Manual/Daily anchors) picks topfinder vs bottomfinder. For Auto modes the TBF direction follows the anchor side: a swing-low anchor fits a **topfinder** (uptrend, fitted to higher lows), a swing-high anchor fits a **bottomfinder** (downtrend, fitted to lower highs). **Auto Last Swing** (default) anchors on whichever significant swing came last and takes its side automatically.

## Visual language

- **Orange line:** launch-anchored MIDAS value; it is the dominant chart object
- **Neutral inner fill:** price is inside the normal value area (`L1–U1`)
- **Amber outer fills:** price is stretched from value (`U1–U2` / `L1–L2`); amber encodes distance, not direction
- **Purple line:** the current topfinder/bottomfinder curve; stronger purple means the fitted move is further advanced. Active mode defaults to **From Fit**, so the curve begins only where the current fit became known; **Retrospective** is explicitly analysis-only
- **Right-edge live context:** Compact (default), Detailed, or Tooltip-only; the detailed view keeps three explicit state rows (`TREND`, `LOCATION`, `EXHAUSTION`) plus `NEXT`, which names the next observable trigger instead of repeating the state
- **Amber dot:** a stretch rejection at the outer band; context only
- **Green/red `R n/5`:** directional MIDAS reclaim after a prior stretch, with annotated quality
- **Purple `EXH n/3`:** an advanced projection plus at least two separate price-reaction clues; exhaustion risk is confirmed, but this is still not a reversal entry
- **Orange `A`:** the active episode's anchor

## The MIDAS curve

From the launch (anchor), the curve is the cumulative volume-weighted average of the source:

```
MIDAS(j) = Σ pᵢ·Vᵢ / Σ Vᵢ        (i from launch to j)
```

In an uptrend price tends to ride above a curve launched from a swing low (dynamic support); in a downtrend below one launched from a swing high (dynamic resistance). The σ bands use the cumulative volume-weighted variance `Σp²V / ΣV − MIDAS²`; ATR bands use a rolling ATR instead.

## Topfinder / bottomfinder

When a trend *accelerates* away from its MIDAS curve, Levine's topfinder/bottomfinder fits a steeper, decelerating curve that catches back up to price and estimates where the move ends — an accelerated exhaustion estimate, not a forecast. It re-weights the accumulation by `wᵢ = 1 − dᵢ/D`, where `dᵢ` is cumulative volume since launch and `D` is the projected **total** volume at which the move terminates:

```
TBF(j) = Σ pᵢ·Vᵢ·(1 − dᵢ/D) / Σ Vᵢ·(1 − dᵢ/D) = (A·D − B) / (C·D − E)
```

`D` is solved in closed form so the topfinder passes through the most recent same-direction swing after the launch (a pullback low for a topfinder, a pullback high for a bottomfinder):

```
D = (B − T·E) / (A − T·C)      with  A=ΣpV, B=ΣpVd, C=ΣV, E=ΣVd, T = fit price
```

The fit is accepted only when it still projects **forward from the current bar** (`D` greater than the volume accumulated *so far*) and the fit pivot occurred after the configured **Minimum Fit Maturity** (default 20% of `D`). Repeated fits compare their projected `D` values:

- `provisional`: first accepted fit
- `stable`: a repeated fit changed `D` by no more than the configured tolerance (default 25%)
- `candidate 1/2`: a strongly shifted candidate is held without replacing the active fit
- a second candidate in the same new `D` region confirms the change and replaces the active fit

In Backpainted mode, fit pivots between the real pivot origin and its later confirmation bar read from the reconstructed canonical episode statistics. They never read immutable Series values from the previous anchor episode, but no longer need to discard an otherwise valid early fit.

The live read reports **progress `d/D`** in these phases:

| State | Meaning |
|---|---|
| `no fit` | no valid forward projection (range / non-accelerating leg) |
| `developing` | fitted, but below 50% of projected cumulative volume |
| `mature` | `d/D ≥ 50%` — projection is decision-relevant, but not late |
| `late` | `d/D ≥` warn threshold (default 85 %) — **advanced move, not a confirmed turn** (`LATE` marker) |
| `passed` | `d/D ≥ 1` — reported as recently passed, beyond fit, or stale depending on overrun and reaction |

Re-fitting on each new same-direction pullback keeps the projection current. Stable small refits retain the current reaction; materially new confirmed fits reset only their own reaction while the episode remembers earlier reactions. The reaction score checks rejection candle, ATR-sized displacement, and return through the inner band. At least 2/3 creates `EXH n/3`. A passed fit without a current-fit reaction becomes **stale** at the configured threshold (default 150%).

## Dashboard

When enabled, the default **Compact** dashboard mirrors the live context with Trend, Location, Exhaustion, and Next. **Detailed** restores the full diagnostic table below. Both modes are timeframe-aware — the header shows the bucket (Intraday `< 4h` / Swing `4h–<1D` / Position `≥ 1D`), and intraday uses a wider stretch bar with softer reversion language.

| Row | Value | Interpretation |
|---|---|---|
| **Location** | normalized distance in σ / ATR / hybrid deviation (`hdev`) | `at value` / `stretched up·down` / `overextended up·down` |
| **Band zone** | inside / U1–U2 / above U2 … | `at value` / `stretched` / `extreme` |
| **Topfinder/Bottomfinder** | phase + `d/D` | fit quality, projection maturity, and whether price has reacted 2/3 |
| **Trend** | above/below value + slope arrow | `buyers / sellers since launch` |
| **Anchor** | bars since anchor (+ `drawn Xb back` if Backpainted) | `fresh (thin)` / `established` |
| **Volume** | percentage of episode bars with reported volume | `volume-weighted` / `mostly volume-weighted` / `mixed fallback` / `equal-weight fallback` |
| **Reclaim Q** | last reclaim's score, `0–5` + direction | `weak` / `medium` / `high quality` |
| **Next** | — | next observable condition, e.g. inner-band test/return, TBF `EXH 2/3` reaction, or MIDAS reclaim/loss |

`NEXT` is not a new signal. It translates the current state into the next condition worth observing; no condition means no setup yet.

## Modes & inputs

| Group | Key inputs |
|---|---|
| Anchor | mode (Manual Time / Daily Open / Auto Last Swing / Auto Swing Low / Auto Swing High), anchor display (Backpainted / Confirmed), manual time, anchor swing left/right (significant degree), source, volume weighting |
| Bands | show, display (Zones / Lines / Zones + Lines), mode (VW StDev / ATR / Hybrid), mult 1 & 2, ATR length |
| Topfinder/Bottomfinder | enable, exhaustion warn `d/D`, minimum fit maturity, stable-fit tolerance, TBF history (From Fit / Retrospective), stale threshold, fit swing left/right |
| Bias | Auto EMA / Up / Down, EMA length, Auto EMA min hold bars before flip |
| Display | Active/Full visual mode, bar-close-confirmed context markers, reclaim settings, Compact/Detailed/Tooltip-only live context, compact/detailed dashboard + position, active anchor, debug |
| Colors | MIDAS, TBF, stretch zone, bullish, bearish |

## Notes

- Auto-anchor modes re-anchor on the most recent **significant** swing (the `Anchor Swing` degree, default 20) — the origin of the current leg. A larger anchor degree keeps the curve on the current move rather than resetting on every minor wiggle (and avoids pinning it to the all-time extreme). The topfinder fits to the *smaller* `Fit Swing` pullbacks within that leg.
- The running sums are re-seeded from the actual pivot bar (`Anchor Swing Right` back) only in **Backpainted** anchor display mode; the pivot only sets the **anchor origin** — it is not a trigger, grade gate, or dedup key (design skill §8). In **Confirmed** mode the curve instead starts flat at the bar the pivot is actually confirmed, so the anchor is never drawn earlier than it was live-knowable — at the cost of a less clean historical look.
- **Volume missing/zero** (`na` or `≤ 0`, e.g. some CFD/forex feeds) uses weight `1.0` only on the affected bar in the default **Per-bar fallback** mode. The hover and detailed dashboard report availability across the complete anchor episode and name mixed weighting explicitly. **Equal weight** deliberately uses weight `1.0` for every bar when reported volume is not meaningful.
- **Reclaim Quality Score** (0–5): counts prior stretch, close location within the full candle range, volume, structure break, and only a direction-coherent TBF bonus (Bottomfinder for bullish reclaim, Topfinder for bearish reclaim). EMA bias classifies the reclaim but no longer blocks it.
- **Auto EMA bias** only flips once price has closed on the new side of the EMA for `Auto EMA: min hold bars` consecutive bars (default 3), which reduces marker whipsaw in choppy phases; set it to 1 to restore the old immediate-flip behaviour.
- MIDAS, bands, and TBF use a one-bar visual break at each re-anchor so independent launch episodes are never joined by a misleading diagonal connector.
- **Active** mode retains a consistent 2,500 bars for MIDAS, zones, and canonical TBF statistics. The bounded active episode is redrawn on the last bar so Pine's realtime rollback cannot reduce it to a one-bar fragment. Previous clouds and marker IDs are bounded; at most 300 active marker labels are retained. **Full** restores every historical episode and `LATE`/`END` events.
- The topfinder is hidden when no valid forward fit exists (`no fit` in the dashboard). This is **expected** in range-bound or non-accelerating markets: the topfinder/bottomfinder only projects *accelerated* (parabolic) legs, so it typically fits on higher timeframes / strong trends and correctly stays `no fit` in intraday ranges (verified on NatGas — daily legs fit and the exhaustion warnings land near the major 2021/2022/2025 tops, while 1h/15m ranges show `no fit`). Turn on **Debug log** to see why a fit was rejected (`D<=d` = projected end already passed / no acceleration).
- **MIDAS (orange) crossing the TBF (purple) is not a signal.** They are different objects — a cumulative-VWAP level vs an accelerated projection — and they coincide at the launch by construction. What carries meaning is the *gap* between them: a TBF pulling far from MIDAS = strong acceleration (the move is outrunning its fair value); the two staying close = little acceleration. A literal crossover is just the projection passing through the level, not a turn.
- Context markers remain deliberately secondary: stretch uses a small amber dot, directional reclaim labels use `R n/5`, and the rarer purple `EXH n/3` appears only after an advanced TBF phase and a qualifying price reaction. Persistent marker creation defaults to confirmed bars; alerts keep their separate bar-close setting.
