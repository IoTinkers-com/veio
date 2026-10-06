"""METHOD-0001 v0.3 — interannual same-month dNBR (land change).

Pre-registered in docs/methods/METHOD-0001.md before execution:
  T-fire  Jose complex (10.069/-64.864): Dec2024-Jan2025 vs Dec2025-Jan2026
  C-urban Valencia urban control, same windows
  T-neg   Bajo Grande (inactive since 2018-11): expect no change
Reuse of the v0.2 pipeline (same masking, grid, thresholds).

Usage: py -3 scripts/method0001_v03.py
Outputs: data/derived/method-0001/v0.3/ (rasters + quicklook figures).
"""
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import method0001_v02 as base  # noqa: E402

import numpy as np  # noqa: E402
from rasterio.transform import from_origin  # noqa: E402

OUT = base.ROOT / "data" / "derived" / "method-0001" / "v0.3"
WINDOWS = {"pre": ("2024-12-01", "2025-01-31"), "post": ("2025-12-01", "2026-01-31")}
TESTS = {
    "T-fire": {"box": (-64.914, 10.019, -64.814, 10.119), "detector": "dnbr",
               "rgb": True, "label": "Petrocedeno fire (interannual same-month)"},
    "C-urban": {"box": (-68.05, 10.13, -67.95, 10.23), "detector": "dnbr",
                "rgb": False, "label": "Valencia urban control"},
    "T-neg": {"box": (-71.764, 10.559, -71.664, 10.659), "detector": "dnbr",
              "rgb": True, "label": "Bajo Grande negative control"},
}


def run(test_id):
    cfg = TESTS[test_id]
    box = cfg["box"]
    transform, w, h = base.grid(box)
    bands = ["B08", "B12"] + (["B04", "B03", "B02"] if cfg["rgb"] else [])
    print(f"[{test_id}] {cfg['label']} grid {w}x{h}")
    pre, n_pre, ids_pre = base.scene_stack(box, WINDOWS["pre"], bands)
    post, n_post, ids_post = base.scene_stack(box, WINDOWS["post"], bands)
    print(f"   scenes pre/post: {n_pre}/{n_post}")
    res = {"test": test_id, "label": cfg["label"], "box": box,
           "windows": WINDOWS, "scenes_pre": n_pre, "scenes_post": n_post,
           "scene_ids_pre": ids_pre, "scene_ids_post": ids_post}
    if pre is None or post is None:
        res["status"] = "insufficient_scenes"
        return res

    nbr = lambda m: (m["B08"] - m["B12"]) / (m["B08"] + m["B12"] + 1e-6)  # noqa: E731
    land = (pre["_water_frac"] < 0.5) & (post["_water_frac"] < 0.5)
    delta = nbr(pre) - nbr(post)
    delta_masked = np.where(land, delta, np.nan)
    mask = land & (delta >= base.THR_DNBR)
    feats, _ = base.components(mask, (4, 10**9), delta_masked, transform)

    res.update({
        "valid_pixels": int(np.isfinite(delta_masked).sum()),
        "pixels_over_threshold": int(mask.sum()),
        "pct_over_threshold": round(100 * mask.sum() / max(int(np.isfinite(delta_masked).sum()), 1), 3),
        "components": len(feats),
        "candidates": feats,
    })

    OUT.mkdir(parents=True, exist_ok=True)
    base.write_tif(OUT / f"{test_id}_change.tif", delta_masked, transform)
    (OUT / f"{test_id}_candidates.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": feats}), encoding="utf-8")
    if cfg["rgb"]:
        rgb_pre, rgb_post = base.rgb_u8(pre, post)
        base.write_tif(OUT / f"{test_id}_rgb_pre.tif", rgb_pre, transform, "uint8", 0)
        base.write_tif(OUT / f"{test_id}_rgb_post.tif", rgb_post, transform, "uint8", 0)
        FIGS = OUT  # figures are generated locally, never committed (ADR-001)
        FIGS.mkdir(parents=True, exist_ok=True)
        base.quicklook(FIGS / f"{test_id}_quicklook.png", rgb_pre, rgb_post,
                       delta_masked, feats, transform,
                       f"METHOD-0001 v0.3 {test_id}: {cfg['label']}", base.THR_DNBR)
    return res


def main():
    allres = {}
    for t in TESTS:
        allres[t] = run(t)
        slim = {k: v for k, v in allres[t].items()
                if k not in ("candidates", "scene_ids_pre", "scene_ids_post")}
        print(json.dumps(slim, indent=1))
        (OUT / f"{t}_results.json").write_text(json.dumps(allres[t], indent=2),
                                               encoding="utf-8")
    verdict = {
        "T-fire": bool(allres["T-fire"].get("components", 0) >= 1),
        "C-urban": bool(allres["C-urban"].get("components", 99) <= 1
                        and allres["C-urban"].get("pct_over_threshold", 99) < 0.5),
        "T-neg": bool(allres["T-neg"].get("pct_over_threshold", 99) < 0.5),
    }
    verdict["validated"] = all(verdict.values())
    allres["verdict"] = verdict
    manifest = {
        "method": "METHOD-0001", "processing_version": "0.3.0",
        "pre_registration_commit": "93b9b25", "run_date": str(date.today()),
        "windows": WINDOWS, "tests": TESTS,
        "parameters": {"res_deg": base.RES, "max_scenes": base.MAX_SCENES,
                       "thr_dnbr": base.THR_DNBR},
        "checksums": {p.name: hashlib.md5(p.read_bytes()).hexdigest()
                      for p in sorted(OUT.glob("*")) if p.suffix != ".json"},
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (OUT / "results.json").write_text(json.dumps(allres, indent=2), encoding="utf-8")
    print("VERDICT:", json.dumps(verdict))


if __name__ == "__main__":
    main()
