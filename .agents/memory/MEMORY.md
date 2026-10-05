# Known traps — index

One Markdown note per trap in this folder; add a line here when a trap is discovered (see `task-close` skill). A trap is anything that cost time or caused a bug and is likely to recur.

- [Windows shell: PowerShell 5, no WSL bash](windows-shell-powershell.md) — use `shell_flavor: powershell`; chain with `;`, not `&&`.
- [FIRMS API: path, day-range and chunk-join quirks](firms-api-quirks.md) — `/api/area/csv/`; DAY_RANGE ≤5; join chunks with explicit newlines.
- [Rasterio/PROJ + Planetary Computer quirks](rasterio-proj-planetary-computer.md) — PROJ_LIB to wheel's proj_data; transform bbox to raster CRS; fixed out_shape; S2 L2A offset.
- [AOI coordinates: OGIM terminal records are offshore loading points](aoi-coordinate-verification.md) — verify AOIs against OSM + ON_OFFSHORE before any method run.
- [VNP46/LAADS: tile convention and access quirks](vnp46-laads-quirks.md) — CMR for URLs; h00 exists (lon0=-180+h*10); v07=10..20N; SDS path with space; filter s3:// links.
