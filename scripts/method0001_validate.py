"""METHOD-0001 validation — optical disturbance detection (VEIO).

Sentinel-2 L2A via Microsoft Planetary Computer (public STAC + signed
assets). For each AOI: median composites for pre/post event windows,
NDVI/NDBI change, disturbance share. Thresholds derived from control
AOIs (pre-registered in docs/methods/METHOD-0001.md).

Reference event: Cardon FCC restart 2025-05 (pre 2025-03..04,
post 2025-06..07). CRP halt 2024-09-17 (5-day) is out of scope for
optical composites — deviation documented in method note.

Outputs: data/derived/method-0001/ (CSV + JSON + manifest).
"""
import hashlib
import json
import os
import sys
from datetime import date
from pathlib import Path

import numpy as np

# PROJ conflict fix: system PATH exposes an old PostGIS proj.db; point PROJ
# at the data bundled with the rasterio wheel BEFORE importing rasterio.
_proj_dir = Path(sys.executable).parent / "Lib" / "site-packages" / "rasterio" / "proj_data"
if _proj_dir.exists():
    os.environ["PROJ_LIB"] = str(_proj_dir)
    os.environ["PROJ_DATA"] = str(_proj_dir)

import planetary_computer
import rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
from pystac_client import Client

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived" / "method-0001"

STAC = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
COLLECTION = "sentinel-2-l2a"
MAX_CLOUD = 30
HALF_KM = 0.03  # ~3 km box around AOI (deg, at ~11.5N)

AOIS = {
    "CRP_Amuay": (-70.171, 11.773),
    "CRP_Cardon": (-70.175, 11.841),
    "El_Palito": (-68.136, 10.452),
    "CTRL_Cariaco": (-64.33, 10.48),
    "CTRL_Chichiriviche": (-68.27, 11.45),
}
WINDOWS = {
    "pre": ("2025-03-01", "2025-04-30"),
    "post": ("2025-06-01", "2025-07-31"),
}


def bbox_for(lon, lat):
    return (lon - HALF_KM, lat - HALF_KM, lon + HALF_KM, lat + HALF_KM)


def composite(lon, lat, window):
    """Median NDVI/NDBI composites over AOI box for a date window."""
    search = STAC.search(
        collections=[COLLECTION],
        bbox=bbox_for(lon, lat),
        datetime=f"{window[0]}/{window[1]}",
        query={"eo:cloud_cover": {"lt": MAX_CLOUD}},
    )
    items = list(search.items())
    acc = {b: [] for b in ("B04", "B08", "B11")}
    used = 0
    for item in items:
        item = planetary_computer.sign(item)
        try:
            baseline = float(item.properties.get("s2:processing_baseline", "0"))
            offset = 1000.0 if baseline >= 4.0 else 0.0  # L2A BOA offset
            for b in acc:
                href = item.assets[b].href
                with rasterio.open(href) as src:
                    tb = transform_bounds("EPSG:4326", src.crs,
                                          *bbox_for(lon, lat), densify_pts=21)
                    win = from_bounds(*tb, transform=src.transform)
                    win = win.intersection(rasterio.windows.Window(
                        0, 0, src.width, src.height))
                    out_h, out_w = (320, 320) if b == "B11" else (640, 640)
                    arr = src.read(1, window=win,
                                   out_shape=(out_h, out_w)).astype("float32")
                    arr = (arr - offset) * 0.0001  # DN -> reflectance
                    if b == "B11":  # 20 m -> 10 m grid
                        arr = np.repeat(np.repeat(arr, 2, axis=0), 2, axis=1)
                    acc[b].append(arr)
            used += 1
        except Exception as e:  # noqa: BLE001 — skip unreadable scenes, log count
            print(f"  skip scene {item.id}: {type(e).__name__}")
    if used == 0:
        return None, 0
    med = {b: np.nanmedian(np.stack(acc[b]), axis=0) for b in acc}  # per-pixel
    return med, used


def indices(med):
    b04, b08, b11 = med["B04"], med["B08"], med["B11"]
    ndvi = (b08 - b04) / (b08 + b04 + 1e-6)
    ndbi = (b11 - b08) / (b11 + b08 + 1e-6)
    return ndvi, ndbi


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = {}
    comps = {}
    for name, (lon, lat) in AOIS.items():
        comps[name] = {}
        for wname, w in WINDOWS.items():
            med, n = composite(lon, lat, w)
            comps[name][wname] = med
            results.setdefault(name, {})[f"{wname}_scenes"] = n
            print(f"{name} {wname}: {n} scenes")

    # thresholds from controls: |change| mean + 2*std
    ctrl_deltas = []
    for name in ("CTRL_Cariaco", "CTRL_Chichiriviche"):
        if all(comps[name].get(w) for w in WINDOWS):
            n_pre, _ = indices(comps[name]["pre"])
            n_post, _ = indices(comps[name]["post"])
            ctrl_deltas.append(np.abs(n_post - n_pre))
    ctrl = np.concatenate([d.ravel() for d in ctrl_deltas]) if ctrl_deltas else None
    thr_ndvi = float(np.nanmean(ctrl) + 2 * np.nanstd(ctrl)) if ctrl is not None else 0.15
    thr_ndbi = thr_ndvi  # same scale heuristic, recorded in manifest

    rows = []
    for name in AOIS:
        if not all(comps[name].get(w) for w in WINDOWS):
            results[name]["status"] = "insufficient_scenes"
            continue
        pre_ndvi, pre_ndbi = indices(comps[name]["pre"])
        post_ndvi, post_ndbi = indices(comps[name]["post"])
        d_ndvi = post_ndvi - pre_ndvi
        d_ndbi = post_ndbi - pre_ndbi
        disturb = ((d_ndvi < -thr_ndvi) | (d_ndbi > thr_ndbi))
        results[name].update({
            "mean_ndvi_pre": float(np.nanmean(pre_ndvi)),
            "mean_ndvi_post": float(np.nanmean(post_ndvi)),
            "mean_ndbi_pre": float(np.nanmean(pre_ndbi)),
            "mean_ndbi_post": float(np.nanmean(post_ndbi)),
            "disturbed_pct": round(100 * float(disturb.mean()), 2),
        })
        rows.append({"aoi": name, "disturbed_pct": results[name]["disturbed_pct"],
                     "d_ndvi_mean": float(np.nanmean(d_ndvi)),
                     "d_ndbi_mean": float(np.nanmean(d_ndbi))})
        np.save(OUT / f"{name}_d_ndvi.npy", d_ndvi)

    import csv
    with (OUT / "aoi_stats.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["aoi", "disturbed_pct",
                                          "d_ndvi_mean", "d_ndbi_mean"])
        w.writeheader()
        w.writerows(rows)

    manifest = {
        "method": "METHOD-0001",
        "processing_version": "0.1.0",
        "run_date": str(date.today()),
        "inputs": {
            "stac": "planetarycomputer sentinel-2-l2a",
            "windows": WINDOWS,
            "aois": AOIS,
        },
        "parameters": {"max_cloud": MAX_CLOUD, "half_km": HALF_KM,
                       "thr_ndvi": thr_ndvi, "thr_ndbi": thr_ndbi,
                       "threshold_source": "controls mean+2std"},
        "outputs": ["aoi_stats.csv", "validation_results.json",
                    "per-AOI d_ndvi .npy"],
        "checksums": {p.name: hashlib.md5(p.read_bytes()).hexdigest()
                      for p in OUT.glob("*.csv")},
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2),
                                       encoding="utf-8")
    (OUT / "validation_results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
