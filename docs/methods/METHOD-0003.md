# METHOD-0003 — SAR infrastructure & vessel monitoring (Sentinel-1)

**Bottom line:** Hypothesis-method: S1 time series detects infrastructure changes and vessel presence under cloud cover (Apr–Jul optical gap). Highest complexity — last to implement.

## Hypothesis
- S1 GRD IW backscatter change (DS-0002, ~10 m, 2014–2026; constellation gap 2022–2024) detects infrastructure modifications at asset AOIs; bright-target detection identifies vessels at terminals.
- Expected signal: structural change signatures; vessel counts at TAECJAA/La Salina consistent with reported queues (Apr 2025).

## Validation plan (before execution)
- Reference events: Alula platform arrival at Lagunillas 2025-09 (documented, visible target); TAECJAA tanker queue 2025-04 (Reuters).
- Controls: open-water AOIs away from lanes; expected FP: wind roughening, layover at fixed structures, aquaculture.
- Acceptance: Alula arrival detected ±2 weeks; vessel counts correlate (directionally) with reported queue; else negative finding recorded.

## Parameters (to pin at implementation)
- Orbit (ascending/descending) selection; speckle filter; change threshold; vessel detector (constant false-alarm rate candidate — not assumed).

## Status
- Not executed. No derived product exists yet.
