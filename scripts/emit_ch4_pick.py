"""Pick the EMIT CH4 enhancement granule with best coverage of the Santa Barbara cell."""
import json
import os
import sys
import urllib.parse
import urllib.request
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
TOKEN = (ROOT / ".secrets" / "edl_token.txt").read_text().strip()
RAW = ROOT / "data" / "raw" / "emit"
RAW.mkdir(parents=True, exist_ok=True)
SEARCH_BOX = (-63.80, 9.50, -63.52, 9.78)     # to find granules
TIGHT = (-63.72, 9.57, -63.60, 9.67)          # Santa Barbara cell
CANDIDATES = ["20260526T153543_2614610_003", "20260526T153555_2614610_004",
              "20260518T184413_2613812_033", "20260427T140148_2611709_018",
              "20260423T153502_2611310_029"]


def links():
    url = ("https://cmr.earthdata.nasa.gov/search/granules.json?"
           + urllib.parse.urlencode({"short_name": "EMITL2BCH4ENH",
                                     "bounding_box": ",".join(str(x) for x in SEARCH_BOX),
                                     "temporal": "2024-01-01T00:00:00Z/2026-10-05T23:59:59Z",
                                     "page_size": 100}))
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOKEN}"})
    data = json.loads(urllib.request.urlopen(req, timeout=180).read())
    out = {}
    for e in data.get("feed", {}).get("entry", []):
        for c in CANDIDATES:
            if c in e.get("title", ""):
                for l in e.get("links", []):
                    href = l.get("href", "")
                    if href.endswith(".tif"):
                        if href.startswith("s3://"):
                            href = ("https://data.lpdaac.earthdatacloud.nasa.gov/"
                                    + href[len("s3://"):])
                        out[c] = (e["title"], href)
    return out


def main():
    found = links()
    results = []
    for c in CANDIDATES:
        if c not in found:
            print(c, "not found")
            continue
        title, href = found[c]
        dest = RAW / (title + ".tif")
        if not dest.exists():
            req = urllib.request.Request(href, headers={"Authorization": f"Bearer {TOKEN}"})
            with urllib.request.urlopen(req, timeout=900) as r, dest.open("wb") as fh:
                fh.write(r.read())
        with rasterio.open(dest) as src:
            bb = rasterio.warp.transform_bounds("EPSG:4326", src.crs, *TIGHT)
            w = from_bounds(*bb, transform=src.transform).round_offsets().round_lengths()
            a = src.read(1, window=w).astype("float64")
            a[a == -9999] = np.nan
        fin = a[np.isfinite(a)]
        frac = fin.size / a.size
        results.append((c, a.shape, round(frac, 3),
                        round(float(np.nanpercentile(fin, 99)), 0) if fin.size else 0,
                        round(float(np.nanmax(fin)), 0) if fin.size else 0))
        print(f"{c}: shape={a.shape} valid={frac:.3f} p99={results[-1][3]} max={results[-1][4]} ppm m")
    best = max(results, key=lambda r: r[2])
    print("BEST coverage:", best[0])


if __name__ == "__main__":
    main()
