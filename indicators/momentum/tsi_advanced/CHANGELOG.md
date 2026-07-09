# Changelog

## v1.2 — 2026-07-09
- Fixed Sentiment Bar color: it used `score > 0 ? colBull : colBear`, coloring the overbought side (positive score) bull and the oversold side (negative score) bear — backwards from every other color cue in the panel (gradient line, Bull/Bear Extreme triangles), where `colBull` marks the oversold/bullish-reversal side and `colBear` the overbought/bearish-reversal side. Swapped to match.

## v1.1 — 2026-07-09
- Added Sentiment Bar (group 8, on by default): live label at the panel's right edge scoring how far TSI sits inside its own stretch zone, ±100 with a mini bar — ported from Williams VIX Fix Advanced's Sentiment Bar.
- Added Signal Quality (group 8, off by default): optional 0-100 score next to each Bull/Bear Extreme marker, weighted 50% stretch-zone depth + 25% context agreement + 25% stall-free — same weighting as Williams VIX Fix Advanced's Spike Quality.

## v1.0 — 2026-06-30
- Initial release: TSI core with smoothed signal, zero midline, ±25 stretch zones, gradient line, shadow fills, TSI/signal fill, histogram, stretch-zone crosses, zero-cross alerts, stall/absorption layer, trend context line, counter-trend weak markers, and trend divergence wedge
