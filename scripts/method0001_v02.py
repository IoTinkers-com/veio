"""METHOD-0001 v0.2 — optical change detection with surface-expression events.

Pre-registered in docs/methods/METHOD-0001.md (commit 93b9b25, before run).

Changes vs v0.1: per-pixel medians on a common EPSG:4326 grid (WarpedVRT),
SCL cloud/shadow mask, <=8 least-cloudy scenes, 20 m grid, fixed a-priori
thresholds, matched controls, visual outputs.

Usage: py -3 scripts/method0001_v02.py [T1 T2 C1 C2]
Outputs: data/derived/method-0001/v0.2/
"""
import hashlib
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import numpy as np

_proj_dir = Path(sys.executable).parent / "Lib" / "site-packages" / "rasterio" / "proj_data"
if _proj_dir.exists():  # see .agents/memory/rasterio-proj-planetary-computer.md
    os.environ["PROJ_LIB"] = str(_proj_dir)
    os.environ["PROJ_DATA"] = str(_proj_dir)
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
OUT = ROOT / "data" / "derived" / "method-0001" / "v0.2"
STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
RES = 0.00018  # deg (~20 m)
MAX_SCENES = 8
SCL_INVALID = {0, 1, 3, 8, 9, 10}
SCL_WATER = 6

TESTS = {
    "T1": {"box": (-71.40, 10.00, -71.20, 10.20), "detector": "nir_water",
           "pre": ("2025-06-01", "2025-08-20"), "post": ("2025-10-01", "2025-12-15"),
           "rgb": True, "label": "Alula jack-up arrival, Lagunillas"},
    "C1": {"box": (-68.05, 10.95, -67.85, 11.15), "detector": "nir_water",
           "pre": ("2025-06-01", "2025-08-20"), "post": ("2025-10-01", "2025-12-15"),
           "rgb": False, "label": "Open-sea water control"},
    "T2": {"box": (-64.914, 10.019, -64.814, 10.119), "detector": "dnbr",
           "pre": ("2025-10-01", "2025-11-18"), "post": ("2025-11-20", "2026-01-31"),
           "rgb": True, "label": "Petrocedeno fire, Jose complex"},
    "C2": {"box": (-68.05, 10.13, -67.95, 10.23), "detector": "dnbr",
           "pre": ("2025-10-01", "2025-11-18"), "post": ("2025-11-20", "2026-01-31"),
           "rgb": False, "label": "Valencia urban land control"},
}
THR_NIR = 0.08     # reflectance jump over water (pre-registered)
THR_DNBR = 0.27    # USGS FIREMON moderate-low lower bound (pre-registered)
SIZE_NIR = (4, 200)
SIZE_DNBR = (4, 10**9)


def grid(box):
    lon_min, lat_min, lon_max, lat_max = box
    w = int(round((lon_max - lon_min) / RES))
    h = int(round((lat_max - lat_min) / RES))
    return from_origin(lon_min, lat_max, RES, RES), w, h


def read_band(href, transform, w, h, nearest=False):
    with rasterio.open(href) as src:
        with WarpedVRT(src, crs="EPSG:4326", transform=transform, width=w,
                       height=h, resampling=(Resampling.nearest if nearest
                                             else Resampling.bilinear),
                       src_nodata=0, nodata=0) as vrt:
            return vrt.read(1)


def scene_stack(box, window, bands):
    stac = Client.open(STAC_URL)
    items = list(stac.search(collections=["sentinel-2-l2a"], bbox=box,
                             datetime=f"{window[0]}/{window[1]}",
                             query={"eo:cloud_cover": {"lt": 60}}).items())
    items = sorted(items, key=lambda i: i.properties.get("eo:cloud_cover", 100))
    items = items[:MAX_SCENES]
    transform, w, h = grid(box)

    def one(item):
        item = planetary_computer.sign(item)
        base = float(item.properties.get("s2:processing_baseline", "0") or 0)
        off = 1000.0 if base >= 4.0 else 0.0
        out = {}
        try:
            scl = read_band(item.assets["SCL"].href, transform, w, h, nearest=True)
            for b in bands:
                raw = read_band(item.assets[b].href, transform, w, h).astype("float32")
                refl = (raw - off) * 0.0001
                refl[raw == 0] = np.nan
                out[b] = refl
        except Exception as e:  # noqa: BLE001
            return item.id, None, f"{type(e).__name__}: {str(e)[:80]}"
        invalid = np.isin(scl, list(SCL_INVALID))
        for b in bands:
            out[b][invalid] = np.nan
        out["_water"] = (scl == SCL_WATER).astype("float32")
        out["_valid"] = (~invalid).astype("float32")
        return item.id, out, None

    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(one, items))
    good = [r[1] for r in results if r[1] is not None]
    for sid, _, err in results:
        if err:
            print(f"   skip {sid}: {err}")
    if not good:
        return None, 0, [r[0] for r in results]
    med = {b: np.nanmedian(np.stack([g[b] for g in good]), axis=0) for b in bands}
    valid = np.sum(np.stack([g["_valid"] for g in good]), axis=0)
    water = np.sum(np.stack([g["_water"] for g in good]), axis=0)
    med["_water_frac"] = np.where(valid > 0, water / np.maximum(valid, 1), 0)
    med["_valid_n"] = valid
    return med, len(good), [r[0] for r in results if r[1] is not None]


def components(mask, size_range, delta, transform):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    feats = []
    if n == 0:
        return feats, lab
    sizes = ndimage.sum(mask, lab, index=np.arange(1, n + 1))
    for k, s in enumerate(sizes, start=1):
        if size_range[0] <= s <= size_range[1]:
            rr, cc = np.where(lab == k)
            r0, c0 = rr.mean(), cc.mean()
            lon, lat = transform * (c0 + 0.5, r0 + 0.5)
            feats.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [round(lon, 6), round(lat, 6)]},
                "properties": {"pixels": int(s), "area_ha": round(float(s) * 4 / 100, 2),
                               "max_delta": round(float(np.nanmax(delta[lab == k])), 3)},
            })
    return feats, lab


def write_tif(path, arr, transform, dtype="float32", nodata=np.nan):
    arr = np.atleast_3d(arr)
    if arr.ndim == 3 and arr.shape[2] in (1, 3) and arr.shape[0] != arr.shape[2]:
        arr = np.moveaxis(arr, 2, 0)
    profile = dict(driver="GTiff", height=arr.shape[1], width=arr.shape[2],
                   count=arr.shape[0], dtype=dtype, crs="EPSG:4326",
                   transform=transform, compress="deflate", nodata=nodata)
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(arr.astype(dtype))


def rgb_u8(med_pre, med_post):
    out = []
    for med in (med_pre, med_post):
        out.append(np.dstack([med["B04"], med["B03"], med["B02"]]))
    both = np.concatenate([o.reshape(-1, 3) for o in out])
    lo = np.nanpercentile(both, 2, axis=0)
    hi = np.nanpercentile(both, 98, axis=0)
    res = []
    for o in out:
        s = np.clip((o - lo) / np.maximum(hi - lo, 1e-6), 0, 1)
        res.append(np.nan_to_num(s * 255).astype("uint8"))
    return res


def quicklook(path, rgb_pre, rgb_post, delta, feats, transform, title, thr):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(18, 6.4))
    ext = [transform.c, transform.c + transform.a * delta.shape[1],
           transform.f + transform.e * delta.shape[0], transform.f]
    ax[0].imshow(rgb_pre, extent=ext); ax[0].set_title("Pre composite (median)")
    ax[1].imshow(rgb_post, extent=ext); ax[1].set_title("Post composite (median)")
    vmax = max(thr * 2, np.nanpercentile(np.abs(delta), 99) if np.isfinite(delta).any() else thr)
    im = ax[2].imshow(delta, extent=ext, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    ax[2].set_title(f"Change index (threshold {thr})")
    for a in ax:
        for f in feats:
            x, y = f["geometry"]["coordinates"]
            a.plot(x, y, "o", mfc="none", mec="yellow", mew=2, ms=14)
        a.set_xlabel("lon"); a.set_ylabel("lat")
    fig.colorbar(im, ax=ax[2], fraction=0.046)
    fig.suptitle(title, fontsize=13)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def run(test_id):
    cfg = TESTS[test_id]
    box = cfg["box"]
    transform, w, h = grid(box)
    det = cfg["detector"]
    bands = ["B08"] + (["B12"] if det == "dnbr" else [])
    if cfg["rgb"]:
        bands += ["B04", "B03", "B02"]
    print(f"[{test_id}] {cfg['label']} grid {w}x{h}")
    pre, n_pre, ids_pre = scene_stack(box, cfg["pre"], bands)
    print(f"   pre scenes used: {n_pre}")
    post, n_post, ids_post = scene_stack(box, cfg["post"], bands)
    print(f"   post scenes used: {n_post}")
    res = {"test": test_id, "label": cfg["label"], "box": box,
           "scenes_pre": n_pre, "scenes_post": n_post,
           "scene_ids_pre": ids_pre, "scene_ids_post": ids_post}
    if pre is None or post is None:
        res["status"] = "insufficient_scenes"
        return res

    if det == "nir_water":
        water = (pre["_water_frac"] >= 0.5)
        delta = post["B08"] - pre["B08"]
        delta_masked = np.where(water, delta, np.nan)
        mask = water & (delta >= THR_NIR)
        feats, _ = components(mask, SIZE_NIR, delta_masked, transform)
        thr = THR_NIR
        res["valid_pixels"] = int(np.isfinite(delta_masked).sum())
    else:
        nbr = lambda m: (m["B08"] - m["B12"]) / (m["B08"] + m["B12"] + 1e-6)  # noqa: E731
        land = (pre["_water_frac"] < 0.5) & (post["_water_frac"] < 0.5)
        delta = nbr(pre) - nbr(post)
        delta_masked = np.where(land, delta, np.nan)
        mask = land & (delta >= THR_DNBR)
        feats, _ = components(mask, SIZE_DNBR, delta_masked, transform)
        thr = THR_DNBR
        res["valid_pixels"] = int(np.isfinite(delta_masked).sum())

    res["pixels_over_threshold"] = int(mask.sum())
    res["pct_over_threshold"] = round(100 * mask.sum() / max(res["valid_pixels"], 1), 3)
    res["components"] = len(feats)
    res["candidates"] = feats

    OUT.mkdir(parents=True, exist_ok=True)
    write_tif(OUT / f"{test_id}_change.tif", delta_masked, transform)
    (OUT / f"{test_id}_candidates.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": feats}), encoding="utf-8")
    if cfg["rgb"]:
        rgb_pre, rgb_post = rgb_u8(pre, post)
        write_tif(OUT / f"{test_id}_rgb_pre.tif", rgb_pre, transform, "uint8", 0)
        write_tif(OUT / f"{test_id}_rgb_post.tif", rgb_post, transform, "uint8", 0)
        quicklook(OUT / f"{test_id}_quicklook.png", rgb_pre, rgb_post, delta_masked,
                  feats, transform, f"METHOD-0001 v0.2 {test_id}: {cfg['label']}", thr)
    return res


def main():
    ids = sys.argv[1:] or list(TESTS)
    OUT.mkdir(parents=True, exist_ok=True)
    allres = {}
    for t in ids:
        allres[t] = run(t)
        print(json.dumps({k: v for k, v in allres[t].items()
                          if k not in ("candidates", "scene_ids_pre", "scene_ids_post")}, indent=1))
        (OUT / f"{t}_results.json").write_text(json.dumps(allres[t], indent=2), encoding="utf-8")
    manifest = {
        "method": "METHOD-0001", "processing_version": "0.2.0",
        "pre_registration_commit": "93b9b25", "run_date": str(date.today()),
        "inputs": {"stac": STAC_URL, "collection": "sentinel-2-l2a",
                   "tests": {k: {kk: vv for kk, vv in v.items() if kk != "rgb"}
                             for k, v in TESTS.items()}},
        "parameters": {"res_deg": RES, "max_scenes": MAX_SCENES,
                       "scl_invalid": sorted(SCL_INVALID), "thr_nir": THR_NIR,
                       "thr_dnbr": THR_DNBR, "size_nir_px": SIZE_NIR,
                       "size_dnbr_min_px": SIZE_DNBR[0]},
        "checksums": {p.name: hashlib.md5(p.read_bytes()).hexdigest()
                      for p in sorted(OUT.glob("*")) if p.suffix in (".tif", ".geojson", ".json")
                      and p.name != "manifest.json"},
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
