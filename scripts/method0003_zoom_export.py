"""METHOD-0003 — native-resolution crop around the Lagunillas detection.

Exports every S1A descending (track 171) RTC VV scene as a small GeoTIFF at
native ~10 m resolution centred on the detected object, plus pre/post medians,
the change map and the detection point. For visual inspection in QGIS.

Output: data/derived/method-0003/v0.1/lagunillas_zoom/  (git-ignored)
Values: VV gamma0 in dB; nodata = NaN. CRS: native UTM zone of the RTC scene.

Usage: py -3 scripts/method0003_zoom_export.py
"""
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
from rasterio.windows import from_bounds  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived" / "method-0003" / "v0.1" / "lagunillas_zoom"
STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
TARGET = (-71.2703, 10.13715)
HALF_LON, HALF_LAT = 0.010, 0.009   # ~1.1 km x 1.0 km at this latitude
BOX = (TARGET[0] - HALF_LON, TARGET[1] - HALF_LAT, TARGET[0] + HALF_LON, TARGET[1] + HALF_LAT)
PRE_END = "2025-08-20"


def read_window_db(src, win):
    lin = src.read(1, window=win).astype("float64")
    lin[lin <= 0] = np.nan
    return (10 * np.log10(lin)).astype("float32")


def write(path, arr, transform, crs):
    profile = dict(driver="GTiff", height=arr.shape[0], width=arr.shape[1],
                   count=1, dtype="float32", crs=crs, transform=transform,
                   compress="deflate", nodata=np.nan)
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(arr, 1)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    c = Client.open(STAC_URL)
    items = list(c.search(collections=["sentinel-1-rtc"], bbox=BOX,
                          datetime="2025-06-01/2025-12-31").items())
    items = sorted([i for i in items if i.properties.get("sat:relative_orbit") == 171
                    and i.properties.get("sat:orbit_state") == "descending"
                    and i.properties.get("platform", "").lower() == "sentinel-1a"],
                   key=lambda i: i.datetime)
    print(f"{len(items)} scenes; box {BOX}")

    # reference geometry (same track/frame -> stable grid)
    with rasterio.open(planetary_computer.sign(items[0]).assets["vv"].href) as src:
        b = rasterio.warp.transform_bounds("EPSG:4326", src.crs, *BOX)
        win = from_bounds(*b, transform=src.transform)
        win = win.intersection(rasterio.windows.Window(0, 0, src.width, src.height))
        crs, ref_transform = src.crs, rasterio.windows.transform(win, src.transform)
        win_t = win.round_offsets().round_lengths()
        H, W = int(win_t.height), int(win_t.width)
    print(f"crop {W}x{H} px at ~10 m, CRS {crs}")

    pre, post, meta = [], [], []
    for it in items:
        it = planetary_computer.sign(it)
        with rasterio.open(it.assets["vv"].href) as src:
            w = from_bounds(*b, transform=src.transform).round_offsets().round_lengths()
            arr = read_window_db(src, w)
            tr = rasterio.windows.transform(w, src.transform)
        date = it.datetime.strftime("%Y-%m-%d")
        write(OUT / f"S1A_{date}_vv_db.tif", arr, tr, crs)
        (pre if date <= PRE_END else post).append(arr)
        meta.append((date, "pre" if date <= PRE_END else "post"))
        print(f"   {date} {'pre' if date <= PRE_END else 'post'} {arr.shape}")

    # common-grid composites (stack assumes identical grid per track)
    def stack_median(arrs):
        n = min(a.shape[0] for a in arrs), min(a.shape[1] for a in arrs)
        return np.nanmedian(np.stack([a[:n[0], :n[1]] for a in arrs]), axis=0)

    mp, ms = stack_median(pre), stack_median(post)
    write(OUT / "COMPOSITE_pre_median_db.tif", mp, ref_transform, crs)
    write(OUT / "COMPOSITE_post_median_db.tif", ms, ref_transform, crs)
    write(OUT / "COMPOSITE_change_post_minus_pre_db.tif", (ms - mp).astype("float32"),
          ref_transform, crs)
    write(OUT / "COMPOSITE_post_bright_frac.tif",
          np.nanmean(np.stack([(a[:mp.shape[0], :mp.shape[1]] >= -8).astype("float32")
                               for a in post]), axis=0), ref_transform, crs)

    (OUT / "detection_point.geojson").write_text(
        '{"type":"FeatureCollection","features":[{"type":"Feature","geometry":'
        '{"type":"Point","coordinates":[-71.2703,10.13715]},"properties":'
        '{"method":"METHOD-0003","pre_reg_passed":"b28e66c","first_bright":"2025-09-01",'
        '"pixels":4,"post_bright_frac":1.0,"pre_bright_frac":0.0}}]}', encoding="utf-8")
    (OUT / "README.txt").write_text(
        "METHOD-0003 v0.1 - Lagunillas detection zoom (native ~10 m Sentinel-1 RTC VV)\n"
        f"Centre -71.2703/10.13715, half-extent {HALF_LON} lon x {HALF_LAT} lat\n"
        "Files: S1A_<date>_vv_db.tif = per-scene VV gamma0 in dB (NaN = nodata);\n"
        "       COMPOSITE_*.tif = pre/post median, change and post brightness frequency;\n"
        "       detection_point.geojson = the detected object.\n"
        "Contains modified Copernicus Sentinel data 2025. Load in QGIS (native UTM).\n",
        encoding="utf-8")
    print(f"written to {OUT}")


if __name__ == "__main__":
    main()
