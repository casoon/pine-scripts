# Changelog

## v1.0.1 — 2026-06-11
- Fixed compile errors: `ta.jma` does not exist in Pine v6 — replaced with the repo-standard inline JMA implementation (phase 0, power 2)
- Fixed `fill()` and `bgcolor()` being called inside `if` blocks (not allowed outside global scope) — visibility toggles moved into the color argument, same visual behavior
- Removed invalid `size` type annotation on the label-size variable
- Header feature list corrected: trend strength is an ATR-normalized gate, not a 0–100 output

## v1.0.0 — 2025-12-22
- Initial release
