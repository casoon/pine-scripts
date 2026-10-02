# Changelog

## v1.3.3 — 2026-10-02
- Oscillator scale no longer inherits the chart symbol's price precision (values like 80,0000 on 4-decimal symbols such as NATGAS) — shows 2 decimals

## v1.3.2 — 2026-10-02
- Fixed: Signal Quality could never exceed ~83 — zone depth was divided by the midline-to-zone distance instead of the zone's own width. Depth is now measured across the OS zone (OS level → 0) and OB zone (OB level → 100), so the documented 0-100 range is reachable; quality values on deep extremes rise accordingly
## v1.3.1 — 2026-09-05
- Data validity: added a hard Exchange-only gate — `volumeIsReal` checks `syminfo.volumetype` (`base`/`quote` only) and every volume/typical-price-flow reference now runs on a gated `vol` value that is `na` on invalid instruments, instead of `nz(volume, 0.0)`
- Removed the neutral-50 no-volume fallback — MFI, signal, histogram, context line, and all signal/alert conditions go blank (`na`) on instruments without real trade volume instead of pinning to a neutral midline value
- Added a Data Contract header block (`Verdict: Exchange-only`)
- Added a one-time "benötigt echtes Handelsvolumen" warning label on the last bar when volume is not real, showing the detected `syminfo.volumetype`

## v1.3 — 2026-07-09
- Fixed Sentiment Bar color: it used `score > 0 ? colBull : colBear`, coloring the overbought side (positive score) bull and the oversold side (negative score) bear — backwards from every other color cue in the panel (gradient line, Bull/Bear Extreme triangles), where `colBull` marks the oversold/bullish-reversal side and `colBear` the overbought/bearish-reversal side. Swapped to match.

## v1.2 — 2026-07-09
- Added Sentiment Bar (group 8, on by default): live label at the panel's right edge scoring how far MFI sits inside its own OB/OS zone, ±100 with a mini bar — ported from Williams VIX Fix Advanced's Sentiment Bar. Reads neutral (0) when the no-volume fallback pins MFI to 50.
- Added Signal Quality (group 8, off by default): optional 0-100 score next to each Bull/Bear Extreme marker, weighted 50% OB/OS-zone depth + 25% context agreement + 25% stall-free — same weighting as Williams VIX Fix Advanced's Spike Quality.

## v1.1 — 2026-07-09
- Raised default Signal Length from 3 to 9 — at equal length to the main-line smoothing (avgLen=3), the signal line tracked the MFI line too closely to produce a visible separation or usable histogram/crossover signal.

## v1.0 — 2026-06-30
- Initial release: MFI core with smoothed signal, neutral no-volume fallback, 50 midline, 80/20 zones, gradient line, shadow fills, MFI/signal fill, histogram, extreme-zone crosses, 50-cross alerts, stall/absorption layer, trend context line, counter-trend weak markers, and trend divergence wedge
