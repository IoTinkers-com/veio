# EMIT CH4 on LP DAAC: links, units and coverage

Date: 2026-10-05 · Tool: devin · Repo: veio

Using EMIT methane enhancement (DS-0014) for an asset zoom:

1. **Two products.** `EMITL2BCH4ENH` (per-pixel methane enhancement, 60 m)
   and `EMITL2BCH4PLM` (estimated plume complexes). Plumes are only a
   subset; a box can have ENH granules and **zero** PLM granules.
2. **ENH is a GeoTIFF COG** (not netCDF), 1 band, `float32`,
   nodata **-9999**, units **ppm·m** (total vertical column enhancement,
   matched filter). V002 (DOI 10.5067/EMIT/EMITL2BCH4ENH.002) adds
   uncertainty and sensitivity bands in the same granule.
3. **CMR links can be `s3://`.** Some granules return
   `s3://lp-prod-protected/...`; convert to
   `https://data.lpdaac.earthdatacloud.nasa.gov/<bucket>/<key>` and send
   the EDL bearer token (`.secrets/edl_token.txt`).
4. **Sparse valid coverage.** EMIT is a narrow ISS swath; per-granule
   valid fraction can be <20% and varies by date. The same scene often has
   two granules (…003/…004); pick by valid fraction over the target box,
   not by bounding box.
5. **Do not over-read absolute values.** The broad background can be
   regional bias / retrieval artefacts; use the sensitivity band to
   correct, and report max percentiles with caveats — no emission rate.

Fix: see `scripts/emit_ch4_pick.py`, `scripts/emit_ch4_export.py`.
