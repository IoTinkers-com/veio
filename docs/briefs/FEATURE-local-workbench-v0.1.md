# Feature brief — Local reproducible workbench (v0.1)
<!-- Cap: ≤1 page. Written by product-architect BEFORE implementation. Plan: docs/briefs/PLAN-local-workbench-v0.1.md -->

**Bottom line:** A two-container app on the researcher's own machine that re-runs one **validated** VEIO method for one asset from public inputs, shows the result beside the dossier's published observation, and checks it against the method note. VEIO stores nothing (ADR-001). First demo: **METHOD-0003 × AST-0009**.

## Core
- **Problem:** after ADR-001 no figure or layer lives in the repo, and the 19 method scripts are loose, call providers directly and depend on one workstation (e.g., PROJ conflicts). Nobody else can reproduce or inspect an observation.
- **Hypothesis:** if method code is packaged once (adapters + manifests) and run in a container, a researcher with Docker reproduces the METHOD-0003 result recorded in its method note, with no VEIO-side storage.
- **Data needed (v0.1, keyless, PUBLIC):** DS-0002 Sentinel-1 RTC (pinned scene IDs) · DS-0010 OCHA boundaries · repo metadata (`registry/*.csv`, `docs/methods/STATUS.md`, dossiers) mounted **read-only**. Keyed sources (DS-0004 FIRMS, DS-0005/0014 Earthdata) wait until v0.2. **DS-0007 is refused.** No external basemap tiles in v0.1.
- **Design:**
  - **Package first:** a `veio` Python package with one adapter per provider (rule 13), a manifest writer and method modules. Existing scripts become thin CLI wrappers, so CLI and app run the same code.
  - **Two containers, no DB, no queue (rule 12):** `web` (static MapLibre build) and `api` (FastAPI + embedded TiTiler + an in-process job runner, max 1 job). A job queue is added only with multiple users (scalability trigger).
  - **Allow-lists, not free input:** assets come from `registry/assets.csv`; runnable methods are those marked Validated/Scope-limited in `STATUS.md`, each via a declared entrypoint. No shell, no uploads.
  - **Flow:** pick AST → see the size estimate → run (download → process) → view layer, figure, manifest and **reproduction check** → export GeoTIFF/GeoJSON.
- **Security & provenance impact:**
  - Data-level checks go through one function (rule 2): RESTRICTED/DISPLAY ONLY → 403.
  - Binds to `127.0.0.1` only; non-root containers; read-only root filesystem; `./data` is the only writable volume.
  - Security headers; schema-validated inputs with a bbox area cap; no secrets in the frontend; no secrets logged.
  - Every output has a manifest (inputs, scene IDs, params, `processing_version`, checksums).
  - Labels keep §2 layers apart: a local re-run is shown as "local re-run — not a VEIO observation", separate from the dossier's **Derived** text. Per-layer attribution and license come from the registry.
- **Risks:**
  1. Upstream drift: scenes get reprocessed or withdrawn → pin scene IDs; report a mismatch, never substitute scenes silently.
  2. The refactor drifts from the published results → reference values are hand-authored from method notes and tested.
  3. Network weight and fragility (~18 SAR scenes, windowed reads) → state the estimate before running; resumable cache in `./data/raw`.
  4. Users may read local outputs as VEIO claims → UI labels and the export header both say otherwise.
- **Acceptance criteria:**
  1. `docker compose up` on a clean machine.
  2. METHOD-0003 × AST-0009 reproduces the method note: 1 object at 10.13715/−71.2703 (±1 px), bright in 11/11 post scenes and 0/7 pre, both controls 0.
  3. Two runs on the pinned inputs give identical output checksums.
  4. Nothing is written outside `./data` (read-only filesystem test).
  5. Negative tests: DS-0007 → 403; METHOD-0001 (not validated) → absent/403; unknown AST → 422; bbox over the cap → 422; the API is unreachable from the LAN.
  6. Quality gate typecheck → lint → test → build passes; `check_docs.py` passes.
- **Out of scope:** hosting or a public Atlas, accounts, unvalidated methods (0001/0004), CH4, keyed sources, uploads, editing dossiers from the app, a database.

## On request
— (on request) wireframes, compose spec, API schema. Phases, gates and alignment rules: `docs/briefs/PLAN-local-workbench-v0.1.md`.
