"""One-off check: recompute METHOD-0002 FIRMS counts at corrected AOIs.

AST-0014 (Jose complex) coordinates corrected from OGIM offshore terminal
record (-64.646, 10.216) to OSM complex centroid (-64.864, 10.069).
Uses cached raw FIRMS downloads (data/raw/firms, 2026-09-04..10-03).
"""
import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "firms"

frames = [pd.read_csv(p) for p in sorted(RAW.glob("*_30d.csv"))]
f = pd.concat(frames, ignore_index=True)
f = f[f.latitude != "latitude"]
for c in ("latitude", "longitude"):
    f[c] = pd.to_numeric(f[c], errors="coerce")
f = f.dropna(subset=["latitude", "longitude"])


def hav(lon1, lat1, lon2, lat2):
    p = math.pi / 180
    a = (math.sin((lat2 - lat1) * p / 2) ** 2
         + math.cos(lat1 * p) * math.cos(lat2 * p)
         * math.sin((lon2 - lon1) * p / 2) ** 2)
    return 2 * 6371 * math.asin(a ** 0.5)


points = {
    "Jose_old_OGIM_terminal": (-64.646, 10.216),
    "Jose_corrected_OSM": (-64.864, 10.069),
}
for name, (lon, lat) in points.items():
    d = f.apply(lambda r: hav(r.longitude, r.latitude, lon, lat), axis=1)
    for r in (1.5, 5.0):
        sub = f[d <= r]
        print(f"{name:24s} r={r}km: {len(sub):4d} hotspots, "
              f"{sub.acq_date.nunique():2d} days")
print("distance old->corrected km:",
      round(hav(-64.646, 10.216, -64.864, 10.069), 1))
