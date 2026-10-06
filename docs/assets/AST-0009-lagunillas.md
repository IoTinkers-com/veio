# AST-0009 — Lagunillas (Costa Oriental del Lago)

**Bottom line:** Legacy lake field (Zulia); sources report China Concord Resources (CCRC) reactivation from 2025 — floating platform "Alula" installed at Lagunillas, targeting 12k→60k bpd by end-2026 across Lago Cinco and Lagunillas Lago.

## Identity
- asset_id: AST-0009 · type: conventional field cluster (lake) · name: Lagunillas / Lagunillas Lago (+ Lago Cinco) · operator: PdVSA; CCRC under 20-yr production-sharing contract (2024) — Source-recorded: Reuters via TotalNews 2025-09-07 (accessed 2026-10-04)
- Status as recorded by sources: ~12,000 bpd current (Reuters, 2025-09); ~16,000 b/d in target wells per expert commentary (Fedecámaras Radio, accessed 2026-10-04)

## Location
- Lake Maracaibo, Lagunillas area, Zulia (Reuters via TotalNews, 2025-09-07); OGIM: 1,010 Zulia well records, 2021 vintage (DS-0012) [GAP: field-cluster coordinates to validate]

## Infrastructure
- "Alula" jack-up platform (first major installation in the lake in years), towed from Zhoushan, positioned Sept 2025 (Reuters via TotalNews/El Diario Tricolor)
- Export/land infrastructure constraints reported: CRP repairs (~$1B estimate), channel draft limits (Fedecámaras Radio)

## Temporal observations
| Date | Source / product | Observation (§2 wording) | Confidence |
|---|---|---|---|
| 2024 | Reuters via El Diario Tricolor (2025-09-05) | CCRC–PdVSA 20-yr production-sharing contract agreed | Moderate |
| 2025-09 | Reuters via TotalNews (2025-09-07) | Alula platform installed at Lagunillas; plan to reactivate ~100 wells; 12k→60k bpd target by end-2026 | Moderate (wire service, sources + imagery) |
| 2025-09 | ecopoliticavenezuela.org | Platform presence documented; environmental debate recorded | Low (civil-society analysis) |

## Change indicators
- **Derived** (METHOD-0003 v0.1, Sentinel-1 RTC VV, S1A descending track 171; pre-registered `b28e66c`, run 2026-10-05): a **new persistent radar-bright object** (VV ≥ −8 dB in 11/11 post-window scenes vs 0/7 pre-window; peak change +20.1 dB) first observed **2025-09-01** at **10.13715 / −71.2703** (Lagunillas shoreline area, ~0.4 km from the reported CCRC office), persisting through 2025-12-30. **Compatible with** the reported Alula jack-up arrival (Reuters, 2025-09-04); radar does not establish identity (rig/vessel/structure). Confidence Moderate. Manifest: `data/derived/method-0003/v0.1/manifest.json`, figure `data/derived/method-0003/v0.1/METHOD-0003-v0.1-ALULA.png`. Open-water screening of the eastern lake found no new object in open water.

## Environmental observations
- Legacy environmental impacts discussed by civil-society sources (ecopoliticavenezuela.org, 2025-09) — **Source-recorded**; no independent verification; no cause claims.

## Methane / flaring association
- OGIM Zulia flaring detections exist (e.g., ENSANADA, 2026-09-14, DS-0012); association to this field cluster [GAP: coords pending].

## Interpretation (separate)
- **Interpretation:** Chinese-backed reactivation marks a documented investment shift in a legacy field; 60k bpd target is a company goal, not an observed outcome. Never merge with observations.

## Provenance
- DS-0012 OGIM v3.0 (accessed 2026-10-04) · totalnewsagency.com 2025-09-07 (2026-10-04) · eldiariotricolor.com 2025-09-05 (2026-10-04) · fedecamarasradio.com (2026-10-04) · ecopoliticavenezuela.org (2026-10-04) · reuters.com 2025-09-04 (2026-10-05) · DS-0002 Sentinel-1 RTC via Planetary Computer, scene IDs in `data/derived/method-0003/v0.1/manifest.json` (2026-10-05)

## Limitations
- Production figures are source-reported, not measured by us; Tía Juana sub-area not separately sourced; field-cluster coordinates still [GAP].
- Radar observation is a single 4-px object at the Lagunillas shoreline (not open lake); identity undetermined; the September 2025 step is coincident with, but does not prove, the reported Alula arrival.

## Confidence
- Moderate — recent, consistent wire-service reporting; targets unverified.
