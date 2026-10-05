# FIRMS API: path, day-range and chunk-join quirks

Date: 2026-10-04 · Tool: devin · Repo: veio

Three quirks cost three debug iterations in METHOD-0002:

1. **Path** is `/api/area/csv/` (slash-separated), not `/api/area_csv/` — the latter returns HTTP 400 "Invalid API call".
2. **DAY_RANGE is 1..5 per request**; longer windows need repeated calls with a start DATE (`/api/area/csv/KEY/SOURCE/BBOX/5/YYYY-MM-DD`), then concatenate.
3. **Chunk concatenation**: API responses may lack trailing newlines — join with explicit `"\n"` per part or pandas glues the last data row of one chunk to the next chunk's header (mixed-width rows, object dtype). Repeated header lines also appear when reading the joined file with a single `read_csv` — filter rows where the first column equals the header name.

**Fix:** see `scripts/method0002_validate.py` (`fetch_firms`, `write_manifest`).
