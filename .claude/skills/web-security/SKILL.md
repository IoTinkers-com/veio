---
name: web-security
description: Security review for VEIO web code against docs/security.md and docs/engineering-rules.md - authZ choke point, input and spatial bounds, uploads, headers, secrets, RESTRICTED leakage.
argument-hint: "[file | PR | design]"
---

Follow AGENTS.md §10 and `docs/security.md`.

## Procedure
1. Design review (before code): does the brief state the access level (PUBLIC/RESEARCH/RESTRICTED) of every endpoint and field? Is RESTRICTED data reachable from any public path?
2. Code review checklist:
   - Authorization only via the single choke-point module (grep-verified); no per-route re-implementation.
   - Every input schema-validated: max_length, bounded pagination, spatial bounds (bbox area, feature count, vertex count).
   - Uploads: size cap, content-type sniffing, no XML external entities (KML), no server-side execution.
   - No secrets in frontend; admin keys header-only, constant-time compare, no default value.
   - Security headers (CSP, X-Frame-Options, nosniff, Referrer-Policy), rate limits on auth/write/tile endpoints, generic 5xx.
   - Indexes (incl. GIST) added in the same migration as any new queried column.
   - Negative tests exist for each access-level boundary (anonymous → RESTRICTED, contributor → admin, cross-tenant).
3. Report findings: location, issue, severity (blocker/major/minor), fix. Blockers prevent merge.

## Output
- Findings table (≤10 lines in chat) + notes appended to the PR/brief. LOG entry via `task-close`.

## Checklist
- Zero blockers; negative tests listed; no new secret strings (gitleaks clean).
