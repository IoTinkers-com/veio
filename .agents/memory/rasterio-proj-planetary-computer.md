# Rasterio/PROJ + Planetary Computer quirks on this machine

Date: 2026-10-04 · Tool: devin · Repo: veio

Four issues cost several debug iterations in METHOD-0001:

1. **PROJ conflict:** system PATH exposes an old PostGIS `proj.db`
   (`C:\PostgreSQL\15\share\contrib\postgis-3.3\proj\proj.db`); rasterio's
   PROJ picks it up → `CRSError: The EPSG code is unknown`. Fix: set
   `PROJ_LIB`/`PROJ_DATA` to `<python>\Lib\site-packages\rasterio\proj_data`
   BEFORE importing rasterio (see `scripts/method0001_validate.py`).
2. **CRS mismatch:** `from_bounds` needs coordinates in the raster's CRS
   (UTM metres), not EPSG:4326 — transform the bbox first with
   `rasterio.warp.transform_bounds`.
3. **Window shapes differ per tile/zone:** stack fails. Fix: read with
   fixed `out_shape` (rasterio resamples on read).
4. **S2 L2A offset:** processing baseline ≥04.00 needs (DN-1000)*0.0001;
   B11 is 20 m — upsample ×2 or read at out_shape matching the 10 m grid.

**Fix:** see `scripts/method0001_validate.py`.
