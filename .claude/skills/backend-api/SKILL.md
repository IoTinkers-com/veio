---
name: backend-api
description: VEIO backend engineering - API endpoints with schema validation, single authZ choke point, spatial bounds, route ordering, documented public API. Active from Sprint 2.
argument-hint: "[endpoint | schema | query]"
---

Follow AGENTS.md §10 and `docs/engineering-rules.md`. Status: stub — fully specified when Sprint 2 starts.

## Procedure (when activated)
1. Every input schema-validated before touching the database: max_length on strings, bounded pagination, numeric ranges, plus spatial bounds (bbox area cap, feature-count cap, geometry vertex cap).
2. Authorization only through the single choke-point module enforcing PUBLIC/RESEARCH/RESTRICTED; grep must show no other access checks. Negative tests per boundary in the same change.
3. RESTRICTED fields never appear in public response schemas — separate response models per level.
4. Literal routes registered before parametric routes; no sandbox/zombie endpoints in production builds.
5. Public read API is documented and open; admin/review endpoints excluded from public docs. Errors: generic messages, details logged server-side only.

## Output
- Endpoint code + tests + API docs; chat ≤6 lines. LOG entry via `task-close`.

## Checklist
- Bounds enforced; choke point grep clean; negative tests pass; no PII/sensitive locations in public responses.
