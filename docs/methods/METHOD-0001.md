# METHOD-0001 — Optical disturbance detection (Sentinel-2 / Landsat)

**Bottom line:** Hypothesis-method for vegetation/soil disturbance around asset AOIs as activity proxy. Validation plan below must pass before any dossier use.

## Hypothesis
- Multi-date spectral change (candidates: NDVI loss, NDBI gain, SWIR change — candidates, not conclusions) within asset AOIs detects disturbances compatible with operational changes (DS-0001 S2 L2A 10–20 m, 2015–2026; DS-0003 Landsat C2 L2 30 m, 1985–2026 baseline).
- Expected signal: disturbance patches appearing within ±60 days of documented events.

## Validation plan (before execution)
- Reference events (from dossiers): Cardón FCC restart 2025-05; CRP halt 2024-09-17 (5-day); El Palito spill 2023-12.
- Control sites: 2 non-O&G AOIs per region (urban + natural), same date pairs.
- Expected false positives: cloud shadow, seasonal flooding (Orinoco delta), agricultural clearing, burn scars.
- Acceptance criteria: known event detected in correct window in ≥2 of 3 references; control FP area <5% of AOI; else method fails and result is recorded as negative finding.

## Parameters (to pin at implementation)
- AOI radius per asset class; compositing window; change threshold (to be set from control distribution — recorded in manifest).

## Status
- Not executed. No derived product exists yet.
