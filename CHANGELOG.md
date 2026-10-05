# Changelog — VEIO

All notable changes to this project are documented here. Format based on Keep a Changelog; versioning starts at 0.x until the public MVP.

## [Unreleased]

### Added — Phase B Discovery (2026-10-04)
- 11 verified dataset cards (`docs/datasets/DS-0001`–`DS-0011`): Sentinel-2, Sentinel-1, Landsat 8/9, NASA FIRMS, NASA Black Marble, World Bank Global Gas Flaring Database, VIIRS Nightfire (DISPLAY ONLY / RESTRICTED), GEM Global Oil Infrastructure Tracker, SkyTruth Cerulean, OCHA HDX Venezuela COD-AB, OpenStreetMap.
- Registry rows for all 11 datasets in `registry/datasets.csv` with license, access date (2026-10-04), redistribution rights and MVP relevance score.

### Added — Sprint 0 (2026-10-04)
- Platform-independent agent system: `AGENTS.md` (single source) + `CLAUDE.md` import + 13 role skills in `.claude/skills/` (read by Devin, Claude Code, OpenCode) + OpenCode slash-command wrappers (ADR-000).
- Engineering and security baseline: `docs/engineering-rules.md` (20 verifiable rules), `docs/security.md` (access matrix, threat model, incident response), `docs/architecture/scalability.md` (trigger thresholds, no measurements yet).
- Governance: README (EN/ES), GOVERNANCE (EN/ES), CONTRIBUTING (EN/ES), CODE_OF_CONDUCT, SECURITY policy, CHANGELOG.
- Licenses: Apache-2.0 (code), CC BY 4.0 (docs/metadata).
- Templates: dataset card, ADR, feature brief, asset dossier, observation, risk.
- Pre-commit hook (gitleaks + skill-name check) and minimal CI (gitleaks + skill check + link check).
- Registry skeleton (`registry/datasets.csv`) and cross-tool session log (`research/LOG.md`).
