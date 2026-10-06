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
- v0.4 (Santa Bárbara per-nucleus characterization) executed 2026-10-05 (pre-registered 4c34ab0; script `scripts/method0002_v04.py`; outputs `data/derived/method-0002/v0.4/`). Verdict: NOT validated (C3).
- v0.5 (fixed/persistent/night-active nuclei) executed 2026-10-05 (pre-registered abcfccf; script `scripts/method0002_v05.py`; outputs `data/derived/method-0002/v0.5/`). Verdict: VALIDATED (scope-limited).

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

## v0.4 results (2026-10-05; script `scripts/method0002_v04.py`; outputs `data/derived/method-0002/v0.4/` + manifest; pre-registered 4c34ab0)
Window 2026-07-07..2026-10-04 (90 days), VIIRS NOAA-20 + S-NPP: **11,480 hotspots** in the box.
| Criterion | Result | Pass? |
|---|---|---|
| C1 structure | **9 nuclei** (≥5 detections, eps 0.01°); largest 4,327 detections at −63.547/9.653 | pass |
| C2 persistence | **8/9** nuclei detected on ≥30% of days; top six on 93–98% of days | pass |
| C3 OGIM match | **47/78** OGIM detections (60.3%) within 1.5 km of a nucleus (threshold 70%) | **FAIL** |
| C4 control | Bajo Grande box: **0 nuclei** | pass |

| nucleus | detections | days (of 90) | persistence | mean FRP | max FRP | matched OGIM |
|---|---|---|---|---|---|---|
| 3 | 4,327 | 88 | 97.8% | 6.2 | 74.7 | 14 |
| 1 | 2,689 | 88 | 97.8% | 10.7 | 221.6 | 11 |
| 4 | 2,128 | 87 | 96.7% | 10.2 | 162.8 | 12 |
| 6 | 1,138 | 87 | 96.7% | 4.7 | 33.6 | 2 |
| 0 | 613 | 86 | 95.6% | 4.2 | 14.9 | 1 |
| 5 | 343 | 84 | 93.3% | 4.2 | 12.3 | 3 |
| 2 | 153 | 65 | 72.2% | 1.6 | 6.6 | 4 |
| 7 | 68 | 31 | 34.4% | 1.3 | 3.8 | 4 |
| 16 | 5 | 3 | 3.3% | 1.3 | 2.1 | 0 |

*Figure generated locally, not committed (ADR-001): `data/derived/method-0002/v0.4/METHOD-0002-v0.4-santabarbara.png`. Contains modified NASA FIRMS data (VIIRS NOAA-20 + S-NPP).*

- **Verdict: NOT validated as registered** (C3 failed). The **per-nucleus structure and persistence are robust** (C1/C2/C4 pass; 8 of 9 nuclei on ≥30% of 90 days), but the OGIM cross-match at 1.5 km reaches only 60.3% (< 70%). No Derived observation added to dossiers.
- Implementation note: the first verdict computed C3 against the nucleus **centroid** (19.2%); corrected to nucleus **membership** (per the wording "within 1.5 km of a nucleus") → 60.3%. The criterion was not changed; verdict unchanged. Diagnostic (not criteria): 3 km → 73.1%, 5 km → 91.0%.
- Interpretation of the C3 failure: many OGIM flaring points are isolated or in fields outside the spatially-clustered FIRMS nuclei (e.g. separate CARITO-MULATA points), and OGIM coordinate precision is unquantified — a 1.5 km match is not supported by this pair of datasets.
- **v0.5 requirements (pre-registered):** justify the match radius from OGIM coordinate precision or use a facility-level match; cross-check nuclei against an independent flare-location source; separate industrial flaring from biomass burning; report FRP-integrated metrics, not just counts.

## v0.5 pre-registration (2026-10-05, committed before execution) — closing the method
Motivation: v0.4 failed C3 because the 1.5 km **point** match to OGIM is not justified — OGIM flaring coordinates are coarse. Measured within-facility spread: Santa Bárbara Sur 17.0 km, Santa Bárbara 10.3, Cotoperí 10.1, Jusepín 9.3, Carito-Mulata 7.9, Pirital 6.2 km. v0.5 replaces the OGIM point match with **intrinsic discriminators** (persistence + stationarity + night activity) that separate fixed industrial flaring from transient/diurnal biomass burning, and keeps OGIM co-location **descriptive** (no pass/fail).

Data: same 90-day FIRMS window (VIIRS N20 + S-NPP), same nuclei (eps 0.01°, ≥5 detections). Metrics add median/max daily-centroid drift and total FRP (MW).

| Criterion | Pass rule |
|---|---|
| C1 structure | ≥8 nuclei with ≥5 detections |
| C2 persistence | ≥50% of nuclei detected on ≥30% of window days |
| C3 stationarity | ≥80% of persistent nuclei with **median** daily-centroid drift ≤1 km |
| C4 night activity | median night fraction of persistent nuclei ≥50% |
| C5 control | Bajo Grande box → 0 nuclei |

- Discriminator rationale: persistent (C2) **and** fixed (C3, median drift) **and** night-active (C4) is the signature of continuous flaring; biomass burning is transient, spatially drifting, and mostly daytime. The daily-centroid drift uses the median to avoid one-day outliers in large multi-source nuclei.
- OGIM co-location reported at 1.5/3/5 km as descriptive context only.
- Validated for "fixed, persistent, night-active thermal point sources" only if C1–C5 pass; otherwise the negative is recorded.

## v0.5 results (2026-10-05; script `scripts/method0002_v05.py`; outputs `data/derived/method-0002/v0.5/` + manifest; pre-registered abcfccf)
Window 2026-07-07..2026-10-04 (90 days), VIIRS N20 + S-NPP, 11,480 hotspots in the box.
| Criterion | Result | Pass? |
|---|---|---|
| C1 structure | 9 nuclei | pass |
| C2 persistence | 8/9 on ≥30% of days | pass |
| C3 stationarity | 8/8 persistent nuclei, median daily-centroid drift ≤1 km | pass |
| C4 night activity | median night fraction 87.3% | pass |
| C5 control | Bajo Grande 0 nuclei | pass |

| nucleus | detections | days/90 | persistence | mean FRP (MW) | max FRP (MW) | night % | median drift (km) |
|---|---|---|---|---|---|---|---|
| 3 | 4,327 | 88 | 97.8% | 6.2 | 74.7 | 85.0 | 0.60 |
| 1 | 2,689 | 88 | 97.8% | 10.7 | 221.6 | 91.7 | 0.25 |
| 4 | 2,128 | 87 | 96.7% | 10.2 | 162.8 | 89.6 | 0.57 |
| 6 | 1,138 | 87 | 96.7% | 4.7 | 33.6 | 79.3 | 0.19 |
| 0 | 613 | 86 | 95.6% | 4.2 | 14.9 | 77.0 | 0.09 |
| 5 | 343 | 84 | 93.3% | 4.2 | 12.3 | 75.2 | 0.11 |
| 2 | 153 | 65 | 72.2% | 1.6 | 6.6 | 97.4 | 0.13 |
| 7 | 68 | 31 | 34.4% | 1.3 | 3.8 | 95.6 | 0.19 |
| (16) | 5 | 3 | 3.3% | 1.3 | 2.1 | 100 | 0.10 |

OGIM co-location (descriptive, not a criterion): 60.3% within 1.5 km, 73.1% within 3 km, 91.0% within 5 km. OGIM's own within-facility spread reaches 17.0 km (Santa Bárbara Sur), 10.3 (Santa Bárbara), 10.1 (Cotoperí), 9.3 (Jusepín), 7.9 (Carito-Mulata) km — a 1.5 km point match is not meaningful for this product.

*Figure generated locally, not committed (ADR-001): `data/derived/method-0002/v0.5/METHOD-0002-v0.5-santabarbara.png`. Contains modified NASA FIRMS data (VIIRS NOAA-20 + S-NPP).*

- **Verdict: VALIDATED (scope-limited) for fixed, persistent, night-active thermal point sources.** All of C1–C5 pass; the Santa Bárbara cluster resolves into 9 spatially distinct nuclei, 8 of them detected on ≥30% of a 90-day window, night-active (median 87.3%) and stationary (median drift ≤1 km) — the signature of continuous flaring, not transient/diurnal biomass burning.
- FRP is instantaneous radiative power (MW) per overpass, **not** an emitted volume or energy; totals are detection-weighted sums and are not reported as emissions.
- Limitation: the OGIM cross-check is descriptive only, due to OGIM's coarse coordinates; a future version should use a precision-justified or facility-level match against an independent source.
- Derived observation added to AST-0012.
