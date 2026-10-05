# Changelog — VEIO

All notable changes to this project are documented here. Format based on Keep a Changelog; versioning starts at 0.x until the public MVP.

## [Unreleased]

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
