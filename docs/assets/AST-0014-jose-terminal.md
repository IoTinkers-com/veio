# AST-0014 — Complejo Industrial José Antonio Anzoátegui + Terminal (TAECJAA)

**Bottom line:** Venezuela's main crude export complex (upgraders + storage + shipping terminal); sources report record 5-year monthly exports (~20.5M bbl in Feb 2025) and tank/pump rehabilitation with Iranian contractors.

## Identity
- asset_id: AST-0014 · type: industrial complex + storage/export terminal · name: Complejo Industrial G/D José Antonio Anzoátegui (CJAA; ex-Complejo Criogénico de Oriente, 1990) incl. Terminal de Almacenamiento y Embarque de Crudo TAECJAA · operator: PDVSA (petrochemical areas: Pequiven) — Source-recorded: es Wikipedia; Prensa Presidencial 2025-03-28 (accessed 2026-10-04)
- Status as recorded by sources: February 2025 closed with 20.5M bbl for export; March target 21M (Prensa Presidencial, 2025-03-28)

## Location
- Complex centroid: 10.069, -64.864 (OpenStreetMap way 265071557 via mapcarta; concordant place record, accessed 2026-10-04), between Barcelona and Puerto Píritu, Anzoátegui (es Wikipedia)
- OGIM offshore terminal records -64.646/10.216 and -64.494/10.194 (DS-0012, 2017) are loading points ~29 km NE — **not** the complex. Correction 2026-10-04: earlier versions of this dossier used -64.646/10.216 as the asset point.
- Visual check (Derived, METHOD-0001 v0.2 composites, Sentinel-2 Oct 2025–Jan 2026): tank farms, process areas and jetties present at the corrected centroid — location consistent. See `docs/methods/figures/METHOD-0001-v0.2-T2.png`.

## Infrastructure
- 740 ha complex; hosts upgraders (Petrocedeño, ex-PetroAnzoátegui/San Félix, Petromonagas — see AST-0005/0007) and Pequiven mixed plants (es Wikipedia, accessed 2026-10-04)
- Terminal: >50 tankers/month, >1.5M bpd loading capacity; TA1-T-01/02 tanks restored with Petropars; new pumps 10k+20k bbl/h (Últimas Noticias [date UNVERIFIED])

## Temporal observations
| Date | Source / product | Observation (§2 wording) | Confidence |
|---|---|---|---|
| 2015 | es Wikipedia (acc. 2026-10-04) | Complex handled ~65% of Venezuelan crude exports (~1.2M b/d) | Moderate (encyclopedic, sourced) |
| 2025-03-28 | Prensa Presidencial | 20.5M bbl exported in February; three lines (production, storage, export) active | Low (state-affiliated) |
| 2025-03-29 | Ciudad Valencia | Monthly export records reported: 17→18→19→20.5→21M bbl | Low (state-affiliated quotes) |
| [Dec, year UNVERIFIED] | Venezuela Política | TAECJAA loading Merey 16/18 mainly to Asia (Singapore, Malaysia, China); waiting vessels and STS transfers reported | Low (single outlet, unnamed report) |

## Change indicators
- **Derived** (METHOD-0002 v0.3.0, recomputed at corrected centroid with `scripts/check_jose_aoi.py` on the same cached inputs): thermal hotspot detections observed within 5 km on 30 of 30 days (750 detections; 311 within 1.5 km, 2026-09-04..10-03) — compatible with continuous industrial thermal sources (upgraders/flares). Confidence Moderate. Correction 2026-10-04: the earlier figure (122 detections / 27 days) referred to the offshore terminal point ~29 km NE, not the complex. Remaining methods: pending.

## Environmental observations
- None recorded in current sources for the terminal itself.

## Methane / flaring association
- Hosts upgraders and petrochemical plants — potential CH4 sources [GAP: no asset-level measurement]; no OGIM flaring detections within 15 km of the corrected centroid (DS-0012, 2026-09-14) despite dense FIRMS thermal detections — OGIM flaring layer appears upstream-oriented [GAP: OGIM detection scope].

## Interpretation (separate)
- **Interpretation:** Rising monthly export figures reported by official sources are consistent with terminal rehabilitation claims; independent vessel-data verification recommended. Never merge with observations.

## Provenance
- DS-0012 OGIM v3.0 (accessed 2026-10-04) · prensapresidencialvenezuela.gob.ve 2025-03-28 (2026-10-04) · ciudadvalencia.com.ve 2025-03-29 (2026-10-04) · ultimasnoticias.com.ve ([date UNVERIFIED], 2026-10-04) · venezuelapolitica.info ([date UNVERIFIED], 2026-10-04) · es.wikipedia CJAA (2026-10-04)

## Limitations
- Official export figures not independently verified; two source dates unverified; no imagery-derived observations yet.

## Confidence
- Moderate — structural facts solid; operational figures official-source only.
