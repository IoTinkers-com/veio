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
