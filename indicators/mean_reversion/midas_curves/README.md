# MIDAS 2.0

An anchored **MIDAS support/resistance curve** (Paul Levine's launch-anchored volume-weighted price) with a true **topfinder / bottomfinder** accelerated curve that forecasts trend exhaustion. It is a **Location + Exhaustion** sensor: it reports *where price sits relative to value* (distance from the curve, band zone) and *how far the launched move has run toward its projected end* (the topfinder d/D progress). Context markers are Setup-level evidence, never hard BUY/SELL triggers.

It is the exhaustion-aware sibling of [`anchored_vwap`](../anchored_vwap/): where Anchored VWAP is a pure Location sensor (distance-in-σ, no triggers), MIDAS 2.0 adds the launch-anchored S/R curve and the accelerated topfinder/bottomfinder that the classic MIDAS methodology is actually known for.

## Features

- MIDAS curve anchored at a **manual time**, **daily open**, or **auto swing** (last / low / high), re-seeded from the real pivot bar, not the lagging confirmation bar
- **Volume-weighted σ bands**, **ATR bands**, or **Hybrid** (average of the two) at two configurable multiples
- **Topfinder / bottomfinder** accelerated curve with closed-form auto-fit — catches up to price and projects where the launched move ends
- **4-stage exhaustion read** (`no fit / running / late / expired`) from the cumulative-volume progress `d/D`
- **Stretched-from-value** and **reclaim-after-stretch** context markers (light, Setup-level)
- **Element | Value | Read** dashboard — every row carries a plain-language interpretation plus a synthesised **TF-aware** conclusion
- Light-theme dashboard, alerts (de-directionalised wording), optional debug log

## Roles (design skill §1)

| Role | What provides it |
|---|---|
| **Location** | distance from the MIDAS curve (σ / ATR), band zone |
| **Exhaustion (Momentum)** | topfinder/bottomfinder `d/D` progress |
| **Trend** | bias (Auto EMA / forced) — colours markers and picks top vs bottom only |
| **Trigger / Setup** | stretched-from-value and MIDAS-reclaim markers (context, not entries) |
| **Quality / Debug** | dashboard + `log.info` events |

The bias is **not** a hard gate on the curve or the exhaustion read — it only colours markers and (for Manual/Daily anchors) picks topfinder vs bottomfinder. For Auto modes the TBF direction follows the anchor side: a swing-low anchor fits a **topfinder** (uptrend, fitted to higher lows), a swing-high anchor fits a **bottomfinder** (downtrend, fitted to lower highs). **Auto Last Swing** (default) anchors on whichever significant swing came last and takes its side automatically.

## The MIDAS curve

From the launch (anchor), the curve is the cumulative volume-weighted average of the source:

```
MIDAS(j) = Σ pᵢ·Vᵢ / Σ Vᵢ        (i from launch to j)
```

In an uptrend price tends to ride above a curve launched from a swing low (dynamic support); in a downtrend below one launched from a swing high (dynamic resistance). The σ bands use the cumulative volume-weighted variance `Σp²V / ΣV − MIDAS²`; ATR bands use a rolling ATR instead.

## Topfinder / bottomfinder

When a trend *accelerates* away from its MIDAS curve, Levine's topfinder/bottomfinder fits a steeper, decelerating curve that catches back up to price and forecasts where the move ends. It re-weights the accumulation by `wᵢ = 1 − dᵢ/D`, where `dᵢ` is cumulative volume since launch and `D` is the projected **total** volume at which the move terminates:

```
TBF(j) = Σ pᵢ·Vᵢ·(1 − dᵢ/D) / Σ Vᵢ·(1 − dᵢ/D) = (A·D − B) / (C·D − E)
```

`D` is solved in closed form so the topfinder passes through the most recent same-direction swing after the launch (a pullback low for a topfinder, a pullback high for a bottomfinder):

```
D = (B − T·E) / (A − T·C)      with  A=ΣpV, B=ΣpVd, C=ΣV, E=ΣVd, T = fit price
```

The fit is accepted only when it still projects **forward from the current bar** (`D` greater than the volume accumulated *so far* — not just at the fit bar — so the projected end is never already in the past). The dashboard reports **progress `d/D`** and a 4-stage state:

| State | Meaning |
|---|---|
| `no fit` | no valid forward projection (range / non-accelerating leg) |
| `running` | fitted, move still early-to-mid through its projection |
| `late` | `d/D ≥` warn threshold (default 85 %) — **advanced move, not a confirmed turn** (`LATE` marker) |
| `expired` | `d/D ≥ 1` — the move ran past its projected end |

Re-fitting on each new same-direction pullback keeps the projection current. `late` is deliberately *not* called "exhausting": it says the move is far through its projected volume, which is context, not a reversal signal.

## Dashboard (Element | Value | Read)

Each row shows the raw value **and** its interpretation; the bottom **Read** row synthesises a single conclusion. The wording is **timeframe-aware** — the header shows the bucket (Intraday `< 4h` / Swing `4h–<1D` / Position `≥ 1D`), and intraday uses a wider stretch bar (it is noisier) with softer reversion language than higher timeframes.

| Row | Value | Read says |
|---|---|---|
| **Location** | distance in σ | `at value` / `stretched up·down` / `overextended up·down` (thresholds: Swing/Position ≥1σ·≥2σ, Intraday ≥1.5σ·≥2.5σ) |
| **Band zone** | inside / U1–U2 / above U2 … | `normal` / `stretched` / `extreme` |
| **Topfinder/Bottomfinder** | state + `d/D` | `no accel` / `move running` / `don't chase` (late) / `overrun` (expired) |
| **Trend** | above/below value + slope arrow | `buyers / sellers since launch` |
| **Anchor** | bars since anchor | `fresh (thin)` / `established` |
| **Read** | — | TF-aware headline, e.g. *"Overextended from value → mean-reversion to MIDAS likely"* (higher TF) vs *"Stretched — intraday, fade only on a trigger"* |

The Read is a **verbalisation of the existing role outputs** (Location / Trend / Exhaustion / Maturity) — it is context, not a new signal or a trigger.

## Modes & inputs

| Group | Key inputs |
|---|---|
| Anchor | mode (Manual Time / Daily Open / Auto Last Swing / Auto Swing Low / Auto Swing High), manual time, anchor swing left/right (significant degree), source |
| Bands | show, mode (VW StDev / ATR / Hybrid), mult 1 & 2, ATR length |
| Topfinder/Bottomfinder | enable, exhaustion warn `d/D`, fit swing left/right (smaller pullback degree) |
| Bias | Auto EMA / Up / Down, EMA length |
| Display | context markers, reclaim stretch lookback, dashboard + position, anchor markers, debug |
| Colors | MIDAS, TBF, bullish, bearish |

## Notes

- Auto-anchor modes re-anchor on the most recent **significant** swing (the `Anchor Swing` degree, default 20) — the origin of the current leg. A larger anchor degree keeps the curve on the current move rather than resetting on every minor wiggle (and avoids pinning it to the all-time extreme). The topfinder fits to the *smaller* `Fit Swing` pullbacks within that leg.
- The running sums are re-seeded from the actual pivot bar (`Anchor Swing Right` back); the pivot only sets the **anchor origin** — it is not a trigger, grade gate, or dedup key (design skill §8).
- The MIDAS and TBF curves jump at each re-anchor — each segment is an independent launch-anchored series.
- The topfinder is hidden when no valid forward fit exists (`no fit` in the dashboard). This is **expected** in range-bound or non-accelerating markets: the topfinder/bottomfinder only projects *accelerated* (parabolic) legs, so it typically fits on higher timeframes / strong trends and correctly stays `no fit` in intraday ranges (verified on NatGas — daily legs fit and the exhaustion warnings land near the major 2021/2022/2025 tops, while 1h/15m ranges show `no fit`). Turn on **Debug log** to see why a fit was rejected (`D<=d` = projected end already passed / no acceleration).
- **MIDAS (orange) crossing the TBF (purple) is not a signal.** They are different objects — a cumulative-VWAP level vs an accelerated projection — and they coincide at the launch by construction. What carries meaning is the *gap* between them: a TBF pulling far from MIDAS = strong acceleration (the move is outrunning its fair value); the two staying close = little acceleration. A literal crossover is just the projection passing through the level, not a turn.
- The TBF (purple) line forces a one-bar break on every re-anchor, so on long-history ("Alle") views you see separate projection episodes rather than one continuous diagonal. Each episode is an independent launch→projection.
- Context markers are deliberately small and unlabelled (design skill §9): they add information without overloading the decision logic.
