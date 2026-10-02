# CoilForge Zones v1.2

Detects price compression zones using a weighted, multi-module scoring system built from ATR compression, ADX chop filter, volume dry-up, impulse context, and historical support/resistance reuse. When a valid zone ends, the indicator stays armed for a configurable watch window and fires a breakout signal when price closes beyond the zone edge with a qualifying bar (and above-average volume where real volume exists).

## Features

- Multi-module compression scoring across five conditions (ATR, ADX, volume, impulse, historical S/R)
- Sensitivity presets — Strict / Balanced / Aggressive / Custom
- Minimum zone duration gate to suppress transient signals
- Dynamic bias detection via upper/lower touch pressure and EMA structure (ADX only as strength weight)
- Zone boxes with quality-based color and directional border coloring
- Post-zone breakout watch window — breakout can fire after the zone formally ends
- Historical pivot reuse detection for S/R confluence
- Old zone boxes with configurable lifetime and count cap
- Breakout alert conditions for both directions

## Scoring

Each bar receives a score (0–80) across five modules. Modules that are disabled contribute their full points unconditionally.

| Module | Points | Active when |
|--------|--------|-------------|
| ATR Compression | 25 | Range / ATR ≤ threshold; score scales linearly |
| ADX Chop | 15 | ADX ≤ threshold; score scales linearly |
| Volume Dry-Up | 15 | Volume below MA on both short and long window |
| Impulse-In Context | 15 | A prior directional move exceeds ATR × multiplier |
| Historical S/R Reuse | 10 | Range boundary aligns with a pivot (or earlier zone edge) from the historical lookback that lies before the current range window |

A bar qualifies as a zone candidate when enough structural evidence agrees (range compression, boundary-touch structure — see `Minimum Structure Evidence`) and the total score meets the minimum threshold. ADX only contributes score points; it is not a hard gate.

## Breakout Watch

When a valid zone ends (age ≥ minimum zone bars), the indicator arms a breakout watch window. A breakout fires when:

1. Close is beyond the zone boundary plus a buffer set by `Breakout Quality`
2. The bar has the body size and close position required by `Breakout Quality`
3. Volume exceeds the volume MA (only with real volume — otherwise this check passes through)
4. Optionally (`Avoid Breakouts Against Box Read`), the zone read does not point the other way

Direction comes from price closing beyond the edge; ADX/DI does not gate the breakout.

After a breakout fires — or after the watch window expires — the armed state clears automatically.

## Volume Data Validity

The Volume Dry-Up module only activates when `syminfo.volumetype` reports real trade volume (`base` or `quote`). On tick-volume instruments it degrades to the same neutral scoring path as a disabled module, and `breakoutVolumeOk` passes through unconditionally instead of gating on a tick-count series. The info table's "Volume" row already reports this as "Unavailable".

## Bias

Within an active zone the indicator counts how many bars tested the upper vs. lower boundary. Combined with the EMA structure (fast vs. slow EMA) and the prior impulse — ADX strength only lowers the touch pressure needed — it classifies the zone bias as: `Up`, `Down`, `Up / Continuation`, `Down / Continuation`, or `Neutral`. The zone box border reflects the current bias.
