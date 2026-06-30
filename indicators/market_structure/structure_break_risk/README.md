# Structure Break Risk

An indicator that answers one question: *how close is the prevailing trend's structure to breaking — and against which level?* It is the companion to [Trend Persistence Score](../../trend_strength/trend_persistence_score/) — where TPS measures how *clean* a trend is, Structure Break Risk (SBR) measures how *close it is to breaking*.

It lives in a dedicated **RSI pane** and draws onto the **price chart** above it (via `force_overlay`), because the read needs both:

- **RSI pane** — the RSI with **momentum-divergence lines** drawn on it. When price makes a higher high while RSI makes a *lower* high (uptrend), or price a lower low while RSI a *higher* low (downtrend), a line marks the failing momentum. Read against the price above — sharing the same time axis — the divergence is unmistakable: the earliest structural crack. A divergence is *price vs. momentum* and is only readable where both are visible, which is why it lives here rather than as an abstract line on price. A compact **"Div"** label carries the RSI values in its tooltip.
- **Price chart** — the decisive **break-level line** the trend must hold, a shaded **risk zone** for the cushion between price and that level, a thin **Trend Context** EMA line, word **event labels** (Watch / Break Pressure / Structure Broken / Pressure Faded) and the info label.

The risk *magnitude* — the same 0–100 composite — is reported in a single compact, mobile-friendly **info label**. Colour encodes the **risk band** (neutral → orange → red → dark red), never the trade direction, so it never reads as buy/sell; direction is stated in words.

SBR is **symmetric by design**: in an uptrend it scores **top-break** risk, in a downtrend **bottom-break** risk. The asymmetry comes entirely from the situation (which trend is active), never from a hardcoded long/short. The trend context **latches** — it holds the last clear direction through transition zones, so risk can build *before* the trend formally flips (exactly where the break is forming). Until a first direction is established the gauge reads `No trend` and sits at zero.

The headline idea: **risk rises as price approaches the decisive break level and extra evidence stacks up** — not only after the break is confirmed. A **Reason** read names the dominant driver in plain language (Approaching break level / Failed breakout / Structure eroding / Momentum divergence / Break confirmed) so the score explains itself.

Pivots are used as **swing-level references only** (Location); the *break event* (a close beyond the opposite swing) is the Trigger. The pivot itself is never the signal.

## Features

- Five evidence sensors across the roles, weighted into one score — never an AND-chain
- Symmetric top-/bottom-break scoring driven by a **latching** prevailing-trend context
- **RSI pane** with 70 / 50 / 30 reference levels and **momentum-divergence lines** drawn on the RSI (price extends but RSI does not), with a compact "Div" label and RSI values in the tooltip — divergence shown where it is actually readable
- **Break-level line** drawn on price (the decisive swing the trend must hold, coloured by the current risk band) + a **risk zone** shading the cushion between price and that level, intensifying as risk rises (shown from Watch upward)
- Thin **Trend Context line** (EMA) on price showing which trend is at risk — colour stays risk-coded, not buy/sell
- Word **event labels** placed on the side at risk — Watch / Break Pressure / Structure Broken / Pressure Faded — with cooldown; confirmed breaks require an EMA context flip
- **State** read — No trend / Quiet / Watch / Break Pressure / Critical / Structure Broken — plus a plain-language **Reason** naming the dominant driver
- Compact, mobile-friendly **info label** (text, not a table; sized Small/Normal/Large): score, state, direction, break level, distance-in-ATR, reason and a **mini-bar per sensor** (BOS shown separately as a confirmed event, not mixed into the score)
- Debug log on state change · risk-band colours encode risk, never direction
- Break Pressure / Critical / Top-Break / Bottom-Break **alerts**

## Sensors

| Sensor | Role | Reads (uptrend → top-break) |
|---|---|---|
| **Near Break Level** | Location → Trigger | Distance from close to the last swing low, in ATR — risk rises on approach (full within `Near Break Level ATR Distance`) |
| **Confirmed BOS** | Trigger | Close below the last swing low — graded by depth in ATR (confirmed break floored at 0.65) |
| **Failed Breakout / SFP** | Trigger + Location | High sweeps above the last swing high but the bar closes back below it |
| **Structure Erosion** | Structure | The most recent swing high is *lower* than the prior one — graded by the drop in ATR |
| **Pivot Divergence** | Momentum | The latest price-pivot high is higher than the prior, but RSI sampled at those pivots is lower |

Each sensor mirrors symmetrically for a downtrend (higher low, break above swing high, bullish divergence, etc.). Transient sensors are held for `Evidence Hold Bars` so the gauge reflects recent structural evidence rather than a single firing bar.

## Score and state

`risk = Σ(sensorᵢ · weightᵢ) / Σweight · 100`, EMA-smoothed, gated to zero when no trend context exists. Interpretation: **0–35** Quiet, no acute break risk · **35–60** Watch · **60–80** Break Pressure, structure turning critical · **80–100** Critical — break very near, or **Structure Broken** once a close confirms beyond the swing with the EMA context flipped. The risk-band colour (neutral → orange → red → dark red) tells you the severity, not the trade direction; *which* structure is tested is named in words ("Uptrend at risk" / "Downtrend at risk").

## How to use

- **Trend management:** rising SBR inside a position warns the trend structure is deteriorating before the move fully reverses.
- **With TPS:** read them together — `SBR high + TPS low` = M-top / structure break plausible (unclean *and* breaking); `SBR low + TPS low` = just range / chop, no clean break; `SBR high + TPS high` = strong trend running but approaching a critical level.
- **Confirmation, not prediction:** the strongest sensor (Break of Structure) only fires on an actual close beyond the swing — SBR escalates as evidence accumulates rather than calling a top in advance.

## Notes

- Symmetric and situation-driven — it never assumes long or short; the active trend decides which structure is tested.
- Default lengths suit swing timeframes (4h/1D). Shorten `Swing Pivot Length` and `Range Window` for intraday.
