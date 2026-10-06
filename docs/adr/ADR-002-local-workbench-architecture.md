# ADR-002: Local workbench architecture — two containers, no database, localhost only

**Status:** Accepted
**Date:** 2026-10-06

## Context
- ADR-001 keeps every generated artifact out of the repository, so the workbench (`docs/briefs/FEATURE-local-workbench-v0.1.md`) becomes the canonical renderer of VEIO outputs.
- The user is one researcher on their own machine. Engineering rule 12 forbids infrastructure without a measured trigger (`docs/architecture/scalability.md`).
- Method runs take minutes (METHOD-0003: 18 Sentinel-1 scenes). The scalability trigger "job > 60 s → queue + worker" is defined for request-path processing on a shared server, not for a single local user.
- Host environments differ: a system PostGIS `proj.db` broke rasterio on the steward's workstation (`.agents/memory/rasterio-proj-planetary-computer.md`).

## Decision
- Ship the workbench as **two containers** via `docker compose`:
  - `web`: static MapLibre build.
  - `api`: FastAPI with embedded TiTiler and an in-process job runner, at most **1 concurrent job**, run off the request path with status polling.
- **No database and no job queue in v0.1.** State is the git-ignored `./data` tree plus manifests.
- **Bind to `127.0.0.1` only.** Non-root users; read-only root filesystem; `./data` is the only writable volume. The repository is mounted **read-only** as the source of registry, `STATUS.md` and dossier metadata.
- **Basemap:** OpenStreetMap standard raster tiles as an **optional** layer, compliant with the OSMF Tile Usage Policy (accessed 2026-10-06):
  - attribution always visible;
  - no prefetch or offline use, and exports exclude basemap tiles;
  - `Referrer-Policy` must not block the Referer (`strict-origin-when-cross-origin` is acceptable);
  - the tile URL is configurable, not hard-coded;
  - the CSP allows `tile.openstreetmap.org`.
- A database, queue or extra service requires a new ADR citing a measured trigger (e.g., >1 concurrent user, multi-user hosting).

## Consequences
- **Positive:** minimal surface; reproducible environment independent of host libraries; no VEIO-side storage; nothing reachable from the LAN.
- **Negative:** one job at a time; no run history beyond `./data`; OSM tiles need internet access and send the viewed area to OSMF servers (to be disclosed in the user guide).
- **Neutral:** a future public Atlas needs its own ADR (object storage, tile provider or self-hosting); this ADR does not cover hosting.

## Alternatives considered
- **Four services (web, api, worker, tiles) plus a queue:** rejected — no measured trigger for a single local user.
- **PostGIS for runs and observations:** rejected — the registry CSVs and manifests already hold the state; adding a DB duplicates the source of truth.
- **No basemap:** rejected — interpreting detections without coastline and settlement context raises the risk of over-interpretation (§2), and the OSMF policy explicitly permits interactive human viewing.
- **Self-hosted or offline tiles:** deferred — unnecessary for v0.1; would be needed for offline use or a public deployment.
