## v0.6 — 2026-06-19
- **Rich WT oscillator visualization** — gradient line color on WT1 and WT2 (teal at OS → red at OB); 4-state histogram (brighter when momentum continues, dimmer on reversal) replacing the simple two-color area; gradient shadow fills between WT1 and the zero line; momentum fill between WT1 and WT2. Two new toggle inputs in the Visuals group: "Show WT Shadow Fill" and "Show WT / Signal Fill".
- **OB/OS hlines** — replaced `plot.style_linebr` (gaps at bar edges) with `hline()` (continuous across all bars).

## v0.5 — 2026-06-17
- Initial version: Tide/Wave/Ripple MTF framework, grade 0–4 signal system, divergence premium marker, StochRSI grade component, position resolution overlay, Horizon Phase Map table.
