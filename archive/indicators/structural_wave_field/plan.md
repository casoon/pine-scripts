# Structural Wave Field — Implementation Plan

Status: 2026-08-28

This file is the current implementation plan. `todo.md` remains the historical concept and design exploration; when both documents differ, this plan reflects the later decisions and the current direction.

## Product decisions

- Keep the indicator on the main chart. Do not turn it into a classical oscillator pane.
- Do not color, replace or overdraw the chart candles.
- Use one shared, price-scaled Flow Axis below price. The previous two-sided candle-anchor renderer was rejected because it was difficult to see and did not communicate the wave hierarchy clearly enough.
- Preserve invariant semantics across bullish and bearish structure:
  - above the Flow Axis = aligned with the active structural direction;
  - below the Flow Axis = counter to the active structural direction.
- Keep the Elliott-context layer. `I5` and `C3` remain contextual sequence labels with hover evidence; they must never claim a formal Elliott 1–5 or ABC count.
- Keep compact hover labels for important events. No permanent phase text on every bar.
- Treat the thin price-following axis as placement only. Structural color, body thickness, opacity and edge condition carry the signal.
- Preserve the completed leg briefly after a neutral structural exit so the transition cannot erase its final maturity/deterioration context.
- Keep the dashboard optional and secondary. The field itself must carry the primary interpretation.
- Do not add Buy/Sell arrows, Fibonacci projections, classical divergence lines or unrelated overlays.

## Intended reading model

The chart answers where price is. The field answers what is happening inside the active structural leg.

| Visual property | Meaning |
|---|---|
| Structural color family | Bullish or bearish structural flow |
| Structural backbone | Strength and confidence of the active structural leg |
| Aligned-body height | Current internal energy working with structure |
| Counter-body height | Current counter pressure against structure |
| Opacity | Wave quality and structural confidence |
| Inner gradient | Energy is building or fading |
| Outer-edge decay | Structural maturity and weakening continuation |
| Amber collapse | Exhaustion while structure still exists |
| Bright ignition | Re-synchronization after a correction |
| Amber outer edge | Early deterioration before full Exhaustion |
| Fading prior-color body | Completed-leg context during neutral transition |
| `I5` / `C3` | Elliott-like impulse or correction context, not a formal count |

The same geometry must read identically in bullish and bearish markets. Direction comes from color and the dashboard; the two sides of the Flow Axis always mean aligned versus countertrend.

## Current implementation status

| Module | Status | Current state | Remaining work |
|---|---|---|---|
| Structural Flow | Implemented, unvalidated | Fast/medium/slow displacement, efficiency, persistence and location are alignment-weighted; hold/entry/flip hysteresis includes an explicit neutral transition | Calibrate thresholds and verify that neutral exits do not fragment valid legs |
| Structural-leg archive | Implemented, unvalidated | Duration, directional displacement normalized by the completed leg's mean ATR, and cycle count are archived | Validate historical baselines across instruments/timeframes |
| Internal Wave | Implemented | Momentum, velocity and acceleration produce a bounded internal wave and aligned energy | Validate weights and sensitivity presets on charts |
| Wave Quality | Implemented | Short efficiency, persistence and smoothness are separated from energy | Validate that quality remains direction-neutral and does not reward noise |
| Counter Pressure / Integrity | Partial | Counter energy, persistence, retracement and structural stress are combined | Validate correction severity; add explicit healthy/aggressive/exhaustive correction classification only if it improves the field |
| Wave Segmentation | Implemented | Non-overlapping aligned/counter segments and transition-bar ownership exist | TradingView compile and chart validation |
| Wave Memory | Implemented, unvalidated | Duration, displacement, peak, integral, quality, efficiency, optional participation and retracement are archived and feed decay/Elliott context | Add correction recovery time only if chart validation shows distinct value |
| Maturity | Implemented, unvalidated | Age, directional extension, cycles, multi-metric decay, efficiency loss and mismatch are combined | Calibrate against completed-leg history and verify Early/Mid/Mature/Late behavior |
| Compression | Partial | Weak counter pressure inside intact structure creates a stored-energy approximation | Validate against flat and deep corrections; avoid interpreting duration alone as compression |
| Re-Sync | Implemented, unvalidated | Each confirmation owns and consumes one completed qualified counter segment; duration/depth, quality, structure confidence and sensitivity-scaled cooldown remain additional symmetric gates | Chart-test selectivity, stage order and realtime ownership |
| Exhaustion | Implemented, unvalidated | Maturity-gated decay and continuation-failure evidence progressively reduce body height and weaken/amber the outer layer | Calibrate collapse strength and event threshold |
| Phase Engine | Implemented, unvalidated | All named phases use persistent pending transitions; structural exit/flip remains immediate | Chart-test flicker versus confirmation lag |
| Elliott Context | Implemented, unvalidated | Multi-metric `I5` and `C3` patterns require combined quality scores and own non-overlapping five-/three-segment event windows | Validate score thresholds and timing; retain cautious wording |
| Participation | Implemented, unvalidated | Off, Volume, Relative Volume and directional Money Flow exist; influence remains secondary in decay/Elliott evidence | Validate feeds with missing or synthetic volume |
| Sensitivity | Implemented, unvalidated | Fast, Balanced and Structural presets change relative windows, thresholds and phase persistence; advanced calibration overrides them | Validate preset separation across the test matrix |
| Renderer | Implemented, unvalidated | Active-only neutral price anchor; invariant aligned-above/counter-below geometry; colored backbone, continuous gradients, deterioration edge, exhaustion collapse, Re-Sync ignition and sensitivity-scaled transition memory | TradingView chart validation and default calibration |
| Labels / Alerts | Implemented, unvalidated | Directional `RS↑/RS↓` plus `F`, `WK`, `EX`, `FF`, `I5`, `C3` use collision-aware outer lanes; Re-Sync consumes one counter segment and Elliott events use non-overlapping ownership windows | Chart-test selectivity, spacing and readability |
| Dashboard | Implemented, unvalidated | Optional diagnostic table preserves final maturity, exhaustion and wave context during neutral transition memory | Verify that current versus prior-leg wording is unambiguous |
| Validation | Missing | Static whitespace and delimiter checks pass | Compile in TradingView and perform visual/regime validation before calling V1 complete |

## Target renderer

### Shared geometry

Use one price-following `fieldBase` below recent price action. The baseline must be derived from recent lows and ATR, not from the visible viewport and not from a fixed absolute price.

The renderer should use a bounded field envelope:

1. `fieldCeiling` remains a small ATR clearance below a short rolling price envelope.
2. `fieldBase` sits one maximum aligned-body height below that ceiling.
3. The aligned body grows upward from `fieldBase`, but never reaches the candles.
4. The counter body grows downward from the same `fieldBase`.
5. Only the baseline and body thickness may be lightly smoothed; excessive lag is not acceptable.

The indicator participates in chart price scaling so the field cannot silently fall outside the visible range. The previous `scale.none` behavior has been removed; the result still requires TradingView verification.

### Layer mapping

- Price-following anchor: thin neutral placement reference shown only during active structure or transition memory; its slope must not imply structural direction or energy.
- Structural backbone: colored once a structural direction exists; minimum opacity and height prevent the field from disappearing during neutral internal energy.
- Aligned body: continuous vertical `fill()` gradient driven by `sqrt(aligned energy)` and relative wave strength, plus a softer inner glow and subtle outer contour.
- Counter body: a narrower/diffuser body below the same axis, driven by counter pressure and correction quality.
- Gradient: energy change affects inner-glow density; it must show building versus fading energy rather than merely recoloring a constant body.
- Maturity: increasingly weak/frayed outer layer, while the structural core remains readable.
- Exhaustion: reduces effective body height and outer density progressively; no abrupt green-to-red reversal signal.
- Transition memory: after a neutral structural exit, fade the completed leg over a sensitivity-scaled window and retain its final dashboard context.
- Re-Sync: short bright ignition growing from the axis into the aligned side.
- Flow Flip: break the old body cleanly and start a new structural color without drawing a bridge through price.

### Visibility requirements

At default settings:

- the backbone remains visible during weak or neutral internal waves;
- medium energy is clearly distinguishable from high energy;
- a correction is recognizable without consulting the dashboard;
- Re-Sync and Exhaustion are visually different;
- the field follows price without touching or coloring candles;
- zooming or autoscaling does not hide the field;
- bullish and bearish examples use the same aligned/counter geometry.

## Implementation sequence

### P0 — Establish a valid baseline

- Keep this plan as the source of truth.
- Run a TradingView compile of the current script and fix compile errors without changing behavior.
- Capture at least one bullish, bearish, correction and transition example for comparison.

### P1 — Rebuild the renderer — code complete, chart validation pending

- Replace the rejected candle-anchor geometry with the shared Flow Axis.
- Restore invariant aligned/counter placement around that axis.
- Make the field participate correctly in price autoscaling.
- Add a visible structural minimum, energy-change gradient, exhaustion collapse and Re-Sync ignition.
- Move all existing event/Elliott labels to the appropriate field position.
- Chart-test visibility before changing more engine logic.

### P2 — Complete structural and phase semantics — code complete, calibration pending

- Separate Structural Strength explicitly into displacement, efficiency, persistence and horizon alignment.
- Add a defined neutral/transition exit to direction hysteresis without creating flip noise.
- Turn phase selection into stable transitions where barwise priority causes flicker.
- Align Re-Sync stages with counter decay → acceleration → velocity/recovery → confirmed aligned energy.

### P3 — Complete adaptive behavior and memory — code complete, validation pending

- Add Fast, Balanced and Structural presets.
- Complete wave-memory metrics only where they affect maturity, comparison, exhaustion or Elliott context.
- Validate leg-history normalization and compression.
- Add Money Flow participation only if it contributes distinct information.

### P4 — Validate Elliott context and UX — code/docs complete, chart validation pending

- Validate `I5`/`C3` timing on completed segments and keep all wording contextual.
- Test label overlap and hover readability.
- Review the dashboard default after the renderer carries the intended interpretation.
- Update README, TradingView description, changelog and catalog to match verified behavior.

### P5 — Release validation

- TradingView Pine v6 compile with no errors or warnings that affect behavior.
- Bar-close events do not disappear or duplicate in realtime.
- No lookahead or future-dependent leg progress.
- Visual checks on multiple instruments and at least 15m, 1h, 4h and Daily.
- Confirm that defaults remain usable without advanced calibration.

## V1 completion criteria

V1 is complete only when:

- all seven core scores have distinct, documented meanings;
- structural direction, internal energy and counter pressure remain separable;
- the shared field is visible, price-following and interpretable without candle modification;
- Expansion, Correction, Re-Sync, Late Expansion and Exhaustion can be distinguished visually;
- wave memory materially influences maturity/relative strength rather than existing only as storage;
- `I5` and `C3` provide cautious Elliott context from completed segments;
- defaults work across the validation matrix;
- the script compiles and has been visually verified in TradingView.
