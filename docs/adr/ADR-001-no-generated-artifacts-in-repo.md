# ADR-001: No generated artifacts in the repository

**Status:** Accepted
**Date:** 2026-10-06

## Context
- AGENTS §12 already fixes that raw, normalized and derived data never mix and that `data/` is git-ignored, but in practice **rendered method figures have been committed** under `docs/methods/figures/` and embedded in method notes and dossiers.
- The steward does not want generated figures or layers stored in the repositories.
- Derived products are heavyweight (a Sentinel-1 RTC scene is ~2 GB), can carry redistribution constraints (e.g. DS-0007 VNF is DISPLAY ONLY / RESTRICTED), and are **reproducible** from public inputs plus committed code.
- A local, reproducible workbench is being designed (see `docs/briefs/FEATURE-local-workbench-v0.1.md`) that generates layers and figures on the user's machine.

## Decision
- The public repository holds only **code, metadata and text**: scripts, registry CSVs, dataset cards, method notes, asset dossiers, briefs, ADRs, templates and governance docs.
- **No generated artifact** — raster, vector layer, rendered figure or derived JSON/KML — is committed. All are produced locally by the workbench into the git-ignored `data/` tree.
- Method notes and dossiers reference generated outputs as **expected local paths** (inline code), never as repository files or image links.
- When a public Atlas exists, it will serve generated artifacts from **object storage** separate from git, under its own ADR.

## Consequences
- **Positive:** lean repository; no redistribution of licensed data; every visual is reproducible; no drift between a committed figure and a re-run.
- **Negative:** GitHub no longer displays figures; the existing `docs/methods/figures/*.png` must be removed from git and re-generated locally; method/dossier references and CI checks must be adjusted.
- **Neutral:** the workbench becomes the canonical renderer of VEIO outputs.

## Alternatives considered
- **Keep small figures in git (status quo)** — rejected: the steward does not want generated artifacts in the repo, and committed figures can drift from re-runs.
- **Commit only the figure source data (numpy/GeoJSON)** — rejected: still generated, heavy and licensing-sensitive.
- **Publish figures to a GitHub Pages branch** — rejected for now: still storing generated artifacts in the repository; object storage is the intended home for the public Atlas.
