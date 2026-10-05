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
- Not executed. No derived product exists yet.
