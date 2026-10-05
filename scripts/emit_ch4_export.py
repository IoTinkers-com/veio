"""Export EMIT CH4 enhancement crops + quicklooks over Santa Barbara.

Uses the two granules with best coverage of the flare cell; overlays FIRMS
hotspots. Output: data/derived/asset-zoom/AST-0012-santa-barbara/methane/.
"""
import csv
import json
import os
import sys
from pathlib import Path

import numpy as np

_proj = Path(sys.executable).parent / "Lib" / "site-packages" / "rasterio" / "proj_data"
if _proj.exists():
    os.environ["PROJ_LIB"] = str(_proj)
    os.environ["PROJ_DATA"] = str(_proj)

import rasterio  # noqa: E402
import rasterio.warp  # noqa: E402
from rasterio.windows import from_bounds  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "emit"
OUT = ROOT / "data" / "derived" / "asset-zoom" / "AST-0012-santa-barbara" / "methane"
FIRMS = ROOT / "data" / "derived" / "method-0002" / "firms_ve_hotspots.csv"
BOX = (-63.80, 9.50, -63.52, 9.78)
TIGHT = (-63.72, 9.57, -63.60, 9.67)
GRANULES = {
    "2026-05-26": RAW / "EMIT_L2B_CH4ENH_002_20260526T153555_2614610_004.tif",
    "2026-04-27": RAW / "EMIT_L2B_CH4ENH_002_20260427T140148_2611709_018.tif",
}


def crop(src, box):
    bb = rasterio.warp.transform_bounds("EPSG:4326", src.crs, *box)
    w = from_bounds(*bb, transform=src.transform).intersection(
        rasterio.windows.Window(0, 0, src.width, src.height)).round_offsets().round_lengths()
    a = src.read(1, window=w).astype("float64")
    a[a == -9999] = np.nan
    return a, rasterio.windows.transform(w, src.transform)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    stats = {}
    arrs = {}
    for date, path in GRANULES.items():
        if not path.exists():
            print("missing", path)
            continue
        with rasterio.open(path) as src:
            a, tr = crop(src, BOX)
            ac, _ = crop(src, TIGHT)
            crs = src.crs
        fin = a[np.isfinite(a)]
        finc = ac[np.isfinite(ac)]
        stats[date] = {"crop_shape": list(a.shape), "valid_frac": round(float(fin.size / a.size), 3),
                       "p90": round(float(np.nanpercentile(finc, 90)), 0) if finc.size else None,
                       "p99": round(float(np.nanpercentile(finc, 99)), 0) if finc.size else None,
                       "max": round(float(np.nanmax(finc)), 0) if finc.size else None,
                       "units": "ppm m"}
        prof = dict(driver="GTiff", height=a.shape[0], width=a.shape[1], count=1, dtype="float32",
                    crs=crs, transform=tr, compress="deflate", nodata=np.nan)
        with rasterio.open(OUT / f"EMIT_CH4ENH_{date}.tif", "w", **prof) as dst:
            dst.write(a.astype("float32"), 1)
        arrs[date] = a
        print(date, stats[date])

    # FIRMS points for overlay
    flon, flat = [], []
    with FIRMS.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            lo, la = float(r["longitude"]), float(r["latitude"])
            if BOX[0] <= lo <= BOX[2] and BOX[1] <= la <= BOX[3]:
                flon.append(lo); flat.append(la)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    n = len(arrs)
    fig, ax = plt.subplots(1, max(n, 1), figsize=(8 * max(n, 1), 7))
    ax = np.atleast_1d(ax)
    for k, (date, a) in enumerate(arrs.items()):
        vr = np.nanpercentile(a, 99.5)
        im = ax[k].imshow(a, cmap="turbo", vmin=0, vmax=vr, extent=[BOX[0], BOX[2], BOX[1], BOX[3]],
                          aspect="auto")
        ax[k].scatter(flon, flat, s=4, c="white", alpha=0.5, label="FIRMS hotspots")
        ax[k].set_title(f"EMIT CH4 enhancement {date}\nmax {stats[date]['max']:.0f} ppm m in cell")
        ax[k].set_xlabel("lon"); ax[k].set_ylabel("lat"); fig.colorbar(im, ax=ax[k], label="ppm m")
    fig.suptitle("AST-0012 Santa Barbara - EMIT methane enhancement vs FIRMS hotspots "
                 "(Contains modified NASA/JPL/EMIT data; NASA FIRMS)")
    fig.tight_layout()
    fig.savefig(OUT / "EMIT_CH4ENH_quicklook.png", dpi=110)
    (OUT / "emit_ch4_results.json").write_text(json.dumps(
        {"source": "EMITL2BCH4ENH V002 (ppm m), NASA LP DAAC, DOI 10.5067/EMIT/EMITL2BCH4ENH.002",
         "box": BOX, "tight_cell": TIGHT, "granules": stats}, indent=2), encoding="utf-8")
    print("saved", OUT)


if __name__ == "__main__":
    main()
