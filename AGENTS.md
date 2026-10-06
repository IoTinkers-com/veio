# AGENTS.md — VEIO (Venezuela Energy Infrastructure Observatory)

Entry point for any coding agent (Devin, Claude Code, OpenCode, Codex, Cursor, …) working in this repository. `CLAUDE.md` imports this file; platform-specific wrappers live in `.opencode/commands/`.

## 1. Mission
- VEIO is an open geospatial observatory documenting the evolution of Venezuela's energy infrastructure with reproducible temporal evidence. First vertical: Oil & Gas. Later verticals (electricity, mining, water…) are designed-for but not built.
- MVP: a public Atlas + **Asset Dossier v0.1** for 10–20 representative O&G assets: what we know, where it comes from, what we process, what we observe, and what we cannot claim.
- Steward: IoTinkers. The project is designed to evolve into a community effort; IoTinkers is not presumed owner of community contributions.

## 2. Core principle (non-negotiable)
Keep four layers separated: **DATA → PROCESSING → OBSERVATION → INTERPRETATION**. Never turn an observation into a conclusion automatically.
- Say: "No visible operational activity observed in available imagery for period X." Not: "This well is abandoned."
- Say: "Persistent dark surface anomaly near infrastructure detected." Not: "This is an oil spill."
- Say: "Changes compatible with activity/intervention observed." Not: "This field was reactivated."
Every statement must trace back to its evidence.

## 3. Working across tools and sessions
- Skills live only in `.claude/skills/` (the one path read by Devin, Claude Code and OpenCode). OpenCode `/name` wrappers in `.opencode/commands/`. Rules live only here; `CLAUDE.md` is a one-line import.
- At session start read the last ~30 lines of `research/LOG.md` and `.agents/memory/MEMORY.md`. At end, append a LOG entry (≤6 lines: date, tool/model, changes, open items, next step).
- State lives in files, not chat memory. One tool at a time; commit between sessions.
- Two-repo boundary: this repo is PUBLIC. Anything sensitive (funding, partners, costs, RESTRICTED data, legal notes) is written only in `veio-internal` and referenced here as "see internal repo" without content.

## 4. Writing style (default: executive)
- Open artifacts with `Bottom line:` (1–3 lines). Bullets/tables over prose; no intros, recaps or marketing adjectives.
- One idea per bullet, ≤~20 words; numbers and units over qualifiers.
- Caps unless the user asks for more: dataset card ≤150 words · ADR ≤1 page · feature brief ≤1 page · asset dossier section ≤1 page each · LOG ≤6 lines · chat reply = short summary + file paths.
- Human-facing docs are bilingual: `X.md` (English) + `X.es.md` (Spanish), same content. Agent-facing files are English-only.
- Unknowns: `[UNVERIFIED]` or `[GAP: …]`. Brevity never drops citations, licenses or limitations.

## 5. Evidence and provenance rules (non-negotiable)
- Never invent datasets, licenses, coverage, resolutions or APIs. Verify every URL before registering; record access date.
- Every factual claim in a dossier/observation cites its source(s). Label statements: **Source-recorded**, **Derived (our processing)**, **Interpretation**.
- Evidence categories: **Low / Moderate / Strong** — always with the reason; never a numeric "truth score".
- Provenance per dataset: source_id, provider, dataset_name, source_url, license, acquisition_date, original_date, version, coverage, resolution, processing, processing_version, checksum when viable. Derived observations trace to their inputs.
- Venezuela regulatory/sanctions facts carry an "as of" date; re-verify if >90 days old. Legal/sanctions questions: flag for counsel, never opine.

## 6. Licensing gate
No dataset enters without: provider, license, attribution requirements, modification rights, redistribution rights, known restrictions. "Public on the internet" ≠ "free to redistribute". If redistribution is unclear → mark **DISPLAY ONLY / RESTRICTED** until verified. The map always displays attribution and license per layer.

## 7. Information levels
- **PUBLIC** — this repo and the future Atlas.
- **RESEARCH** — working analysis, drafts; public repo unless flagged.
- **RESTRICTED** — `veio-internal` only (agreements, security, privacy, IP, sensitive locations).
Design for these levels from the start; do not build complex security in the MVP.

## 8. Ethics
No accusations, no unverified claims, no attribution of responsibility, no environmental conclusions without evidence, no inferences about people, no unnecessary publication of sensitive information. Technical, descriptive language. Observation ≠ Interpretation ≠ Conclusion.

## 9. Workflow
DISCOVER → DEFINE → RESEARCH → DESIGN → IMPLEMENT → TEST → VALIDATE → DOCUMENT → DEPLOY. Never jump to IMPLEMENT.
Before implementing any significant feature, `product-architect` produces a **feature brief** (problem, hypothesis, data needed, design, risks, acceptance criteria) from `templates/feature-brief.md`. Any significant decision = one ADR (`docs/adr/`); supersede with a new ADR, never edit.

## 10. Engineering and security rules
`docs/engineering-rules.md` (each rule states its check) and `docs/security.md` (access matrix, threat model, incident response) are binding for all web code. Summary: single authorization choke point enforcing PUBLIC/RESEARCH/RESTRICTED; schema-validated inputs with length/pagination/spatial bounds; indexes (incl. GIST) in the same migration; migrations only via the migration tool; derived values persisted only with formula + source; quality gate **typecheck → lint → test → build** before closing any task; no infra without a measured trigger; one adapter per external service; no secrets in frontend; security headers, rate limits, generic 5xx, non-root containers; uploads validated (size, type, no XML external entities); only already-public infrastructure locations are published.

## 11. Roles (skills)
`product-architect` (coordinator), `dataset-card`, `geo-method`, `asset-dossier`, `scientific-review`, `web-security`, `docs-bilingual`, `task-close`, `data-pipeline`, `devops`, `backend-api`, `map-frontend`, `contribution-review`. The Product Architect coordinates; no role overrides an ADR without a new ADR. Known traps go to `.agents/memory/` (index in `MEMORY.md`, one note per trap).
- **Documentation ownership (no dedicated docs agent):** each role updates its own artifacts; `task-close` updates `CHANGELOG.md`, `research/LOG.md` and `.agents/memory/` every task; `docs-bilingual` enforces EN/ES parity; `product-architect` owns `docs/foundation/PLATFORM.md` and `docs/methods/STATUS.md`, refreshed whenever a method's validation status or a Derived observation changes. CI runs `scripts/check_docs.py` to block drift (registry↔files, methods↔dashboard, Derived citations, bilingual orphans).

## 12. Conventions
- IDs: `DS-####` dataset · `AST-####` asset · `OBS-####` observation · `EVD-####` evidence · `ANM-####` anomaly · `ADR-###` decision · `CTR-####` contribution. Next ID = max existing + 1; check files/CSV before writing.
- Registry: `registry/datasets.csv`; dataset cards in `docs/datasets/DS-####.md`.
- CSV: UTF-8, comma, quoted fields. Dates ISO-8601. Coordinates EPSG:4326 unless stated.
- Raw, normalized and derived data never mix; `data/` is git-ignored (object storage later, ADR).

## 13. Independence
No Simple Map assets, brand, datasets, code or client information. No third-party proprietary content. External integrations use existing clients/adapters; read-only first. Design for provider migration.

## 14. Git
- One task = one commit; `CHANGELOG.md` and API docs updated in the same task that changes behavior.
- Commit trailer: `Assisted-by: <tool>` (e.g. `Assisted-by: Devin`). Never `Co-Authored-By` or `Generated with`.
- Enable hooks once per clone: `git config core.hooksPath .githooks` (secret scan + skill-name check). CI runs the full gate.
