# Contributing — VEIO

Thanks for interest in an open observatory of Venezuela's energy infrastructure. This guide gets you productive in ~10 minutes.

## Setup
```bash
git clone https://github.com/IoTinkers-com/veio && cd veio
git config core.hooksPath .githooks   # enables secret scan + skill-name check
```
No runtime dependencies yet (Sprint 0). CI runs secret scanning and doc checks.

## How work happens
1. **Pick or propose a task.** Significant features need a feature brief (`templates/feature-brief.md`) written by the Product Architect before implementation.
2. **One task = one commit.** Update `CHANGELOG.md` (and API docs when they exist) in the same commit.
3. **Quality gate before closing:** typecheck → lint → test → build (stages activate as the stack grows; Sprint 0 = docs + secret scan).
4. **Reviews:** scientific-review (claims vs evidence) and web-security (when code) must pass before merge.
5. **Bilingual docs:** human-facing docs exist as `X.md` (EN) + `X.es.md` (ES), updated in the same commit.

## Rules you must know
- Read `AGENTS.md` — it binds humans and agents alike. Highlights: DATA → PROCESSING → OBSERVATION → INTERPRETATION never merge; no invented datasets/licenses; licensing gate (unclear redistribution → DISPLAY ONLY/RESTRICTED); no accusations or unverified claims; only already-public infrastructure locations are published.
- Engineering rules: `docs/engineering-rules.md` (each rule has a check). Security: `docs/security.md`.
- Decisions: one ADR per decision (`docs/adr/`); supersede, never edit.
- Known traps: `.agents/memory/` — add a note when you discover one.

## Contributing observations/evidence (from Sprint 5)
Submissions include: contributor, source, date, location, evidence, method, license, description. Workflow: Submitted → Under Review → Validated / Rejected / Superseded, with history preserved. See `docs/governance` and the `contribution-review` skill.

## Commit style
Imperative message; trailer `Assisted-by: <tool>` when an AI agent did the work (e.g. `Assisted-by: Devin`). Never `Co-Authored-By` or `Generated with`.

## Conduct
See `CODE_OF_CONDUCT.md`. Report security issues privately (see `SECURITY.md`).
