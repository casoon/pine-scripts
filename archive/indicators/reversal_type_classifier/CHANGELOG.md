# Changelog

## v1.2.1 — 2026-10-02
- Fixed: the outcome window started at the pivot bar itself, so the pivot candle's own range counted toward the Snapback target, MFE/MAE and the minimum-move filter (a wide pivot bar could be classified A Snapback at 0 bars). The window now covers only the bars after the pivot; "bars to target" counts from the first bar after the pivot

## v1.2 — 2026-05-06
- Initial release
