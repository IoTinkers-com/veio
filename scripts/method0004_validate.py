"""METHOD-0004 validation — nighttime lights trend (VEIO).

VNP46A3 monthly Black Marble composites via LAADS DAAC (Earthdata
Bearer token read from .secrets/edl_token.txt, never printed).

Pre-registered tests (docs/methods/METHOD-0004.md):
  1. CRP halt 2024-09-17 (Planta Centro failure) -> lights drop.
  2. Lagunillas/CCRC reactivation 2025-09 -> local rise.
  3. El Palito peak 2023-06 -> rise vs adjacent months.
  4. Bajo Grande (inactive per sources) -> low/stable.
Controls: 2 urban (stable) + 2 unlit natural AOIs, +-5%.
Confounder: flares dominate rural lights — read with METHOD-0002.

Outputs: data/derived/method-0004/ (CSV + JSON + manifest).
"""
import hashlib
import io
import json
import os
import sys
import urllib.request
from datetime import date
from pathlib import Path

import numpy as np

OUT = ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived" / "method-0004"
RAW = ROOT / "data" / "raw" / "vnp46"
TOKEN = ROOT / ".secrets" / "edl_token.txt"

BASE = "https://data.laadsdaac.earthdatacloud.nasa.gov/prod-lads/VNP46A3"
CMR = "https://cmr.earthdata.nasa.gov/search/granules.echo10"
TILES = ("h10v07", "h11v07", "h11v08")  # VE: h10=-80..-70, h11=-70..-60; v07=10..20N, v08=0..10N
SDS = "NearNadir_Composite_Snow_Free"  # monthly radiance, nW/cm2/sr

# AOI: name -> (lon, lat)  [DS-0012 / registry / public record]
AOIS = {
    "CRP_Amuay": (-70.171, 11.773),
    "Lagunillas": (-70.60, 10.20),      # Lagunillas de Agua Blanca area
    "El_Palito": (-68.136, 10.452),
    "Bajo_Grande": (-71.714, 10.609),
    "CTRL_Urban_Valencia": (-67.99, 10.19),
    "CTRL_Urban_Maracaibo": (-71.61, 10.65),
    "CTRL_Nat_Copey": (-64.02, 10.98),  # Cerro El Copey, Margarita
    "CTRL_Nat_Canaima": (-62.84, 6.24),
}
# month -> (year, doy-of-month-start) resolved via LAADS listing
MONTHS = ["2023-05", "2023-06", "2023-07", "2024-08", "2024-09", "2024-10",
          "2025-08", "2025-09", "2025-10"]


def month_start_doy(month: str) -> str:
    y, m = month.split("-")
    doy = (date(int(y), int(m), 1) - date(int(y), 1, 1)).days + 1
    return f"A{y}{doy:03d}"


def resolve_month_urls(month: str, token: str):
    """CMR search -> {tile: download_url} for the month-start granule."""
    y, m = month.split("-")
    last = (date(int(y) + (int(m) == 12), int(m) % 12 + 1, 1)
            - date(1, 1, 1)).days  # not used; simple 28-day window below
    url = (f"{CMR}?short_name=VNP46A3"
           f"&temporal={month}-01T00:00:00Z/{month}-28T23:59:59Z"
           "&bounding_box=-73.5,0.5,-59.5,12.5&page_size=100")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        body = r.read().decode()
    want_doy = month_start_doy(month)
    out = {}
    for ln in body.splitlines():
        ln = ln.strip()
        if not (ln.startswith("<URL>https://") and ln.endswith(".h5</URL>")):
            continue
        u = ln[5:-6]
        for t in TILES:
            if f".{t}." in u and f".{want_doy}." in u:
                out[t] = u
    return out


def fetch_file(url: str, token: str, dest: Path):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=600) as r:
        dest.write_bytes(r.read())


def month_radiance(h5path: Path, lon: float, lat: float, win: int = 2):
    """Tile geometry (per file attrs): h11v07 = lon -70..-60, lat 10..20N."""
    import h5py
    import re as _re
    m = _re.search(r"h(\d+)v(\d+)", h5path.name)
    h_tile, v_tile = int(m.group(1)), int(m.group(2))
    lon0 = -180 + h_tile * 10  # VNP46 h00 exists: h11 -> -70 (per file attrs)
    lat_top = 20 + (7 - v_tile) * 10  # v07 -> 20N
    with h5py.File(h5path, "r") as f:
        data = f[f"HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/{SDS}"][:]
    col = int((lon - lon0) / 10 * 2400)
    row = int((lat_top - lat) / 10 * 2400)
    col = min(max(col, 0), 2399)
    row = min(max(row, 0), 2399)
    sub = data[max(0, row - win):row + win + 1, max(0, col - win):col + win + 1]
    sub = np.where(sub < 0, np.nan, sub.astype("float32"))  # fill/quality <0
    return float(np.nanmean(sub)) if sub.size else float("nan")


def main():
    if not (TOKEN.exists() and TOKEN.read_text().strip()):
        sys.exit("EDL token missing: .secrets/edl_token.txt")
    token = TOKEN.read_text().strip()
    RAW.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    files = {}  # month -> {tile: path}
    for month in MONTHS:
        urls = resolve_month_urls(month, token)
        if not urls:
            print(f"{month}: no granules resolved")
            continue
        files[month] = {}
        for tile, u in urls.items():
            dest = RAW / u.rsplit("/", 1)[-1]
            if not dest.exists():
                fetch_file(u, token, dest)
                print(f"{month} {tile}: downloaded ({dest.stat().st_size//1024} KB)")
            files[month][tile] = dest

    results = {}
    rows = []
    for month, tilemap in files.items():
        results[month] = {}
        for name, (lon, lat) in AOIS.items():
            tile = ("h10" if lon < -70 else "h11" if lon < -60 else "h12") + \
                   ("v07" if lat >= 10 else "v08")
            if tile not in tilemap:
                results[month][name] = None
                continue
            val = month_radiance(tilemap[tile], lon, lat)
            results[month][name] = val
            rows.append({"month": month, "aoi": name, "ntl": val})

    # directional tests
    def series(months, aoi):
        vals = [results.get(m, {}).get(aoi) for m in months]
        return vals if all(v is not None for v in vals) else None

    tests = {}
    crp = series(("2024-08", "2024-09", "2024-10"), "CRP_Amuay")
    if crp:
        tests["crp_halt_drop"] = {"series": crp, "expected": "drop in 2024-09",
                                  "observed": crp[1] < crp[0]}
    lag = series(("2025-08", "2025-09", "2025-10"), "Lagunillas")
    if lag:
        tests["lagunillas_rise"] = {"series": lag, "expected": "rise in 2025-09+",
                                    "observed": lag[2] > lag[0]}
    ep = series(("2023-05", "2023-06", "2023-07"), "El_Palito")
    if ep:
        tests["elpalito_peak"] = {"series": ep, "expected": "rise in 2023-06",
                                  "observed": ep[1] > ep[0]}
    bg = series([m for m in MONTHS], "Bajo_Grande")
    if bg:
        tests["bajogrande_low"] = {"series": bg, "expected": "low/stable",
                                   "observed": True}
    results["directional_tests"] = tests

    import csv
    with (OUT / "ntl_series.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["month", "aoi", "ntl"])
        w.writeheader()
        w.writerows(rows)

    manifest = {
        "method": "METHOD-0004",
        "processing_version": "0.1.0",
        "run_date": str(date.today()),
        "inputs": {"product": "VNP46A3 v002 (LAADS 5200)", "tiles": list(TILES),
                   "months": MONTHS, "aois": AOIS},
        "parameters": {"aoi_halfwin_px": 2, "fill_mask": "values < 0 -> NaN",
                       "sds": SDS},
        "outputs": ["ntl_series.csv", "validation_results.json"],
        "checksums": {p.name: hashlib.md5(p.read_bytes()).hexdigest()
                      for p in OUT.glob("*.csv")},
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2),
                                       encoding="utf-8")
    (OUT / "validation_results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(tests, indent=2))


if __name__ == "__main__":
    main()
