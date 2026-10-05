# Changelog — VEIO

All notable changes to this project are documented here. Format based on Keep a Changelog; versioning starts at 0.x until the public MVP.

## [Unreleased]

### Added — METHOD-0003 v0.1 run (2026-10-05)
- First SAR method: Sentinel-1 RTC VV (S1A descending track 171), pre-registered in `b28e66c` before execution; outputs `data/derived/method-0003/v0.1/` with manifest + checksums, figure under `docs/methods/figures/`.
- **Verdict: VALIDATED (scope-limited).** One new persistent radar-bright object detected at Lagunillas (10.13715/−71.2703), bright in 11/11 post-window scenes vs 0/7 pre, first observed 2025-09-01, confirmed in ascending geometry; both open-lake controls 0. Validated only for "new persistent bright object over pre-window dark water", not for identity or open-water platform/vessel detection (eastern-lake screening negative).
- Derived observation added to AST-0009 (compatible with the reported Alula jack-up arrival, Reuters 2025-09-04; identity undetermined).

### Added — METHOD-0001 v0.3 run (2026-10-04)
- Interannual same-month dNBR (Dec-Jan 2024/25 vs 2025/26), pre-registered in `6755ad1` before execution. Verdict: NOT validated as registered — but the seasonal confounder is fixed (José 51% → 0.32% over threshold); remaining failures are control-design errors (urban component-count criterion; "negative" box contained all of Cabimas). v0.4 control rules pre-registered in the method note. Fire scar not detectable as a coherent signature at 20 m.

### Changed — METHOD-0001/0004 v0.2 runs + corrections (2026-10-04)
- v0.2 designs pre-registered in commit `93b9b25` before execution; both executed with visual outputs (RGB composites, change maps, daily/monthly series) and figures committed under `docs/methods/figures/`.
- METHOD-0001 v0.2: NOT validated (dNBR confounded by seasonal drying; water detector non-specific vs algal blooms; land control failed). Root cause: adjacent instead of same-season windows (author error, documented).
- METHOD-0004 v0.2: NOT validated (daily event test underpowered, z = −0.12; Maracaibo same-month trend +40% below pre-registered 1.5×).
- **Correction:** the v0.1 "Maracaibo lights ~doubled" candidate was a seasonal-comparison artefact — withdrawn.
- **Correction:** AST-0014 José complex AOI moved ~29 km from an OGIM offshore terminal point to the OSM complex centroid; METHOD-0002 figure for José corrected to 750 detections / 30 days (was 122 / 27, wrong location). Location visually confirmed in Sentinel-2 composites.

### Added — METHOD-0004 validation run (2026-10-04)
- Nighttime-lights pipeline (`scripts/method0004_validate.py`, VNP46A3 monthly via LAADS/CMR; outputs `data/derived/method-0004/` with manifest). Validation verdict: NOT validated (1/4 directional tests; controls unstable; monthly granularity can't see 5-day events; AOI coordinate quality decisive). Redesign pre-registered (daily VNP46A2, verified AOIs, flare masking). Candidate observation flagged: Maracaibo lights ~doubled 2023→2025.

### Added — METHOD-0001 pilot run (2026-10-04)
- Optical disturbance pipeline (`scripts/method0001_validate.py`, Sentinel-2 L2A via Planetary Computer; outputs `data/derived/method-0001/` with manifest). Validation verdict: INCONCLUSIVE/FAILED as designed — reference events lack surface expression at 10–20 m, ocean-dominated controls, seasonal confounder. Redesign requirements pre-registered (same-season pairs, land controls, surface-expression events). No Derived observations added to dossiers.

### Added — METHOD-0002 validation run (2026-10-04)
- First executed geo-method: FIRMS hotspot time series (`scripts/method0002_validate.py`, outputs `data/derived/method-0002/` with manifest). Validation history v0.1.0→v0.3.0 recorded: site-level detection FAILS (36–66% < 80%); validated as cluster-density and facility-differential indicator (controls clean; Amuay 284/30d vs Bajo Grande 0/0).
- Derived observations added to dossiers AST-0001, 0002, 0004, 0012, 0014 with manifest references; METHOD-0002 note updated with results, verdict and documented deviations.

### Added — Asset Dossier v0.1, batch 1 (2026-10-04)
- Feature brief `docs/briefs/FEATURE-asset-dossier-v0.1.md` (17 assets, validated shortlist).
- Asset registry `registry/assets.csv` (AST-0001..0004) and dossiers for the 4 refineries: CRP Paraguaná, El Palito, Morón, Bajo Grande — every claim dated and cited; observation/interpretation separated; OGIM coordinate discrepancies flagged.

### Added — Asset Dossier v0.1, batches 2–4 + reviews (2026-10-04)
- Dossiers AST-0005..0017: Faja upgraders (San Félix/Roraima, Sinovensa, Petrocedeño, Petropiar), conventional fields (Lagunillas, Quiriquire, Jusepín, Santa Bárbara, Boquerón), midstream/export (José TAECJAA, La Salina, Temblador) and offshore group (Dragon + 4 unidentified records).
- Shortlist corrected (v0.1.1): Sincor = Petrocedeño; all four upgraders at José, Anzoátegui.
- Scientific review of batches 1–4: zero blockers; 2 corrections applied (AST-0011 same-day detections; AST-0012 count 33 verified). Review record: `docs/reviews/2026-10-04-dossiers-batches-2-4.md`.

### Added — Phase B Discovery (2026-10-04)
- 11 verified dataset cards (`docs/datasets/DS-0001`–`DS-0011`): Sentinel-2, Sentinel-1, Landsat 8/9, NASA FIRMS, NASA Black Marble, World Bank Global Gas Flaring Database, VIIRS Nightfire (DISPLAY ONLY / RESTRICTED), GEM Global Oil Infrastructure Tracker, SkyTruth Cerulean, OCHA HDX Venezuela COD-AB, OpenStreetMap.
- 4 more cards from leads surfaced in a separate private research workspace (public third-party datasets only): OGIM v3.0 infrastructure database (`DS-0012`), TROPOMI CH4 (`DS-0013`), EMIT CH4 plumes (`DS-0014`), EDGAR_2025_GHG gridmaps (`DS-0015`).
- Registry rows for all 15 datasets in `registry/datasets.csv` with license, access date (2026-10-04), redistribution rights and MVP relevance score.

### Added — Sprint 0 (2026-10-04)
- Platform-independent agent system: `AGENTS.md` (single source) + `CLAUDE.md` import + 13 role skills in `.claude/skills/` (read by Devin, Claude Code, OpenCode) + OpenCode slash-command wrappers (ADR-000).
- Engineering and security baseline: `docs/engineering-rules.md` (20 verifiable rules), `docs/security.md` (access matrix, threat model, incident response), `docs/architecture/scalability.md` (trigger thresholds, no measurements yet).
- Governance: README (EN/ES), GOVERNANCE (EN/ES), CONTRIBUTING (EN/ES), CODE_OF_CONDUCT, SECURITY policy, CHANGELOG.
- Licenses: Apache-2.0 (code), CC BY 4.0 (docs/metadata).
- Templates: dataset card, ADR, feature brief, asset dossier, observation, risk.
- Pre-commit hook (gitleaks + skill-name check) and minimal CI (gitleaks + skill check + link check).
- Registry skeleton (`registry/datasets.csv`) and cross-tool session log (`research/LOG.md`).
