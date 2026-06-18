# Changelog

## v1.1.0 — 2026-06-11
- Alert conditions added for long/short signals
- HTF request now passes `lookahead=barmerge.lookahead_off` explicitly
- Label budget raised to 500 — with high "Max divergence objects" settings the two labels per divergence could exceed the old cap of 300, silently dropping the oldest divergence labels

## v1.0.0
- Initial release
