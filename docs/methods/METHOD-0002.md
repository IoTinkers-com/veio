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
- Not executed. No derived product exists yet.
