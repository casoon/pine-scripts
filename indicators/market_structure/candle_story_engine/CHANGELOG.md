# Changelog

## v1.10.0 — 2026-08-17
- Added Liquidity Sweep detection: a wick that pierces a recent N-bar high/low and closes back inside it (possible stop-hunt/liquidity grab). Marker, alert and data-window export only — deliberately not added to BUY/SELL evidence until validated, matching the existing Compression Breakout Attempt

## v1.9.1 — 2026-08-12
- Corrected Body Dominance: directional body participation is now measured against every candle in the sequence, including Doji. A single small bullish/bearish body can no longer receive an artificial 60-point body-dominance share simply because there are no opposite-colour bodies.
- Collapsed the correlated Sequence Pressure, Dominance and Close Persistence inputs into one 55% sequence role; the current candle is the separate 45% trigger role. The score no longer presents these overlapping OHLC measures as four independent votes.
- Candle Quality now qualifies only same-direction pressure. A large body/range can no longer add directional score to the side opposite the candle's measured pressure.
- Classic-pattern score weight now applies only to a reversal pattern against an established EMA trend; a pattern can no longer amplify an already-aligned continuation score it already helped create through candle/sequence structure.
- Capped close-progress-per-range at ±1 before deceleration scoring, preventing gap moves from saturating exhaustion.
- Body contraction is now colour-agnostic, so the first shrinking counter-candle can contribute to exhaustion.
- Fixed compression-zone rendering: a breakout attempt no longer expands the completed zone box with its own expansion candle.
- Tightened breakout acceptance: the resolution candle must close beyond the attempt candle extreme, not merely print an intrabar extension.

## v1.5.0 — 2026-08-11
- Range Expansion × ATR is now functional: confirmed compression-breakout attempts require recent compression, ATR-range expansion, a break of the pre-breakout range and a directional close; they have markers, data-window output and alerts but deliberately do not alter BUY/SELL evidence
- Doji are explicitly separated from Hammer/Shooting-Star detection, preventing zero-body wick candles from being misclassified as those patterns
- Added missing Morning/Evening Star chart markers when classic pattern markers are enabled

## v1.4.0 — 2026-08-11
- Fixed a lost-signal edge case: a threshold cross that did not yet meet `Minimum Score Improvement` no longer arms the state silently and prevents a later qualifying signal
- Corrected the Deceleration Engine to split the available close-to-close progress intervals into balanced older/recent groups; renamed its documented measure to progress-per-range because ATR cancels from the ratio
- Added `Confirm Signals on Bar Close` (default on). BUY/SELL, exhaustion, compression, follow-through, failure markers and their alerts are now stable at candle close by default

## v1.3.0 — 2026-08-11
- Fixed remaining signal over-firing on lower timeframes: the "in control" state (`bullSignalCondition`/`bearSignalCondition`) still flickered bar-to-bar because ~30% of evidence is driven by the single current candle, so one weak pullback candle mid-trend could drop evidence under the threshold for a bar and re-trigger a "fresh" signal on the next strong candle. Entry/exit now use hysteresis (new "Signal Exit Buffer" input, default 15): arm at Signal Threshold, only disarm once evidence drops the buffer amount below it. Losing to the opposite side or tripping exhaustion still exits immediately

## v1.2.2 — 2026-08-11
- Removed text captions from BUY/SELL/EXH/✓/FAIL markers — shape + color already carry the meaning, and the text was overlapping into unreadable clutter on lower timeframes with dense signals

## v1.2.1 — 2026-08-11
- Fixed invisible marker text: BUY/SELL, EXH (bull) and both Follow-Through checkmarks used `textcolor = color.white` (bear EXH used `color.black`) — `plotshape()` text has no background box, so it painted directly onto the chart background and vanished on TradingView's default light theme. All six now use the same color as their own shape (matching the pattern the FAIL markers already used), readable on both light and dark themes

## v1.2.0 — 2026-08-11
- Fixed signal over-firing: the bar-to-bar "score improving" delta was embedded in the persistent `bullSignalCondition`/`bearSignalCondition` state, causing it to flicker mid-trend and re-fire a "fresh" BUY/SELL on nearly every bar of an established move. The improving check now only gates the state *transition*, so a signal fires once per trend leg instead of repeatedly
- Follow-through/Failure now anchor to the actual signal bar (`newBullSignal[1]`/`newBearSignal[1]`) instead of the persistent control state, so they no longer re-evaluate on every bar the trend stays in control
- Compression marker now uses hysteresis (arms at score ≥60, re-arms only after dropping ≤45) instead of a single hard threshold, preventing repeated firing on score wobble around 60

## v1.1.0 — 2026-08-11
- Deceleration Engine: replaced the single-candle `pressureChange` momentum-fade score in the Exhaustion Engine with a progress-per-range comparison across the sequence (older-half vs. recent-half average) — a more precise trend-fatigue read than a bar-to-bar delta
- Removed dead `bodyGrowing` variable left over from the initial draft

## v1.0.0 — 2026-08-11
- Initial release: Candle Pressure, Candle Quality, recency-weighted multi-candle Sequence Engine, Buyer/Seller Dominance, Close Persistence, Body Contraction and Range Compression tracking, Trend Context, Bull/Bear Exhaustion (decoupled from BUY/SELL), Follow-through and Signal Failure detection, classic candlestick patterns as supporting evidence only, full data-window export for research
