# MTF WaveTrend Opportunity Hunter

MTF confluence pane around WaveTrend. The core idea: make multi-timeframe confluence **visible over time** instead of reducing it to a one-bar label. The pane shows a net confluence histogram (long minus short final score) plus five heat ribbons — one per scoring layer plus a noise floor — so you can always see *why* a signal fired or *which layer* is currently blocking one. A RRG-inspired rotation map shows where the confluence is heading. Signals fire on a slim three-condition gate; Quality grades them (A/B) instead of filtering them out.

## Features

- **Confluence pane**: net score histogram (−100…+100, green/red) with ±60 strong-confluence reference lines
- **Heat ribbons**: Regime / Opportunity / Timing / Quality as color strips (green = long-side dominance, red = short-side, gray = neutral) plus a **Noise ribbon** (green = unusually clean tape, orange = unusually noisy) — the "why (no) signal" view over the full history
- **Confluence Rotation Map** (RRG-inspired): quadrant inset right of the last bar — x = net confluence, y = confluence momentum — with a curved polyline trail. Quadrants: LEADING (+/+), WEAKENING (+/−), LAGGING (−/−), IMPROVING (−/+). A clockwise rotation through IMPROVING → LEADING is the classic early-entry path
- **Ultimate Smoother core** (John Ehlers, TASC 04/2024): optional zero-lag replacement for the EMA core of WaveTrend (default on) — earlier crosses at the same length, less whipsaw than shortening the EMA
- **Entropy noise floor**: Shannon sign-entropy of the Trigger TF, percentile-ranked over a lookback window — self-calibrating per instrument, weighted into Quality (20%)
- **Slim gate** (three conditions instead of five thresholds):
  1. Regime bias — Regime score ≥ minimum on the Regime TF (default Daily)
  2. Setup pullback — Opportunity score ≥ minimum on the Setup TF (default 4H)
  3. Trigger — WaveTrend cross on the Trigger TF (default 1H)
- **Quality as grade, not gate**: signals are labeled A or B based on the Quality score (Efficiency Ratio, ATR band, optional RS filter, JMA acceleration) — no signal is blocked by it
- **Persistent TP/SL zones on the price chart** (`force_overlay`): risk box (entry→SL, red), first-target box (entry→TP1, green), TP2/TP3 as dashed/dotted lines; zones extend while the trade is active and freeze on exit warning
- **Pivot reference (control overlay, never a gate)**: confirmed swing highs/lows (`ta.pivothigh`/`ta.pivotlow`, configurable left/right bars) plotted as triangles at the actual pivot bar. On a signal, a dotted connector runs from the current swing extreme (low for long, high for short) to the entry, and the label prints distance, proximity and the driving scores (`ΔLow 3b / 0.8R · P68` / `O62 R71 T80 Q58`) — small distance = signal fired close to the swing. The reference is the *live* current-leg extreme, so a fresh unconfirmed low is used instead of a stale pivot; a `⚠K` flag marks knife-catches (entry below the last confirmed swing low). The pivot is by nature lagging and is used **only** to review accuracy — it does not influence which signals fire
- **Exit warnings gated to active trades**: orange × only after a signal, when trend health drops below 45 or WT crosses back
- **ARMED state**: dashboard shows when Regime + Opportunity pass and only the WT cross is missing — a cross on the next bars would fire
- **JMA smoothing**: Everget-style JMA (phase −100…+100, power 1.0–4.0), consistent with the repo's other indicators
- **Alerts**: long/short signal, long/short Grade A signal, long/short exit warning

## Scoring layers

All four layers are computed for both sides (0–100 each); the ribbons show the net (long − short).

### Regime (Regime TF)

| Component | Points |
|---|---|
| WT1 above signal line | 25 |
| WT1 rising | 20 |
| Close > EMA50 > EMA200 (bull) / inverse (bear) | 30 |
| ADX ≥ minimum | 15 |
| WT histogram rising/falling | 10 |

### Opportunity (Setup TF)

- Pullback depth vs. JMA in ATR units (45%)
- WT extreme proximity (35%)
- WT turning in signal direction (+20)

### Timing (Trigger TF — display context; the gate is the cross itself)

- WT cross (35) + WT momentum (30) + JMA structure (25) + Setup-TF WT direction (10)

### Quality (Trigger TF — grades A/B)

- Efficiency Ratio (30%) + ATR within 0.7×–2.2× of its 20-bar SMA (20%) + optional RS slope vs. benchmark (15%) + JMA acceleration (15%) + entropy noise floor (20%, inverted percentile rank — clean tape scores high)

## Reading the pane

- **Histogram crossing above +60 with all ribbons green** — strong long confluence
- **Three ribbons green, Timing gray** — ARMED: waiting for the trigger cross
- **Regime ribbon flips while in a trade** — expect an exit warning
- **Histogram near zero, ribbons mixed** — no edge, stand aside
- **Noise ribbon orange** — tape unusually noisy for this instrument; expect grade B signals
- **Rotation dot in IMPROVING moving toward LEADING** — confluence building; in WEAKENING — long confluence stalling even if the histogram is still positive

## Final score weights (display only)

Regime 35% + Opportunity 30% + Timing 25% + Quality 10% — shown in the dashboard and as the histogram, not used as a gate.
