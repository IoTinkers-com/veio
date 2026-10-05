# VEIO — Venezuela Energy Infrastructure Observatory

**Bottom line:** An open geospatial observatory documenting the evolution of Venezuela's energy infrastructure with reproducible temporal evidence. First vertical: Oil & Gas. The first product is a public Atlas; the core artifact is the **Asset Dossier** — what we know, where it comes from, what we process, what we observe, and what we cannot claim.

## Principles
- **DATA → PROCESSING → OBSERVATION → INTERPRETATION** — never merged. See `AGENTS.md` §2 for wording rules.
- Open data, open methodology, reproducible processing, documented provenance.
- Licensing gate: no dataset without verified license, attribution and redistribution rights; unclear → DISPLAY ONLY / RESTRICTED.
- Ethics: no accusations, no unverified claims, no responsibility attribution. Technical, descriptive language.

## Repository map
| Path | Content |
|---|---|
| `AGENTS.md` | Rules for any AI agent (single source; `CLAUDE.md` imports it) |
| `.claude/skills/` | 13 role skills (read by Devin, Claude Code, OpenCode) |
| `docs/engineering-rules.md`, `docs/security.md`, `docs/architecture/scalability.md` | Binding engineering/security baseline |
| `docs/adr/` | Architecture decision records |
| `docs/briefs/` | Feature briefs (dossier v0.1, change indicators v0.2) |
| `docs/methods/` | Geo-method notes — hypothesis + validation plan + results |
| `docs/assets/`, `registry/assets.csv` | Asset Dossiers (AST-0001..0017) and asset registry |
| `docs/datasets/`, `registry/datasets.csv` | Dataset cards (DS-0001..0015) and matrix |
| `docs/reviews/` | Scientific review records |
| `scripts/` | Method validation scripts (reproducible, manifested outputs) |
| `docs/foundation/` | Technical & Product Foundation |
| `templates/` | Card/ADR/brief/dossier templates |
| `.agents/memory/` | Known traps for agents |
| `research/LOG.md` | Cross-tool session log |

Companion private repository `veio-internal` holds RESTRICTED material (funding, partners, sensitive data notes). It is referenced, never mirrored, here.

## Status
MVP evidence base in place: 15 verified dataset cards, 17 Asset Dossiers v0.1 (reviewed), 4 geo-method notes (1 validated as differential/density indicator, 2 redesigns pre-registered). No web product yet — Atlas UI is Sprint 2+.

## Contributing
See `CONTRIBUTING.md`. Contributions follow a review workflow (Submitted → Under Review → Validated/Rejected/Superseded) with history preserved.

## License
- Code: Apache-2.0 (`LICENSE`).
- Documentation, methodology and metadata: CC BY 4.0 (`LICENSE-docs`).
- Datasets keep their own licenses — always check the dataset card and the map attribution.

## Security
See `SECURITY.md`. Report vulnerabilities privately via GitHub security advisories — never in public issues.
