# Correlated indicators are one vote

Composite scripts in this collection combine many inputs into one score: RSI, StochRSI, WaveTrend,
CCI, Williams %R, MFI, divergences, zones, structure. The more inputs agree, the higher the score.

## What was seen

Counting simultaneous alerts as independent votes was tried and dropped. The votes are not
independent. RSI, StochRSI, WaveTrend, CCI and Williams %R in their extreme zones all say the same
thing: price has moved far in a short time. Five oscillators in agreement are one observation, made
five times.

The same holds for the collection as a whole. Many scripts describe the same basic information with a
different smoothing, a different score and a different name. Adding them up creates confidence that
the data does not contain.

## What follows

- One input per information family: momentum, trend, structure, volatility, and volume where the
  data supports it.
- Check whether a composite score shows anything its strongest single part does not. If not, the
  composite is decoration.
- Missing evidence is not rescaled to a full score. A score built from three of eight inputs is a
  three-input score and should say so.
