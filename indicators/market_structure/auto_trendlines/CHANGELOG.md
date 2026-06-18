# Changelog

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
