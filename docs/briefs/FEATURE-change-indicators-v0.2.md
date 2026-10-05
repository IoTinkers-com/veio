# Feature brief — Dossier change indicators v0.2

**Bottom line:** Add evidence-based change indicators to the 17 dossiers via 4 validated methods (optical, thermal, SAR, lights) — closing the "Change indicators: none yet" gap.

## Core
- **Problem:** Dossiers document status from third-party sources but no observation is yet derived by VEIO; change claims are absent, limiting the observatory's core value.
- **Hypothesis:** Multi-temporal analysis of registered datasets (DS-0001..0005) yields reproducible change observations at asset AOIs, validated against dated events already in the dossiers.
- **Data needed:** DS-0001 Sentinel-2 L2A · DS-0003 Landsat C2 L2 · DS-0004 FIRMS · DS-0002 Sentinel-1 GRD · DS-0005 Black Marble VNP46 — all PUBLIC, all with open licenses.
- **Design:** 4 method notes (METHOD-0001..0004), each hypothesis-first with validation plan before any run. Implementation order: 002 (FIRMS, cheapest) → 001 (optical) → 004 (lights) → 003 (SAR). Outputs to `data/derived/` with manifests; observations appended to dossiers labelled **Derived**.
- **Security & provenance:** All inputs PUBLIC; derived products carry manifests (inputs, params, processing_version, checksum); only already-public AOIs; no RESTRICTED.
- **Risks:** (1) confounders — seasonal flooding (Delta), biomass burning vs flaring, flare-dominated lights; (2) S1 constellation gap 2022–2024; (3) validation reference events are press-based, not ground truth — confidence capped at Moderate.
- **Acceptance criteria:** Each method: validation executed with pre-registered criteria; negative results recorded; every dossier observation traces to manifest; scientific-review pass.
- **Out of scope:** New data collection, real-time monitoring, non-O&G verticals, Atlas UI.

## On request
— (on request) detailed design, wireframes
