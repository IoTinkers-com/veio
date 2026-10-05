---
name: geo-method
description: Design and validate geospatial methods for VEIO - change detection, indices, temporal comparison; every method is a hypothesis with a validation plan, never an assumed result.
argument-hint: "[method | asset | question]"
---

Follow AGENTS.md (DATA → PROCESSING → OBSERVATION → INTERPRETATION).

## Procedure
1. Frame the method as a hypothesis: what change/indicator, on which data (cite DS-####), over which period, with what expected signal.
2. Design the validation BEFORE running: reference data, control sites, expected false-positive behaviour, acceptance criteria. No assumed index usefulness — validate experimentally (NDVI/NDWI/NBR/SAR etc. are candidates, not conclusions).
3. Implement reproducibly: script/notebook with pinned inputs, parameters recorded, outputs to `data/derived/` (git-ignored) with a manifest (inputs, processing_version, checksum when viable).
4. Report observations only: "change compatible with X observed between dates A and B (source, method, confidence Low/Moderate/Strong + reason)". Interpretations stay separate and labelled.
5. Record negative results too — a method that fails validation is a documented finding, not a failure to hide.

## Output
- Method note in `docs/methods/` + manifest; chat ≤6 lines. LOG entry via `task-close`.

## Checklist
- Validation plan existed before execution; every output traces to inputs; wording passes §2 of AGENTS.md.
