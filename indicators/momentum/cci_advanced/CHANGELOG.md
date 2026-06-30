# Changelog

## v1.2.0 — 2026-06-30
- Trend context line (group 9): a slow CCI plotted faint behind the fast line — the trend the fast CCI rests on (price-dependent support), single-timeframe
- Counter-trend conviction: an extreme cross fired against the trend context's side of zero now renders as a weak/absorbed triangle, alongside the stall layer; both are independently toggleable (`useStall` / `useCtx`)
- Colors: split into two color languages — teal/pink stays on the fast CCI gradient (oscillator level), new Long/Short colors (green/red, configurable) drive the trend context line and histogram so directional bias reads at a glance
- Trend↔CCI divergence wedge: the area between the fast line and the trend context fills only when the two move in opposite directions — long color for a fast pullback into a rising trend (supported dip), short color for a fast rally into a falling trend (unsupported bounce); n-bar slope + min-slope noise guard for low timeframes

## v1.1.0 — 2026-06-30
- Stall/absorption layer (group 8): flags bars where the CCI cools/heats sharply while price barely moves (momentum decoupled from price); single-timeframe, symmetric, additive — the cross logic is unchanged
- Cross conviction: an extreme cross contradicted by flat price now renders as a small/faded triangle ("absorbed"), a confirmed cross stays solid
- Histogram fades during a stall to flag hollow momentum
- Display: removed the "CCI↑/CCI↓" text next to extreme triangles — the triangle alone marks the signal

## v1.0.2 — 2026-06-30
- Alerts: added a "Alerts only on bar close (confirmed)" toggle (default on); all alert conditions now respect it, preventing intrabar repaint of the named alerts

## v1.0.1 — 2026-06-29
- Alerts: messages standardized to `CCIA · EVENT · {{ticker}} {{interval}}` so they identify symbol/timeframe on multi-chart setups (titles unchanged)

## v1.0 — 2026-06-18
- Initial release: CCI with pluggable smoothing, three scale modes, gradient visualization, OB/OS fills, extreme-zone signal filter, and alert conditions
