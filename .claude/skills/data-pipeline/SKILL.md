---
name: data-pipeline
description: VEIO data engineering - raw/normalized/derived separation, ingestion pipelines, migrations with history, indexes incl. GIST, provenance manifests. Active from Sprint 1.
argument-hint: "[dataset | pipeline | migration]"
---

Follow AGENTS.md §5, §10, §12. Status: stub — fully specified when Sprint 1 starts.

## Procedure (when activated)
1. Layers never mix: `data/raw/` (immutable, checksummed) → `data/normalized/` (cleaned, typed, CRS-normalized) → `data/derived/` (outputs of processing with manifests).
2. Every pipeline run records: inputs (DS-#### + versions), parameters, code version, outputs, checksums. Reproducible from the manifest alone.
3. Schema changes only via the migration tool chosen in an ADR — never manual SQL; every new queried column gets its index (GIST for geometry) in the same migration.
4. Ingestion respects the licensing gate: DISPLAY ONLY/RESTRICTED datasets are not redistributed, only referenced.
5. Validate before load: geometry validity, CRS, bounds, duplicates; quarantine failures with a reason.

## Output
- Pipeline code + manifest + migration; chat ≤6 lines. LOG entry via `task-close`.

## Checklist
- Layers separated; manifest complete; migration indexed; no unlicensed redistribution.
