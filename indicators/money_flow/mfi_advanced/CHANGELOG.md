# Changelog

## v1.2 — 2026-07-09
- Added Sentiment Bar (group 8, on by default): live label at the panel's right edge scoring how far MFI sits inside its own OB/OS zone, ±100 with a mini bar — ported from Williams VIX Fix Advanced's Sentiment Bar. Reads neutral (0) when the no-volume fallback pins MFI to 50.
- Added Signal Quality (group 8, off by default): optional 0-100 score next to each Bull/Bear Extreme marker, weighted 50% OB/OS-zone depth + 25% context agreement + 25% stall-free — same weighting as Williams VIX Fix Advanced's Spike Quality.

## v1.1 — 2026-07-09
- Raised default Signal Length from 3 to 9 — at equal length to the main-line smoothing (avgLen=3), the signal line tracked the MFI line too closely to produce a visible separation or usable histogram/crossover signal.

## v1.0 — 2026-06-30
- Initial release: MFI core with smoothed signal, neutral no-volume fallback, 50 midline, 80/20 zones, gradient line, shadow fills, MFI/signal fill, histogram, extreme-zone crosses, 50-cross alerts, stall/absorption layer, trend context line, counter-trend weak markers, and trend divergence wedge
