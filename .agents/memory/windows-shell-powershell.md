# Windows shell: PowerShell 5, no WSL bash

Date: 2026-10-04 · Tool: devin

On this Windows machine the default bash session fails (WSL cannot translate paths, `getpwuid` errors) and Windows PowerShell 5 rejects `&&` as a command separator.

**Trap:** shell commands fail or misparse when assuming bash or modern PowerShell syntax.

**Fix:** start shells with `shell_flavor: "powershell"` and chain commands with `;` instead of `&&`.
