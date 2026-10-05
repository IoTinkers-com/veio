"""Combined preview of the Santa Barbara zoom package (SAR + optical + FIRMS)."""
import csv
import os
import sys
from pathlib import Path

import numpy as np

_proj = Path(sys.executable).parent / "Lib" / "site-packages" / "rasterio" / "proj_data"
if _proj.exists():
    os.environ["PROJ_LIB"] = str(_proj)
    os.environ["PROJ_DATA"] = str(_proj)

import rasterio
import rasterio.warp

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "derived" / "asset-zoom" / "AST-0012-santa-barbara"
FIRMS = ROOT / "data" / "derived" / "method-0002" / "firms_ve_hotspots.csv"
BOX = (-63.80, 9.50, -63.52, 9.78)

flon, flat = [], []
with FIRMS.open(encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        lo, la = float(r["longitude"]), float(r["latitude"])
        if BOX[0] <= lo <= BOX[2] and BOX[1] <= la <= BOX[3]:
            flon.append(lo); flat.append(la)

panels = [
    (BASE / "sar_context" / "S1_median_context_db.tif", "S1 RTC VV median (dB)", "gray", -22, -2),
    (BASE / "sar" / "COMPOSITE_median_db.tif", "S1 RTC VV median, high zoom (dB)", "gray", -22, -2),
    (BASE / "optical" / "S2_2026-09-22_rgb_u8.tif", "S2 2026-09-22 true colour", None, None, None),
]
fig, ax = plt.subplots(1, 3, figsize=(19, 6.6))
for a, (path, title, cmap, lo, hi) in zip(ax, panels):
    with rasterio.open(path) as src:
        arr = src.read()
        if src.crs is not None and src.crs.to_string() != "EPSG:4326":
            b = rasterio.warp.transform_bounds(src.crs, "EPSG:4326", *src.bounds)
        else:
            b = (src.bounds.left, src.bounds.bottom, src.bounds.right, src.bounds.top)
        ext = [b[0], b[2], b[1], b[3]]
    if arr.shape[0] == 3:
        arr = np.moveaxis(arr, 0, 2)
        a.imshow(arr, extent=ext, aspect="auto")
    else:
        im = a.imshow(arr[0], extent=ext, cmap=cmap, vmin=lo, vmax=hi, aspect="auto")
        fig.colorbar(im, ax=a, fraction=0.046)
    a.scatter(flon, flat, s=3, c="red", alpha=0.4)
    a.set_title(title); a.set_xlabel("lon"); a.set_ylabel("lat")
fig.suptitle("AST-0012 Santa Barbara - SAR / optical zoom with FIRMS hotspots (red). "
             "Contains modified Copernicus Sentinel data 2026; NASA FIRMS")
fig.tight_layout()
out = BASE / "preview_sar_optical_firms.png"
fig.savefig(out, dpi=110)
print("saved", out)
