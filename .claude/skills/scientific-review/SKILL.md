---
name: scientific-review
description: Scientific and editorial review for VEIO - claims vs evidence, observation/interpretation separation, reproducibility, licensing gate; blocks unsupported statements.
argument-hint: "[file | PR | all-changed]"
---

Follow AGENTS.md (§2, §5, §6, §8).

## Procedure
1. Read the target (dossier, method note, brief, docs). For every factual claim: is there a cited source or a derived product with a manifest? Flag `[UNVERIFIED]` gaps.
2. Wording audit: find conclusions disguised as observations ("abandoned", "spill", "reactivated") and propose §2-compliant rewrites.
3. Evidence audit: are Low/Moderate/Strong categories used with reasons? Is any numeric "truth score" present (forbidden)?
4. Provenance audit: can each derived result be re-run from recorded inputs + parameters + versions?
5. Licensing audit: any new dataset without license/redistribution fields → block (DISPLAY ONLY/RESTRICTED).
6. Ethics audit: accusations, responsibility attribution, inferences about people, sensitive locations → block.
7. Report findings as a table: location, issue, severity (blocker/major/minor), suggested fix. Do not edit the author's content unless asked.

## Output
- Findings table in chat (≤10 lines) + optional `docs/reviews/<target>.md`. LOG entry via `task-close`.

## Checklist
- Zero unresolved blockers before merge; reproducibility confirmed or flagged.
