# CoilForge Zones v1.2

Detects price compression zones using a weighted, multi-module scoring system built from ATR compression, ADX chop filter, volume dry-up, impulse context, and historical support/resistance reuse. When a valid zone ends, the indicator stays armed for a configurable watch window and fires a confirmed breakout signal only when price exits with volume and rising ADX.

## Features

- Multi-module compression scoring across five conditions (ATR, ADX, volume, impulse, historical S/R)
- Sensitivity presets — Strict / Balanced / Aggressive / Custom
- Minimum zone duration gate to suppress transient signals
- Dynamic bias detection via upper/lower touch pressure and DI comparison
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
| Historical S/R Reuse | 10 | Zone boundary aligns with a pivot from the lookback window |

A bar qualifies as a zone candidate when the mandatory gates (ATR, ADX) pass and the total score meets the minimum threshold.

## Breakout Watch

When a valid zone ends (age ≥ minimum zone bars), the indicator arms a breakout watch window. A breakout fires when:

1. Close crosses above (up) or below (down) the zone boundary
2. Volume exceeds the volume MA
3. ADX is rising (current > prior bar)

After a breakout fires — or after the watch window expires — the armed state clears automatically.

## Bias

Within an active zone the indicator counts how many bars tested the upper vs. lower boundary. Combined with DI direction and the prior impulse, it classifies the zone bias as: `Up`, `Down`, `Up / Continuation`, `Down / Continuation`, or `Neutral`. The zone box border reflects the current bias.
