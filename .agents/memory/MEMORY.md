# Known traps — index

One Markdown note per trap in this folder; add a line here when a trap is discovered (see `task-close` skill). A trap is anything that cost time or caused a bug and is likely to recur.

- [Windows shell: PowerShell 5, no WSL bash](windows-shell-powershell.md) — use `shell_flavor: powershell`; chain with `;`, not `&&`.
- [FIRMS API: path, day-range and chunk-join quirks](firms-api-quirks.md) — `/api/area/csv/`; DAY_RANGE ≤5; join chunks with explicit newlines.
