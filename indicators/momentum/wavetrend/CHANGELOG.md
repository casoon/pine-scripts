# Changelog

## v1.3.0 — 2026-08-19
Consolidation release from an external code review. No default-config behavior
change on the validated 1H/4H/1D range — see notes on each fix.

- **Fix (critical): gate scoring gave a free point for every DISABLED gate.** `longGateScore`/`shortGateScore` summed `not enabled or passed` across all 8 gates, so an off gate always contributed 1 — at default settings (all 8 off) the score was always 8/8 regardless of what an enabled gate actually did, and enabling one gate that then failed could still pass at `minGateScore=6`. Replaced with a confluence percentage: only gates you've enabled count toward the total, and `minGateConfluencePct` (new, default 100 = every enabled gate must pass) is checked against that. Behavior-neutral at default settings (all gates off either way); only changes outcomes for configs with 1+ gates already enabled, where it now actually enforces them
- **Fix (critical): HTF Trend Filter never reached the signal.** `_htfBullOK`/`_htfBearOK` were computed correctly but only ever read by the debug log — `useHTFFilter` was a no-op for anyone who turned it on. Folded into the confluence system above as a 9th criterion. Default OFF, so no default-config change
- Fix: HTF auto-mapping used `chartTF × 6` snapped to standard TFs, which didn't match the mapping documented in its own tooltip (a 15m chart landed on 4H, not the documented 1H; 1H landed on 1D, not 4H). Now maps directly off the documented breakpoints
- Added HTF confirmed/live toggle (`htfConfirmedOnly`, default on): confirmed uses the standard `[1]`-offset + `lookahead_on` non-repaint idiom; live uses the previous behavior. Matters now that HTF actually gates signals
- Fix: Auto-Calibrate's bar-count scaling (`_scaleBars`) had no ceiling — on a 1m chart (`_tfScale`=240) `percLookback` alone reached 48000. Added a per-parameter cap, set well above what each parameter reaches at 1H (`_tfScale`=4, the fastest TF in the validated range) so 1H/4H/1D are unaffected; only the runaway below 1H is bounded. The three parameters used as explicit historical offsets (`wtOsc[n]`, `low[n]`, `high[n]`) get the tightest caps since those silently break past `max_bars_back=500`
- Fix: `useExtD=false` hid the Wave Anatomy dashboard row but the percentile-rank score component kept counting toward `longScore`/`shortScore` regardless — "Enable" only ever disabled the display, not the effect. Now gated consistently. No change at the default (Extension D on)
- Fix: signal-source resolution was inconsistent — the tooltip's "Source" label used Cross > Zero > Persist priority, but the divergence-type-by-source selection (`divTypeBySource`) checked Persist first. A signal that was simultaneously a Cross and a Persist trigger could show "Source: Cross" while scoring itself against Persist's (Hidden) divergence type. Unified into one canonical `_longSignalSource`/`_shortSignalSource`, used everywhere
- Extension D's correction-depth metric only ever modeled a bull cycle (trough → peak → correcting down). Added the mirrored bear cycle (peak → trough → correcting up); whichever pivot is more recent determines which cycle is active, and the dashboard color now flips correctly for the bear case (a deep correction there is the bounce erasing losses — bullish, not bearish)
- Added an opt-in "Price + Oscillator confirmed" divergence pivot mode: default behavior only requires an oscillator pivot at the compared bar, this additionally requires a confirmed price pivot at the same bar. Default unchanged (Oscillator-only)
- In Adaptive (Percentile) zone mode, signals use the dynamic `upperThreshold`/`lowerThreshold`, but the chart only ever drew the fixed Upper/Lower Band `hline()`s (hline can't take a series). Added a `plot()` of the dynamic thresholds, visible only in Adaptive mode
- **Behavior change:** the strong-cross `alert()` call was nested inside the same `not showSignals` branch as its label — with `Show Signal Markers` on (the default), the strong-cross alert never fired at all. Alerts now fire on `crosses != 'None'` alone, independent of marker visibility. At default settings this means the strong-cross alert now actually fires where it previously silently didn't
- Fixed a stale tooltip claiming Auto-Calibrate "compresses oscillator parameters" as the reason for the persist-depth-block override on slow TFs — the WT engine itself is explicitly never auto-cal scaled (see the comment two lines above it in the source); the real mechanism is `sustainMin` compressing toward its floor on slow TFs combined with large raw oscillator swings per bar
- Gated the HTF and Compare Symbol `request.security()` calls behind their own enable toggles (both simple/input values, so this is legal in Pine) instead of running unconditionally every bar when off by default
- **Fix: the "recent OS/OB visit" window (`_visitWinA`, gates Cross signals) and its tighter score-bonus sibling (`_recentVisitA`) were both auto-cal scaled by calendar time (e.g. 12h) while the oscillator engine itself is deliberately bar-fixed (never auto-cal scaled).** Below 1H this desyncs badly: the same 12h window that's a tight 12-bar check at 1H becomes 48 bars at 15m — long enough to span most of a full oscillator cycle, so a "Cross" could fire with the oscillator having drifted from deep oversold all the way back to mid-range and still count as OS-anchored. Capped `_visitWinA`/`_recentVisitA`/`_zoneHoldA` at their own 1H-reference value (12/8/8 bars) instead of the earlier flat 50-bar cap — 1H/4H/1D never reached either cap so they're unaffected; 15m and faster are now meaningfully tighter
- The Cross signal tooltip showed a "Recent OS/OB visit (≤N bars)" score line but never showed the actual (looser) threshold that gated the Cross in the first place (`_visitWinA`, a different variable from the score's `_recentVisitA`) — a signal could show `✓ Source: Cross` next to `✗ Recent OS visit` with no way to tell why. Added an explicit `From OS/OB: N bars (Cross needs ≤X)` line showing the real gate, and relabeled the score line to "Fresh OS/OB visit" to distinguish it from the gate line above it
- Signal marker tooltips restructured: score threshold now shown next to the score itself ("Score 3/5 (need ≥1)"); added a Gates line (`X/Y passed (Z%)`) for Cross-sourced signals — the gate confluence outcome was computed but never surfaced anywhere before, so there was no way to see why a cross passed or failed the gate stage without Debug Mode. Omitted for Zero/Persist sources, since those don't go through the gate system at all. Shows "none enabled" instead of a confusing "0/0 passed (100%)" when no gates are turned on. Realigned all label columns to a consistent width
- Fix: all label tooltips (cross markers and signal markers) used a full-width `────` separator line that's wider than TradingView's tooltip box renders it — it wrapped onto its own short orphan line instead of forming one clean rule. Replaced with blank-line section breaks, which can't wrap since there's nothing to wrap
- **Fix: HTF StochRSI could repaint.** When the StochRSI Timeframe input was set genuinely higher than the chart TF, its `request.security` fallback used `lookahead_off` alone, which doesn't guarantee a non-repainting HTF value — the K/D reading could still move on the forming HTF bar and look different after a reload. Same/lower TF (the far more common case, including the default empty = chart TF) was never affected. Added `stochHTFConfirmedOnly` (default on), applying the same `[1]`+`lookahead_on` idiom as the main HTF filter only when the resolved StochRSI TF is genuinely higher than the chart TF — same/lower TF still uses the live path so no unnecessary lag is introduced there. Also fixed the `stochTF` tooltip, which claimed this path "uses request.security at TF close" — it didn't
- Fix: `_htfBullOK`/`_htfBearOK` treated `na(htfWtOsc)` (warm-up, data gaps) as passing when `useHTFFilter` was on — a "require HTF confirmation" gate that fails open on missing data isn't actually requiring anything in exactly the case where there's nothing to confirm against. Now fails closed: requires a real (non-na) value in the expected direction
- Fix: manually setting `HTF Timeframe` to something not actually higher than the chart TF (e.g. "60" on a 4H chart) silently defeated the filter's purpose — nothing validated that it was still a genuine higher timeframe. Added `_htfValid` (compile-time constant, since both sides are simple/input-derived) and folded it into the same fail-closed check above, so a misconfigured manual HTF blocks signals instead of silently no-op'ing
- Fix: `divTypeBySource`'s tooltip documents Zero-cross signals as falling back to either divergence type, but the code only distinguished Persist (Hidden) from "everything else" (Regular) — a Zero-sourced signal was scored as if it were Cross-sourced (Regular-only), contradicting its own tooltip. Now a real 3-way match on signal source (Persist/Cross/fallback), matching what's documented. `_longSrcIsPersist`/`_shortSrcIsPersist` (now unused after this fix) removed

## v1.2.0 — 2026-08-19
- Added optional Chart Overlay: projects the oscillator, signal line, and histogram directly onto the price panel (Top/Middle/Bottom placement, adjustable height/offset/lookback, optional highlight fill) — off by default, purely cosmetic, no effect on signals/gates/scores
- This is the classic on-chart WaveTrend projection the README already described and had partially bug-fixed (crossState/divState top-level scope, float divState) but never actually implemented; the histogram-baseline-in-Middle-mode fix documented there is applied in this port
- Added optional Compare Symbol: WaveTrend zone of a second symbol (default BTCUSDT) as a dashboard row. Implemented by reusing the existing HTF oscillator helper against a different symbol instead of duplicating the full engine + a parallel chart-label system — no new chart clutter, no gating effect
- Fix: the branding logo table (bottom-right) collided with the dashboard's last row in short/compact panes, rendering on top of the new Compare cell — moved logo to top-left, clear of both the dashboard (top-right) and the debug table (bottom-left)
- Input tooltips no longer quote backtest figures (win rates, profit factors, drawdowns) or rank signals against each other. Every tooltip now describes what the setting does and why it exists; the measured numbers stay in the internal assessment record where their instrument, timeframe, and sample size travel with them. Same cleanup applied to `wavetrend_v3`. No logic, defaults, or signals changed
- Fix: Chart Overlay's `line.new`/`box.new` calls were missing `force_overlay=true` — since this script isn't `overlay=true`, they drew in the oscillator pane instead of on the price chart (invisible/nonsensical there, since the y-coordinates are in price-domain units). The whole feature was inert until this was added

## v1.1.3 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v3.2.3 (wavetrend_v3) — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v2.0.3 (wavetrend_v2) — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.1.2 — 2026-06-30
- Alerts: messages standardized to `WT · EVENT · {{ticker}} {{interval}}` for a uniform format across the library (titles unchanged)

## v3.2.2 (wavetrend_v3) — 2026-06-30
- Alerts: messages standardized to `WT3 · EVENT · {{ticker}} {{interval}}` for a uniform format across the library (titles unchanged)

## v2.0.2 (wavetrend_v2) — 2026-06-30
- Alerts: messages standardized to `WT2 · EVENT · {{ticker}} {{interval}}` for a uniform format across the library (titles unchanged)

## v1.1.1 — 2026-06-29
- Fix: WaveTrend cross alerts no longer repaint intrabar — `alert()` now fires once per bar close instead of the default once-per-bar (which could fire on a forming bar that later un-crosses)

## v3.2.1 (wavetrend_v3) — 2026-06-11
- Fix: exit-reason texts rewritten from multi-line ternaries to if/else (Pine v6 compile error CE10156)
- Fix: max_bars_back raised 500 → 1000 — auto-scaled macro POC lookback can reach 1000 bars on sub-4H charts and would exceed the old history buffer at runtime
- Dashboard tables now include the standard frame styling

## v2.0.1 (wavetrend_v2) — 2026-06-11
- Fix: JMA-approx smoothing used the length as the alpha exponent (`beta^length` ≈ 0 → effectively no smoothing); now uses the standard power of 2, consistent with all other JMA implementations in this repo
- Dashboard table now includes the standard frame styling

## v1.1 — 2026-06-11
- Fix: dashboard bias label used integer equality checks on a fractional score (momentum contributes ±0.5), so values like +1.5 fell through to "Strong Bear" — buckets are now range-based

## v1.0
- Initial release
