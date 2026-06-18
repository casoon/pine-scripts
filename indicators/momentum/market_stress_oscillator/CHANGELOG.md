# Changelog

## v1.0.1 — 2026-06-11
- Fix: bias line color rewritten from a multi-line ternary to a single line (Pine v6 compile error CE10156)
- Preset summary table restyled to the standard light theme; cleared via table.clear when hidden instead of writing empty cells
- Removed duplicated calculateJMA_wind helper — HTF wind bias now uses the shared calculateJMA (identical math, separate call-site state)

## v1.0.0
- Initial release
