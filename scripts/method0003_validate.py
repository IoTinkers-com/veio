"""METHOD-0003 v0.1 — Sentinel-1 RTC: new persistent radar-bright objects.

Pre-registered in docs/methods/METHOD-0003.md before execution.

Design:
  T-Alula (positive): Lagunillas lake/terminal box — the reported Sep-2025
    jack-up arrival ("Alula", CCRC, Reuters) should appear as a NEW radar
    object that persists. Qualifies if bright (VV gamma0 >= BRIGHT_DB) in
    >= POST_FRAC of post-window scenes and in <= PRE_FRAC of pre-window
    scenes, on pre-window dark water; >= 1 component; first-bright inside
    ALULA_INSTALL.
  C-water-1/2 (controls): open lake boxes with no reported new infrastructure,
    same windows and detector; pass if 0 qualifying components.
  Supplementary (not scored): ascending-geometry cross-check at the detected
    object; eastern-lake screening recorded in the method note.

Input : DS-0002 Sentinel-1 RTC (Sentinel-1A, descending relative orbit 171),
        VV gamma0, Microsoft Planetary Computer STAC.
Output: data/derived/method-0003/v0.1/ (rasters + quicklook figures).

Usage: py -3 scripts/method0003_validate.py [ALULA LAGO_SUR LAGO_OESTE]
"""
import hashlib
import json
import os
import sys
from datetime import date
from pathlib import Path

import numpy as np

_proj = Path(sys.executable).parent / "Lib" / "site-packages" / "rasterio" / "proj_data"
if _proj.exists():
    os.environ["PROJ_LIB"] = str(_proj)
    os.environ["PROJ_DATA"] = str(_proj)
os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
os.environ.setdefault("GDAL_HTTP_MULTIRANGE", "YES")

import planetary_computer  # noqa: E402
import rasterio  # noqa: E402
from pystac_client import Client  # noqa: E402
from rasterio.enums import Resampling  # noqa: E402
from rasterio.transform import from_origin  # noqa: E402
from rasterio.vrt import WarpedVRT  # noqa: E402
from scipy import ndimage  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived" / "method-0003" / "v0.1"
CACHE = Path(os.environ.get("M0003_CACHE", Path(os.environ.get("TEMP", ".")) / "m0003_cache"))
STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
COLLECTION = "sentinel-1-rtc"
TRACK, STATE, PLATFORM = 171, "descending", "sentinel-1a"
ASC_TRACK, ASC_STATE = 4, "ascending"
RES = 0.0001                      # ~11 m grid (EPSG:4326)
PRE = ("2025-06-01", "2025-08-20")
POST = ("2025-09-01", "2025-12-30")
WATER_DB = -15.0                  # pre-window median below this = water
BRIGHT_DB = -8.0                  # a scene counts as "bright object present"
POST_FRAC = 0.90                  # >= fraction of post scenes bright
PRE_FRAC = 0.00                   # <= fraction of pre scenes bright
SIZE = (4, 2000)                  # component size in px (~0.05..24 ha at 11 m)
ALULA_INSTALL = ("2025-09-01", "2025-10-31")  # reported month + margin
WATER_K = 10                      # neighbourhood for the context water fraction
ASC_MONTHS = ("2025-06", "2025-08", "2025-09", "2025-11")
TESTS = {
    "ALULA": {"box": (-71.40, 10.00, -71.20, 10.20), "role": "positive",
              "label": "Lagunillas lake/terminal (reported Alula jack-up arrival, Sep 2025)"},
    "LAGO_SUR": {"box": (-71.30, 9.60, -71.10, 9.80), "role": "control",
                 "label": "Southern Lake Maracaibo open water"},
    "LAGO_OESTE": {"box": (-71.60, 10.05, -71.40, 10.25), "role": "control",
                   "label": "Western Lake Maracaibo open water"},
}


def grid(box):
    lon_min, lat_min, lon_max, lat_max = box
    w = int(round((lon_max - lon_min) / RES))
    h = int(round((lat_max - lat_min) / RES))
    return from_origin(lon_min, lat_max, RES, RES), w, h


def read_db(item, transform, w, h):
    with rasterio.open(item.assets["vv"].href) as src:
        with WarpedVRT(src, crs="EPSG:4326", transform=transform, width=w, height=h,
                       resampling=Resampling.nearest, src_nodata=-32768, nodata=-32768) as vrt:
            lin = vrt.read(1).astype("float64")
    lin[lin <= 0] = np.nan
    return (10 * np.log10(lin)).astype("float32")


def scene_items(box, track=TRACK, state=STATE, platform=PLATFORM):
    c = Client.open(STAC_URL)
    items = list(c.search(collections=[COLLECTION], bbox=box,
                          datetime="2025-06-01/2025-12-31").items())
    items = [i for i in items
             if i.properties.get("sat:relative_orbit") == track
             and i.properties.get("sat:orbit_state") == state
             and i.properties.get("platform", "").lower() == platform]
    return sorted(items, key=lambda i: i.datetime)


def cached_db(name, item, transform, w, h):
    p = CACHE / name / (item.id + ".npy")
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        return np.load(p)
    a = read_db(planetary_computer.sign(item), transform, w, h)
    np.save(p, a)
    return a


def write_tif(path, arr, transform, dtype="float32", nodata=np.nan):
    profile = dict(driver="GTiff", height=arr.shape[0], width=arr.shape[1],
                   count=1, dtype=dtype, crs="EPSG:4326", transform=transform,
                   compress="deflate", nodata=nodata)
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(arr.astype(dtype), 1)


def components(mask, transform):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    feats = []
    if n == 0:
        return feats
    sizes = ndimage.sum(mask, lab, index=np.arange(1, n + 1))
    for k, s in enumerate(sizes, start=1):
        if SIZE[0] <= s <= SIZE[1]:
            rr, cc = np.where(lab == k)
            r0, c0 = rr.mean(), cc.mean()
            lon, lat = transform * (c0 + 0.5, r0 + 0.5)
            feats.append({"component": len(feats) + 1, "pixels": int(s),
                          "lon": round(lon, 6), "lat": round(lat, 6), "rr": rr, "cc": cc})
    return feats


def ascending_check(box, feats):
    """Non-scored: does the object also step in ascending geometry?"""
    if not feats:
        return []
    transform, w, h = grid(box)
    items = scene_items(box, ASC_TRACK, ASC_STATE, PLATFORM)
    items = [i for i in items if i.datetime.strftime("%Y-%m") in ASC_MONTHS]
    out = []
    for it in items:
        a = read_db(planetary_computer.sign(it), transform, w, h)
        vals = [float(np.nanmedian(a[f["rr"], f["cc"]])) for f in feats]
        out.append({"date": it.datetime.strftime("%Y-%m-%d"),
                    "median_db": [round(v, 1) for v in vals]})
    return out


def run(name):
    cfg = TESTS[name]
    box = cfg["box"]
    transform, w, h = grid(box)
    items = scene_items(box)
    print(f"[{name}] {cfg['label']} grid {w}x{h}; {len(items)} scenes")
    recs = [(it.datetime.strftime("%Y-%m-%d"), cached_db(name, it, transform, w, h))
            for it in items]
    is_pre = np.array([d <= PRE[1] for d, _ in recs])
    stack = np.stack([a for _, a in recs])
    pre, post = stack[is_pre], stack[~is_pre]
    mp = np.nanmedian(pre, axis=0)
    ms = np.nanmedian(post, axis=0)
    water = mp < WATER_DB
    pre_frac = np.nanmean(pre >= BRIGHT_DB, axis=0)
    post_frac = np.nanmean(post >= BRIGHT_DB, axis=0)
    mask = water & (post_frac >= POST_FRAC) & (pre_frac <= PRE_FRAC)
    feats = components(mask, transform)

    water_around = ndimage.uniform_filter(water.astype("float32"),
                                          size=2 * WATER_K + 1, mode="constant")
    dates = [d for d, _ in recs]
    for f in feats:
        vals = stack[:, f["rr"], f["cc"]]
        present = np.nanmean(vals >= BRIGHT_DB, axis=1) >= 0.5
        f["first_bright"] = dates[int(np.argmax(present))] if present.any() else None
        f["pre_bright_frac"] = round(float(np.nanmean(pre_frac[f["rr"], f["cc"]])), 3)
        f["post_bright_frac"] = round(float(np.nanmean(post_frac[f["rr"], f["cc"]])), 3)
        f["water_frac_230m"] = round(float(np.nanmean(water_around[f["rr"], f["cc"]])), 2)
        f["max_change_db"] = round(float(np.nanmax(ms[f["rr"], f["cc"]] - mp[f["rr"], f["cc"]])), 1)

    res = {"test": name, "role": cfg["role"], "label": cfg["label"], "box": box,
           "scenes": len(recs), "scenes_pre": int(is_pre.sum()),
           "scenes_post": int((~is_pre).sum()), "scene_ids": [i.id for i in items],
           "grid": {"w": w, "h": h, "res_deg": RES}, "water_pixels": int(water.sum()),
           "components": len(feats),
           "candidates": [{k: v for k, v in f.items() if k not in ("rr", "cc")} for f in feats]}
    if name == "ALULA":
        res["ascending_check"] = ascending_check(box, feats)

    OUT.mkdir(parents=True, exist_ok=True)
    change = ms - mp
    write_tif(OUT / f"{name}_pre_median_db.tif", mp, transform)
    write_tif(OUT / f"{name}_post_median_db.tif", ms, transform)
    write_tif(OUT / f"{name}_change_db.tif", change, transform)
    write_tif(OUT / f"{name}_post_bright_frac.tif", post_frac, transform)
    feats_geo = [{"type": "Feature",
                  "geometry": {"type": "Point", "coordinates": [f["lon"], f["lat"]]},
                  "properties": {k: v for k, v in f.items() if k not in ("rr", "cc")}}
                 for f in feats]
    (OUT / f"{name}_candidates.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": feats_geo}, indent=2),
        encoding="utf-8")
    quicklook(name, mp, ms, change, feats, transform)
    (OUT / f"{name}_results.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"   components: {len(feats)} "
          f"{[(f['lon'], f['lat'], f['pixels'], f['first_bright']) for f in feats]}")
    return res


def quicklook(name, mp, ms, change, feats, transform):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    h, w = mp.shape
    ext = [transform.c, transform.c + transform.a * w, transform.f + transform.e * h, transform.f]
    fig, ax = plt.subplots(1, 3, figsize=(18, 6.4))
    for a, arr, t, cm, lo, hi in ((ax[0], mp, "PRE median VV (dB)", "gray", -25, 0),
                                  (ax[1], ms, "POST median VV (dB)", "gray", -25, 0),
                                  (ax[2], change, "POST-PRE (dB)", "RdBu_r", -12, 12)):
        im = a.imshow(arr, extent=ext, cmap=cm, vmin=lo, vmax=hi)
        a.set_title(t); fig.colorbar(im, ax=a, fraction=0.046)
    for a in ax:
        for f in feats:
            a.plot(f["lon"], f["lat"], "o", mfc="none", mec="lime", mew=2, ms=16)
        a.set_xlabel("lon"); a.set_ylabel("lat")
    ax[2].set_title(f"POST-PRE (dB); {len(feats)} new persistent object(s)\n"
                    f"S1A track {TRACK} descending VV")
    fig.suptitle(f"METHOD-0003 v0.1 {name}")
    fig.tight_layout()
    OUT.mkdir(parents=True, exist_ok=True)  # figures generated locally, never committed (ADR-001)
    fig.savefig(OUT / f"METHOD-0003-v0.1-{name}.png", dpi=110)
    plt.close(fig)


def main():
    names = sys.argv[1:] or list(TESTS)
    allres = {}
    for n in names:
        allres[n] = run(n)
    verdict = {}
    for n in names:
        cands = allres[n]["candidates"]
        if TESTS[n]["role"] == "positive":
            qual = [c for c in cands
                    if c["first_bright"] and ALULA_INSTALL[0] <= c["first_bright"] <= ALULA_INSTALL[1]]
            verdict[n] = {"pass": bool(qual), "qualifying": len(qual)}
        else:
            verdict[n] = {"pass": len(cands) == 0, "qualifying": len(cands)}
    verdict["validated"] = all(v["pass"] for v in verdict.values())
    allres["verdict"] = verdict
    manifest = {
        "method": "METHOD-0003", "processing_version": "0.1.0",
        "pre_registration": os.environ.get("M3_PREREG", ""),
        "run_date": str(date.today()),
        "input": {"stac": STAC_URL, "collection": COLLECTION, "asset": "vv",
                  "platform": PLATFORM, "relative_orbit": TRACK, "orbit_state": STATE},
        "windows": {"pre": PRE, "post": POST},
        "parameters": {"res_deg": RES, "water_db": WATER_DB, "bright_db": BRIGHT_DB,
                       "post_frac": POST_FRAC, "pre_frac": PRE_FRAC, "size_px": SIZE,
                       "alula_install_window": ALULA_INSTALL},
        "tests": {k: {kk: vv for kk, vv in v.items()
                      if kk not in ("candidates", "ascending_check")}
                  for k, v in allres.items() if k in TESTS},
        "checksums": {p.name: hashlib.md5(p.read_bytes()).hexdigest()
                      for p in sorted(OUT.glob("*"))
                      if p.suffix in (".tif", ".geojson", ".json") and p.name != "manifest.json"},
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (OUT / "results.json").write_text(json.dumps(allres, indent=2, default=str), encoding="utf-8")
    print("VERDICT:", json.dumps(verdict))


if __name__ == "__main__":
    main()
