# AST-0012 — Santa Bárbara / Santa Bárbara Sur

**Bottom line:** Light-crude field, north Monagas; used as diluent for Merey-16 exports per Reuters; OGIM records 33 flaring detections (19 Santa Bárbara + 14 Sur) on 2026-09-14 — largest name-cluster in the VE extract (next: Cotoperi, 12).

## Identity
- asset_id: AST-0012 · type: conventional light-crude field · name: Santa Bárbara / Santa Bárbara Sur · operator: PdVSA — Source-recorded: Reuters via GHM Abogados; Descifrado 2021-04-22 (accessed 2026-10-04)
- Status as recorded by sources: production suspended in 85 wells after associated-gas pipeline explosion (Reuters [date UNVERIFIED]); field crude used as Merey diluent (Reuters; Descifrado 2021)

## Location
- North Monagas (Reuters via GHM Abogados, accessed 2026-10-04); OGIM flaring anchors: 43 detections spanning 9.56–9.71 lat, -63.56 to -63.73 lon (DS-0012, SRC_DATE 2026-09-14)

## Infrastructure
- Planta de Extracción Santa Bárbara (PDVSA Gas) present at field (contractor record, Grupo Luna Rodríguez [date UNVERIFIED])
- Role in export chain: diluent supply to José blending (Descifrado 2021-04-22; Reuters)

## Temporal observations
| Date | Source / product | Observation (§2 wording) | Confidence |
|---|---|---|---|
| 2021-04-22 | Descifrado | Santa Bárbara + Mesa 30 dilution role increased after 2019 sanctions cut naphtha imports; national light-crude output ~160k bpd | Moderate (multiple industry sources) |
| [~2020–22 UNVERIFIED] | Reuters via GHM Abogados | Pipeline explosion; ≥30k bpd light-crudo cut; 85 wells stopped; Merey-16 supply risk noted | Moderate (wire service, anonymous sources) |
| 2026-09-14 | DS-0012 OGIM | 33 flaring detections across Santa Bárbara/Sur cluster (19 + 14; largest name-cluster in extract) | Moderate (dataset; method unpublished [GAP]) |

## Change indicators
- **Derived** (METHOD-0002 v0.3.0, manifest `data/derived/method-0002/manifest.json`): 1,046 thermal hotspot detections within 5 km of the Santa Bárbara/Sur cluster over 30 days (2026-09-04..10-03) — dense persistent thermal activity compatible with extensive flaring; largest cluster tested in the VE extract. Confidence Moderate. Remaining methods: pending.
- **Derived** (METHOD-0002 v0.5, pre-registered `abcfccf`, run 2026-10-05; manifest `data/derived/method-0002/v0.5/manifest.json`): the cluster resolves into **9 thermal nuclei** over a 90-day window (2026-07-07..10-04); **8 detected on ≥30% of days** (largest 4,327 detections at 97.8% persistence, mean FRP 6.2 MW, max 74.7 MW; second 2,689 at 97.8%, mean FRP 10.7 MW, max 221.6 MW), all **night-active** (median night fraction 87%) and **stationary** (median daily-centroid drift ≤1 km) — compatible with continuous flaring; Bajo Grande control 0 nuclei. OGIM co-location 91% within 5 km (OGIM coordinates coarse). Confidence Moderate. Figure `docs/methods/figures/METHOD-0002-v0.5-santabarbara.png`.

## Environmental observations
- Dense flaring cluster observed (DS-0012) — detections only; no volume, efficiency or cause claims.

## Methane / flaring association
- Largest flaring name-cluster in the VE extract: 33 OGIM detections (DS-0012, 2026-09-14); associated-gas pipeline failure reported historically (Reuters) — **Source-recorded**, dates [UNVERIFIED].

## Interpretation (separate)
- **Interpretation:** Diluent-role economics plausibly keep the field prioritized despite infrastructure fragility. Never merge with observations.

## Provenance
- DS-0012 OGIM v3.0 (accessed 2026-10-04) · ghm.com.ve (Reuters copy, accessed 2026-10-04) · descifrado.com 2021-04-22 (2026-10-04) · grupolunarodriguez.com (2026-10-04) · DS-0004 NASA FIRMS (VIIRS N20 + S-NPP, 90-day window; processed by VEIO 2026-10-05)

## Limitations
- Reuters article date not verified; current well count/production unknown [GAP]; flaring **volumes** (and emitted energy) unquantified — FRP is radiative power per overpass, not an emission rate; no optical/SAR imagery observations yet; OGIM coordinates too coarse for a point-level cross-check.

## Confidence
- Moderate — diluent role well-documented; current status partial.
