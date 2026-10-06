# Asset × Evidence matrix

**Bottom line:** Which of the 17 assets have a VEIO-derived observation, by method. **Empty cells are the gaps** — and they are the next work items.

Legend: **●** Derived observation from a **validated** method (used in the dossier) · **○** visual/location check from an **unvalidated** method (not a change observation) · **◐** exploratory (no validated method) · **—** none.

Methods: METHOD-0001 optical · METHOD-0002 thermal · METHOD-0003 radar · METHOD-0004 lights · CH4 (proposed).

| AST | Asset | 0001 Optical | 0002 Thermal | 0003 Radar | 0004 Lights | CH4 | Notes / next |
|---|---|---|---|---|---|---|---|
| AST-0001 | CRP Paraguaná | — | ● | — | — | — | Amuay 284 hotspots / 27 d; Cardón none within 5 km [flare-stack coords GAP] |
| AST-0002 | El Palito | — | ● | — | — | — | 36 hotspots / 18 d; co-located with OGIM "LECHOSO" (~4 km) |
| AST-0003 | Morón | — | — | — | — | — | no method applied yet; CH4 potential [GAP] |
| AST-0004 | Bajo Grande | — | ● | — | — | — | 0 hotspots / 30 d (absence observation; not site-level proof) |
| AST-0005 | Petro San Félix | — | — | — | — | — | upgrader coords [GAP]; no method applied |
| AST-0006 | Sinovensa | — | — | — | — | — | blending plant; no method applied |
| AST-0007 | Petrocedeño | — | — | — | — | — | 2025-11 fire not detectable at 20 m (METHOD-0001 v0.3, not validated) |
| AST-0008 | Petropiar | — | — | — | — | — | upgrader coords [GAP]; no method applied |
| AST-0009 | Lagunillas | ○ | — | ● | — | — | new persistent radar object 2025-09-01 (Alula-compatible); location check (0001 ○) |
| AST-0010 | Quiriquire | — | — | — | — | — | field coords [GAP]; no method applied |
| AST-0011 | Jusepín | — | — | — | — | — | OGIM detections are source-recorded; no VEIO-derived observation |
| AST-0012 | Santa Bárbara | — | ● | — | — | ◐ | 1,046 hotspots / 30 d; v0.5: 9 nuclei, 8 persistent; EMIT CH4 exploratory |
| AST-0013 | Boquerón | — | — | — | — | — | single OGIM detection (source-recorded); no method applied |
| AST-0014 | José / TAECJAA | ○ | ● | — | — | — | 750 hotspots / 30 d; fire test not validated (0001 v0.3); location check (0001 ○) |
| AST-0015 | La Salina | — | — | — | — | — | terminal mapping [GAP]; no method applied |
| AST-0016 | Temblador | — | — | — | — | — | status [GAP]; candidate for swap |
| AST-0017 | Offshore (Dragon + 4) | — | — | — | — | — | 5 records, 1 identified; no method applied |

## How to read it
- A **●** requires a pre-registered method that passed its tests; the observation lives in the dossier's `Change indicators` and cites a manifest.
- An **○** is a by-product visual check (e.g., confirming a location), labelled as such; it is **not** evidence of change.
- **—** is not "no activity" — it means **we have not yet produced an observation**. Absence of evidence, not evidence of absence.

## Gaps this exposes
- **11 of 17 assets** have no VEIO-derived observation: AST-0003, 0005, 0006, 0007, 0008, 0010, 0011, 0013, 0015, 0016, 0017.
- Methods **0001 (optical)** and **0004 (lights)** are not validated → entire rows of "—" that no method currently fills.
- Methane is exploratory only (AST-0012), no method.
- Coordinate `[GAP]`s block several assets (0005–0008, 0010, 0015).

## How this stays true
`scripts/check_docs.py` fails in CI if any asset in `registry/assets.csv` or any `METHOD-####` is missing from this matrix (and its Spanish twin).
