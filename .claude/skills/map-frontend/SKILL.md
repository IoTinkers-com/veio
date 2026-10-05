---
name: map-frontend
description: VEIO frontend and map engineering - layers, Asset Dossier UI, timeline, response-shape guards, accessibility, attribution display. Active from Sprint 2.
argument-hint: "[page | component | layer]"
---

Follow AGENTS.md §4, §10 and `docs/engineering-rules.md`. Status: stub — fully specified when Sprint 2 starts.

## Procedure (when activated)
1. Map layers always display dataset attribution and license (AGENTS.md §6); layer toggles mirror the access level of the underlying data.
2. Asset Dossier view: identity, location, sources, timeline of dated observations, changes, environmental observations, confidence and limitations — understandable in under five minutes without GIS knowledge.
3. After any fetch, validate the response shape before storing in state (error objects crash downstream `.filter()`); handle non-2xx explicitly.
4. No secrets, tokens or admin keys in client code; call the backend only.
5. Accessibility as part of the flow: keyboard navigation, contrast, alt text for imagery; UI language per product decision (likely Spanish-first with English toggle).

## Output
- Component code + tests; chat ≤6 lines. LOG entry via `task-close`.

## Checklist
- Attribution visible; shape guards present; a11y checks pass; no client secrets.
