# Structure Break Risk

A forward-looking **0–100 risk gauge** that answers one question: *how much evidence is there that the prevailing trend's structure is breaking down?* It is the companion to [Trend Persistence Score](../../trend_strength/trend_persistence_score/) — where TPS measures how *clean* a trend is, Structure Break Risk (SBR) measures how *close it is to breaking*.

SBR is **symmetric by design**: in an uptrend it scores **top-break** risk, in a downtrend **bottom-break** risk. The asymmetry comes entirely from the situation (which trend is active), never from a hardcoded long/short. The trend context **latches** — it holds the last clear direction through transition zones, so risk can build *before* the trend formally flips (exactly where the break is forming). Until a first direction is established the gauge reads `No Context` and sits at zero.

The headline idea: **risk rises as price approaches the decisive break level and extra evidence stacks up** — not only after the break is confirmed. A **Reason** read names the dominant driver (Near Break Level / Failed Breakout / Structure Erosion / RSI Divergence / Confirmed BOS) so the score explains itself.

Pivots are used as **swing-level references only** (Location); the *break event* (a close beyond the opposite swing) is the Trigger. The pivot itself is never the signal.

## Features

- Five evidence sensors across the roles, weighted into one score — never an AND-chain
- Symmetric top-/bottom-break scoring driven by a **latching** prevailing-trend context
- **State** read — No Context / Low / Elevated / High / Critical — plus a **Reason** explaining the dominant driver
- Two-dimensional oscillator: **height** = risk, **colour** = implied resolution (red = top-break/bearish, green = bottom-break/bullish), **saturation** = risk level, plus an optional heat-column fill
- Optional **confirmed-break markers** on the bar price actually closes beyond the opposite swing (a real BOS event), default off
- Single compact **info label** (mobile-friendly, sized Small/Normal/Large) carrying the full read — risk, state, direction, reason and all five sensor values — plus a debug log on state change
- High / Critical / Top-Break / Bottom-Break **alerts**

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

`risk = Σ(sensorᵢ · weightᵢ) / Σweight · 100`, EMA-smoothed, gated to zero when no trend context exists. Interpretation: **0–35** no acute break risk · **35–60** watch · **60–80** high, structure turning critical · **80–100** break very near or already confirmed. The implied-direction colour tells you which way a resolution would break.

## How to use

- **Trend management:** rising SBR inside a position warns the trend structure is deteriorating before the move fully reverses.
- **With TPS:** read them together — `SBR high + TPS low` = M-top / structure break plausible (unclean *and* breaking); `SBR low + TPS low` = just range / chop, no clean break; `SBR high + TPS high` = strong trend running but approaching a critical level.
- **Confirmation, not prediction:** the strongest sensor (Break of Structure) only fires on an actual close beyond the swing — SBR escalates as evidence accumulates rather than calling a top in advance.

## Notes

- Symmetric and situation-driven — it never assumes long or short; the active trend decides which structure is tested.
- Default lengths suit swing timeframes (4h/1D). Shorten `Swing Pivot Length` and `Range Window` for intraday.
