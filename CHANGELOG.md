# Changelog — VEIO

All notable changes to this project are documented here. Format based on Keep a Changelog; versioning starts at 0.x until the public MVP.

## [Unreleased]

### Added — ADR-002 + ADR-003: workbench decisions accepted (2026-10-06)
- `docs/adr/ADR-002-local-workbench-architecture.md` (**Accepted**): two containers (`web`, `api` with embedded TiTiler + 1-job runner), no DB/queue, `127.0.0.1` only, non-root + read-only root fs, repo mounted read-only; optional OSM basemap under the OSMF Tile Usage Policy (attribution visible, no prefetch/offline, exports exclude tiles, Referer not blocked, configurable URL).
- `docs/adr/ADR-003-veio-package-adapters-reference-values.md` (**Accepted**): `veio` package with one adapter per provider, single data-level check, manifest writer; incremental migration (v0.1 = METHOD-0003 only); hand-authored `tests/reference/METHOD-####.yaml` permitted under ADR-001, enforced by a verbatim-in-method-note check in `check_docs.py`.
- Workbench brief and plan updated: P0 done; decisions resolved; P1/P3 gates carry the ADR conditions.

### Changed — Local workbench brief v0.1 aligned to rules + plan (2026-10-06)
- `docs/briefs/FEATURE-local-workbench-v0.1.md` revised against AGENTS §2/§6/§10, ADR-001 and engineering rules: package-first refactor with one adapter per provider (rule 13); 2 containers, no DB/queue (rule 12); validated-method and asset allow-lists; single data-level choke point (rule 2); `127.0.0.1` binding, read-only root fs; "local re-run ≠ VEIO observation" labelling; reproduction checked against hand-authored reference values from the METHOD-0003 note; concrete negative tests.
- `docs/briefs/PLAN-local-workbench-v0.1.md`: phases P0–P5 with owner skills and gates (ADR-002/003 first), and mechanical alignment rules (runtime read of repo metadata, shared package, new `check_docs.py` rules, contract tests) — no new agent.

### Added — Asset × Evidence matrix (2026-10-06)
- `docs/assets/EVIDENCE-MATRIX.md` + `.es.md`: 17 assets × methods with the observation type per cell (● validated Derived · ○ unvalidated visual check · ◐ exploratory · — none). Exposes the gaps: 11 of 17 assets have no VEIO-derived observation; methods 0001/0004 unvalidated; methane exploratory.
- `scripts/check_docs.py` now fails if any asset in `registry/assets.csv` or any `METHOD-####` is missing from the matrix (EN + ES). README and PLATFORM link it.

### Changed — Apply ADR-001: generated figures removed from the repo (2026-10-06)
- Removed `docs/methods/figures/*.png` (12 files) from git. Method figures are now generated locally under `data/derived/method-*/` by the scripts that produce them.
- Updated `scripts/method0001_v03.py`, `method0002_v04.py`, `method0002_v05.py`, `method0003_validate.py` to write figures into their `data/derived/...` output directory.
- Method notes (0001–0004) and dossiers (AST-0009/0012/0014) now reference figures as **expected local paths** (inline code), not repository files.
- `scripts/check_docs.py` now fails if any committed raster/figure is found (ADR-001). `docs/foundation/figures/pipeline.svg` is hand-authored source, not a generated artifact, and remains.
- Historical CHANGELOG/LOG entries from before this change still mention `docs/methods/figures/` — they are records of that time and are not rewritten.

### Added — ADR-001 + local workbench brief (2026-10-06)
- `docs/adr/ADR-001-no-generated-artifacts-in-repo.md`: **Accepted** — the repository holds only code, metadata and text; no generated artifact (raster, layer, figure, derived JSON) is committed; outputs are generated locally and, for the future public Atlas, served from object storage.
- `docs/briefs/FEATURE-local-workbench-v0.1.md`: docker-compose local workbench (download → process → display) for researchers; PUBLIC datasets only; DS-0007 excluded; nothing written outside `./data`.
- Migration implied by ADR-001 (next step): remove `docs/methods/figures/*.png`, convert method/dossier figure links to expected local paths, adjust CI checks.

### Added — Documentation ownership + CI docs-drift check (2026-10-06)
- `AGENTS.md` §11 now assigns documentation ownership explicitly (no dedicated docs agent): each role owns its artifacts; `task-close` refreshes `STATUS.md`/`PLATFORM.md` when a method's status or a Derived observation changes; `docs-bilingual` enforces EN/ES parity; `product-architect` owns the foundation dashboards.
- `scripts/check_docs.py` (stdlib) added to CI (`docs` job): blocks drift between registry and files, method notes and `STATUS.md`, `**Derived**` citations and method notes, and orphan `.es.md` files. First run found and fixed a missing manifest citation in AST-0014.
- `task-close` and `docs-bilingual` skills updated accordingly.

### Added — Platform explainer + method status dashboard (2026-10-06)
- `docs/foundation/PLATFORM.md` + `.es.md`: executive, plain-language "how VEIO works" one-pager — the four layers, a worked end-to-end example (Santa Bárbara), the four methods at a glance, the status vocabulary, what we can/cannot claim, honest gaps, and a glossary. Pipeline diagram `docs/foundation/figures/pipeline.svg`.
- `docs/methods/STATUS.md` + `.es.md`: one row per method (question, input, plain processing, validation status, outputs, dossiers fed) + "what each method can/cannot say" + the queue.
- README (EN/ES) now links both as the entry point; status line refreshed.

### Added — METHOD-0002 v0.5 run (2026-10-05)
- Closes the Santa Bárbara nuclei method: replaces the unjustified 1.5 km OGIM point match (OGIM within-facility spread up to 17 km) with intrinsic discriminators — persistence + median stationarity + night activity. Pre-registered `abcfccf`; outputs `data/derived/method-0002/v0.5/`, figure committed.
- **Verdict: VALIDATED (scope-limited)** for fixed, persistent, night-active thermal point sources: 9 nuclei, 8 on ≥30% of 90 days, median night fraction 87%, median daily-centroid drift ≤1 km, Bajo Grande control 0. Derived observation added to AST-0012.

### Added — METHOD-0002 v0.4 run (2026-10-05)
- Santa Bárbara per-nucleus flaring characterization (FIRMS 90-day window, single-link nuclei at ~1.1 km), pre-registered in `4c34ab0` before execution; outputs `data/derived/method-0002/v0.4/` + manifest, figure under `docs/methods/figures/`.
- **Verdict: NOT validated (C3).** Structure and persistence robust (9 nuclei, 8 detected on ≥30% of 90 days; top 4,327 detections at 97.8% persistence); Bajo Grande control 0. OGIM match within 1.5 km = 60.3% (< 70% threshold), so no dossier observation added. Implementation correction (centroid → nucleus membership) documented; criterion unchanged.
- Fixes the FIRMS 5-day-chunk header-join bug (parse per chunk) and updates the memory note.

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
