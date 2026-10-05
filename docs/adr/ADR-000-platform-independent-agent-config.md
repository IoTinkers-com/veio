# ADR-000: Platform-independent agent configuration

**Status:** Accepted
**Date:** 2026-10-04

## Context
VEIO is developed with AI agents across at least three platforms (Devin, Claude Code, OpenCode). Each platform discovers rules and skills from different paths:
- Rules: Devin + OpenCode read `AGENTS.md`; Claude Code (as of 2026-10) reads only `CLAUDE.md` (AGENTS.md support is an open request, anthropics/claude-code#31005).
- Skills: Devin, Claude Code and OpenCode **all** read `.claude/skills/<name>/SKILL.md`. OpenCode also reads `.agents/skills/` and `.opencode/skills/`, but duplicate skill names across paths break its discovery. Symlinks are unreliable on Windows and Claude Code pollutes symlinked skill dirs with internal files.

## Decision
1. `AGENTS.md` is the single source of rules. `CLAUDE.md` contains exactly one line: `@AGENTS.md` (Claude Code import). No duplicated rule content anywhere.
2. All skills live only in `.claude/skills/<name>/SKILL.md` — the one path all three platforms read. No copies in `.agents/skills/` or `.devin/skills/`.
3. Skill frontmatter uses only the common subset: `name` (must equal the directory name), `description`, `argument-hint`. No `allowed-tools` (tool names differ per platform); skill bodies use generic action verbs, never platform tool names.
4. OpenCode slash-command wrappers live in `.opencode/commands/<name>.md` (only OpenCode reads them) and contain no logic — they load the matching skill.
5. Enforcement is platform-neutral: git `pre-commit` hook (`.githooks/`, enabled via `git config core.hooksPath .githooks`) + CI. No agent-specific hooks or subagent configs.
6. Session state is plain Markdown (`research/LOG.md`, `.agents/memory/`), readable by any tool.

## Consequences
- Positive: identical behavior across platforms; one place to update rules/skills; no duplicate-name breakage; enforcement works for humans too.
- Negative: `.claude/skills/` is Claude-Code-flavored until the open `.agents/skills/` standard is adopted by Claude Code; minor cosmetic mismatch.
- Neutral: when Claude Code supports `.agents/skills/`, migration is one `git mv` + ADR update.

## Alternatives considered
- Duplicate skills in `.agents/skills/` + `.claude/skills/`: rejected — OpenCode duplicate-name failure and drift risk.
- Symlink `.claude/skills` → `.agents/skills`: rejected — unreliable on Windows; Claude Code writes internal files into the target.
- Per-platform hooks/subagent configs: rejected — maintenance ×3, and enforcement belongs in git/CI anyway.
