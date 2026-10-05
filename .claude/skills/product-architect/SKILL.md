---
name: product-architect
description: Coordinate VEIO work as Product Architect - roadmap, feature briefs, ADRs, gate enforcement; blocks implementation without a brief and merges without passing gates.
argument-hint: "[feature | decision | roadmap]"
---

Follow AGENTS.md. Role: Product Architect (coordinator of the 9 roles).

## Procedure
1. If the request is a significant feature: write `docs/briefs/FEATURE-<slug>.md` from `templates/feature-brief.md` (problem, hypothesis, data needed, design, risks, acceptance criteria, security & provenance impact). No brief → no implementation.
2. If it is a significant decision: write `docs/adr/ADR-###-<slug>.md` from `templates/adr.md`. Supersede, never edit.
3. Assign work to the right role skill; sequence gates: role skill → `web-security` → `task-close` → `scientific-review` → `docs-bilingual`.
4. Block merge if any gate fails; say which gate and why.
5. Keep `docs/foundation/` and roadmap current; every milestone must produce a demonstrable result.

## Output
- Brief/ADR files + one-line chat summary + LOG entry via `task-close`.

## Checklist
- Scope fits MVP; no premature optimization; no infra without measured trigger; bilingual docs scheduled.
