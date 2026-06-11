# MSO — Market Stress Oscillator

Bi-directional Williams VIX Fix stress oscillator. Downside stress (dip/fear) and upside stress (blow-off/greed) are computed as separate WVF series, z-scored over a rolling window, and plotted mirrored around zero. Stress extremes are filtered by JMA trend slope and ADX, clustered via peak-hold, and validated with an ATR-normalized follow-through check that classifies each event as accepted or rejected.

## Features

- Bi-directional Williams VIX Fix: separate downside (close-high vs low) and upside (close-low vs high) stress lines, z-scored
- Per-timeframe presets (15m / 1h / 4h / D / W / M, auto-selected by chart TF or manual) for WVF lookback, z-window, z-threshold, JMA length, ADX minimum, and quality settings
- Quality gating: minimum extreme duration, cooldown between events, JMA slope filter, ADX trend-strength filter
- Peak-hold clustering: only the strongest bar per stress cluster generates an event
- Acceptance/rejection: forward follow-through measured in ATR multiples over a reaction window — DA/DR (downside) and UA/UR (upside) chart labels, with Classic LA/LR/SA/SR label mode
- Acceptance score (0–1) plotted in the pane as line or histogram
- Macro bias line (downside z minus upside z, smoothed) with dominance band, fill, regime background, and zero-cross markers
- HTF wind labels: higher-timeframe (D/W) bias flips labeled on the chart
- Clarity labels: bias regime entry aligned with the HTF wind above a configurable threshold
- Stress zones drawn as boxes in the pane (accepted = stronger fill), peak level lines and reaction lines on the chart
- Pivot validation with ZigZag-style filters and optional Pine-log event logging (stress → pivot matching) for CSV export
- Intuitive (downside = green) or Technical (downside = red) color mode
- Alerts: downside/upside accepted and rejected, clarity regime entry, HTF wind flip

## Event Logic

1. A stress extreme fires when the z-score exceeds the per-TF threshold for at least the minimum number of bars and the JMA slope + ADX filters agree.
2. With peak-hold enabled, the cluster's strongest bar becomes the event candidate when the cluster ends.
3. After the reaction window, follow-through (in ATR from the peak price) decides acceptance: `follow >= MinFollow ATR` → accepted, otherwise rejected.
4. Cooldown bars suppress new events in the same direction after each evaluation.
