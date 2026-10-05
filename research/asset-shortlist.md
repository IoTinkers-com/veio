# Asset shortlist v0.1 — proposal (gate: user validates)

**Bottom line:** 17 candidate assets for Asset Dossier v0.1, selected for segment and geographic representativeness from OGIM v3.0 (DS-0012) plus recent flaring detections. All are already-public infrastructure locations. Validate before feature brief + dossiers.

## Selection criteria
- Segment coverage: refining, Faja heavy-oil upgraders, conventional fields, export/midstream, offshore.
- Public identity: named in OGIM v3.0 or established public record — no novel location disclosure (§10).
- Observation potential: imagery-observable footprint + complementary layers (flaring detections, FIRMS DS-0004, Sentinel DS-0001/0002).
- Geographic spread: Zulia, Falcón, Carabobo, Anzoátegui, Monagas, Bolívar/Guárico, offshore.

## Candidates

### Refining
| AST | Asset | State | OGIM anchor |
|---|---|---|---|
| AST-0001 | Centro de Refinación Paraguaná (Amuay–Cardón) | Falcón | AMUAY + CRP records (-70.17, 11.77/-11.84) |
| AST-0002 | Refinería El Palito | Carabobo | named record (-68.14, 10.45) |
| AST-0003 | Refinería Morón | Carabobo | named record (-68.21, 10.66) |
| AST-0004 | Refinería Bajo Grande | Zulia | named record (-71.71, 10.61) |

### Faja del Orinoco (heavy oil, upgraders)
| AST | Asset | State | OGIM anchor |
|---|---|---|---|
| AST-0005 | Petroanzoátegui (Sincor legacy) | Anzoátegui/Monagas | well clusters [coords to validate] |
| AST-0006 | Petrolera Sinovensa | Anzoátegui | well clusters [coords to validate] |
| AST-0007 | Petrocedeño (Junín) | Bolívar/Guárico | well clusters [coords to validate] |
| AST-0008 | Petropiar (Hamaca) | Anzoátegui/Bolívar | well clusters [coords to validate] |

### Conventional fields
| AST | Asset | State | OGIM anchor |
|---|---|---|---|
| AST-0009 | Lagunillas–Tía Juana (COL legacy cluster) | Zulia | well cluster, 2021 vintage |
| AST-0010 | Quiriquire field | Monagas | wells + Repsol public record |
| AST-0011 | Jusepín | Monagas | flaring detection 2026-09-14 |
| AST-0012 | Santa Bárbara field | Monagas | flaring detection 2026-09-14 |
| AST-0013 | Boquerón field | Monagas | flaring detection 2026-09-14 |

### Midstream / export
| AST | Asset | State | OGIM anchor |
|---|---|---|---|
| AST-0014 | José complex + export terminal | Anzoátegui | terminal records (-64.6 to -64.8) |
| AST-0015 | La Salina terminal + COL pipeline node | Zulia | terminal record |
| AST-0016 | Temblador tank yard | Monagas | OGIM TANK YARD (-63.06, 8.87) |

### Offshore
| AST | Asset | State | OGIM anchor |
|---|---|---|---|
| AST-0017 | Offshore platforms (Gulf of Venezuela / Lake) | Zulia/Falcón | 5 offshore records [identity to validate] |

## Notes
- OGIM VE extract (11 CSVs) copied to `data/ogim_venezuela/` (git-ignored); provenance DS-0012.
- OGIM refinery/terminal records are 2017 vintage; well records 2021; flaring detections 2026-09-14. Identity↔coordinate mapping for JV upgraders and offshore platforms needs validation in each dossier [GAP].
- Ethics: names and locations only as already public; no status claims beyond sources.

## Next
- User validates shortlist → feature brief (Asset Dossier v0.1) → dossiers in batches.
