"""METHOD-0003 screening — wide eastern-lake map of new persistent bright objects.

Discovery only: finds where new bright radar objects appeared Sep-Dec 2025 vs
Jun-Aug 2025, to place the pre-registered AOI on evidence rather than a guess.
"""
import os
import time
from pathlib import Path

import numpy as np

_proj = Path(os.sys.executable).parent / "Lib" / "site-packages" / "rasterio" / "proj_data"
if _proj.exists():
    os.environ["PROJ_LIB"] = str(_proj); os.environ["PROJ_DATA"] = str(_proj)
os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
os.environ.setdefault("GDAL_HTTP_MULTIRANGE", "YES")

import planetary_computer  # noqa: E402
import rasterio  # noqa: E402
from pystac_client import Client  # noqa: E402
from rasterio.enums import Resampling  # noqa: E402
from rasterio.transform import from_origin  # noqa: E402
from rasterio.vrt import WarpedVRT  # noqa: E402
from scipy import ndimage  # noqa: E402

BOX = (-71.60, 9.55, -71.05, 10.45)   # eastern Lake Maracaibo (costa oriental)
RES = 0.0005                          # ~55 m
TMP = Path(r"C:\Users\hecto\AppData\Local\Temp\opencode")
CACHE = TMP / "m0003_cache" / "SCREEN"
BRIGHT = -8.0


def grid():
    lon0, lat0, lon1, lat1 = BOX
    return from_origin(lon0, lat1, RES, RES), int(round((lon1-lon0)/RES)), int(round((lat1-lat0)/RES))


def read_db(item, transform, w, h):
    with rasterio.open(item.assets["vv"].href) as src:
        with WarpedVRT(src, crs="EPSG:4326", transform=transform, width=w, height=h,
                       resampling=Resampling.nearest, src_nodata=-32768, nodata=-32768) as vrt:
            lin = vrt.read(1).astype("float64")
    lin[lin <= 0] = np.nan
    return (10*np.log10(lin)).astype("float32")


def main():
    c = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
    items = list(c.search(collections=["sentinel-1-rtc"], bbox=BOX,
                          datetime="2025-06-01/2025-12-31").items())
    sel = sorted([i for i in items if i.properties.get("sat:relative_orbit") == 171
                  and i.properties.get("sat:orbit_state") == "descending"
                  and i.properties.get("platform", "").lower() == "sentinel-1a"],
                 key=lambda i: i.datetime)
    transform, w, h = grid()
    CACHE.mkdir(parents=True, exist_ok=True)
    recs = []
    for it in sel:
        p = CACHE / (it.id + ".npy")
        if p.exists():
            a = np.load(p)
        else:
            t0 = time.time()
            a = read_db(planetary_computer.sign(it), transform, w, h)
            np.save(p, a)
            print(f"   read {it.datetime:%m-%d} {time.time()-t0:.0f}s")
        recs.append((it.datetime.strftime("%Y-%m-%d"), a))
    is_pre = np.array([d <= "2025-08-20" for d, _ in recs])
    st = np.stack([a for _, a in recs])
    dates = [d for d, _ in recs]
    pre, post = st[is_pre], st[~is_pre]
    mp = np.nanmedian(pre, axis=0); ms = np.nanmedian(post, axis=0)
    pre_frac = np.nanmean(pre >= BRIGHT, axis=0)
    post_frac = np.nanmean(post >= BRIGHT, axis=0)
    mask = (pre_frac <= 0.0) & (post_frac >= 0.9) & (mp < -12) & (ms >= -8)
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    sizes = ndimage.sum(mask, lab, index=np.arange(1, n+1)) if n else []
    order = np.argsort(sizes)[::-1] if n else []
    print(f"scenes {len(recs)}; mask {int(mask.sum())} px; {n} comps")
    res = []
    for k in order[:25]:
        kk = k+1
        rr, cc = np.where(lab == kk)
        r0, c0 = rr.mean(), cc.mean()
        lon = BOX[0]+c0*RES; lat = BOX[3]-r0*RES
        series = np.nanmedian(st[:, rr, cc], axis=1)
        present = np.nanmean(st[:, rr, cc] >= BRIGHT, axis=1) >= 0.5
        first = dates[int(np.argmax(present))] if present.any() else None
        print(f"   comp n={int(sizes[k])} ({lon:.4f},{lat:.4f}) first={first} "
              f"pre_med={mp[int(r0),int(c0)]:.0f} post_med={ms[int(r0),int(c0)]:.0f}")
        res.append((lon, lat, int(sizes[k]), first))
    # figure
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ext = [BOX[0], BOX[2], BOX[1], BOX[3]]
    fig, ax = plt.subplots(1, 3, figsize=(20, 8))
    for a, arr, t, cm, lo, hi in ((ax[0], mp, "PRE median dB", "gray", -25, 0),
                                  (ax[1], ms, "POST median dB", "gray", -25, 0),
                                  (ax[2], ms-mp, "POST-PRE dB", "RdBu_r", -12, 12)):
        im = a.imshow(arr, extent=ext, cmap=cm, vmin=lo, vmax=hi, aspect="auto")
        a.set_title(t); fig.colorbar(im, ax=a, fraction=0.04)
    for lon, lat, sz, first in res:
        ax[2].plot(lon, lat, "o", mfc="none", mec="lime", mew=2, ms=14)
    fig.suptitle(f"METHOD-0003 screening eastern lake; {n} new persistent comps")
    fig.savefig(TMP / "m0003_screen.png", dpi=110, bbox_inches="tight")
    print("saved", TMP / "m0003_screen.png")


if __name__ == "__main__":
    main()
