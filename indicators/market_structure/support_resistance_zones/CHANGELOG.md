# Changelog

## v0.1.11 — 2026-08-12
- Prevented routine Pivot Cluster / Multiple Test double scoring: an accepted PC candidate now suppresses the MT pivot candidate on the same side; MT is normally awarded only after repeated real lifecycle touches, while its stricter pivot clustering remains a fallback when PC is not accepted

## v0.1.10 — 2026-08-12
- Replaced the hard 120-pivot storage cap with pruning by actual `Pivot Cluster History` bar distance, so configured long-history cluster and liquidity searches are no longer silently truncated on pivot-dense charts

## v0.1.9 — 2026-08-12
- Registry merge now evaluates every valid same-direction target and selects the nearest zone midpoint instead of taking the first matching zone in age/storage order

## v0.1.8 — 2026-08-12
- Compact-base departure is now one source of evidence: when both Base and Supply/Demand are enabled, it creates and scores `SD` only; `BASE` is the fallback when Supply/Demand is disabled. This removes the former `BASE+SD` double count from one raw pattern

## v0.1.7 — 2026-08-12
- Equal High/Low liquidity detection now searches all retained confirmed pivots inside the configured tolerance instead of comparing only the immediately preceding pivot; intervening unrelated pivots no longer hide valid LIQ zones

## v0.1.6 — 2026-08-12
- Candidate ingestion and lifecycle updates now run on confirmed bars only, preventing intrabar OB/base/FVG/gap candidates and transient touch/break/reaction states
- Prevented birth-bar self-touches and same-break-bar flip confirmations: a new zone cannot validate itself; a flipped zone waits for a later interaction before a reaction can confirm it
- Classical GAP zones now represent only the residual unfilled range (`high[1]..low` bullish, `high..low[1]` bearish); opening gaps filled by the same candle no longer create boxes
- Added `lastEvidenceBar`, updated on every merge, so fresh reinforcement extends a zone's analysis lifetime without changing its visual creation anchor; broken zones are no longer merge targets
- Renderer now selects supports at/below and resistances at/above current price; overlap de-duplication is per direction

## v0.1.5 — 2026-08-12
- Small gap between box and label — label x moved from `rightBar + 1` to `rightBar + 3`, so it no longer sits flush against the box's right edge

## v0.1.4 — 2026-08-12
- Zones no longer auto-extend infinitely to the right (`extend.right`). Replaced the `Extend Zones Right` toggle with a bounded `Right Projection · Bars` input (default 15, matching `fib_reaction_memory`'s `Right Projection · Bars`) — box and label now end a fixed number of bars past the current bar instead of running off-chart
- Moved the zone label from inside/at the box's right edge to just past the new bounded right edge (`rightBar + 1`), so it no longer overlaps the box — same right-projected-label pattern as `fib_reaction_memory`
- Increased label size from `size.tiny` to `size.small`

## v0.1.3 — 2026-08-12
- Fixed the rendered box's left edge: it used `z.originBar`, which keeps regressing to the oldest ever-merged evidence on every merge (`math.min` in `f_ingestCandidate`) — so any zone reinforced multiple times over a long history reports an origin near the start of the lookback window regardless of how recently it was actually reinforced, making every long-lived zone visually indistinguishable ("started forever ago"). Box left edge now uses `z.createdBar` (when the Zone entity itself was instantiated, never regressed by merges) instead; `originBar` is kept for provenance in the hover tooltip only
- Added an on-chart zone state label (`NEW`/`TESTED`/`CONFIRMED`/`WEAK`/`BROKEN`/`FLIPPED`), new `Show Zone State` toggle (default on) — validity was previously only visible by hovering the tooltip

## v0.1.2 — 2026-08-12
- Fixed overlapping-zone rendering: `f_selectNearest` picked the N nearest zones per side purely by distance to price, with no check for whether they overlap each other — on a volatile chart (4H XAGUSD user report) this stacked several overlapping bands directly on top of one another with colliding labels, even though each individual zone's width was already correctly ATR-bounded after v0.1.1. New `f_overlapsSelected` skips a candidate zone that price-overlaps an already-selected (nearer, higher-priority) zone, so the rendered set no longer stacks

## v0.1.1 — 2026-08-12
- Fixed zone width freeze: a zone merged during a high-ATR period stayed that wide forever because `maxMergedWidthAtr` was only checked at merge-time against the ATR *at that moment* — `z.top`/`z.bottom` only ever grew (`math.max`/`math.min`), never shrank as volatility dropped. The lifecycle engine now re-checks every live zone's width against `maxMergedWidthAtr * current ATR` each bar and re-centers it if it has drifted wider (user report from a real XAGUSD chart: zones spanning roughly half the visible price range, unreadable stacked labels)
- Confluence (EMA/VWAP/Fibonacci/psychological level/relative volume) is now evaluated only when a zone is actually touched, not on every bar for every live zone (`f_applyConfluence`, called from the touch-detection block). Continuous evaluation meant a wide zone accumulated confluence merely by being wide — any drifting EMA/VWAP eventually passes through a large enough box — which is why several unrelated zones converged on nearly identical scores (~78) regardless of genuine local agreement

## v0.1.0 — 2026-08-12
- Initial engine-foundation build: detector -> ZoneCandidate -> registry -> merge -> confluence -> scoring -> lifecycle -> renderer/logs pipeline
- Detectors: Pivot Cluster, Multiple Tests, Base, Supply/Demand, Order Block, Fair Value Gap, Price Gap, Equal High/Low Liquidity
- Confluence: EMA, VWAP, Fibonacci (rolling high/low), psychological level, relative volume
- Lifecycle: touch detection with cooldown, ATR-target reaction validation with horizon, confirmed break detection, optional Support/Resistance flip on break
- Nearest-to-price renderer (score-filtered, top N per side) with hover tooltips, Pine Log event logging, Validation/Debug operating modes with a statistics table
- Rewrote several multi-line ternary expressions from the original draft as `if`/`else` (registry merge-distance calc, `f_addSource`, reaction-rate calc) to avoid the known Pine v6 CE10156 trap on line-broken ternaries over series/UDT-field types
- Not yet compiled in the TradingView Pine Editor and not yet calibrated on any chart
