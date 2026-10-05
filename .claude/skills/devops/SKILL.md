---
name: devops
description: VEIO infrastructure and CI/CD - quality gate in CI, pre-commit, non-root containers, branch protection, backups, scalability triggers. Active from Sprint 1.
argument-hint: "[ci | container | deploy | backup]"
---

Follow AGENTS.md §10 and `docs/architecture/scalability.md`. Status: stub — fully specified when Sprint 1 starts.

## Procedure (when activated)
1. CI mirrors the local gate in the same order (typecheck → lint → test → build) plus gitleaks and skill-name check; `permissions: read-all` on workflows.
2. Containers: multi-stage, non-root user, dev ports bound to 127.0.0.1, `.dockerignore` (`.git`, `.env`, `data/`, caches).
3. No infrastructure without a measured trigger from the scalability table; document each addition in an ADR.
4. Backups and restore tested before any real data; retention documented in `docs/security.md`.
5. Branch protection on `main`: required CI, no force push; secret scanning enabled.

## Output
- Config files + ADR if architecture changed; chat ≤6 lines. LOG entry via `task-close`.

## Checklist
- Gate order matches locally and in CI; containers non-root; triggers documented.
