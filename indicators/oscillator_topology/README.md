# Oscillator Topology

Analyzes the shape of WaveTrend movements rather than their magnitude or direction. Curvature, peak/trough width, and asymmetry encode information that is not visible in the raw oscillator value. A V-Spike signals an aggressive, high-conviction reversal; a Round Top indicates exhaustion building slowly; a Flat Zone signals trend death or distribution; an Asymmetric shape (fast rise, slow fall, or vice versa) hints at hidden directional flow. Each classified pivot is annotated on the chart; the dashboard summarizes the current dominant shape.

## Features

- Curvature at WT pivot extremes: 2nd derivative normalized by ATR to make it scale-free
- Width of the last WT peak/trough: bars spent within the extreme zone
- Asymmetry index: rise speed versus fall speed measured at each pivot
- Shape classification per pivot: V-Spike / Round / Flat / Asymmetric
- Curvature plot and shape label drawn at each classified pivot
- Dashboard with the current dominant shape and a topology summary

## Settings

| Group | Setting | Default | Notes |
|---|---|---|---|
| WaveTrend | Channel Length | 10 | |
| WaveTrend | Average Length | 21 | |
| Topology Settings | Pivot Left Bars | 5 | Confirmation bars to the left of each pivot |
| Topology Settings | Pivot Right Bars | 5 | Confirmation bars to the right of each pivot |
| Topology Settings | V-Spike Curvature Threshold | 3.0 | Normalized curvature above this = V-Spike; lower = more sensitive |
| Topology Settings | Flat Zone Min Bars | 4 | Minimum consecutive bars near extreme to classify as Flat |
| Topology Settings | Flat Zone Tolerance | 0.15 | Fraction of pivot height defining the flat band |
| Display | Show Curvature Line | on | |
| Display | Show Shape Labels | on | Labels at classified pivots |
| Display | Show Dashboard | on | |
