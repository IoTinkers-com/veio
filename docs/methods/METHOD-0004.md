# METHOD-0004 — Nighttime lights trend (Black Marble)

**Bottom line:** Hypothesis-method: monthly lights trend (VNP46, ~500 m) around asset areas tracks activity level. Area-level only — never asset-level claims.

## Hypothesis
- Monthly nighttime-light radiance trends around asset AOIs (DS-0005, 2012–2026) move in direction compatible with reported activity changes.
- Expected signal: radiance drop after major outages; rise during documented reactivations.

## Validation plan (before execution)
- Reference events: CRP halt 2024-09-17 (Planta Centro failure — expect regional lights drop); Lagunillas/CCRC reactivation 2025-09 (expect local rise, possibly sub-pixel); El Palito 2023 peak.
- Known confounder: gas flares dominate rural lights — must be read jointly with METHOD-0002, never alone.
- Controls: 2 urban AOIs (stable) + 2 unlit natural AOIs.
- Acceptance: directional agreement with ≥3 of 4 reference events; controls stable (±5%); else negative finding recorded.

## Parameters (to pin at implementation)
- Product: VNP46A3 monthly (v2.0); AOI = 3×3 pixels around asset; outlier screening via quality flags.

## Status
- Executed 2026-10-04 (v0.1.0; script `scripts/method0004_validate.py`; outputs `data/derived/method-0004/`, manifest with checksums). Data: VNP46A3 v002 monthly, tiles h10v07/h11v07/h11v08 via LAADS (Earthdata Bearer).

## Validation results (2026-10-04, 9 months: 2023-05..07, 2024-08..10, 2025-08..10)
| Test | Expected | Observed | Result |
|---|---|---|---|
| CRP halt 2024-09 (5-day) | Sep drop | 27.5→35.4→20.7 (rise then drop) | **FAIL** — monthly composite dilutes 5-day event |
| Lagunillas reactivation 2025-09 | rise | 0.0 all months | **FAIL** — AOI coords unverified [GAP], dead extraction |
| El Palito peak 2023-06 | Jun rise | 2.55→1.52→5.30 (May→Jul +108%) | **FAIL** as registered; ramp visible across quarter with lag |
| Bajo Grande inactive | low/stable | 5–21 nW fluctuating | pass (weak test) |
| Controls ±5% | stable | Valencia ±15%; Maracaibo +95% (78→153); Copey +100% | **FAIL** |

- **Verdict: NOT validated (1/4 directional, controls unstable).** No Derived observations added to dossiers.
- Findings: (1) monthly granularity cannot see 5-day events; (2) ramps appear with lag across quarters; (3) AOI coordinate quality is decisive — guessed coords produce dead extractions; (4) flares dominate asset AOIs (CRP 20–35 nW) — must mask jointly with METHOD-0002; (5) Maracaibo lights nearly doubled 2023→2025 — itself a candidate observation for the Atlas (city reactivation), pending validation.
- **Redesign (pre-registered for v0.2):** daily VNP46A2 for short events; AOI coords resolved from dossier validation first; flare masking via METHOD-0002 outputs; control criterion = trend match, not ±5%.

## v0.2 pre-registration (2026-10-04, committed before execution)
Design changes: daily VNP46A2 (`Gap_Filled_DNB_BRDF-Corrected_NTL`, Mandatory_Quality_Flag ≤ 1) for short events; same-month comparisons for trends; AOI gate (baseline median > 0.5 nW/cm²/sr, else "unverifiable AOI" — reported, not scored); flare masking with FIRMS VIIRS standard-processing (SP) hotspots; known confounder windows excluded.

| Test | AOI | Data / windows | Pass criterion |
|---|---|---|---|
| T1 CRP 5-day halt 2024-09-17..21 (dossier AST-0001) | Amuay 5×5 px (-70.171, 11.773) | VNP46A2 daily; baseline 2024-09-01..09-16 (excludes 2024-08-30/31 national blackout — BBC/El País/EFE 2024-08-30); event 09-17..09-21 | Flare-masked event mean departs from baseline by \|z\| ≥ 2 (direction recorded: drop = lights off, rise = possible emergency flaring) |
| T2 Maracaibo trend (candidate observation from v0.1) | Maracaibo city 5×5 px (-71.61, 10.65) | VNP46A3 monthly, **same months** Aug–Oct of 2023, 2024, 2025 | Maracaibo 2025/2023 ratio ≥ 1.5 **and** Valencia (-68.00, 10.18) ratio within 0.85–1.15 |
| C1 sensor stability | Canaima (-62.84, 6.24) | both | daily: \|z\| < 2 in T1 event window; monthly: < 1 nW all months |
| Context (not scored) | Valencia urban | T1 windows | Regional grid effect reported — the 2024-09 halt is attributed to a Planta Centro (Carabobo) failure, so a Valencia dip is expected and does not invalidate T1 |

- Dropped from v0.1 (carried to v0.3 backlog, not hidden): Lagunillas rise (AOI unverifiable until METHOD-0001 T1 locates the platform), El Palito monthly peak (flare-dominated AOI).
- Method validated for dossier use per test: a passing test validates only that use case.
