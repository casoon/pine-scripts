# Changelog

Changes to Kestrel Opportunity Lens are recorded here using Semantic Versioning.

## [Unreleased]

### Added

- **Data window:** Review events per direction as 1/0 export series.
- **Review lock:** `Suppress new windows until review` can be switched off so every valid opportunity is recorded; on by default.

### Changed

- **Episode spacing:** Accepted starts now need at least the configured spacing (previously one bar more than configured).
- **Trend context:** The neutral context is labelled "mixed" instead of "mixed / range"; it means price side and EMA slope disagree, not necessarily a sideways market.

### Fixed

- **Review reminders:** With the review lock off, each setup keeps its own review reminder; previously a newer setup overwrote the pending review of the older one. The review tooltip no longer shows the data of a setup that fires on the same bar.
- **Window highlight:** The background now also covers the setup or expiry bar that closes the window.
- **Data window:** Recovery values are now also exported on the setup or expiry bar that closes the window; previously they were missing on exactly that bar.

## [0.2.0] - 2026-11-17

### Added

- **Short side:** Mirrored short opportunity windows as an independent state machine, selectable via `Both` / `Long` / `Short`; one shared symmetric rule set.
- **Trend context:** EMA20 side and slope recorded at every event as with-trend / counter-trend / mixed; shown in tooltips, dashboard and data window, never used as a filter.
- **Data window:** Per-direction recovery values and start/setup/expiry event series for chart-data export.

### Changed

- **Recovery:** Williams and price recovery are measured from the extreme since the window start instead of a rolling 12-bar lookback; the start bar can no longer deliver a setup on its own. The `Recovery lookback` input is removed.
- **Decision window:** The window now spans exactly the configured number of bars including the start bar (previously one bar more) and expires on its last bar.
- **Markers:** Zone, setup, expiry and review events are plain symbols without text; hovering a marker shows the values and conditions behind it.
- **Dashboard and alerts:** Separate long and short columns; eight alerts (start, setup, expiry, review per direction) replace the four long-only alerts.

## [0.1.0] - 2026-11-16

### Added

- **Indicator:** Initial rule-based opportunity windows, Williams/price recovery conditions, optional WaveTrend confirmation, dashboard and confirmed-bar alerts.
- **Research:** Initial unpublished draft; no trained model weights or account simulation.
