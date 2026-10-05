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
- Executed 2026-10-04 (v0.1.0 pilot; script `scripts/method0001_validate.py`; outputs `data/derived/method-0001/`, manifest with checksums). Data: Sentinel-2 L2A via Microsoft Planetary Computer (public STAC).

## Validation results (2026-10-04) — reference event: Cardón FCC restart 2025-05
| AOI | scenes pre/post | NDVI pre→post | NDBI pre→post | disturbed % |
|---|---|---|---|---|
| CRP_Amuay | 13/14 | 0.252→0.192 | 0.154→0.215 | 0.0 |
| CRP_Cardon | 7/8 | 0.268→0.208 | 0.184→0.239 | 0.0 |
| El_Palito | 0/1 | — | — | insufficient scenes |
| CTRL_Cariaco | 10/6 | -0.130→-0.028 | — | 0.0 |
| CTRL_Chichiriviche | 1/7 | -0.041→-0.040 | — | 0.0 |

- **Verdict: INCONCLUSIVE / FAILED as designed.** Three design flaws found:
  1. Reference events lack surface expression at 10–20 m (a FCC unit restart is not optically visible); only 1 of 3 references testable (CRP 5-day halt out of scope for composites — deviation documented; El Palito spill: insufficient cloud-free scenes).
  2. Control AOIs poorly chosen (ocean-dominated → degenerate thresholds).
  3. Seasonal confounder: windows straddle dry→wet transition; NDVI/NDBI shifts are seasonal, not event-driven.
- **Redesign requirements (pre-registered for v0.2):** same-season window pairs (±same months in adjacent years); land-based control AOIs; event types with surface expression (construction, clearing, tank farm changes); threshold from control distribution on land pixels.
- No Derived observations added to dossiers — nothing validated.
