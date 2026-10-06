---
name: docs-bilingual
description: Keep VEIO human-facing documentation bilingual - English X.md plus Spanish X.es.md with identical content; agent-facing files stay English-only.
argument-hint: "[file | all-changed]"
---

Follow AGENTS.md §4.

## Procedure
1. For every human-facing doc changed (README, GOVERNANCE, CONTRIBUTING, foundation, method status dashboard, dataset cards, method notes, asset dossiers): ensure the `.es.md` twin exists and matches the English version section by section.
2. Translate faithfully; keep technical terms, IDs (DS-####, AST-####) and code identifiers in English. Do not localize URLs or file names.
3. Run the executive style on both versions: bottom line first, bullets/tables, no marketing language.
4. If content diverges, fix both; never let the Spanish copy lag more than one commit.
5. Agent-facing files (AGENTS.md, skills, templates, CI) are English-only — do not translate them.

## Output
- Updated EN/ES pairs; chat: list of files touched. LOG entry via `task-close`.

## Checklist
- Every changed human doc has its .es.md twin updated in the same commit.
