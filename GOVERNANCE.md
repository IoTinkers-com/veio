# Governance — VEIO

## Principles
1. **Transparency:** methods, data sources and processing are documented and public (except RESTRICTED material, whose existence and handling rules are public even when content is not).
2. **Reproducibility:** every derived result can be re-run from recorded inputs, parameters and code versions.
3. **Attribution:** every dataset and contributor is credited; the map always shows per-layer attribution and license.
4. **Correction:** errors are corrected with dated, visible amendments; superseded observations stay linked, never silently deleted.
5. **Versioning:** datasets, processing and decisions are versioned (DS/OBS/ADR identifiers + processing_version).
6. **Editorial independence:** interpretations are separated from observations; funders and partners get no editorial control over findings.
7. **Conflict of interest:** reviewers declare conflicts; declarations are recorded with the review.

## Roles
- **Steward:** IoTinkers hosts and maintains the project; it does not presume ownership of community contributions.
- **Maintainers:** merge rights; enforce gates (scientific-review, web-security, task-close).
- **Reviewers:** validate contributions and dossiers.
- **Contributors:** submit observations/evidence with license and method.

## Decision-making
- Technical/product decisions: ADR (one decision = one ADR; supersede, never edit).
- Community governance evolution (IP, trademarks, contributor agreements): documented in `veio-internal/legal/` until ratified publicly.

## Information levels
PUBLIC / RESEARCH / RESTRICTED per `AGENTS.md` §7. RESTRICTED material lives only in the private companion repo; its handling rules are public, its content is not.

## License of outputs
Code Apache-2.0; docs/methodology/metadata CC BY 4.0; datasets under their own licenses with attribution displayed.
