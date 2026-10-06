"""METHOD-0002 v0.4 — Santa Barbara per-nucleus flaring characterization.

Pre-registered in docs/methods/METHOD-0002.md before execution.

  Data : FIRMS VIIRS N20 + S-NPP NRT, Santa Barbara box, 90-day window.
  Nuclei: single-link clusters (eps 0.01 deg ~ 1.1 km, >=5 detections).
  Metrics: detections, days detected, persistence %, mean/max FRP, day/night.
  Match : OGIM flaring detections within 1.5 km of a nucleus.
  Control: Bajo Grande box (no known flaring) -> expect no nucleus.
Outputs: data/derived/method-0002/v0.4/ (CSV/JSON + figure).
Never prints the FIRMS key. Usage: py -3 scripts/method0002_v04.py
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
OUT = ROOT / "data" / "derived" / "method-0002" / "v0.4"
RAW = ROOT / "data" / "raw" / "firms"
OGIM = ROOT / "data" / "ogim_venezuela" / "Natural_Gas_Flaring_Detections.csv"
SB_BOX = (-63.85, 9.45, -63.45, 9.80)
CTRL_BOX = (-71.78, 10.55, -71.65, 10.67)      # Bajo Grande (no known flaring)
SATS = ("VIIRS_SNPP_NRT", "VIIRS_NOAA20_NRT")
DAYS = 90
EPS = 0.01          # ~1.1 km
MIN_SAMPLES = 5
MATCH_KM = 1.5
PERSIST_FRAC = 0.30
MIN_NUCLEI = 8


def bbox_str(b):
    return f"{b[0]},{b[1]},{b[2]},{b[3]}"


def fetch(sat, box, days):
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=days - 1)
    name = f"{sat}_{days}d_{box[0]}_{box[1]}.csv"
    rawp = RAW / name
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
            frames.append(pd.read_csv(io.StringIO(t)))   # header per chunk -> parse separately
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
    df = pd.concat(frames, ignore_index=True)
    df["acq_date"] = pd.to_datetime(df["acq_date"])
    df["frp"] = pd.to_numeric(df["frp"], errors="coerce").fillna(0)
    return df


def haversine(lon1, lat1, lon2, lat2):
    p = np.pi / 180
    a = (np.sin((lat2 - lat1) * p / 2) ** 2
         + np.cos(lat1 * p) * np.cos(lat2 * p) * np.sin((lon2 - lon1) * p / 2) ** 2)
    return 2 * 6371 * np.arcsin(a ** 0.5)


def nuclei(xy, min_samples=MIN_SAMPLES, eps=EPS):
    tree = cKDTree(xy)
    pairs = np.array(list(tree.query_pairs(eps)))
    n = len(xy)
    if len(pairs) == 0:
        return np.array([-1] * n)
    g = coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(n, n))
    _, lab = connected_components(g, directed=False)
    counts = np.bincount(lab)
    small = np.where(counts < min_samples)[0]
    for k in small:
        lab[lab == k] = -1
    return lab


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    firms = load_box(SB_BOX)
    firms = firms.dropna(subset=["latitude", "longitude"])
    print(f"SB hotspots: {len(firms)} over {firms.acq_date.nunique()} days")
    xy = firms[["longitude", "latitude"]].to_numpy()
    lab = nuclei(xy)
    firms["nucleus"] = lab

    win_days = (firms.acq_date.max() - firms.acq_date.min()).days + 1
    ogim = pd.read_csv(OGIM)
    ogim_sb = ogim[(ogim.lon.between(SB_BOX[0], SB_BOX[2]))
                   & (ogim.lat.between(SB_BOX[1], SB_BOX[3]))]

    records = []
    for k in sorted(set(lab)):
        if k == -1:
            continue
        idx = np.where(lab == k)[0]
        sub = firms.iloc[idx]
        days_det = sub.acq_date.dt.date.nunique()
        # match OGIM
        matches = 0
        for _, o in ogim_sb.iterrows():
            if (haversine(sub.longitude.to_numpy(), sub.latitude.to_numpy(),
                          o.lon, o.lat) <= MATCH_KM).any():
                matches += 1
        records.append({
            "nucleus": int(k), "detections": int(len(sub)),
            "lon": round(float(sub.longitude.mean()), 5),
            "lat": round(float(sub.latitude.mean()), 5),
            "days_detected": int(days_det),
            "persistence_pct": round(100 * days_det / win_days, 1),
            "mean_frp": round(float(sub.frp.mean()), 2),
            "max_frp": round(float(sub.frp.max()), 2),
            "night_pct": round(100 * float((sub.daynight == "N").mean()), 1),
            "sats": sorted(sub.sat.unique()),
            "first_date": str(sub.acq_date.min().date()),
            "last_date": str(sub.acq_date.max().date()),
            "ogim_matched": int(matches),
        })
    records.sort(key=lambda r: r["detections"], reverse=True)
    members = [np.where(lab == k)[0] for k in sorted(set(lab)) if k != -1]

    # control
    ctrl = load_box(CTRL_BOX)
    ctrl = ctrl.dropna(subset=["latitude", "longitude"])
    cxy = ctrl[["longitude", "latitude"]].to_numpy()
    clab = nuclei(cxy) if len(cxy) else np.array([])
    ctrl_nuclei = int(len([k for k in set(clab) if k != -1])) if len(cxy) else 0

    # C3: OGIM point matched if within MATCH_KM of any hotspot in any nucleus
    ogim_matched = sum(
        1 for _, o in ogim_sb.iterrows()
        if any((haversine(xy[idx, 0], xy[idx, 1], o.lon, o.lat) <= MATCH_KM).any()
               for idx in members))
    # documented diagnostics at wider radii (not criteria)
    diag = {}
    for r in (3.0, 5.0):
        diag[f"{r}km_pct"] = round(100 * sum(
            1 for _, o in ogim_sb.iterrows()
            if any((haversine(xy[idx, 0], xy[idx, 1], o.lon, o.lat) <= r).any()
                   for idx in members)) / max(len(ogim_sb), 1), 1)
    persistent = sum(1 for r in records if r["persistence_pct"] >= 100 * PERSIST_FRAC)
    verdict = {
        "C1_structure": {"nuclei": len(records), "min_required": MIN_NUCLEI,
                         "pass": len(records) >= MIN_NUCLEI},
        "C2_persistence": {"persistent": persistent, "nuclei": len(records),
                           "pass": persistent >= 0.5 * len(records) and len(records) > 0},
        "C3_ogim_match": {"matched": ogim_matched, "ogim_in_box": int(len(ogim_sb)),
                          "pct": round(100 * ogim_matched / max(len(ogim_sb), 1), 1),
                          "threshold_pct": 70, "pass": ogim_matched >= 0.70 * max(len(ogim_sb), 1),
                          "diagnostic": diag},
        "C4_control": {"ctrl_nuclei": ctrl_nuclei, "pass": ctrl_nuclei == 0},
    }
    verdict["validated"] = all(v["pass"] for v in verdict.values() if isinstance(v, dict))

    # outputs
    with (OUT / "nuclei.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(records[0].keys()))
        w.writeheader()
        w.writerows(records)
    feats = [{"type": "Feature",
              "geometry": {"type": "Point", "coordinates": [r["lon"], r["lat"]]},
              "properties": {k: v for k, v in r.items() if k not in ("lon", "lat")}}
             for r in records]
    (OUT / "nuclei.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": feats}, indent=2), encoding="utf-8")
    piv = (firms[firms.nucleus != -1]
           .groupby([firms.acq_date.dt.date, "nucleus"]).size().unstack(fill_value=0))
    piv.to_csv(OUT / "daily_series.csv")

    figure(records)
    res = {"method": "METHOD-0002", "processing_version": "0.4.0", "run_date": str(date.today()),
           "box": SB_BOX, "control_box": CTRL_BOX, "window_days": win_days,
           "hotspots": int(len(firms)), "parameters": {"eps_deg": EPS, "min_samples": MIN_SAMPLES,
                                                       "match_km": MATCH_KM, "days": DAYS},
           "nuclei": records, "control": {"hotspots": int(len(ctrl)), "nuclei": ctrl_nuclei},
           "verdict": verdict}
    (OUT / "results.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    manifest = {"method": "METHOD-0002", "processing_version": "0.4.0",
                "pre_registration": os.environ.get("M0002_PREREG", ""), "run_date": str(date.today()),
                "inputs": {"firms": "VIIRS_SNPP_NRT + VIIRS_NOAA20_NRT area/csv",
                           "boxes": {"santa_barbara": SB_BOX, "bajo_grande": CTRL_BOX}},
                "parameters": {"days": DAYS, "eps_deg": EPS, "min_samples": MIN_SAMPLES,
                               "match_km": MATCH_KM, "persist_frac": PERSIST_FRAC},
                "checksums": {p.name: hashlib.md5(p.read_bytes()).hexdigest()
                              for p in sorted(OUT.glob("*"))
                              if p.suffix in (".csv", ".geojson", ".json") and p.name != "manifest.json"}}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"nuclei": len(records), "persistent": persistent,
                      "ogim_matched": ogim_matched, "ogim_in_box": int(len(ogim_sb)),
                      "ctrl_nuclei": ctrl_nuclei, "verdict": verdict}, indent=2))


def figure(records):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(16, 7))
    sc = ax[0].scatter([r["lon"] for r in records], [r["lat"] for r in records],
                       s=[max(20, r["detections"]) for r in records],
                       c=[r["persistence_pct"] for r in records], cmap="YlOrRd",
                       edgecolors="k", vmin=0, vmax=100)
    for r in records:
        ax[0].annotate(str(r["nucleus"]), (r["lon"], r["lat"]), fontsize=8)
    fig.colorbar(sc, ax=ax[0], label="persistence % of days")
    ax[0].set_title("Santa Barbara FIRMS nuclei (size = detections)")
    ax[0].set_xlabel("lon"); ax[0].set_ylabel("lat")
    ax[1].barh([str(r["nucleus"]) for r in records][::-1],
               [r["detections"] for r in records][::-1], color="#c0392b")
    ax[1].set_xlabel("FIRMS detections (90 days)"); ax[1].set_ylabel("nucleus")
    ax[1].set_title(f"{len(records)} nuclei, {DAYS}-day window")
    fig.suptitle("METHOD-0002 v0.4 - Santa Barbara per-nucleus flaring (NASA FIRMS)")
    fig.tight_layout()
    OUT.mkdir(parents=True, exist_ok=True)  # figures generated locally, never committed (ADR-001)
    fig.savefig(OUT / "METHOD-0002-v0.4-santabarbara.png", dpi=110)
    plt.close(fig)


if __name__ == "__main__":
    main()
