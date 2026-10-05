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

- **Verdict: INCONCLUSIVE / FAILED as designed.** Four design flaws found:
  1. Reference events lack surface expression at 10–20 m (a FCC unit restart is not optically visible); only 1 of 3 references testable (CRP 5-day halt out of scope for composites — deviation documented; El Palito spill: insufficient cloud-free scenes).
  2. Control AOIs poorly chosen (ocean-dominated → degenerate thresholds).
  3. Seasonal confounder: windows straddle dry→wet transition; NDVI/NDBI shifts are seasonal, not event-driven.
  4. Script bug: band medians were computed as scalars (missing `axis=0`) — per-pixel change was never computed in v0.1.0; `disturbed_pct` was degenerate. Fixed in script; re-run required for v0.2.
- **Redesign requirements (pre-registered for v0.2):** same-season window pairs (±same months in adjacent years); land-based control AOIs; event types with surface expression (construction, clearing, tank farm changes); threshold from control distribution on land pixels.
- No Derived observations added to dossiers — nothing validated.

## v0.2 pre-registration (2026-10-04, committed before execution)
Design changes: per-pixel medians on a common EPSG:4326 grid (WarpedVRT; no stretch of partial tiles); SCL cloud/shadow mask (classes 3, 8, 9, 10); ≤8 least-cloudy scenes per window; 20 m analysis grid; fixed a-priori thresholds (no control-derived circularity); land/water controls matched to each detector; events chosen for **surface expression**.

| Test | AOI (box) | Windows (pre / post) | Detector | Pass criterion |
|---|---|---|---|---|
| T1 Alula jack-up arrival, Lagunillas (Reuters, 2025-09) | lon -71.40..-71.20, lat 10.00..10.20 [location UNVERIFIED] | 2025-06-01..08-20 / 2025-10-01..12-15 | New persistent NIR-bright object over water: ΔB08 ≥ +0.08 on pixels water (SCL=6) in ≥50% of pre scenes; connected component 4–200 px (0.16–8 ha) | ≥1 qualifying component |
| T2 Petrocedeño fire (Reuters, 2025-11-19) | José complex, centre 10.069/-64.864, ±0.05° | 2025-10-01..11-18 / 2025-11-20..2026-01-31 | dNBR = NBR_pre − NBR_post ≥ 0.27 (USGS FIREMON moderate-low class lower bound); land pixels; component ≥4 px | ≥1 qualifying component inside box |
| C1 water stability | open sea lon -68.05..-67.85, lat 10.95..11.15 | T1 windows | T1 detector | 0 qualifying components |
| C2 land stability | Valencia urban, centre 10.18/-68.00, ±0.05° | T2 windows | T2 detector | ≤1 component and <0.5% pixels over threshold |

- Expected false positives: moored vessels (removed by median unless persistent), lemna blooms (diffuse — excluded by ≤200 px size cap), cloud residue, industrial surfaces with low NBR contrast (T2 may fail for physical reasons — a fire on concrete/steel has weak dNBR).
- Visual outputs (per test AOI): RGB pre/post GeoTIFFs, change-index GeoTIFF, candidates GeoJSON, PNG quicklook.
- Method validated for dossier use only if T1 **or** T2 passes **and** both controls pass; the passing detector alone is validated.
