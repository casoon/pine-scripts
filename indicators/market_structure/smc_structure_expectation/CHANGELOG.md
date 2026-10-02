# Changelog

## v1.1.5 — 2026-10-02
- Fix: the leg-strength part of OB priority was effectively dead — it was only computed in High/Low-cross mode with confirmation, and there it divided a leg by itself (ratio ≈ 1, never "strong"). The swing preceding each BOS level is now stored; on a valid BOS, impulse = prior low → broken high and correction = broken high → HL (mirrored for bearish: prior high → broken low vs broken low → LH). Computed in both BOS modes, so the leg-strength priority bonus and the STR/WEK log tag now reflect the actual legs

## v1.1.4 — 2026-10-02
- Fix: order block reaction type, mitigation and invalidation were already checked on the BOS bar that created the OB — the impulse bar's own low/high often sits inside the zone, so the OB could count as tapped or mitigated at birth and its reaction type froze there. These checks now start on the bar after the BOS
- "Only HIGH Priority OB Alerts" tooltip now states that the standard Bullish/Bearish Confirmation alerts never fire while it is on

## v1.1.3 — 2026-10-02
- Fix: Bullish/Bearish BOS, the order blocks created from them, their alerts and labels almost never fired. The expectation flags (Expect HL / LH / Continuation / Failure) were only true on the single bar an expectation was set, while BOS checks them on the later break bar. The flags now follow the persistent expectation state on every bar — this also makes the "Expect HL/LH" invalidation and the Expectation bar coloring work beyond that first bar

## v1.1.2 — 2026-09-05
- Fix: OB volume bonus (relative-volume score tiers) and the optional "Require Volume > SMA(20)" filter used raw `volume` with no check on `syminfo.volumetype` — on feeds that report tick volume, this scored/gated order blocks against a meaningless tick count. Added a `volumeIsReal` guard (`base`/`quote` only); the score bonus now degrades to +0 (na) instead of a fabricated tier, and the volume filter passes through neutrally instead of blocking OB creation when volume isn't real
- Added a one-time chart label on the last bar when volume isn't real, so the degradation is visible instead of silent
- Data Contract header block added (`Volume: OPTIONAL`, `Verdict: CFD-degraded`)

## v1.1.1 — 2026-06-29
- Alerts: messages standardized to `SMCE · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.1.0 — 2026-06-11
- Fix: displacement window input ("Displacement Lookback" / auto-adjust window) is now actually used — displacement was previously hardcoded to a 3-bar window regardless of settings
- Fix: BOS cross detection (`ta.crossover`/`ta.crossunder`) and Layer-4 swing-break crosses moved to global scope — calling them inside conditional branches builds inconsistent history and could miss or fake cross events after a BOS level was consumed
- Fix: expectation zone now uses a single tracked box instead of creating a new box every bar (stacked transparency, box-limit churn)
- Dashboard and OB rejection heatmap converted to the standard light-theme table style
- Removed dead code: unused `medianRange` series and write-only `legHigh`/`legLow` state

## v1.0.0
- Initial release
