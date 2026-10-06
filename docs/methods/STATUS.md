# Method status dashboard

**Bottom line:** One row per geo-method — the question it answers, its input, its processing in plain language, its validation status and what it feeds. Technical detail stays in `docs/methods/METHOD-####.md`.

Legend — **Validated** · **Scope-limited** (validated only for a stated narrow claim) · **Pre-registered** (design committed, not run) · **Not validated** · **Exploratory**.

| Method | Question (one line) | Input | Processing (plain) | Status | Outputs | Feeds dossiers |
|---|---|---|---|---|---|---|
| **0001** Optical | Did the land surface change? | DS-0001 Sentinel-2 · DS-0003 Landsat | Cloud-masked before/after composites; NDVI / dNBR change | **Not validated** (v0.3, 2026-10-05) | `data/derived/method-0001/v0.3/` | none |
| **0002** Thermal | Is there persistent flaring? | DS-0004 FIRMS (VIIRS) | Count hotspots per asset; group into nuclei; persistence, night %, FRP | **Validated** (v0.3 differential/density; v0.5 fixed nuclei, scope-limited) | `data/derived/method-0002/v0.5/` | AST-0001, 0002, 0004, 0012, 0014 |
| **0003** Radar | Did a new hard object appear under clouds? | DS-0002 Sentinel-1 RTC | Per-scene brightness persistence; new persistent bright objects over water | **Scope-limited** (v0.1, 2026-10-05) | `data/derived/method-0003/v0.1/` | AST-0009 |
| **0004** Night lights | Do lights rise or fall? | DS-0005 VIIRS Black Marble (VNP46) | Daily / monthly radiance trends per AOI | **Not validated** (v0.2) | `data/derived/method-0004/v0.2/` | none |
| *CH4 (proposed)* | Is there a methane enhancement? | DS-0013 TROPOMI · DS-0014 EMIT | Per-pixel enhancement (ppm·m); not yet a VEIO method | **Exploratory** | `data/derived/asset-zoom/AST-0012-*/methane/` | none |

## How to read a status
- **Validated / Scope-limited** → the method passed pre-registered tests and may appear in a dossier as **Derived**.
- **Not validated** → the negative is recorded; the method is **not** used for dossier claims. A redesign may follow as a new pre-registered version.
- **Pre-registered** → the design is committed in git *before* execution.
- **Exploratory** → an ad-hoc lead with no validated method; never a dossier observation.

## What each method can and cannot say
| Method | Can say | Cannot say |
|---|---|---|
| 0002 Thermal | "persistent thermal activity compatible with flaring"; counts, persistence, night fraction | gas volume, cause, operator, absence proof at a point |
| 0003 Radar | "a new persistent radar-bright object appeared over water" | what the object *is* (rig / vessel / structure) |
| 0001 Optical | (pending validation) | — |
| 0004 Lights | (pending validation) | — |

## In the queue (not yet run)
- **CH4 (METHOD-0005)** — needs a feature brief before implementation; validate EMIT against known plumes.
- **METHOD-0001 v0.4** — corrected land controls (area-share criterion; facility-footprint negative control).
- **METHOD-0004 v0.3** — larger AOIs, robust statistics, flare masking before event tests.
- **METHOD-0003 v0.2** — terminal vessel-presence with independent ground truth; port-clutter mask.
- **METHOD-0002 v0.6 (optional)** — facility-level match to an independent flare-location source; time-integrated FRP.
