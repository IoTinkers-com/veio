---
name: asset-dossier
description: Build or update a VEIO Asset Dossier - identity, location, infrastructure, temporal observations, change indicators, environmental observations, provenance and confidence for one energy asset.
argument-hint: "[AST-#### | new candidate]"
---

Follow AGENTS.md (§2 wording, §5 evidence, §6 licensing).

## Procedure
1. New candidate: propose `AST-####` from public datasets only (cite DS-####); check diversity criteria (region, asset type, data availability). Register in `registry/assets.csv`.
2. Create/update `docs/assets/AST-####-<slug>.md` from `templates/asset-dossier.md`: Identity, Location (public coordinates only), Infrastructure, Historical imagery, Temporal observations (dated, sourced), Change indicators (from `geo-method`, labelled Derived), Environmental observations (generic anomaly categories only), Methane/flaring association, Provenance (every source with date/version), Confidence (Low/Moderate/Strong + reason), Limitations (what we cannot claim).
3. Every factual line cites a source or a derived product with its manifest. Observations and interpretations are separate sections.
4. Sensitive location or unclear publication rights → RESTRICTED: move the dossier to `veio-internal`, leave a public stub.

## Output
- Dossier file + registry row; chat ≤6 lines + path. LOG entry via `task-close`.

## Checklist
- Wording passes AGENTS.md §2; no unsupported claims; limitations section present; provenance complete.
