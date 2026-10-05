---
name: contribution-review
description: Review community contributions to VEIO - license, evidence, method, location sensitivity; states Submitted/Under Review/Validated/Rejected/Superseded with history preserved. Active from Sprint 5.
argument-hint: "[CTR-####]"
---

Follow AGENTS.md §5, §6, §8. Status: stub — fully specified when Sprint 5 starts.

## Procedure (when activated)
1. Register the submission as `CTR-####` with: contributor, source, date, location, evidence, method, license, description. State starts at Submitted.
2. Verify: license permits the use; evidence supports the description; method is reproducible or clearly marked as an observation; location is not sensitive (else RESTRICTED).
3. Move through Under Review → Validated / Rejected / Superseded with reviewer, date and reason recorded. History is never silently deleted; superseded items stay linked.
4. Validated contributions enter the same provenance chain as institutional data, labelled as community-sourced.
5. Conflicts of interest declared by reviewers are recorded.

## Output
- Review record + state change; chat ≤6 lines. LOG entry via `task-close`.

## Checklist
- License verified; evidence checked; history preserved; no accusations or identifications.
