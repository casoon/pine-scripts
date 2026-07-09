# Changelog

## v1.3 — 2026-07-09
- Fixed Sentiment Bar color: it used `score > 0 ? colBull : colBear`, coloring the overbought side (positive score) bull and the oversold side (negative score) bear — backwards from every other color cue in the panel (gradient line, Bull/Bear Extreme triangles), where `colBull` marks the oversold/bullish-reversal side and `colBear` the overbought/bearish-reversal side. Swapped to match.

## v1.2 — 2026-07-09
- Added Sentiment Bar (group 8, on by default): live label at the panel's right edge scoring how far Fisher sits inside its own OB/OS zone, ±100 with a mini bar — ported from Williams VIX Fix Advanced's Sentiment Bar.
- Added Signal Quality (group 8, off by default): optional 0-100 score next to each Bull/Bear Extreme marker, weighted 50% OB/OS-zone depth + 25% context agreement + 25% stall-free — same weighting as Williams VIX Fix Advanced's Spike Quality.

## v1.1 — 2026-07-09
- Removed fixed ±3 upper/lower zone boundary hlines and their OB/OS zone fill — these forced the panel's autoscale regardless of the actual (smoothed) Fisher range, compressing the lines near zero when the smoothed value stayed well under ±3. The panel now autoscales to the real data range.
- Raised default Signal Length from 3 to 9 — at a length close to the main-line smoothing (avgLen=2), the signal line tracked the Fisher line too closely to produce a visible separation or usable histogram/crossover signal.

## v1.0 — 2026-06-30
- Initial release: Fisher Transform core with smoothed signal, zero midline, ±1.5 extreme zones, gradient line, shadow fills, Fisher/signal fill, histogram, extreme-zone crosses, zero-cross alerts, stall/absorption layer, trend context line, counter-trend weak markers, and trend divergence wedge
