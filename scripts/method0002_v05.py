"""METHOD-0002 v0.5 — Santa Barbara nuclei: fixed, persistent, night-active sources.

Pre-registered in docs/methods/METHOD-0002.md before execution.

Builds on v0.4. Adds the discriminators that separate industrial flaring from
biomass burning (persistence + stationarity + night fraction) and reports
integrated FRP. OGIM co-location is descriptive (its coordinates are coarse:
within-facility spread up to ~17 km), not a pass/fail criterion.

Outputs: data/derived/method-0002/v0.5/ + figure. Usage: py -3 scripts/method0002_v05.py
"""
import csv
import hashlib
import io
import json
import os
import urllib.request
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

ROOT = Path(__file__).resolve().parents[1]
KEY = (ROOT / ".secrets" / "firms_mapkey.txt").read_text().strip()
OUT = ROOT / "data" / "derived" / "method-0002" / "v0.5"
RAW = ROOT / "data" / "raw" / "firms"
OGIM = ROOT / "data" / "ogim_venezuela" / "Natural_Gas_Flaring_Detections.csv"
FIGS = ROOT / "docs" / "methods" / "figures"
SB_BOX = (-63.85, 9.45, -63.45, 9.80)
CTRL_BOX = (-71.78, 10.55, -71.65, 10.67)
SATS = ("VIIRS_SNPP_NRT", "VIIRS_NOAA20_NRT")
DAYS = 90
EPS, MIN_SAMPLES = 0.01, 5
PERSIST_FRAC, STATION_KM, NIGHT_PCT, MIN_NUCLEI, STATION_MIN_FRAC = 0.30, 1.0, 50, 8, 0.80


def bbox_str(b):
    return f"{b[0]},{b[1]},{b[2]},{b[3]}"


def fetch(sat, box, days):
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=days - 1)
    rawp = RAW / f"{sat}_{days}d_{box[0]}_{box[1]}.csv"
    if rawp.exists():
        return pd.read_csv(rawp)
    frames = []
    d = start
    while d <= end:
        ce = min(d + timedelta(days=4), end)
        url = (f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
               f"{KEY}/{sat}/{bbox_str(box)}/5/{d.isoformat()}")
        with urllib.request.urlopen(urllib.request.Request(url), timeout=120) as r:
            t = r.read().decode()
        if "Invalid" in t[:80] or "MAP_KEY" in t[:80]:
            raise RuntimeError("FIRMS API rejected the key")
        if t.strip():
            frames.append(pd.read_csv(io.StringIO(t)))   # per-chunk headers
        d = ce + timedelta(days=1)
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(rawp, index=False)
    return df


def load_box(box):
    frames = []
    for sat in SATS:
        df = fetch(sat, box, DAYS)
        df["sat"] = sat.replace("VIIRS_", "").replace("_NRT", "")
        frames.append(df)
    df = pd.concat(frames, ignore_index=True).dropna(subset=["latitude", "longitude"])
    df["acq_date"] = pd.to_datetime(df["acq_date"])
    df["frp"] = pd.to_numeric(df["frp"], errors="coerce").fillna(0)
    return df


def km(lon1, lat1, lon2, lat2):
    p = np.pi / 180
    a = (np.sin((lat2 - lat1) * p / 2) ** 2
         + np.cos(lat1 * p) * np.cos(lat2 * p) * np.sin((lon2 - lon1) * p / 2) ** 2)
    return 2 * 6371 * np.arcsin(a ** 0.5)


def cluster(xy, min_samples=MIN_SAMPLES, eps=EPS):
    tree = cKDTree(xy)
    pairs = np.array(list(tree.query_pairs(eps)))
    if len(pairs) == 0:
        return np.array([-1] * len(xy))
    g = coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(len(xy), len(xy)))
    _, lab = connected_components(g, directed=False)
    cnt = np.bincount(lab)
    for k in np.where(cnt < min_samples)[0]:
        lab[lab == k] = -1
    return lab


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    firms = load_box(SB_BOX)
    xy = firms[["longitude", "latitude"]].to_numpy()
    lab = cluster(xy)
    firms["nucleus"] = lab
    win_days = (firms.acq_date.max() - firms.acq_date.min()).days + 1

    ogim = pd.read_csv(OGIM)
    og = ogim[(ogim.lon.between(SB_BOX[0], SB_BOX[2]))
              & (ogim.lat.between(SB_BOX[1], SB_BOX[3]))]

    records = []
    for k in sorted(set(lab)):
        if k == -1:
            continue
        sub = firms[firms.nucleus == k]
        cx, cy = sub.longitude.mean(), sub.latitude.mean()
        disps = [km(grp.longitude.mean(), grp.latitude.mean(), cx, cy)
                 for _, grp in sub.groupby(sub.acq_date.dt.date)]
        disp_med = float(np.median(disps)) if disps else 0.0
        disp_max = float(np.max(disps)) if disps else 0.0
        records.append({
            "nucleus": int(k), "detections": int(len(sub)),
            "lon": round(float(cx), 5), "lat": round(float(cy), 5),
            "days_detected": int(sub.acq_date.dt.date.nunique()),
            "persistence_pct": round(100 * sub.acq_date.dt.date.nunique() / win_days, 1),
            "mean_frp": round(float(sub.frp.mean()), 2),
            "max_frp": round(float(sub.frp.max()), 2),
            "total_frp_mw": round(float(sub.frp.sum()), 0),
            "night_pct": round(100 * float((sub.daynight == "N").mean()), 1),
            "centroid_drift_med_km": round(disp_med, 2),
            "centroid_drift_max_km": round(disp_max, 2),
            "sats": sorted(sub.sat.unique()),
            "first_date": str(sub.acq_date.min().date()),
            "last_date": str(sub.acq_date.max().date()),
        })
    records.sort(key=lambda r: r["detections"], reverse=True)
    members = [xy[lab == k] for k in sorted(set(lab)) if k != -1]
    persistent = [r for r in records if r["persistence_pct"] >= 100 * PERSIST_FRAC]
    stationary = [r for r in persistent if r["centroid_drift_med_km"] <= STATION_KM]

    # OGIM precision + descriptive co-location
    spreads = {}
    for name, grp in og.groupby("FAC_NAME"):
        pts = grp[["lon", "lat"]].to_numpy()
        if len(pts) >= 2:
            spreads[name] = round(max(km(pts[i, 0], pts[i, 1], pts[j, 0], pts[j, 1])
                                       for i in range(len(pts)) for j in range(i + 1, len(pts))), 2)
    coloc = {}
    for r in (1.5, 3.0, 5.0):
        coloc[f"{r}km_pct"] = round(100 * sum(
            1 for _, o in og.iterrows()
            if any((km(m[:, 0], m[:, 1], o.lon, o.lat) <= r).any() for m in members))
            / max(len(og), 1), 1)

    ctrl = load_box(CTRL_BOX)
    cxy = ctrl[["longitude", "latitude"]].to_numpy()
    clab = cluster(cxy) if len(cxy) else np.array([])
    ctrl_nuclei = int(len([k for k in set(clab) if k != -1])) if len(cxy) else 0

    med_night = float(np.median([r["night_pct"] for r in persistent])) if persistent else 0
    verdict = {
        "C1_structure": {"nuclei": len(records), "min": MIN_NUCLEI, "pass": len(records) >= MIN_NUCLEI},
        "C2_persistence": {"persistent": len(persistent), "nuclei": len(records),
                           "pass": len(persistent) >= 0.5 * len(records) and records != []},
        "C3_stationarity": {"stationary": len(stationary), "persistent": len(persistent),
                            "threshold_km": STATION_KM,
                            "pass": len(stationary) >= STATION_MIN_FRAC * max(len(persistent), 1)},
        "C4_night_activity": {"median_night_pct": round(med_night, 1), "threshold": NIGHT_PCT,
                              "pass": med_night >= NIGHT_PCT},
        "C5_control": {"ctrl_nuclei": ctrl_nuclei, "pass": ctrl_nuclei == 0},
        "ogim_colocation_descriptive": {"pct": coloc, "within_facility_spread_km": spreads},
    }
    verdict["validated"] = all(v["pass"] for k, v in verdict.items()
                               if k.startswith("C") and isinstance(v, dict))

    with (OUT / "nuclei.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(records[0].keys()))
        w.writeheader(); w.writerows(records)
    feats = [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [r["lon"], r["lat"]]},
              "properties": {k: v for k, v in r.items() if k not in ("lon", "lat")}} for r in records]
    (OUT / "nuclei.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": feats}, indent=2), encoding="utf-8")
    (firms[firms.nucleus != -1].groupby([firms.acq_date.dt.date, "nucleus"]).size()
     .unstack(fill_value=0).to_csv(OUT / "daily_series.csv"))

    res = {"method": "METHOD-0002", "processing_version": "0.5.0", "run_date": str(date.today()),
           "box": SB_BOX, "control_box": CTRL_BOX, "window_days": win_days,
           "hotspots": int(len(firms)), "nuclei": records, "verdict": verdict,
           "ogim_box": int(len(og))}
    (OUT / "results.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    manifest = {"method": "METHOD-0002", "processing_version": "0.5.0",
                "pre_registration": os.environ.get("M0002_PREREG", ""), "run_date": str(date.today()),
                "inputs": {"firms": "VIIRS_SNPP_NRT + VIIRS_NOAA20_NRT area/csv, 90 d",
                           "ogim": "Natural_Gas_Flaring_Detections.csv (DS-0012, 2026-09-14)"},
                "parameters": {"days": DAYS, "eps_deg": EPS, "min_samples": MIN_SAMPLES,
                               "persist_frac": PERSIST_FRAC, "station_km": STATION_KM,
                               "night_pct": NIGHT_PCT},
                "checksums": {p.name: hashlib.md5(p.read_bytes()).hexdigest()
                              for p in sorted(OUT.glob("*"))
                              if p.suffix in (".csv", ".geojson", ".json") and p.name != "manifest.json"}}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    figure(records)
    print(json.dumps({"nuclei": len(records), "persistent": len(persistent),
                      "stationary": len(stationary), "median_night_pct": round(med_night, 1),
                      "ctrl_nuclei": ctrl_nuclei, "ogim_colocation": coloc,
                      "verdict": verdict["validated"]}, indent=2))


def figure(records):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(16, 7))
    sc = ax[0].scatter([r["lon"] for r in records], [r["lat"] for r in records],
                       s=[max(20, r["detections"]) for r in records],
                       c=[r["night_pct"] for r in records], cmap="plasma",
                       edgecolors="k", vmin=0, vmax=100)
    for r in records:
        ax[0].annotate(str(r["nucleus"]), (r["lon"], r["lat"]), fontsize=8)
    fig.colorbar(sc, ax=ax[0], label="night detections %")
    ax[0].set_title("Santa Barbara nuclei (size = detections, colour = night %)")
    ax[0].set_xlabel("lon"); ax[0].set_ylabel("lat")
    ax[1].scatter([r["persistence_pct"] for r in records],
                  [r["centroid_drift_med_km"] for r in records],
                  s=[max(20, r["detections"]) for r in records], c="#c0392b", edgecolors="k")
    for r in records:
        ax[1].annotate(str(r["nucleus"]), (r["persistence_pct"], r["centroid_drift_med_km"]), fontsize=8)
    ax[1].axhline(STATION_KM, ls="--", c="gray", label=f"{STATION_KM} km drift")
    ax[1].set_xlabel("persistence % of days"); ax[1].set_ylabel("median daily-centroid drift (km)")
    ax[1].set_title("Fixed sources = high persistence, low drift"); ax[1].legend()
    fig.suptitle("METHOD-0002 v0.5 - Santa Barbara nuclei: fixed, persistent, night-active (NASA FIRMS)")
    fig.tight_layout()
    FIGS.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGS / "METHOD-0002-v0.5-santabarbara.png", dpi=110)
    plt.close(fig)


if __name__ == "__main__":
    main()
