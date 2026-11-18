# CoilForge Zones v1.2

Detects price compression zones using a weighted, multi-module scoring system built from ATR compression, ADX chop filter, volume dry-up, impulse context, and historical support/resistance reuse. When a valid zone ends, the indicator stays armed for a configurable watch window and fires a breakout signal when price closes beyond the zone edge with a qualifying bar (and above-average volume where real volume exists).

## Features

- Multi-module compression scoring across five conditions (ATR, ADX, volume, impulse, historical S/R)
- Sensitivity presets — Strict / Balanced / Aggressive / Custom
- Minimum zone duration gate (bars the zone condition actually held) to suppress transient signals
- Dynamic bias detection via upper/lower touch pressure and EMA structure (ADX only as strength weight)
- Zone boxes with quality-based color and directional border coloring
- Post-zone breakout watch window — breakout can fire after the zone formally ends
- Historical pivot reuse detection for S/R confluence
- Old zone boxes with configurable lifetime and count cap
- Breakout alert conditions for both directions

## Scoring

Each bar receives a score (0–80) across five modules. The score is normalized over the modules that are enabled and measurable: a disabled module — or Volume Dry-Up without real volume — drops out of the weighting instead of contributing points.

| Module | Points | Active when |
|--------|--------|-------------|
| ATR Compression | 25 | Range / ATR ≤ threshold; 40% of the points at the threshold, rising linearly to 100% |
| ADX Chop | 15 | ADX ≤ threshold; 40% of the points at the threshold, rising linearly to 100% |
| Volume Dry-Up | 15 | Volume below MA on both short and long window |
| Impulse-In Context | 15 | The move into the base (measured before the range window, frozen when the zone starts) exceeds ATR × multiplier |
| Historical S/R Reuse | 10 | Range boundary aligns with a pivot (or earlier zone edge) from the historical lookback that lies before the current range window |

A bar qualifies as a zone candidate when enough structural evidence agrees (range compression, boundary-touch structure — see `Minimum Structure Evidence`) and the total score meets the minimum threshold. Once running, the zone holds while at least one of the structure conditions still holds — score and full structure only decide the start. ADX only contributes score points; it is not a hard gate.

## Breakout Watch

When a valid zone ends (the zone condition held for at least `Minimum Zone Bars`), the indicator arms a breakout watch window. A breakout fires when:

1. Close is beyond the zone boundary plus a buffer set by `Breakout Quality`
2. The bar has the body size and close position required by `Breakout Quality`
3. Volume exceeds the volume MA (only with real volume — otherwise this check passes through)
4. Optionally (`Avoid Breakouts Against Box Read`), the zone read does not point the other way

Direction comes from price closing beyond the edge; ADX/DI does not gate the breakout. Breakouts are evaluated on confirmed bars only, so markers and alerts do not appear and vanish on the open bar. The read used by `Avoid Breakouts Against Box Read` is frozen at the last bar of the zone — the breakout bar does not change it.

After a breakout fires — or after the watch window expires — the armed state clears automatically.

## Volume Data Validity

The Volume Dry-Up module only activates when `syminfo.volumetype` reports real trade volume (the feed delivers volume and the type is not `tick`). On tick-volume instruments it drops out of the score weighting, like a disabled module, and `breakoutVolumeOk` passes through unconditionally instead of gating on a tick-count series. The info table's "Volume" row already reports this as "Unavailable".

## Bias

Within an active zone the indicator counts how many bars tested the upper vs. lower boundary. Combined with the EMA structure (fast vs. slow EMA) and the prior impulse — ADX strength only lowers the touch pressure needed — it classifies the zone bias as: `Up`, `Down`, `Up / Continuation`, `Down / Continuation`, or `Neutral`. The zone box border reflects the current bias.

The zone box is drawn back over the range window that qualified it. A dotted vertical line inside the box marks the bar the zone was actually detected on — only from there on was the zone visible in real time.
