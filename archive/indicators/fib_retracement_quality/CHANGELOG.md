# Changelog

## v1.1 — 2026-06-11
- Fixed compile error: multi-line ternaries with series operands in the nearest-level lookup rewritten as if/else chains
- Added alert conditions for high-quality bull and bear retracement signals

## v1.0 — 2026-05-16
- Initial release
- Bullish retracement quality: prior low → swing high → retracement low, scored vs Fibonacci levels
- Bearish retracement quality: prior high → swing low → retracement high, scored vs Fibonacci levels
- Fibonacci levels: 0.236, 0.382, 0.5, 0.618, 0.786 with quality multipliers (0.618 = highest)
- Score 0–100: proximity to nearest level × level multiplier
- Signal: long/short when quality ≥ configurable threshold (default 65)
- Score and level labels at exact pivot bars
- Dashboard: last bull/bear quality score + level hit + active signal
