## v1.0 — 2026-06-28
- Initial release: compression coil detection (symbolic-entropy complexity + box-counting fractal dimension + efficiency) with a scored release-break engine
- Role-separated design — band break is the only trigger; the Setup Score is multiplicative (coil ceiling × release dynamics) so a high coil alone cannot fire, instead of a hard AND-chain
- HTF regime classifies each break as Release (continuation) or Base Break (counter-trend structural change, higher threshold)
- Per-direction signal cooldown; single choppiness quality veto; Watch → Setup → Trigger staging
- Light-theme dashboard with role-score breakdown and a debug log on every break (including the block reason)
