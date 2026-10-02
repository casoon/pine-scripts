# Changelog

## v1.0.1 — 2026-10-02
- Exhaustion no longer counts the same peak-decay ratio several times: the `repeatedWeakPeaks` term was removed from continuation failure (already present via wave-strength decay in decay evidence and maturity); continuation failure is now 0.53 × price/pressure mismatch + 0.47 × failed expansion. Maturity's wave-decay weight is unchanged

## v1.0.0 — 2026-08-28
- Initial release: multi-horizon Structural Flow Engine with persistence/alignment and hold/entry/flip hysteresis, Fast/Balanced/Structural presets, Internal Wave Engine (momentum/velocity/acceleration), non-overlapping wave segmentation with expanded metric archive and event ownership, directional leg maturity, Counter Pressure/Structural Integrity, persistent phase transitions, completed-counter-segment-owned Re-Sync with adaptive cooldown and directional RS↑/RS↓ labels, Exhaustion/Failed Expansion and early deterioration scoring, optional Volume/Relative Volume/Money Flow participation, quality-gated non-overlapping I5/C3 context windows, price-scaled renderer with active-only neutral anchor, continuous gradients, inner glow and sensitivity-scaled transition memory, collision-aware hover labels, dashboard and bar-close-confirmed alerts
