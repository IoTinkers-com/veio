# Feature brief — Local reproducible workbench (v0.1)
<!-- Cap: ≤1 page. Written by product-architect BEFORE implementation. -->

**Bottom line:** A `docker-compose` app that runs on the user's own machine, downloads public layers locally, runs VEIO's committed scripts, and shows the resulting layers together with our published observations — so VEIO stores no data and every figure is reproducible.

## Core
- **Problem:** VEIO's evidence is text-first; the derived layers/figures are not distributable and a researcher cannot explore an asset's evidence or reproduce it without the private data tree.
- **Hypothesis:** if the workbench downloads public inputs and runs the *same committed scripts* locally, a researcher can reproduce and inspect VEIO's observations per asset, with nothing stored by VEIO (per `ADR-001`).
- **Data needed:** PUBLIC only — DS-0002 Sentinel-1 RTC (no key), DS-0001 Sentinel-2 (no key), DS-0010 OCHA boundaries, DS-0011 OSM, DS-0012 OGIM; later DS-0004 FIRMS (user MapKey), DS-0005 Black Marble / DS-0014 EMIT (user EDL token). **DS-0007 VNF excluded (RESTRICTED).**
- **Design:** `docker-compose` services — `web` (MapLibre GL + asset panel), `api`/`worker` (FastAPI + GDAL/rasterio; executes method scripts), `tiles` (TiTiler over local COGs); shared git-ignored `./data` volume. Flow per asset: pick AST-#### → **Download** (clip inputs to the AOI) → **Process** (run the method script) → view layers + generated figure + the dossier's Derived observation + manifest link → export (GeoTIFF/GeoJSON). The method catalog is derived from `docs/methods/STATUS.md`; an observations index is generated from the dossiers.
- **Security & provenance impact:** no server-side storage; credentials only in the user's local volume; no secrets in the frontend; every generated product carries a manifest (inputs, params, checksums); RESTRICTED datasets are refused; only already-public AOIs are used.
- **Risks:** (1) credential friction for keyed sources (FIRMS/EMIT); (2) heavyweight SAR downloads (state the size before starting); (3) method scripts assume specific endpoints — portability and version pinning needed.
- **Acceptance criteria:** `docker-compose up` starts all services; for one validated method (METHOD-0003) and one asset (AST-0009) the app downloads, processes, renders the layer + figure, and links the dossier observation; **nothing is written outside `./data`**; a RESTRICTED dataset request is refused; two runs on the same inputs produce matching manifests; the docs drift check (`scripts/check_docs.py`) still passes.
- **Out of scope:** server hosting, user accounts, unvalidated methods (METHOD-0001/0004), methane (METHOD-0005 proposed), collaborative editing, real-time monitoring.

## On request
— (on request) detailed design, wireframes, per-service compose spec.
