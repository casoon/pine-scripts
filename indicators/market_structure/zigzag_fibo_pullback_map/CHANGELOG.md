# Changelog

## v1.3.0 — 2026-10-02
- Fixed: the "Break" outcome could never occur — it was judged at the next opposite pivot, which by construction always lies beyond the pullback pivot. The break is now judged at the next same-type pivot: Break when it undercuts (up impulse) or exceeds (down impulse) the pullback pivot; otherwise HH/LL/Weak from the follow-through pivot as before. The outcome stays Pending until that pivot exists. The Break outlook penalty and the confluence exclusion now take effect; the "R Break" marker sits on the breaking pivot

## v1.2.1 — 2026-06-11
- Fixed current-zone bounds being stuck at 0.000–0.236: the live zone box and zone-boundary fan levels now follow the actual retracement zone (tuple destructuring shadowed the outer variables)
- Fixed compact (5-column) stats table header showing "Fib" over the Outcome column

## v1.2.0
- Initial release
