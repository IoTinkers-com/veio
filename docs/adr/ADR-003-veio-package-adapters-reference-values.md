# ADR-003: `veio` package with provider adapters and hand-authored reference values

**Status:** Accepted
**Date:** 2026-10-06

## Context
- Method code lives in 19 standalone scripts under `scripts/`. Each calls Planetary Computer, LAADS, CMR or FIRMS directly, against engineering rule 13 (one adapter per external service).
- The workbench must run the **same** code as the published validation runs. A second implementation would drift from the method notes.
- Reproduction must be checkable, but ADR-001 forbids committing manifests or derived JSON. The published numbers live only as text in `docs/methods/METHOD-####.md`.
- The Sentinel-1 scene IDs used by METHOD-0003 v0.1 are recorded only in the local, uncommitted manifest.

## Decision
- **Create a `veio` Python package**:
  - `veio/adapters/<provider>.py`: the only modules allowed to import provider SDKs or call provider endpoints;
  - `veio/access.py`: the single data-level check (PUBLIC/RESEARCH/RESTRICTED, DISPLAY ONLY) read from `registry/datasets.csv`;
  - `veio/manifest.py`: inputs, scene IDs, parameters, `processing_version`, checksums;
  - `veio/methods/m####.py`: method logic.
- **Incremental migration:** v0.1 migrates only METHOD-0003 and the adapters it needs (Planetary Computer, HDX). Other methods move into the package when they enter the workbench. Migrated scripts become thin CLI wrappers over the package; unmigrated scripts stay as they are until then.
- **Reference values:** each method runnable in the workbench has `tests/reference/METHOD-####.yaml` with expected results and pinned input identifiers (e.g., scene IDs).
  - **Hand-authored only**, transcribed from the method note — never dumped or generated from a run.
  - This is test metadata, not a generated artifact, so it is permitted under ADR-001.
  - `scripts/check_docs.py` fails if any numeric value in a reference file does not appear verbatim in its method note, or if a reference file exists for a method that is not Validated/Scope-limited in `STATUS.md`.
- **Workbench entrypoints** exist only for methods marked Validated/Scope-limited; CI blocks an entrypoint for any other method.

## Consequences
- **Positive:** one implementation for CLI and app; provider changes touch one module; reproduction is testable without committing outputs; the method note stays the single source of published numbers.
- **Negative:** refactoring effort before any UI exists; the old and packaged script styles coexist during migration; pinned scenes can be withdrawn upstream (reported as a mismatch, never silently substituted).
- **Neutral:** unit tests use synthetic arrays created at test time, so no fixtures are committed.

## Alternatives considered
- **Refactor all 19 scripts now:** rejected — large up-front cost, and most methods are not validated or not in v0.1.
- **The app shells out to the existing scripts:** rejected — keeps direct provider calls (rule 13) and allows arbitrary execution paths.
- **Commit the run manifest as the reference:** rejected — a generated artifact (ADR-001).
- **Parse expected values from the method note at test time:** rejected for v0.1 — prose tables are fragile to parse; the verbatim check gives the same guarantee with a simpler format.
