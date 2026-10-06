# Plan — Local reproducible workbench v0.1

**Bottom line:** Six phases, each ending in something demonstrable. The critical path is P1 (packaging the method code). The UI comes last because it only renders what the package already reproduces. Brief: `FEATURE-local-workbench-v0.1.md`.

## Phases
| # | Phase | Owner skill | Deliverable | Gate (done when) |
|---|---|---|---|---|
| P0 | Decisions | product-architect | **ADR-002** workbench architecture (2 containers, no DB/queue, `127.0.0.1` only, repo mounted read-only); **ADR-003** `veio` package + adapters (rule 13) | Both ADRs Accepted by the steward |
| P1 | Core package | data-pipeline, geo-method | `veio/` with `adapters/` (planetary_computer, hdx; laads/firms stubbed for v0.2), `access.py` (single data-level check), `manifest.py`, `methods/m0003.py`; `scripts/method0003_validate.py` becomes a thin wrapper; `tests/reference/METHOD-0003.yaml` (hand-authored from the method note: object, counts, controls, pinned scene IDs) | `python -m veio run METHOD-0003 --asset AST-0009` in a container reproduces the reference values; unit tests use synthetic arrays only (nothing committed, ADR-001) |
| P2 | API | backend-api, web-security | FastAPI: `GET /assets`, `/methods` (validated only), `/datasets` (attribution, level), `POST /runs`, `GET /runs/{id}`, `/runs/{id}/manifest`; TiTiler over `./data`; headers; schema validation; bbox cap | All acceptance negative tests pass (403/422, LAN unreachable); OpenAPI committed as text |
| P3 | Web | map-frontend | MapLibre + asset panel: dossier statements labelled Source-recorded / Derived / Interpretation; a separate "local re-run" section with the reproduction check (✓ / mismatch); per-layer attribution; size estimate before running; export | Keyboard navigation + contrast checks; layer shows the AST-0009 detection with attribution |
| P4 | Packaging & CI | devops | `docker-compose.yml`, non-root images pinned by digest, read-only root fs + `./data` volume, lockfiles (deps ≥7 days old), CI job running typecheck → lint → test → build (mypy/ruff/pytest; tsc/eslint/vitest/vite) | CI green; image builds reproducible; gitleaks clean |
| P5 | Validate & document | scientific-review, docs-bilingual, task-close | Clean-machine acceptance run (Windows + Linux); user guide `docs/foundation/WORKBENCH.md` + `.es.md` (human-facing → bilingual); PLATFORM/STATUS links; CHANGELOG/LOG | All brief acceptance criteria met; scientific-review confirms §2 labelling in the UI |

Order: P0 → P1 → (P2 ∥ P4 skeleton) → P3 → P5. v0.2 backlog: METHOD-0002 with the user's FIRMS MapKey (`.env`, never in the frontend), more assets, Earthdata sources.

## Alignment without new agents
The app must not hold its own copy of VEIO's facts. Alignment is enforced mechanically, not by an agent's memory:
- **Single source of truth at runtime:** the app reads `registry/*.csv`, `STATUS.md` and dossiers from the repo, mounted read-only. No catalog is duplicated.
- **Shared code:** CLI scripts and the app call the same `veio` package, so there is no second implementation that can diverge.
- **CI rules added to `scripts/check_docs.py`:**
  - every Validated/Scope-limited method in STATUS has a registered entrypoint and a `tests/reference/METHOD-####.yaml`;
  - no entrypoint exists for a Not-validated method;
  - every dataset an entrypoint uses is registered and not RESTRICTED.
- **Contract tests** on the parsers (CSV columns, STATUS table, dossier `**Derived**` lines), so a format change in the docs breaks CI instead of silently breaking the app.
- **Roles:** the existing skills already cover the work (backend-api, map-frontend, devops, web-security, data-pipeline). `task-close` gains one line: if a method's status changes, update its entrypoint and reference file in the same commit (CI blocks it otherwise).

## Open decisions for the steward
1. Approve ADR-002/003 scope (2 containers, no DB, package refactor first).
2. Reference values are hand-authored YAML (metadata, not generated output). Confirm this is consistent with ADR-001.
3. Basemap: none in v0.1 (local S1 composite + OCHA boundaries), or OSM tiles subject to the OSM tile usage policy [UNVERIFIED for app use].
