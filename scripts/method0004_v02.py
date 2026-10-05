"""METHOD-0004 v0.2 — nighttime lights: daily event test + same-month trend.

Pre-registered in docs/methods/METHOD-0004.md (commit 93b9b25, before run).

T1  CRP 5-day halt 2024-09-17..21: VNP46A2 daily, QF<=1, flare-masked with
    FIRMS VIIRS_SNPP_SP hotspots; baseline 2024-09-01..09-16 (national
    blackout 2024-08-30/31 excluded by design). Pass: |z| >= 2.
T2  Maracaibo trend: VNP46A3 monthly Aug-Oct 2023/2024/2025.
    Pass: Maracaibo 2025/2023 >= 1.5 and Valencia ratio in 0.85..1.15.
C1  Canaima: daily |z| < 2 in event window; monthly < 1 nW.
Context (not scored): Valencia daily series in T1 windows.

Secrets: .secrets/edl_token.txt, .secrets/firms_mapkey.txt (never printed).
Outputs: data/derived/method-0004/v0.2/ (CSV, JSON, PNG, GeoTIFF, manifest).
"""
import csv
import hashlib
import io
import json
import math
import os
import re
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

import numpy as np

_proj_dir = Path(sys.executable).parent / "Lib" / "site-packages" / "rasterio" / "proj_data"
if _proj_dir.exists():
    os.environ["PROJ_LIB"] = str(_proj_dir)
    os.environ["PROJ_DATA"] = str(_proj_dir)

import h5py  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived" / "method-0004" / "v0.2"
RAW_A2 = ROOT / "data" / "raw" / "vnp46a2"
RAW_A3 = ROOT / "data" / "raw" / "vnp46"
TOKEN = (ROOT / ".secrets" / "edl_token.txt").read_text().strip()
MAPKEY = (ROOT / ".secrets" / "firms_mapkey.txt").read_text().strip()
CMR = "https://cmr.earthdata.nasa.gov/search/granules.echo10"

AOI = {
    "CRP_Amuay": (-70.171, 11.773),
    "Maracaibo": (-71.61, 10.65),
    "Valencia": (-68.00, 10.18),
    "Canaima": (-62.84, 6.24),
}
T1_AOIS = ("CRP_Amuay", "Valencia", "Canaima")
BASELINE = (date(2024, 9, 1), date(2024, 9, 16))
EVENT = (date(2024, 9, 17), date(2024, 9, 21))
RECOVERY = (date(2024, 9, 22), date(2024, 9, 30))
TREND_MONTHS = [f"{y}-{m:02d}" for y in (2023, 2024, 2025) for m in (8, 9, 10)]
HALF = 2  # 5x5 px
FLARE_KM = 1.0


def tile_of(lon, lat):
    return f"h{int((lon + 180) // 10):02d}v{int((90 - lat) // 10) - 0:02d}"


def tile_bounds(name):
    h, v = map(int, re.search(r"h(\d+)v(\d+)", name).groups())
    return -180 + h * 10, 20 + (7 - v) * 10  # lon0, lat_top (VNP46 convention)


def cmr_urls(short, t0, t1, bbox):
    url = (f"{CMR}?short_name={short}&temporal={t0}T00:00:00Z/{t1}T23:59:59Z"
           f"&bounding_box={bbox}&page_size=200")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOKEN}"})
    body = urllib.request.urlopen(req, timeout=120).read().decode()
    return sorted({ln.strip()[5:-6] for ln in body.splitlines()
                   if ln.strip().startswith("<URL>https://") and ln.strip().endswith(".h5</URL>")})


def fetch(url, dest):
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOKEN}"})
    with urllib.request.urlopen(req, timeout=600) as r:
        dest.write_bytes(r.read())
    return dest


def rc(lon, lat, fname):
    lon0, lat_top = tile_bounds(fname)
    return int((lat_top - lat) / 10 * 2400), int((lon - lon0) / 10 * 2400)


def _attr(ds, key, default):
    v = ds.attrs.get(key, default)
    return float(np.ravel(v)[0]) if v is not None else default


def read_a2(path):
    """Daily NTL with CF scaling applied; QF > 1 (poor/fill) -> NaN."""
    with h5py.File(path, "r") as f:
        g = f["HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields"]
        ds = g["Gap_Filled_DNB_BRDF-Corrected_NTL"]
        raw = ds[:]
        fill = _attr(ds, "_FillValue", 65535)
        scale = _attr(ds, "scale_factor", 1.0)
        offset = _attr(ds, "add_offset", 0.0)
        qf = g["Mandatory_Quality_Flag"][:]
    ntl = raw.astype("float32") * scale + offset
    ntl[raw == fill] = np.nan
    ntl[qf > 1] = np.nan
    return ntl


def firms_sp(lon, lat, days):
    """VIIRS_SNPP_SP hotspots within FLARE_KM of AOI over the given dates."""
    bbox = f"{lon - 0.05},{lat - 0.05},{lon + 0.05},{lat + 0.05}"
    pts = []
    d = days[0]
    while d <= days[1]:
        url = (f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAPKEY}/"
               f"VIIRS_SNPP_SP/{bbox}/5/{d.isoformat()}")
        txt = urllib.request.urlopen(urllib.request.Request(
            url, headers={"User-Agent": "veio/0.2"}), timeout=120).read().decode()
        if txt.strip() and not txt.startswith("Invalid"):
            for row in csv.DictReader(io.StringIO(txt)):
                pts.append((float(row["longitude"]), float(row["latitude"])))
        d += timedelta(days=5)
    return pts


def hav(lon1, lat1, lon2, lat2):
    p = math.pi / 180
    a = (math.sin((lat2 - lat1) * p / 2) ** 2 + math.cos(lat1 * p)
         * math.cos(lat2 * p) * math.sin((lon2 - lon1) * p / 2) ** 2)
    return 2 * 6371 * math.asin(a ** 0.5)


def flare_mask(lon, lat, fname, hotspots):
    """Boolean 5x5 mask: True where pixel centre within FLARE_KM of a hotspot."""
    lon0, lat_top = tile_bounds(fname)
    r0, c0 = rc(lon, lat, fname)
    m = np.zeros((2 * HALF + 1, 2 * HALF + 1), bool)
    for i in range(-HALF, HALF + 1):
        for j in range(-HALF, HALF + 1):
            plat = lat_top - (r0 + i + 0.5) * 10 / 2400
            plon = lon0 + (c0 + j + 0.5) * 10 / 2400
            m[i + HALF, j + HALF] = any(hav(plon, plat, x, y) <= FLARE_KM for x, y in hotspots)
    return m


def run_t1():
    RAW_A2.mkdir(parents=True, exist_ok=True)
    days = [BASELINE[0] + timedelta(n) for n in range((RECOVERY[1] - BASELINE[0]).days + 1)]
    tiles = sorted({tile_of(*AOI[a]) for a in T1_AOIS})
    print(f"[T1] tiles {tiles}, {len(days)} days")
    urls = cmr_urls("VNP46A2", BASELINE[0].isoformat(), RECOVERY[1].isoformat(),
                    "-71,6,-62,12")
    by_key = {}
    for u in urls:
        m = re.search(r"\.A(\d{7})\.(h\d+v\d+)\.", u)
        if m and m.group(2) in tiles:
            by_key[(m.group(1), m.group(2))] = u
    print(f"   granules resolved: {len(by_key)} (expected ~{len(days) * len(tiles)})")

    hotspots = firms_sp(*AOI["CRP_Amuay"], (BASELINE[0], EVENT[1]))
    print(f"   FIRMS SP hotspots near Amuay (Sep 1-21 2024): {len(hotspots)}")

    rows = []
    fmask = None
    for d in days:
        doy = f"{d.year}{d.timetuple().tm_yday:03d}"
        for a in T1_AOIS:
            t = tile_of(*AOI[a])
            u = by_key.get((doy, t))
            if not u:
                rows.append({"date": d.isoformat(), "aoi": a, "raw": None, "masked": None, "n": 0})
                continue
            p = fetch(u, RAW_A2 / u.rsplit("/", 1)[-1])
            ntl = read_a2(p)
            r0, c0 = rc(*AOI[a], p.name)
            win = ntl[r0 - HALF:r0 + HALF + 1, c0 - HALF:c0 + HALF + 1]
            raw = float(np.nanmean(win)) if np.isfinite(win).any() else None
            masked = None
            if a == "CRP_Amuay":
                if fmask is None:
                    fmask = flare_mask(*AOI[a], p.name, hotspots)
                wm = np.where(fmask, np.nan, win)
                masked = float(np.nanmean(wm)) if np.isfinite(wm).any() else None
            rows.append({"date": d.isoformat(), "aoi": a, "raw": raw,
                         "masked": masked if a == "CRP_Amuay" else raw,
                         "n": int(np.isfinite(win).sum())})
    return rows, hotspots, fmask


def zscore(rows, aoi, key):
    def vals(lo, hi):
        return [r[key] for r in rows if r["aoi"] == aoi and r[key] is not None
                and lo <= date.fromisoformat(r["date"]) <= hi]
    b, e = vals(*BASELINE), vals(*EVENT)
    if len(b) < 5 or not e:
        return {"status": "insufficient_valid_days", "baseline_n": len(b), "event_n": len(e)}
    mu, sd = float(np.mean(b)), float(np.std(b, ddof=1))
    z = (float(np.mean(e)) - mu) / sd if sd > 0 else float("nan")
    return {"baseline_n": len(b), "event_n": len(e), "baseline_mean": round(mu, 2),
            "baseline_sd": round(sd, 2), "event_mean": round(float(np.mean(e)), 2),
            "z": round(z, 2), "direction": "drop" if z < 0 else "rise",
            "baseline_median": round(float(np.median(b)), 2)}


def run_t2():
    RAW_A3.mkdir(parents=True, exist_ok=True)
    out = {}
    for month in TREND_MONTHS:
        y, m = map(int, month.split("-"))
        doy = f"A{y}{(date(y, m, 1) - date(y, 1, 1)).days + 1:03d}"
        urls = cmr_urls("VNP46A3", f"{month}-01", f"{month}-28", "-72,6,-62,11")
        out[month] = {}
        for a in ("Maracaibo", "Valencia", "Canaima"):
            t = tile_of(*AOI[a])
            u = next((x for x in urls if f".{doy}." in x and f".{t}." in x), None)
            if not u:
                out[month][a] = None
                continue
            p = fetch(u, RAW_A3 / u.rsplit("/", 1)[-1])
            with h5py.File(p, "r") as f:
                d = f["HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/NearNadir_Composite_Snow_Free"][:]
            d = np.where(d < 0, np.nan, d.astype("float32"))
            r0, c0 = rc(*AOI[a], p.name)
            out[month][a] = float(np.nanmean(d[r0 - HALF:r0 + HALF + 1, c0 - HALF:c0 + HALF + 1]))
        print(f"   {month}: " + ", ".join(f"{k}={v:.1f}" if v is not None else f"{k}=NA"
                                         for k, v in out[month].items()))
    return out


def plot_t1(rows, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    for k, a in enumerate(T1_AOIS):
        sel = [r for r in rows if r["aoi"] == a]
        x = [date.fromisoformat(r["date"]) for r in sel]
        ax[k].plot(x, [r["raw"] if r["raw"] is not None else np.nan for r in sel],
                   "o-", label="raw", color="0.6")
        if a == "CRP_Amuay":
            ax[k].plot(x, [r["masked"] if r["masked"] is not None else np.nan for r in sel],
                       "o-", label="flare-masked", color="tab:red")
        ax[k].axvspan(EVENT[0], EVENT[1], color="orange", alpha=0.25, label="halt 09-17..21")
        ax[k].set_ylabel(f"{a}\nnW/cm²/sr")
        ax[k].legend(loc="upper right", fontsize=8)
    ax[0].set_title("METHOD-0004 v0.2 T1 — VNP46A2 daily NTL, Sep 2024 (QF<=1)")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def plot_t2(trend, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 5))
    for a, c in (("Maracaibo", "tab:red"), ("Valencia", "tab:blue"), ("Canaima", "0.5")):
        ys = [trend[m][a] if trend[m][a] is not None else np.nan for m in TREND_MONTHS]
        ax.plot(TREND_MONTHS, ys, "o-", color=c, label=a)
    ax.set_ylabel("nW/cm²/sr (5x5 px mean)")
    ax.set_title("METHOD-0004 v0.2 T2 — VNP46A3 monthly, same months Aug-Oct 2023/24/25")
    ax.legend()
    plt.xticks(rotation=45)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def change_map(path_tif, path_png):
    """Maracaibo-basin NTL change Aug-Oct 2025 vs 2023 (h10v07), GeoTIFF + PNG."""
    import rasterio
    from rasterio.transform import from_origin
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def mean_year(y):
        arrs = []
        for m in (8, 9, 10):
            doy = f"A{y}{(date(y, m, 1) - date(y, 1, 1)).days + 1:03d}"
            hits = sorted(RAW_A3.glob(f"VNP46A3.{doy}.h10v07.*.h5"))
            if hits:
                with h5py.File(hits[0], "r") as f:
                    d = f["HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/NearNadir_Composite_Snow_Free"][:]
                arrs.append(np.where(d < 0, np.nan, d.astype("float32")))
        return np.nanmean(np.stack(arrs), axis=0) if arrs else None

    a23, a25 = mean_year(2023), mean_year(2025)
    if a23 is None or a25 is None:
        return None
    # crop to Venezuela west: lon -73.5..-70, lat 8..12.6 inside h10v07 (lon -80..-70, lat 10..20)
    lon0, lat_top = -80.0, 20.0
    px = 2400 / 10
    r0, r1 = int((lat_top - 12.6) * px), int((lat_top - 10.0) * px)
    c0, c1 = int((-73.5 - lon0) * px), int((-70.0 - lon0) * px)
    d23, d25 = a23[r0:r1, c0:c1], a25[r0:r1, c0:c1]
    diff = d25 - d23
    tr = from_origin(lon0 + c0 / px, lat_top - r0 / px, 1 / px, 1 / px)
    with rasterio.open(path_tif, "w", driver="GTiff", height=diff.shape[0], width=diff.shape[1],
                       count=1, dtype="float32", crs="EPSG:4326", transform=tr,
                       compress="deflate", nodata=np.nan) as dst:
        dst.write(diff.astype("float32"), 1)
    ext = [tr.c, tr.c + diff.shape[1] / px, tr.f - diff.shape[0] / px, tr.f]
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    ax[0].imshow(np.log1p(np.nan_to_num(d25)), extent=ext, cmap="magma")
    ax[0].set_title("NTL Aug-Oct 2025 (log1p)")
    v = np.nanpercentile(np.abs(diff), 99)
    im = ax[1].imshow(diff, extent=ext, cmap="RdBu_r", vmin=-v, vmax=v)
    ax[1].set_title("Change 2025 − 2023 (Aug-Oct mean), nW/cm²/sr")
    for a_ in ax:
        a_.plot(*AOI["Maracaibo"], "y+", ms=14, mew=2)
    fig.colorbar(im, ax=ax[1], fraction=0.046)
    fig.tight_layout()
    fig.savefig(path_png, dpi=110)
    plt.close(fig)
    return tr


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = {}

    rows, hotspots, fmask = run_t1()
    with (OUT / "t1_daily.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["date", "aoi", "raw", "masked", "n"])
        w.writeheader()
        w.writerows(rows)
    results["T1"] = {
        "CRP_Amuay_masked": zscore(rows, "CRP_Amuay", "masked"),
        "CRP_Amuay_raw": zscore(rows, "CRP_Amuay", "raw"),
        "Valencia_context": zscore(rows, "Valencia", "raw"),
        "Canaima_C1": zscore(rows, "Canaima", "raw"),
        "firms_sp_hotspots": len(hotspots),
        "flare_masked_pixels": int(fmask.sum()) if fmask is not None else None,
    }
    plot_t1(rows, OUT / "t1_daily.png")

    trend = run_t2()
    results["T2"] = {"series": trend}
    def ymean(a, y):
        v = [trend[f"{y}-{m:02d}"][a] for m in (8, 9, 10) if trend[f"{y}-{m:02d}"][a] is not None]
        return float(np.mean(v)) if v else None
    for a in ("Maracaibo", "Valencia", "Canaima"):
        results["T2"][a] = {str(y): ymean(a, y) for y in (2023, 2024, 2025)}
    plot_t2(trend, OUT / "t2_trend.png")
    change_map(OUT / "ntl_change_2025_vs_2023_west.tif", OUT / "ntl_change_2025_vs_2023_west.png")

    (OUT / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    manifest = {
        "method": "METHOD-0004", "processing_version": "0.2.0",
        "pre_registration_commit": "93b9b25", "run_date": str(date.today()),
        "inputs": {"VNP46A2": "LAADS v002 daily, CMR-resolved", "VNP46A3": "LAADS v002 monthly",
                   "FIRMS": "VIIRS_SNPP_SP area API", "aois": AOI},
        "parameters": {"baseline": [str(x) for x in BASELINE], "event": [str(x) for x in EVENT],
                       "qf_max": 1, "aoi_px": 2 * HALF + 1, "flare_km": FLARE_KM,
                       "trend_months": TREND_MONTHS},
        "checksums": {p.name: hashlib.md5(p.read_bytes()).hexdigest()
                      for p in sorted(OUT.glob("*")) if p.suffix in (".csv", ".json", ".tif")
                      and p.name != "manifest.json"},
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in results.items() if k != "T2"} |
                     {"T2": {k: v for k, v in results["T2"].items() if k != "series"}}, indent=1))


if __name__ == "__main__":
    main()
