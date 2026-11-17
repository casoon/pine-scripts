# Volume is not always volume

Volume-based tools (VWAP, volume profile, MFI, CVD, Wyckoff volume tests) assume the volume series
measures what was traded in the market. On many symbols it does not.

## What was learned

- **Volume exists ≠ volume is valid.** A CFD feed can deliver real numbers on every bar that are only
  the broker's own volume, a fraction of exchange volume with a share that changes over the day.
  `syminfo.volumetype` then reports a real volume type, and a guard on it passes. It separates "some
  volume" from "no volume", not exchange volume from broker volume.
- **`nz(volume)` is not a guard.** It turns missing data into a zero that the rest of the formula
  treats as information.
- **Pseudo volume becomes evidence.** Two scripts replaced missing volume with a minimum value and
  then computed an MFI from it. The output looked like money flow and was price only.
- **A wrong conclusion from the wrong source.** At one point the collection stated that a broker
  delivers zero volume. The evidence was the stored bars of another application whose streaming path
  did not carry the field. Measured directly at the source, the broker did deliver volume. The
  statement had spread into about twenty-five comments, tooltips and READMEs, in two contradicting
  generations, before it was corrected.

## What follows

- A tool's meaning comes from its input data, not from its math. Correctly processed garbage is
  garbage.
- Where the data does not carry the information, the indicator shows less, not a substitute value.
- Facts about a data source are measured at the source, not inferred from a downstream copy.
