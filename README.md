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
| `docs/foundation/` | Technical & Product Foundation |
| `docs/datasets/`, `registry/datasets.csv` | Dataset cards and matrix |
| `templates/` | Card/ADR/brief/dossier templates |
| `.agents/memory/` | Known traps for agents |
| `research/LOG.md` | Cross-tool session log |

Companion private repository `veio-internal` holds RESTRICTED material (funding, partners, sensitive data notes). It is referenced, never mirrored, here.

## Status
Sprint 0 — Discovery & Foundation. No product code yet; see `docs/foundation/` and the roadmap.

## Contributing
See `CONTRIBUTING.md`. Contributions follow a review workflow (Submitted → Under Review → Validated/Rejected/Superseded) with history preserved.

## License
- Code: Apache-2.0 (`LICENSE`).
- Documentation, methodology and metadata: CC BY 4.0 (`LICENSE-docs`).
- Datasets keep their own licenses — always check the dataset card and the map attribution.

## Security
See `SECURITY.md`. Report vulnerabilities privately via GitHub security advisories — never in public issues.
