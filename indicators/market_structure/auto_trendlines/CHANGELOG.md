# Changelog

## [Unreleased]

### Added
- **Role flip:** once `Break confirmation (closes)` consecutive closes after its last touch lie beyond a line by more than the tolerance, the line flips role — broken resistance turns into support (green, dashed, label `Flip`) and vice versa. A flipped line that price closes back through by the same count is dropped. Only near-horizontal lines (below `Sloped / Flat Cutoff`) flip; a broken sloped trendline is dropped (default 2, 0 = ignore breaks)

### Changed
- **Labels:** touch count and retest distance share one label at the line end (size small), so labels of converging lines no longer stack on the current bar; the distance shows a leading zero (`0.06 ATR`)
- **Inputs:** the `Line Fit` tooltip states that it only applies to the Combinatorial method

### Fixed
- **Violation filter:** lines anchored at an extreme pivot were exempt from `Max Violation %`, so lines that price had closed through for months were still drawn; the extreme anchor now only raises the score

## v1.1.1 — 2026-06-11
- Fixed compile error in OLS refinement (comma-separated variable declarations split into single statements)
- Fixed convex hull geometry: cross product now uses bar coordinates instead of array indices, so the envelope is a true hull in chart space even with unevenly spaced pivots

## v1.1
- Directional detection mode (falling resistance / rising support pair scan) alongside Combinatorial
- Outer fit mode (shift OLS line to the outermost inlier)
- Violation %, relevance distance and sloped/near-horizontal filters
- Retest highlighting with distance label

## v1.0
- Initial release
