# Compression Fractal Release

Compression Fractal Release (CFR) detects a **compressed, corrective coil** inside a higher-timeframe trend and trades the moment that coil resolves into a clean directional break — the *release*. The break of the prior correction band is the only trigger; how tightly the market was coiled and how decisively the coil is resolving are scored as weighted evidence, and a single choppiness veto filters low-quality breaks. The HTF regime decides whether a break is a trend **continuation** (Release) or a **structural change** out of a base (Base Break).

The indicator follows the repo's role model: every sensor has exactly one role, and the firing logic is a weighted score gated by a timing trigger — not a hard AND-chain.

## Roles

| Role | Sensor | Question |
|---|---|---|
| **Trend** | HTF EMA slope | In which direction is the market working? (continuation vs. counter-trend) |
| **Location** | Compression complexity + box-counting fractal dimension + efficiency | How tightly is the market coiled? |
| **Momentum** | Release dynamics (complexity falling + efficiency rising) | Is the coil resolving *now*? |
| **Trigger** | Break of the prior correction band | Is there a timing signal *now*? |
| **Quality** | Choppiness Index veto | Is a clean break even possible here? |

## Metrics

- **Compression complexity** — bar returns are symbolised into five states (strong/weak up, neutral, weak/strong down) in ATR steps, then state entropy is combined with the state-transition rate. High = busy/corrective path, low = clean/directional. This is a Pine-tractable approximation of compressibility, not true LZ compression.
- **Fractal dimension** — box-counting FDI (1 = smooth/trend, ~1.5+ = jagged/range), captured as an FD score (0–100). Box-counting is used instead of Katz FD, which saturates at 2.0 on price data and stops discriminating.
- **Efficiency** — net displacement over total path length. Low efficiency + high complexity = a wound spring.
- **Choppiness Index** — independent range-based quality sensor used only as a veto.

## Scoring

- **Coil strength** (0–1) = `complexity·0.5 + fdScore·0.3 + (1 − efficiency)·0.2`. The strongest coil in the break-length window before the break feeds the score.
- **Release dynamics** (0–1) = average of complexity dropping and efficiency rising on the break bar.
- **Setup Score** (0–1) = `coil · (MinReleaseShare + (1 − MinReleaseShare) · releaseDyn)`. The coil sets the ceiling; release dynamics scale it. The multiplication is deliberate — a high coil **alone** cannot clear the threshold, so a real release is required, not just a wound spring.

A break fires a signal only when the Setup Score clears its threshold, choppiness is below the veto, **and** the per-direction cooldown has elapsed. Continuation breaks (with the HTF trend) use the lower `Release Score Threshold`; counter-trend base breaks need the higher `Base Break Score Threshold` plus a prior base.

## Signals

- **Release ↑ / ↓** — coil released in the HTF trend direction (continuation).
- **Base Break ↑ / ↓** — break against the HTF trend out of a prior base (structural change; needs more evidence).
- **Setup Watch** (grey circle) — coiled, trend-aligned, and price is near the break band but has not yet broken.

## Regime Background

- Green tint — clean trend (low complexity, low FD, high efficiency).
- Orange tint — correction/coil inside a trend.
- Blue tint — base (high complexity, low efficiency).

## Dashboard

Light-theme table (top-right) showing state, HTF trend, Setup Score, coil strength, release dynamics, raw compression, fractal dimension, and choppiness (red when above the veto).

## Debug

Two parseable `log.info` streams (Debug input group):

- **CFR BREAK** — one row per confirmed band break with raw metrics (compression, efficiency, fractal dim, choppiness, coil, release dynamics) and the block reason (`veto:chop`, `no-regime`, `score<thr`, `cooldown`, or `ok`) — so missed signals are always attributable.
- **CFR BAR** (toggle) — one row per confirmed bar carrying the full metric distribution, for offline threshold calibration.

Export the Pine logs to CSV and run `python3 scripts/analyze_cfr.py <logdir>` to get the metric distribution, regime occupancy, break-reason tally and tercile-based regime-threshold suggestions. The log calibrates the regime/background and Base-Break precondition only — signal *profitability* needs an R-outcome backtest, which the log cannot measure.

## Inputs

- **Analysis** — analysis length, correction break length, compression symbol ATR step
- **Trend Context** — higher timeframe, trend EMA length, EMA slope length
- **Regime Thresholds** — high/low complexity and efficiency bounds for the background regime
- **Signal Scoring** — min release share, release & base-break thresholds, signal cooldown, choppiness length and veto
- **Display** — background, dashboard, break bands, signal labels
