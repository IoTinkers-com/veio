"""METHOD-0002 validation — FIRMS hotspot time series (VEIO).

Reads a FIRMS MapKey from .secrets/firms_mapkey.txt (never printed),
queries the FIRMS area_csv API for the Venezuela bbox over the last
N days (max 1 year back), and validates the METHOD-0002 hypothesis:

  1. Site test:      hotspot presence at >=80% of OGIM flaring sites.
  2. Density test:   Santa Barbara cluster counts.
  3. Differential:   CRP (active per sources) >> Bajo Grande (inactive).
  4. Controls:       2 no-flaring AOIs, persistence <10%.

Outputs: data/derived/method-0002/ (CSV + manifest). Never prints the key.
"""
import csv
import hashlib
import io
import json
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
KEY_FILE = ROOT / ".secrets" / "firms_mapkey.txt"
OUT = ROOT / "data" / "derived" / "method-0002"
RAW = ROOT / "data" / "raw" / "firms"
OGIM = ROOT / "data" / "ogim_venezuela"

VE_BBOX = "-73.5,0.5,-59.5,12.6"  # lon_min,lat_min,lon_max,lat_max
DAYS_BACK = 30  # NRT API window (<=365)
RADIUS_KM = 1.5  # match radius >= ~4 VIIRS pixels

ASSETS = {  # name -> (lon, lat)  [DS-0012 / registry]
    "CRP_Amuay": (-70.171, 11.773),
    "CRP_Cardon": (-70.175, 11.841),
    "Bajo_Grande": (-71.714, 10.609),
    "El_Palito": (-68.136, 10.452),
    "Jose_TAECJAA": (-64.646, 10.216),
}
CONTROLS = {  # no known O&G flaring
    "CTRL_Cariaco": (-64.33, 10.48),
    "CTRL_Chichiriviche": (-68.27, 11.45),
}


def haversine_km(lon1, lat1, lon2, lat2):
    import math
    p = math.pi / 180
    a = (math.sin((lat2 - lat1) * p / 2) ** 2
         + math.cos(lat1 * p) * math.cos(lat2 * p)
         * math.sin((lon2 - lon1) * p / 2) ** 2)
    return 2 * 6371 * math.asin(a ** 0.5)


def fetch_firms(satellite: str) -> pd.DataFrame:
    """FIRMS area_csv: DAY_RANGE is 1..5 per request with optional start DATE."""
    key = KEY_FILE.read_text().strip()
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=DAYS_BACK - 1)
    parts = []
    d = start
    while d <= end:
        chunk_end = min(d + timedelta(days=4), end)
        url = (f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
               f"{key}/{satellite}/{VE_BBOX}/5/{d.isoformat()}")
        req = urllib.request.Request(url,
                                     headers={"User-Agent": "veio-method0002/0.1"})
        with urllib.request.urlopen(req, timeout=120) as r:
            text = r.read().decode()
        if "Invalid" in text[:60] or "MAP_KEY" in text[:60]:
            raise RuntimeError(f"FIRMS API rejected the key: {text[:80]}")
        parts.append(text)
        d = chunk_end + timedelta(days=1)
    (RAW / f"{satellite}_{DAYS_BACK}d.csv").write_text(
        "".join(p if p.endswith("\n") else p + "\n" for p in parts),
        encoding="utf-8")
    dfs = [pd.read_csv(io.StringIO(p)) for p in parts if p.strip()]
    return pd.concat(dfs, ignore_index=True)


def main():
    key_ok = KEY_FILE.exists() and KEY_FILE.read_text().strip()
    if not key_ok:
        sys.exit("MapKey file missing: .secrets/firms_mapkey.txt")

    ogim = pd.read_csv(OGIM / "Natural_Gas_Flaring_Detections.csv")
    sites = (ogim.groupby("FAC_NAME")[["lon", "lat"]]
             .mean().reset_index())
    print(f"OGIM flaring sites (unique names): {len(sites)}")

    raw_files = sorted(RAW.glob("*_30d.csv"))
    if len(raw_files) >= 2:
        print("reusing raw downloads (offline re-run)")
        frames = []
        for p in raw_files:
            df = pd.read_csv(p)
            df["satellite"] = ("VIIRS_SNPP_NRT" if "snpp" in p.name.lower()
                               or "SNPP" in p.name else "VIIRS_NOAA20_NRT")
            frames.append(df)
    else:
        frames = []
        for sat in ("VIIRS_SNPP_NRT", "VIIRS_NOAA20_NRT"):
            df = fetch_firms(sat)
            df["satellite"] = sat
            frames.append(df)
            print(f"{sat}: {len(df)} hotspots fetched")
    firms = pd.concat(frames, ignore_index=True)
    firms["acq_date"] = pd.to_datetime(firms["acq_date"])

    for radius in (1.5, 5.0):
        results = run_validation(firms, sites, radius)
        (OUT / f"validation_results_v0.3.0_r{radius}.json").write_text(
            json.dumps(results, indent=2), encoding="utf-8")
        print(f"--- radius {radius} km ---")
        print(json.dumps(results, indent=2))


def run_validation(firms, sites, radius):
    results = {"radius_km": radius}
    hit = 0
    for _, s in sites.iterrows():
        d = firms.apply(lambda r: haversine_km(r.longitude, r.latitude,
                                               s.lon, s.lat), axis=1)
        if (d <= radius).any():
            hit += 1
    results["site_test"] = {"sites": len(sites), "hit": hit,
                            "pct": round(100 * hit / len(sites), 1),
                            "threshold": 80}

    sb = sites[sites.FAC_NAME.str.contains("SANTA BARBARA")]
    n_sb = 0
    for _, s in sb.iterrows():
        d = firms.apply(lambda r: haversine_km(r.longitude, r.latitude,
                                               s.lon, s.lat), axis=1)
        n_sb += int((d <= radius).sum())
    results["density_test"] = {"sb_sites": len(sb), "hotspots_matched": n_sb}

    for name, (lon, lat) in ASSETS.items():
        d = firms.apply(lambda r: haversine_km(r.longitude, r.latitude,
                                               lon, lat), axis=1)
        sub = firms[d <= radius]
        results.setdefault("differential", {})[name] = {
            "hotspots": int(len(sub)),
            "days_with_hotspot": int(sub.acq_date.nunique()),
        }

    for name, (lon, lat) in CONTROLS.items():
        d = firms.apply(lambda r: haversine_km(r.longitude, r.latitude,
                                               lon, lat), axis=1)
        sub = firms[d <= radius]
        results.setdefault("controls", {})[name] = {
            "hotspots": int(len(sub)),
            "pct_days": round(100 * sub.acq_date.nunique() / DAYS_BACK, 1),
        }
    return results


def write_manifest():
    OUT.mkdir(parents=True, exist_ok=True)
    firms_ve = pd.concat(
        [pd.read_csv(p) for p in sorted(RAW.glob("*_30d.csv"))],
        ignore_index=True)
    firms_ve = firms_ve[firms_ve.latitude != "latitude"]
    for c in ("latitude", "longitude"):
        firms_ve[c] = pd.to_numeric(firms_ve[c], errors="coerce")
    firms_ve = firms_ve.dropna(subset=["latitude", "longitude"])
    firms_ve = firms_ve[(firms_ve.longitude >= -73.5)
                        & (firms_ve.longitude <= -59.5)
                        & (firms_ve.latitude >= 0.5)
                        & (firms_ve.latitude <= 12.6)]
    firms_ve.to_csv(OUT / "firms_ve_hotspots.csv", index=False)
    manifest = {
        "method": "METHOD-0002",
        "processing_version": "0.3.0",
        "run_date": str(date.today()),
        "history": [
            "v0.1.0 r=1.5 km, midpoint AOI: FAILED site test (36.4%<80%), "
            "differential null (CRP 0 vs BajoGrande 0).",
            "v0.2.0 r=1.5+5 km: site 66.2%<80%; CRP 0 traced to midpoint-AOI "
            "artifact (mean of Amuay/Cardon OGIM points falls between the "
            "refineries); raw-file join bug found (glued header rows).",
            "v0.3.0 per-facility AOIs (Amuay, Cardon separate), newline-safe "
            "raw write; criteria unchanged (site>=80%, controls<10%).",
        ],
        "inputs": {
            "firms_api": "area/csv VIIRS_SNPP_NRT + VIIRS_NOAA20_NRT, "
                         f"bbox {VE_BBOX}, last {DAYS_BACK}d (5-day chunks)",
            "ogim": "data/ogim_venezuela/Natural_Gas_Flaring_Detections.csv "
                    "(DS-0012, SRC_DATE 2026-09-14)",
        },
        "parameters": {"radii_km": [1.5, 5.0], "days_back": DAYS_BACK,
                       "site_threshold_pct": 80, "control_threshold_pct": 10},
        "outputs": ["validation_results_v0.3.0_r1.5.json",
                    "validation_results_v0.3.0_r5.0.json",
                    "firms_ve_hotspots.csv"],
        "checksums": {p.name: hashlib.md5(p.read_bytes()).hexdigest()
                      for p in OUT.glob("*.csv")},
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2),
                                       encoding="utf-8")


if __name__ == "__main__":
    main()
    write_manifest()
