# VEIO — how the platform works

**Bottom line:** VEIO turns public satellite and map data into dated, located **observations** about Venezuela's energy infrastructure — each one traceable to its source data, its processing, and a stated confidence, and kept separate from interpretation.

## 1. The question
What is changing in Venezuela's energy infrastructure — where, when, and how well can we prove it — using only reproducible public evidence?

## 2. The four layers (never merged)
![Pipeline](figures/pipeline.svg)

| Layer | Plain meaning | Where it lives |
|---|---|---|
| **DATA** | Public, licensed datasets we did not create | `docs/datasets/DS-####.md` |
| **PROCESSING** | Our scripts that turn data into derived products | `scripts/`, `data/derived/` (manifest + checksums) |
| **OBSERVATION** | A dated, located statement of *what the data shows* | Asset Dossiers, `Change indicators` |
| **INTERPRETATION** | What it *might* mean — hypotheses, kept apart | Asset Dossiers, `Interpretation` |

## 3. From input to result — one worked example
The Santa Bárbara flaring analysis (AST-0012), end to end:

| Step | In plain language |
|---|---|
| **Input** | NASA **FIRMS** thermal hotspots (satellite, VIIRS) over the field, 90 days |
| **Processing** | Group hotspots into **nuclei**; measure how many days each is detected, at night, and how stationary it is |
| **Observation** | The cluster resolves into **9 nuclei; 8 detected on ≥30% of 90 days; night-active (median 87%); stationary** → *compatible with continuous flaring* |
| **Not claimed** | Volume of gas, cause, operator, or that any of it is illegal |

Every arrow above is reproducible: same input + same script → same result, with a manifest of files and checksums.

## 4. The four methods at a glance
| Method | Looks at (input) | Question in one line | Status |
|---|---|---|---|
| **0001** Optical | Sentinel-2, Landsat | Did the surface change (buildings, clearing, burn)? | **Not validated** |
| **0002** Thermal | FIRMS hotspots | Is there persistent flaring activity? | **Validated** (differential/density + fixed nuclei) |
| **0003** Radar | Sentinel-1 | Did a new hard object appear (rig, vessel, structure) under clouds? | **Validated, scope-limited** |
| **0004** Night lights | VIIRS Black Marble | Do city/asset lights rise or fall? | **Not validated** |
| *CH4 (proposed)* | TROPOMI, EMIT | Is there a methane enhancement? | *Exploratory only* |

Detail and live status: `docs/methods/STATUS.md`.

## 5. Status language
| Label | Meaning |
|---|---|
| **Validated** | Passed its pre-registered tests; used in dossiers |
| **Validated, scope-limited** | Passed, but only for a stated, narrow claim |
| **Pre-registered** | Design written and committed *before* running; not run yet |
| **Not validated** | Tests did not pass; the negative is recorded; **not** used in dossiers |
| **Exploratory** | No method yet; a lead, not a result |

## 6. What we can and cannot claim
- Every observation cites its source dataset, its processing, and its limitations.
- Evidence strength is **Low / Moderate / Strong**, always with the reason — never a numeric truth score.
- We **do not** accuse, attribute responsibility, or state environmental conclusions without evidence.

## 7. Where to look next
| If you want… | Open |
|---|---|
| The whole picture | this page + `docs/methods/STATUS.md` |
| How one method works | `docs/methods/METHOD-####.md` |
| What we know about one asset | `docs/assets/AST-####-*.md` |
| Which assets still have gaps | `docs/assets/EVIDENCE-MATRIX.md` |
| A dataset's license and coverage | `docs/datasets/DS-####.md` |
| What changed recently | `CHANGELOG.md`, `research/LOG.md` |

## 8. Current gaps (honest)
- **11 of 17 assets** have no VEIO-derived observation yet.
- **2 of 4 methods** (optical, night lights) are not validated.
- Some asset coordinates remain `[GAP]`; methane is not a method yet.
- No public web product yet — the Atlas UI is Sprint 2+.

## Glossary
- **SAR** — radar imagery that sees through clouds (Sentinel-1).
- **dNBR** — a burn-severity index from before/after imagery.
- **FRP** — fire radiative power (MW) at satellite overpass; a brightness, not a gas volume.
- **ppm·m** — methane column enhancement unit (EMIT).
- **Hotspot** — a thermal-anomaly pixel detected by FIRMS.
- **Pre-registration** — committing a method's design *before* running it, so results cannot be reverse-engineered.
