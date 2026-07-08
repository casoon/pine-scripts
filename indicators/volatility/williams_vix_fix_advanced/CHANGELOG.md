# Changelog

## v1.9 — 2026-07-07
- Fixed: bearish stall/absorption used the bullish `stallNow` flag — added an independent `bStallNow` computed from `bwvf`, so bull-side stalls no longer suppress/soften bear spikes
- Added Spike Quality (0–100): how far a spike pushed past its own band/context EMA, penalized by stall/absorption; captured per side into `lastBullQuality`/`lastBearQuality`
- Added Reclaim: marks price reclaiming the range within N bars of a non-absorbed spike, with the originating spike's quality shown on the label; new "Reclaim Long"/"Reclaim Short" alerts
- Fixed: Reclaim labels were placed at `low`/`high` (the underlying instrument's price) instead of `wvf`/`-bwvf` — blew up the oscillator panel's scale to the instrument's price range
- Reclaim labels shrunk to a single tiny colored arrow (▲/▼) — the spike quality and description moved into the hover tooltip instead of being printed on the label
- Added View Mode (Clean / Balanced / Full) to control how many layers show at once — addresses the panel being visually overloaded with WVF, Bear WVF, both band pairs, both context lines, zone fills, and the divergence fill all active by default

## v1.8 — 2026-07-07
- Replaced the per-bar Bull/Bear Spike arrow markers with a Sentiment Bar: a live ±100 bull/bear dominance score (`WVF ÷ its band − Bear-WVF ÷ its band`) with a mini bar, on the right edge of the panel — the arrows were easy to miss and didn't say how strong the current read was
- Reworked the Sentiment Bar from a fixed Bullish/Bearish label to the graded score above, so it reflects the current WVF/Bear-WVF balance instead of asserting a discrete state
- Input renamed: "Show Spike Markers" → "Show Sentiment Bar"
- Removed the now-unused "Long context (weak)" color input

## v1.7 — 2026-07-02
- Linienfarben: grün/rot entfernt (suggerierte fälschlich Long/Short-Richtung); Bull-WVF ist jetzt Cyan (hell = aktiv, gedimmt = inaktiv), Bear-WVF ist Lila — die Pfeile bleiben die eigentliche Signal-Aussage

## v1.6 — 2026-07-02
- Spiegel-Modell: Bear-WVF wird als `-bwvf` unterhalb der Nulllinie gespiegelt — obere Hälfte = Angst/Boden-Signal (grün), untere Hälfte = Sorglosigkeit/Top-Signal (rot)
- Context-EMA für beide Seiten (`ctxWVF` und `ctxBWVF`), Bänder ebenfalls gespiegelt
- Zone-Fills zwischen WVF/Bear-WVF und Nulllinie ersetzen die alten Shadow-Fills
- Nulllinie als zentrale Trennlinie, optionale ±Referenzlinien

## v1.5 — 2026-07-02
- WVF-Linie binär eingefärbt: grün (#00c853) wenn WVF ≥ Context-EMA (Surge), rot (#d50000) wenn darunter (Abkühlung); beide Farben als Inputs konfigurierbar

## v1.4 — 2026-07-02
- Histogram entfernt; WVF-Linie zeigt stattdessen den Zustand: Gradient (calm→fear) wenn WVF ≥ Context-EMA (Surge), gedämpftes Cyan wenn WVF < Context-EMA (Abkühlung)

## v1.3 — 2026-07-02
- Removed `hline(obLevel=20)` — was anchoring Y-axis to 0–100→0–20 range, making the panel illegible on instruments where WVF stays below 5
- Spike markers now fire only on the first crossing bar (`spikeCross = spikeRaw and not spikeRaw[1]`), eliminating dense marker clusters during sustained spike conditions

## v1.2 — 2026-07-02
- Context line changed from a higher-period WVF to EMA(WVF, N) — acts as a D-line (signal line); histogram (WVF − context) now spikes positive on fear extremes instead of going deeply negative
- `usePercentile` default changed to off — only the StdDev 2σ band triggers spikes by default, reducing noise on sub-daily / low-volatility instruments
- Removed `hline(100)` and `pTop = plot(100)` — these anchored the Y-axis to 0–100 regardless of actual WVF values, making the panel illegible on sub-daily/forex instruments
- Removed StdDev Band fill-to-top (fill between band and 100 no longer exists)

## v1.1 — 2026-07-02
- Spike markers moved to `location.absolute` — appear at the actual WVF value instead of fixed top/bottom panel edges
- Added `Min absolute WVF level for spike` input (default 0, disabled) — allows suppressing trivial spikes on instruments where WVF values are inherently small (e.g. forex hourly: set to 5–10)
- `Min WVF Surge` (stall detection) default lowered 5.0 → 2.0 so stall detection is active for small-range WVF values

## v1.0 — 2026-07-02
- Initial release: Bullish + Bearish WVF, StdDev/percentile spike bands, stall/absorption, slow-WVF context, divergence wedge, histogram, gradient coloring, shadow fills, 5 alert conditions
