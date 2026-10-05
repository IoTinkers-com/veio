"""Santa Barbara (AST-0012) flaring/CH4 zoom export for QGIS.

Around the densest FIRMS flare cell:
  - Sentinel-1 RTC VV per-scene native (~10 m) crops + median composite;
  - a wider S1 median context composite (~33 m, EPSG:4326);
  - Sentinel-2 L2A true-colour crops (~10 m) for the least-cloudy scenes;
  - FIRMS hotspot and OGIM flaring detection point layers.
Output under data/derived/asset-zoom/AST-0012-santa-barbara/.

Usage: py -3 scripts/santabarbara_zoom_export.py
"""
import csv
import json
import os
from pathlib import Path

import numpy as np

_proj = Path(os.sys.executable).parent / "Lib" / "site-packages" / "rasterio" / "proj_data"
if _proj.exists():
    os.environ["PROJ_LIB"] = str(_proj)
    os.environ["PROJ_DATA"] = str(_proj)
os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
os.environ.setdefault("GDAL_HTTP_MULTIRANGE", "YES")

import planetary_computer  # noqa: E402
import rasterio  # noqa: E402
import rasterio.warp  # noqa: E402
from pystac_client import Client  # noqa: E402
from rasterio.enums import Resampling  # noqa: E402
from rasterio.transform import from_origin  # noqa: E402
from rasterio.vrt import WarpedVRT  # noqa: E402
from rasterio.windows import from_bounds  # noqa: E402
from rasterio.windows import transform as win_transform  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived" / "asset-zoom" / "AST-0012-santa-barbara"
STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
FIRMS = ROOT / "data" / "derived" / "method-0002" / "firms_ve_hotspots.csv"
OGIM = ROOT / "data" / "ogim_venezuela" / "Natural_Gas_Flaring_Detections.csv"
BOX_WIDE = (-63.80, 9.50, -63.52, 9.78)
BOX_CTX = (-63.78, 9.53, -63.55, 9.73)
SAR_PERIOD = ("2026-08-01", "2026-10-05")
SAR_HALF = (0.012, 0.011)
CTX_RES = 0.0003
OPT_HALF = (0.014, 0.013)


def densest_cell():
    from collections import Counter
    with FIRMS.open(encoding="utf-8") as fh:
        cells = Counter((round(float(r["longitude"]), 2), round(float(r["latitude"]), 2))
                        for r in csv.DictReader(fh)
                        if BOX_WIDE[0] <= float(r["longitude"]) <= BOX_WIDE[2]
                        and BOX_WIDE[1] <= float(r["latitude"]) <= BOX_WIDE[3])
    top = cells.most_common(1)[0]
    print(f"densest FIRMS cell: {top[0]} ({top[1]} hotspots)")
    return top[0]


def write(path, arr, transform, crs, dtype="float32", nodata=np.nan):
    arr = np.atleast_3d(arr)
    if arr.shape[0] not in (1, 3, 4) and arr.shape[2] in (1, 3, 4):
        arr = np.moveaxis(arr, 2, 0)
    profile = dict(driver="GTiff", height=arr.shape[1], width=arr.shape[2],
                   count=arr.shape[0], dtype=dtype, crs=crs, transform=transform,
                   compress="deflate", nodata=nodata)
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(arr.astype(dtype))


def s1_items():
    c = Client.open(STAC_URL)
    items = list(c.search(collections=["sentinel-1-rtc"], bbox=BOX_WIDE,
                          datetime="/".join(SAR_PERIOD)).items())
    sel = sorted([i for i in items if i.properties.get("sat:relative_orbit") == 62
                  and i.properties.get("sat:orbit_state") == "ascending"],
                 key=lambda i: i.datetime)
    return [planetary_computer.sign(i) for i in sel]


def read_db(src, win):
    lin = src.read(1, window=win).astype("float64")
    lin[lin <= 0] = np.nan
    return (10 * np.log10(lin)).astype("float32")


def do_sar(lon, lat):
    (OUT / "sar").mkdir(parents=True, exist_ok=True)
    (OUT / "sar_context").mkdir(parents=True, exist_ok=True)
    box = (lon - SAR_HALF[0], lat - SAR_HALF[1], lon + SAR_HALF[0], lat + SAR_HALF[1])
    items = s1_items()
    print(f"SAR: {len(items)} ascending track-62 scenes")
    crops, ctxs, ref = [], [], {}
    transform_ctx = from_origin(BOX_CTX[0], BOX_CTX[3], CTX_RES, CTX_RES)
    wctx = int(round((BOX_CTX[2] - BOX_CTX[0]) / CTX_RES))
    hctx = int(round((BOX_CTX[3] - BOX_CTX[1]) / CTX_RES))
    for it in items:
        href = it.assets["vv"].href
        with rasterio.open(href) as src:
            b = rasterio.warp.transform_bounds("EPSG:4326", src.crs, *box)
            w = from_bounds(*b, transform=src.transform).round_offsets().round_lengths()
            arr = read_db(src, w)
            tr = win_transform(w, src.transform)
            if not ref:
                ref = {"crs": src.crs, "transform": tr}
        date = it.datetime.strftime("%Y-%m-%d")
        write(OUT / "sar" / f"S1_{date}_vv_db.tif", arr, tr, ref["crs"])
        crops.append(arr)
        with rasterio.open(href) as src:
            with WarpedVRT(src, crs="EPSG:4326", transform=transform_ctx, width=wctx,
                           height=hctx, resampling=Resampling.average,
                           src_nodata=-32768, nodata=-32768) as vrt:
                lin = vrt.read(1).astype("float64")
        lin[lin <= 0] = np.nan
        ctxs.append((10 * np.log10(lin)).astype("float32"))
        print(f"   {date} crop={arr.shape} ctx={ctxs[-1].shape}")
    write(OUT / "sar" / "COMPOSITE_median_db.tif", np.nanmedian(np.stack(crops), axis=0),
          ref["transform"], ref["crs"])
    n = min(a.shape[0] for a in ctxs), min(a.shape[1] for a in ctxs)
    write(OUT / "sar_context" / "S1_median_context_db.tif",
          np.nanmedian(np.stack([a[:n[0], :n[1]] for a in ctxs]), axis=0),
          transform_ctx, "EPSG:4326")
    print("   composites written")


def do_optical(lon, lat):
    (OUT / "optical").mkdir(parents=True, exist_ok=True)
    c = Client.open(STAC_URL)
    items = [i for i in c.search(collections=["sentinel-2-l2a"], bbox=BOX_WIDE,
                                 datetime="/".join(SAR_PERIOD),
                                 query={"eo:cloud_cover": {"lt": 60}}).items()]
    items = sorted(items, key=lambda i: i.properties.get("eo:cloud_cover", 100))[:2]
    box = (lon - OPT_HALF[0], lat - OPT_HALF[1], lon + OPT_HALF[0], lat + OPT_HALF[1])
    for it in items:
        it = planetary_computer.sign(it)
        bands, tr, crs = {}, None, None
        for name in ("B04", "B03", "B02"):
            with rasterio.open(it.assets[name].href) as s2:
                b = rasterio.warp.transform_bounds("EPSG:4326", s2.crs, *box)
                w = from_bounds(*b, transform=s2.transform).round_offsets().round_lengths()
                if tr is None:
                    tr, crs = win_transform(w, s2.transform), s2.crs
                bands[name] = s2.read(1, window=w).astype("float32")
        base = float(it.properties.get("s2:processing_baseline", "0") or 0)
        off = 1000.0 if base >= 4.0 else 0.0
        rgb = np.dstack([(bands[k] - off) * 0.0001 for k in ("B04", "B03", "B02")])
        date = it.datetime.strftime("%Y-%m-%d")
        write(OUT / "optical" / f"S2_{date}_rgb.tif", rgb, tr, crs)
        lo = np.nanpercentile(rgb.reshape(-1, 3), 2, axis=0)
        hi = np.nanpercentile(rgb.reshape(-1, 3), 98, axis=0)
        u8 = np.nan_to_num(np.clip((rgb - lo) / np.maximum(hi - lo, 1e-6), 0, 1) * 255).astype("uint8")
        write(OUT / "optical" / f"S2_{date}_rgb_u8.tif", u8, tr, crs, "uint8", 0)
        print(f"   optical {date} cloud={it.properties.get('eo:cloud_cover')}")


def do_points():
    (OUT / "flaring").mkdir(parents=True, exist_ok=True)

    def inbox(lo, la):
        return BOX_WIDE[0] <= lo <= BOX_WIDE[2] and BOX_WIDE[1] <= la <= BOX_WIDE[3]

    feats = []
    with FIRMS.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if inbox(float(r["longitude"]), float(r["latitude"])):
                feats.append({"type": "Feature",
                              "geometry": {"type": "Point",
                                           "coordinates": [float(r["longitude"]), float(r["latitude"])]},
                              "properties": {"date": r["acq_date"], "sat": r["satellite"],
                                             "frp": float(r["frp"] or 0)}})
    (OUT / "flaring" / "FIRMS_hotspots.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": feats}), encoding="utf-8")
    print(f"   FIRMS points: {len(feats)}")
    feats = []
    with OGIM.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if inbox(float(r["lon"]), float(r["lat"])):
                feats.append({"type": "Feature",
                              "geometry": {"type": "Point",
                                           "coordinates": [float(r["lon"]), float(r["lat"])]},
                              "properties": {"name": r["FAC_NAME"], "src_date": r["SRC_DATE"]}})
    (OUT / "flaring" / "OGIM_flaring.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": feats}), encoding="utf-8")
    print(f"   OGIM points: {len(feats)}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lon, lat = densest_cell()
    do_points()
    do_sar(lon, lat)
    do_optical(lon, lat)
    (OUT / "README.txt").write_text(
        "AST-0012 Santa Barbara - flaring zoom (QGIS)\n"
        f"Centro del maximo FIRMS: {lon}/{lat}; caja amplia {BOX_WIDE}\n"
        "sar/          S1 RTC VV por escena (dB, nativo ~10 m) + COMPOSITE_median_db.tif\n"
        "sar_context/  S1 mediana contexto (~33 m, EPSG:4326)\n"
        "optical/      S2 L2A color verdadero (~10 m), escenas menos nubladas\n"
        "flaring/      FIRMS_hotspots.geojson (2026-09-04..10-03) + OGIM_flaring.geojson\n"
        "NaN = nodata. Contains modified Copernicus Sentinel data 2026.\n"
        "NASA FIRMS hotspots; OGIM v3.0 flaring detections.\n", encoding="utf-8")
    print(f"written to {OUT}")


if __name__ == "__main__":
    main()
