---
name: task-close
description: End-of-task harness for any VEIO role - runs the quality gate, updates CHANGELOG and docs, records known traps and the session LOG, makes one commit with the Assisted-by trailer.
argument-hint: "[summary of the task]"
---

Follow AGENTS.md §9, §11, §14.

## Procedure
1. Quality gate, in this fixed order, before closing: typecheck → lint → test → build (commands per current stack; skip stages that do not exist yet and say so). All must pass. The docs gate includes `scripts/check_docs.py` (drift check).
2. Update in the same commit: `CHANGELOG.md` (if behavior/docs changed), API docs (if endpoints changed), `.agents/memory/` (new trap discovered → one note + MEMORY.md index line).
3. If a method's **validation status** or a **Derived observation** changed: update `docs/methods/STATUS.md` **and** `STATUS.es.md` (and `docs/foundation/PLATFORM.md`/`.es.md` if the method set changed). Run `scripts/check_docs.py`; it must pass.
4. Append `research/LOG.md` entry (≤6 lines: date, tool/model, changes, open items, next step).
5. Stage exactly the files of this task; one commit; message imperative, trailer `Assisted-by: <tool>` (never Co-Authored-By / Generated with). Push if the user asked or the session is ending.
6. If the gate fails: fix or report blockers — never commit red.

## Output
- Commit hash + gate result in chat (≤4 lines).

## Checklist
- Gate green (incl. `scripts/check_docs.py`); STATUS/PLATFORM refreshed if a method changed; LOG and memory updated; single commit; trailer correct; no secrets staged (gitleaks via pre-commit).
