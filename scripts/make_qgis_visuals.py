"""Generate QGIS-ready visuals from VEIO derived data.

Outputs to data/derived/qgis_visuals/ (git-ignored):
  - GeoJSON layers (EPSG:4326): assets, ogim_refineries, ogim_terminals,
    ogim_flaring_2026-09-14, firms_hotspots_30d, ogim_wells
  - GeoTIFF: vnp46_2025-08_ve.tif (Black Marble radiance mosaic),
    crp_d_ndvi_*.tif (METHOD-0001 pilot NDVI change)
Load in QGIS via drag & drop or Layer > Add Layer.
"""
import csv
import json
import os
import sys
from pathlib import Path

import numpy as np

# PROJ conflict fix (see .agents/memory/rasterio-proj-planetary-computer.md)
_proj_dir = Path(sys.executable).parent / "Lib" / "site-packages" / "rasterio" / "proj_data"
if _proj_dir.exists():
    os.environ["PROJ_LIB"] = str(_proj_dir)
    os.environ["PROJ_DATA"] = str(_proj_dir)

import rasterio
from rasterio.transform import from_origin

ROOT = Path(__file__).resolve().parents[1]
OGIM = ROOT / "data" / "ogim_venezuela"
M2 = ROOT / "data" / "derived" / "method-0002"
M1 = ROOT / "data" / "derived" / "method-0001"
OUT = ROOT / "data" / "derived" / "qgis_visuals"


def geojson(points, fields, path):
    feats = []
    for row in points:
        props = {f: row.get(f) for f in fields}
        feats.append({
            "type": "Feature",
            "geometry": {"type": "Point",
                         "coordinates": [float(row["lon"]), float(row["lat"])]},
            "properties": props,
        })
    fc = {"type": "FeatureCollection", "features": feats}
    path.write_text(json.dumps(fc), encoding="utf-8")
    print(f"{path.name}: {len(feats)} features")


def ogim_layer(src, fields, name):
    with (OGIM / src).open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    geojson(rows, fields, OUT / f"{name}.geojson")
    return len(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # vectors from OGIM (DS-0012)
    ogim_layer("Crude_Oil_Refineries.csv",
               ["FAC_NAME", "FAC_TYPE", "STATE_PROV", "SRC_DATE"],
               "ogim_refineries")
    ogim_layer("Petroleum_Terminals.csv",
               ["FAC_TYPE", "STATE_PROV", "SRC_DATE"], "ogim_terminals")
    ogim_layer("Natural_Gas_Flaring_Detections.csv",
               ["FAC_NAME", "FAC_TYPE", "SRC_DATE"],
               "ogim_flaring_2026-09-14")
    ogim_layer("Oil_and_Natural_Gas_Wells.csv",
               ["FAC_NAME", "FAC_TYPE", "FAC_STATUS", "STATE_PROV", "SRC_DATE"],
               "ogim_wells")

    # FIRMS hotspots (METHOD-0002)
    with (M2 / "firms_ve_hotspots.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["lon"], r["lat"] = r["longitude"], r["latitude"]
    fields = ["acq_date", "satellite", "confidence", "frp", "daynight"]
    geojson(rows, fields, OUT / "firms_hotspots_30d.geojson")

    # asset registry points
    with (ROOT / "registry" / "assets.csv").open(encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r.get("lon")]
    for r in rows:
        r["name"] = r.pop("name")
    geojson(rows, ["name", "type", "state", "status"], OUT / "veio_assets.geojson")

    # VNP46A3 mosaic 2025-08 (tiles h10v07, h11v07, h11v08)
    raw = ROOT / "data" / "raw" / "vnp46"
    tiles = sorted(raw.glob("VNP46A3.A2025213.*.h5"))
    if tiles:
        rasters = []
        for t in tiles:
            import h5py
            import re
            with h5py.File(t, "r") as f:
                d = f["HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/NearNadir_Composite_Snow_Free"][:]
            d = np.where(d < 0, np.nan, d.astype("float32"))
            m = re.search(r"h(\d+)v(\d+)", t.name)
            h, v = int(m.group(1)), int(m.group(2))
            lon0 = -180 + h * 10
            lat_top = 20 + (7 - v) * 10
            tr = from_origin(lon0, lat_top, 10 / 2400, 10 / 2400)
            rasters.append((d, tr))
        res = 10 / 2400  # deg per px
        canvas = np.full((4800, 4800), np.nan, dtype="float32")
        for d, tr in rasters:
            lon0 = tr.c; lat_top = tr.f  # from_origin(f, c) -> .f=lat_top, .c=lon0
            col = int((lon0 + 80) / res)
            row = int((20 - lat_top) / res)
            canvas[row:row + 2400, col:col + 2400] = d
        transform = from_origin(-80, 20, res, res)
        mosaic = canvas[np.newaxis, :, :]
        profile = dict(driver="GTiff", height=mosaic.shape[1],
                       width=mosaic.shape[2], count=1, dtype="float32",
                       crs="EPSG:4326", transform=transform,
                       nodata=np.nan)
        tif = OUT / "vnp46_2025-08_ve.tif"
        with rasterio.open(tif, "w", **profile) as dst:
            dst.write(mosaic.astype("float32"))
        print(f"{tif.name}: {mosaic.shape} written")

    # NDVI change rasters from METHOD-0001 pilot (skip 0-d scalar arrays)
    for npy in sorted(M1.glob("*_d_ndvi.npy")):
        aoi = npy.name.replace("_d_ndvi.npy", "")
        arr = np.load(npy)
        if arr.ndim < 2:
            print(f"{npy.name}: scalar (v0.1.0 pilot bug) — skipped")
            continue
        lon, lat = {"CRP_Amuay": (-70.171, 11.773),
                    "CRP_Cardon": (-70.175, 11.841)}[aoi]
        tr = from_origin(lon - 0.03, lat + 0.03, 0.06 / arr.shape[1],
                         0.06 / arr.shape[0])
        profile = dict(driver="GTiff", height=arr.shape[0],
                       width=arr.shape[1], count=1, dtype="float32",
                       crs="EPSG:4326", transform=tr, nodata=np.nan)
        tif = OUT / f"{aoi}_d_ndvi.tif"
        with rasterio.open(tif, "w", **profile) as dst:
            dst.write(arr.astype("float32"))
        print(f"{tif.name}: {arr.shape} written")


if __name__ == "__main__":
    main()
