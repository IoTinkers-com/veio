# Sentinel-1 on Planetary Computer: use RTC, not GRD

Date: 2026-10-05 · Tool: devin · Repo: veio

Issues found while building METHOD-0003 (SAR):

1. **GRD assets are not analysis-ready.** In the `sentinel-1-grd`
   collection, the `vv`/`vh` COGs have **no CRS** (`src.crs is None`,
   identity transform, raw radar pixel indices). Calibration/geocoding
   live in the separate `schema-*` assets. Reading them with `WarpedVRT`
   fails (`CRSError`/`WindowError`).
2. **Use `sentinel-1-rtc` instead.** RTC (Microsoft) is gamma0, float32,
   one UTM zone per scene, nodata `-32768`, **water is not masked**
   (unlike some RTC products) — directly usable for time series.
   Convert to dB: `10*log10(v)` with `v>0`.
3. **File size ~2 GB/scene.** Windowed reads via `rasterio`/GDAL from the
   remote COG take ~10–20 s per scene; cache per-scene grids to `.npy`.
4. **Platform property case varies** (`SENTINEL-1A` vs `sentinel-1a`):
   compare `str(...).lower()`.
5. **Track selection.** For the lake, S1A **descending relative orbit 171**
   gave a consistent 12-day series (18 scenes Jun–Dec 2025); S1C is offset
   6 days. Keep one platform+track to avoid geometry/radiometry mixing.
   RTC item id date is `id.split("_")[5]`.
6. **Open-water vs nearshore:** a strict open-water neighbourhood test
   (>=90% water in ~230 m) removes legitimate nearshore lake targets;
   report the water fraction instead of gating on it when the AOI is
   a nearshore terminal.

Fix: see `scripts/method0003_validate.py`.
