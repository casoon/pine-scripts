# WaveTrend Advanced Smoothing

WaveTrend oscillator with a pluggable smoothing kernel and a rich visualization layer. The core formula follows the classic WaveTrend algorithm (EMA-based channel normalization), but every smoothing step can be replaced with one of eight kernels. Scale mode normalizes the output range independently of the kernel choice.

## Features

- **8 smoothing kernels** — EMA (classic), SMA, RMA, WMA, SuperSmoother (Ehlers), T3 (Tillson), KAMA (Kaufman), JMA (Jurik approximation)
- **Three scale modes** — Classic (raw values), Clamp ±100, Adaptive ±100 (dynamic range normalization)
- **Gradient line color** — WT main line transitions from bull color near OS to bear color near OB via `color.from_gradient`
- **Gradient shadow fills** — bear tint above zero (intensifies near OB), bull tint below zero (intensifies near OS)
- **4-state histogram** — rising positive / falling positive / falling negative / recovering negative, each in a distinct opacity
- **WT / Signal fill** — optional shaded fill between the main and signal lines
- **OB/OS zone fills** — flat color fills between the first and second OB/OS levels
- **Signal markers** — large triangles at extreme crosses (OB/OS zone), small circle dots for all other crosses
- **Alerts** — bull/bear extreme cross + plain cross-up / cross-down

## Smoothing Notes

All three smoothing steps (channel smoothing, deviation smoothing, oscillator smoothing) share the same kernel selection. KAMA and JMA are stateful filters; their internal state is correctly initialized with `var` so they persist across bars. SuperSmoother is a two-pole Ehlers filter — its state variables are also declared `var`.

## Scale Modes

| Mode | Behavior |
|---|---|
| Classic | Output follows raw CI normalization; values can exceed ±100 on high-momentum instruments |
| Clamp ±100 | Hard clips to `[-100, 100]` — useful for visual consistency |
| Adaptive ±100 | Rescales to `[-100, 100]` based on the highest absolute value over the adaptive lookback — maintains proportional shape while bounding the display range |
