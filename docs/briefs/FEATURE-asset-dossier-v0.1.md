# Feature brief — Asset Dossier v0.1

**Bottom line:** Build 17 evidence-linked dossiers (AST-0001..0017, validated shortlist) — the MVP's core artifact: what we know, where it comes from, what we observe, what we cannot claim.

## Core
- **Problem:** Venezuela's energy infrastructure evolution has no reproducible public record linking observations to evidence; claims circulate without provenance.
- **Hypothesis:** The 15 registered datasets (esp. DS-0012 OGIM locations + DS-0001/0002/0003 imagery + DS-0004/0007 flaring) support v0.1 dossiers for all 17 assets that pass scientific review.
- **Data needed:** DS-0012 (locations; PUBLIC) · DS-0001/0002/0003 (optical/SAR imagery; PUBLIC) · DS-0004 (hotspots; PUBLIC) · DS-0006 (flaring context; PUBLIC) · DS-0010 (boundaries; PUBLIC) · DS-0013/0014 (CH4; PUBLIC) · DS-0007 VNF (DISPLAY ONLY / RESTRICTED — reference findings, never republish data).
- **Design:** One dossier per asset from `templates/asset-dossier.md`: identity → location → infrastructure → temporal observations → change indicators → provenance & confidence. Batches of 4–5 (batch 1: refineries AST-0001..0004). Every claim cited with access date; labels **Source-recorded / Derived / Interpretation**; evidence **Low/Moderate/Strong** with reason.
- **Security & provenance:** All content PUBLIC; only already-public locations (§10). Derived observations trace to inputs; derived products carry manifests. No RESTRICTED material; no VNF machine-readable republication.
- **Risks:** (1) identity↔coordinate mismatch for JV upgraders/offshore [GAP] — resolve per dossier before publication; (2) stale OGIM vintages (2017/2021) — label SRC_DATE, status claims only from dated sources; (3) scope creep across 17 assets — v0.1 section cap ≤1 page each.
- **Acceptance criteria:** 17/17 dossiers pass `scientific-review`; every factual claim has ≥1 dated citation; zero unlabeled interpretations; observation methods reference a geo-method hypothesis; bilingual `.es.md` versions scheduled before Atlas publication.
- **Out of scope:** Atlas web UI and API (Sprint 2+), community contributions (Sprint 5), non-O&G verticals, real-time monitoring, new data collection.

## On request
— (on request) detailed design, wireframes
