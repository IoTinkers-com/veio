"""Overview figure: FIRMS hotspot density + OGIM flaring over Santa Barbara."""
import csv
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FIRMS = ROOT / "data" / "derived" / "method-0002" / "firms_ve_hotspots.csv"
OGIM = ROOT / "data" / "ogim_venezuela" / "Natural_Gas_Flaring_Detections.csv"
OUT = ROOT / "data" / "derived" / "asset-zoom" / "AST-0012-santa-barbara"
BOX = (-63.80, 9.50, -63.52, 9.78)
ASSET = (-63.662301, 9.622276)

lon, lat = [], []
with FIRMS.open(encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        lo, la = float(r["longitude"]), float(r["latitude"])
        if BOX[0] <= lo <= BOX[2] and BOX[1] <= la <= BOX[3]:
            lon.append(lo); lat.append(la)
olon, olat, onam = [], [], []
with OGIM.open(encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        lo, la = float(r["lon"]), float(r["lat"])
        if BOX[0] <= lo <= BOX[2] and BOX[1] <= la <= BOX[3]:
            olon.append(lo); olat.append(la); onam.append(r["FAC_NAME"])

fig, ax = plt.subplots(1, 2, figsize=(16, 7.5))
for a, bins in ((ax[0], 60), (ax[1], 160)):
    h = a.hist2d(lon, lat, bins=bins, range=[[BOX[0], BOX[2]], [BOX[1], BOX[3]]],
                 cmap="inferno", norm=matplotlib.colors.LogNorm())
    fig.colorbar(h[3], ax=a, label="hotspots / cell")
a = ax[0]
a.scatter(olon, olat, s=28, facecolors="none", edgecolors="cyan", label="OGIM flaring")
a.plot(*ASSET, marker="*", color="red", ms=18, label="AST-0012 centroid")
a.legend(loc="upper right")
a.set_title("FIRMS hotspots 2026-09-04..10-03 (all)")
a.set_xlabel("lon"); a.set_ylabel("lat")
ax[1].set_title("zoom density"); ax[1].set_xlabel("lon"); ax[1].set_ylabel("lat")
fig.suptitle("AST-0012 Santa Barbara flaring overview (3503 FIRMS points, 69 OGIM)")
fig.tight_layout()
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "overview_firms.png", dpi=110)
print("saved", OUT / "overview_firms.png")
