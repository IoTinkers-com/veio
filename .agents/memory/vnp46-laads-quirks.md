# VNP46/LAADS: tile convention and access quirks

Date: 2026-10-04 · Tool: devin · Repo: veio

Five issues cost several debug iterations in METHOD-0004:

1. **LAADS archive listings are JS-rendered** — no .h5 links in the HTML.
   Resolve granule URLs via CMR instead:
   `cmr.earthdata.nasa.gov/search/granules.echo10?short_name=VNP46A3&temporal=...&bounding_box=...`;
   download URLs point to `data.laadsdaac.earthdatacloud.nasa.gov` (Bearer token).
2. **CMR returns `s3://` URLs too** — filter to `https://`.
3. **VNP46 tile convention differs from MODIS**: h00 exists, so
   `lon0 = -180 + h*10` (h11 = -70..-60), and v07 = 10..20N
   (`lat_top = 20 + (7-v)*10`). Verify against file attrs
   (WestBoundingCoord / NorthBoundingCoord) — a 1-tile offset puts AOIs
   in the ocean and returns silent 0.0 radiance.
4. **VNP46A3 monthly SDS** is `HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/`
   (space in "Data Fields"); no GridLat/GridLon datasets; monthly radiance
   SDS is `NearNadir_Composite_Snow_Free`; fill values are negative.
5. Monthly granule filename DOY = month start (A2025213 = Aug 1) but CMR
   temporal search also returns adjacent months — filter by filename DOY.

**Fix:** see `scripts/method0004_validate.py`.
