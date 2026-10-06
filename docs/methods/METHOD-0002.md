# METHOD-0002 — Thermal hotspot time series (FIRMS)

**Bottom line:** Hypothesis-method: hotspot frequency/persistence within asset AOIs tracks reported operational status (flaring proxy). Cheapest method — first to implement.

## Hypothesis
- Sustained VIIRS/MODIS hotspot presence within asset AOIs (DS-0004, ~375 m/1 km, 2012–2026) is compatible with active flaring; sustained absence is compatible with inactive or non-flaring status.
- Expected signal: hotspot recurrence at flare locations; drops after documented halts.

## Validation plan (before execution)
- Reference: OGIM flaring detections (DS-0012, 2026-09-14) — expect hotspot presence at ≥80% of detection sites in a 2026 window; Santa Bárbara cluster (33 detections) as density test.
- Event test: CRP halt 2024-09-17 (5-day) — expect anomaly in daily series at Amuay/Cardón AOI.
- Controls: 2 AOIs without known flaring (same states); expected FP: biomass burning (dry season), gas plants without flares.
- Acceptance: ≥80% site detection; control persistence <10%; else negative finding recorded.

## Parameters (to pin at implementation)
- AOI radius (≥1 pixel = ~375 m); confidence filter (nominal/high); day/night; persistence definition (≥N detections in M days).

## Status
- Executed 2026-10-04 (v0.1.0 → v0.3.0; script `scripts/method0002_validate.py`; outputs `data/derived/method-0002/`, manifest with checksums).

## Validation results (2026-10-04, window 2026-09-04..10-03, VIIRS S-NPP + NOAA-20 NRT, 29,558 hotspots in VE bbox)
| Test | Criterion | r=1.5 km | r=5.0 km | Result |
|---|---|---|---|---|
| Site detection | ≥80% of 77 OGIM sites | 36.4% | 66.2% | **FAIL both** |
| Density (Santa Bárbara) | signal present | 286 | 1,046 | pass |
| Differential | active >> inactive | all 0 (AOI artifact) | Amuay 284/27d · José 750/30d* · El Palito 36/18d vs Bajo Grande 0/0 | pass |

*Correction 2026-10-04: José AOI in v0.3.0 used an OGIM offshore terminal point ~29 km from the complex (122/27d). Recomputed at the OSM complex centroid (-64.864, 10.069) on the same cached inputs: 750 detections / 30 days at 5 km. Verdict unchanged (strengthened).
| Controls | <10% days | 0% | 0% | pass |

- **Verdict:** NOT validated for site-level detection or absence claims. Validated as **cluster-density and facility-differential indicator** (controls clean; active/inactive discrimination works at 5 km with per-facility AOIs).
- Deviations from pre-registration (documented in manifest): radius 1.5→5 km after diagnostic; midpoint AOI → per-facility AOIs (scripting bug); 2024-09-17 CRP event test substituted by differential test (NRT API covers ≤1 year).
- Interpretation for OGIM mismatch: OGIM detections (2026-09-14 snapshot) vs FIRMS 30-day window differ in method and epoch; coordinate precision of OGIM points unquantified [GAP].

## v0.4 pre-registration (2026-10-05, committed before execution) — Santa Bárbara per-nucleus characterization
Scope: move METHOD-0002 from a coarse differential/density indicator to a **per-flare-nucleus** temporal characterization of the Santa Bárbara cluster (the densest in the VE extract).
- Data: FIRMS VIIRS S-NPP + NOAA-20 NRT, box −63.85,9.45,−63.45,9.80, **90-day window** (5-day chunks).
- Nucleus: single-link (connected-components) spatial clustering at eps = 0.01° (~1.1 km), minimum 5 detections.
- Metrics per nucleus: detections, days detected, persistence % of window days, mean/max FRP, night %, satellites, first/last date, and OGIM detections matched within 1.5 km.

| Criterion | Pass rule |
|---|---|
| C1 structure | ≥8 nuclei with ≥5 detections |
| C2 persistence | ≥50% of nuclei detected on ≥30% of window days |
| C3 OGIM match | ≥70% of OGIM flaring detections in the box within 1.5 km of a nucleus |
| C4 control | Bajo Grande box (−71.78,10.55,−71.65,10.67) → 0 nuclei |

- Validated for per-nucleus characterization only if all four pass; otherwise the negative is recorded.
- Known limits: FIRMS cannot separate flaring from other combustion (biomass burning); OGIM is a single snapshot (2026-09-14); FRP is radiometric, not an emitted volume; persistence is detection frequency, not continuous combustion.
