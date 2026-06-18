# Changelog

## v1.0.1 — 2026-06-11
- Fixed script not compiling: removed invalid `return` statements (Pine has no `return` keyword), split comma-separated variable declarations, restructured early-exit guards into if-blocks
- Fixed `f_make_smart_label()` being called before its definition — drawing and pattern scans now run in one block after all function definitions
- Guarded the previous-pivot lookup loop against a negative start index

## v1.0.0
- Initial release
