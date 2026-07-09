# Changelog

## v1.4 — 2026-07-09
- Fixed Sentiment Bar color: it used `score > 0 ? colBull : colBear`, coloring the overbought side (positive score) bull and the oversold side (negative score) bear — backwards from every other color cue in the panel (gradient line, Bull/Bear Stretch triangles), where `colBull` marks the oversold/bullish-reversal side and `colBear` the overbought/bearish-reversal side. Swapped to match.

## v1.3 — 2026-07-09
- Added Sentiment Bar (group 8, on by default): live label at the panel's right edge scoring how far ROC sits inside its own stretch zone, ±100 with a mini bar — ported from Williams VIX Fix Advanced's Sentiment Bar, adapted from a bull/bear two-formula comparison to a single signed line vs. its own zone.
- Added Signal Quality (group 8, off by default): optional 0-100 score next to each Bull/Bear Stretch marker, weighted 50% stretch-zone depth + 25% context agreement + 25% stall-free — same weighting as Williams VIX Fix Advanced's Spike Quality.

## v1.2 — 2026-07-09
- Raised default Signal Length from 3 to 9 — at equal length to the main-line smoothing (avgLen=3), the signal line tracked the ROC line too closely to produce a visible separation or usable histogram/crossover signal.

## v1.1 — 2026-07-09
- Removed fixed ±20 upper/lower zone boundary hlines and their stretch-zone fill — these forced the panel's autoscale regardless of actual ROC range, compressing the ROC/signal/context lines near zero on instruments where ROC magnitude stays well under 20. The panel now autoscales to the real data range.

## v1.0 — 2026-06-30
- Initial release: percentage ROC core with smoothed signal, zero midline, ±5% stretch zones, gradient line, shadow fills, ROC/signal fill, histogram, stretch-zone crosses, zero-cross alerts, stall/absorption layer, trend context line, counter-trend weak markers, and trend divergence wedge
