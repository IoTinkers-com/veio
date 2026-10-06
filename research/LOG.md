# Session log (append-only, ≤6 lines per entry)

## 2026-10-04 — devin — Sprint 0 setup
- Created public repo skeleton: AGENTS.md (+CLAUDE.md import), 13 skills (.claude/skills) + 13 OpenCode wrappers, engineering-rules, security, scalability, ADR-000, memory index, templates, bilingual governance, licenses, pre-commit, minimal CI.
- Companion private repo veio-internal created (funding/partners/legal/risks/restricted-data).
- Open: user confirms OpenCode + Claude Code skill discovery; branch protection after first push. Next: Discovery & Foundation v0.1 (Phase B).

## 2026-10-04 — devin (GLM) — Phase B Discovery
- Registered 11 datasets (DS-0001–DS-0011) with verified licenses, access dates and MVP scores: S2, S1, Landsat, FIRMS, Black Marble, WB flaring DB, VNF (DISPLAY ONLY/RESTRICTED), GEM GOIT, Cerulean, HDX COD-AB, OSM. Cards + registry rows + CHANGELOG.
- Open: bilingual pass on dataset cards (§4) undecided; GEM GOGET/GOGPT and Sentinel-1 constellation status [UNVERIFIED] pending; VNF license application decision (internal repo).
- Next: select 10–20 representative assets (needs asset shortlist) or ADR for imagery access pipeline; enable hooks already done (`core.hooksPath` set).

## 2026-10-04 — devin (GLM) — Cross-repo intake (Phase B addendum)
- Registered DS-0012..0015 from leads surfaced in a separate private research workspace (public third-party datasets only; no external client/partner context imported): OGIM v3.0 (CC BY, score 5), TROPOMI CH4 (4), EMIT CH4 plumes (3; V001 decommissioned 2026-03-26 → V2), EDGAR_2025_GHG (2).
- Licenses verified from provider pages 2026-10-04; §13 respected — cards cite providers only.
- Open: OGIM update cadence [UNVERIFIED]; EMIT V2 record start [GAP]. Next: asset shortlist for dossiers.

## 2026-10-04 — devin (GLM) — Asset shortlist v0.1 (proposal)
- Drafted 17 candidates (AST-0001..0017): 4 refineries, 4 Faja upgraders, 5 conventional fields, 3 midstream/export, 1 offshore group. Criteria: segment/geographic coverage, public identity, observation potential.
- Source: OGIM v3.0 VE extract (DS-0012) copied to data/ogim_venezuela/ (git-ignored); flaring detections 2026-09-14.
- Open: JV upgrader + offshore identity↔coords validation [GAP]. Gate: user validates shortlist → feature brief → dossiers.

## 2026-10-04 — devin (GLM) — Feature brief + dossier batch 1 (refineries)
- Shortlist validated by user. Brief: docs/briefs/FEATURE-asset-dossier-v0.1.md. Registry assets.csv created (AST-0001..0004).
- Dossiers AST-0001..0004 (CRP Paraguaná, El Palito, Morón, Bajo Grande) with dated sources (Reuters 2025-05/2026-07, Wikipedia, Notitarde 2026-04); OGIM flaring associations (LECHOSO, ENSANADA 2026-09-14); coord discrepancies flagged [GAP].
- Open: scientific-review gate for batch 1; Morón/Bajo Grande coords need imagery validation. Next: batch 2 (Faja upgraders) on user go.

## 2026-10-04 — devin (GLM) — Scientific review batch 1 + dossier batch 2 (Faja upgraders)
- Review batch 1: zero blockers, 4 minor fixes applied (inline citations for rankings, approximate date flag). Commit 44d4e7f.
- Shortlist corrected (v0.1.1): Sincor = Petrocedeño (not Petroanzoátegui = Petro San Félix); all four upgraders at José complex, Anzoátegui.
- Dossiers AST-0005..0008 written: San Félix (off line ~2019, areas → Petro Roraima 2024), Sinovensa (blending 165k b/d, steadiest), Petrocedeño (fires 2025-11-19 Reuters), Petropiar (Chevron license wind-down 2025-03, scenarios 105-138k bpd).
- Open: Argus article dates [UNVERIFIED]; exact upgrader coords [GAP]; scientific-review batch 2. Next: batch 3 (conventional fields) on user go.

## 2026-10-04 — devin (GLM) — Dossier batch 3 (conventional fields)
- Dossiers AST-0009..0013: Lagunillas (CCRC/Alula reactivation, 12k→60k bpd target 2026), Quiriquire (Petroquiriquire JV, Repsol 71.3k boe/d 2025), Jusepín (gas plant + Jusepin 200; legacy field), Santa Bárbara (43 flaring detections — densest cluster; Merey diluent role), Boquerón (operating; Roszarubezhneft stake flagged for counsel).
- Registry assets.csv now AST-0001..0013 (13/17).
- Open: scientific-review batch 2+3; coords for Lagunillas/Quiriquire [GAP]. Next: batch 4 (midstream AST-0014..0016 + offshore AST-0017) on user go.

## 2026-10-04 — devin (GLM) — Dossier batch 4 (midstream + offshore) — all batches done
- AST-0014 José/TAECJAA (20.5M bbl Feb 2025 official; Petropars tank rehab), AST-0015 La Salina (Blend 22, tanker queue Apr 2025, hull-staining leaks), AST-0016 Temblador tank yard (evidence thin [GAP]; candidate for swap), AST-0017 offshore (Dragon: license 2023→revoked 2025→re-authorized [UNVERIFIED]; 4/5 platforms unidentified).
- Registry assets.csv complete: AST-0001..0017 (17/17).
- Open: scientific-review batches 2–4; Temblador candidate swap decision; Dragon license re-verify <90 d. Next: reviews.

## 2026-10-04 — devin (GLM) — Scientific review batches 2–4 (complete)
- Zero blockers; 2 corrections applied: AST-0011 "persistent"→same-day detections; AST-0012 count 43→33 (verified vs extract; largest name-cluster confirmed). Record: docs/reviews/2026-10-04-dossiers-batches-2-4.md.
- Dossier v0.1 complete: 17/17 assets, all claims dated+cited, interpretations separated, ethics/licensing pass.
- Open: Temblador swap decision; Dragon license re-verify <90 d; imagery validation of flagged coords; bilingual .es.md pass before Atlas. Next: geo-method briefs for change indicators (v0.2) or MVP packaging.

## 2026-10-04 — devin (GLM) — Change-indicator brief + 4 method notes (v0.2, not executed)
- Brief: docs/briefs/FEATURE-change-indicators-v0.2.md. Method notes METHOD-0001..0004 (optical disturbance, FIRMS hotspots, SAR, Black Marble lights) — hypothesis + validation plan pre-registered, acceptance criteria set, negative results to be recorded.
- Implementation order agreed in brief: 002 FIRMS (cheapest) → 001 optical → 004 lights → 003 SAR. Nothing executed yet; no derived products exist.
- Open: METHOD-#### prefix not in §12 conventions (added de facto); validation reference events are press-based (confidence cap Moderate). Next: execute METHOD-0002 validation or MVP packaging on user pick.

## 2026-10-04 — devin (GLM) — METHOD-0002 executed and validated (partial)
- FIRMS API via user MapKey (stored in git-ignored .secrets/); 29,558 VE hotspots, 30-day window, VIIRS S-NPP+NOAA-20. Script scripts/method0002_validate.py; outputs data/derived/method-0002/ + manifest (checksums).
- Honest result: site-level detection FAILS pre-registered 80% (36.4% r1.5 / 66.2% r5.0); validated as cluster-density (SB 1,046/30d) and facility-differential (Amuay 284/27d, José 122/27d, El Palito 36/18d vs Bajo Grande 0) indicator; controls 0%. Deviations documented (radius, per-facility AOIs, event-test substitution).
- Derived observations added to AST-0001/0002/0004/0012/0014. Traps: FIRMS API path is /api/area/csv/ (not area_csv); DAY_RANGE max 5; chunk joins need explicit newlines.
- Open: OGIM↔FIRMS coordinate/method mismatch [GAP]; remaining methods pending. Next: METHOD-0001/0004 or MVP packaging on user pick.

## 2026-10-04 — devin (GLM) — METHOD-0001 pilot executed (inconclusive, documented)
- S2 L2A via Planetary Computer; pipeline works end-to-end (composites, NDVI/NDBI change, controls) after fixing PROJ conflict, CRS transform, out_shape and L2A offset (memory note added).
- Verdict: INCONCLUSIVE/FAILED as designed — FCC restart not optically visible; ocean controls; seasonal confounder. Redesign pre-registered in METHOD-0001 (same-season pairs, land controls, surface-expression events). No dossier observations added.
- Open: METHOD-0001 v0.2 redesign; METHOD-0004 pending. Next: user pick (redesign, METHOD-0004, MVP packaging).

## 2026-10-04 — devin (GLM) — METHOD-0004 executed (not validated, documented)
- VNP46A3 monthly via LAADS/CMR (user EDL token in .secrets/); 27 tiles, 9 months, 8 AOIs. Tile convention trap fixed via file attrs (h00 exists; v07=10..20N) — memory note added.
- Verdict: NOT validated (1/4 directional; controls unstable; monthly can't see 5-day events; Lagunillas AOI coords dead [GAP]). Candidate observation: Maracaibo lights ~x2 2023→2025 (pending validation). Redesign pre-registered.
- Open: METHOD-0001 v0.2 + METHOD-0004 v0.2 redesigns; AOI coords validation. Next: MVP packaging or redesigns on user pick.

## 2026-10-04 — devin (GLM) — MVP packaging + first push
- README EN/ES updated: repo map (assets/briefs/methods/reviews/scripts) + status (15 datasets, 17 dossiers, 4 methods). Pushed 89aad88..d9c3bc8 to IoTinkers-com/veio. Branch protection ON: required checks CI/secrets+CI/docs, no force-push, admins bypass.
- Open: METHOD-0001/0004 v0.2 redesigns; AOI coords; bilingual pass of dossiers; Temblador swap. Next: user pick.

## 2026-10-04 — devin (GLM) — v0.2 redesigns executed (both NOT validated) + AST-0014 correction
- Pre-registered 0001/0004 v0.2 in 93b9b25 before running. 0001: dNBR = seasonal drying (C2 fail); water detector hits algal blooms (77 non-specific). 0004: CRP halt z=-0.12 (2/5 event days valid); Maracaibo Aug-Oct +40% < 1.5x. Author error: 0001 used adjacent, not same-season, windows.
- Corrections: AST-0014 AOI was an OGIM offshore point 29 km away (José = 750 hotspots/30d, not 122/27d); v0.1 "Maracaibo ~x2" withdrawn (seasonal artefact). Figures in docs/methods/figures/.
- Open: v0.3 rules (same-month windows, bloom gate or SAR for platforms, availability check before event tests). Validated so far: METHOD-0002 differential/density only.

## 2026-10-04 — devin (GLM) — METHOD-0001 v0.3 executed (not validated; controls redesigned)
- Interannual same-month dNBR (pre-registered 6755ad1). Seasonal confounder fixed (José 51%→0.32%). Verdict: NOT validated — C-urban failed on component count (15>1, criterion unrealistic), T-neg box contained all of Cabimas + wetlands (control-design error; strong change at tank-farm area consistent with reported Chevron storage ops). Fire scar not detectable as coherent signature at 20 m.
- v0.4 rules pre-registered in method note (area-share criteria; facility-footprint negative control; coherent-component requirement for fire claims).
- Open: v0.4 run or pivot to METHOD-0003 SAR (Alula test lives there). Next: user pick.

## 2026-10-05 — devin (GLM) — METHOD-0003 v0.1 executed (VALIDATED, scope-limited)
- SAR via Sentinel-1 RTC (Planetary Computer): S1A descending track 171, 7 pre / 11 post scenes 2025. Detector = per-scene brightness persistence (VV ≥ −8 dB in ≥90% post, 0% pre) over pre-dark water. Pre-registered b28e66c, then run.
- Result: 1 new persistent object at Lagunillas 10.13715/−71.2703, first bright 2025-09-01, persistent to 2025-12-30, peak +20 dB; confirmed in ascending track 4; both open-lake controls 0 → VALIDATED for "new persistent bright object"; NOT for identity or open-water detection (eastern-lake ~55 m screening found none).
- Derived observation added to AST-0009 (compatible with reported Alula jack-up, Reuters 2025-09-04; identity undetermined). Figure + manifest in repo. Discovery used to pin params (documented); scratch scripts removed.
- Open: v0.2 (terminal vessel-presence with independent ground truth; port clutter mask; SLC/coherence). Validated so far: METHOD-0002 (differential/density), METHOD-0003 (bright-object, scope-limited).

## 2026-10-05 — devin (GLM) — AST-0012 Santa Bárbara: zoom flaring + CH4 (exploratory)
- QGIS package `data/derived/asset-zoom/AST-0012-santa-barbara/` (git-ignored): S1 RTC VV per-scene ~10 m (11 asc track 62, ago–oct 2026) + median + ~33 m context; S2 L2A true colour (2026-09-22/09-02); FIRMS 3.503 hotspots + 69 OGIM detections; EMIT CH4 crops.
- Flaring: densest FIRMS cell (-63.73/9.62, 303/30 d); 69 OGIM detections (Santa Bárbara/Sur, Carito-Mulata). Consistent with AST-0012 dossier (METHOD-0002).
- CH4 (exploratory, no validated method): EMITL2BCH4ENH V002 (ppm·m) covers the cell on 2026-05-26 (max ≈2161) and 2026-04-27 (max ≈2855) — elevated enhancement; broad background/artefacts not excluded; no emission rate. Not added to dossiers.
- Scripts committed (santabarbara_zoom_export/overview/preview, emit_ch4_pick/export); memory note on EMIT LP DAAC quirks. Open: propose METHOD-0005 (CH4) brief or validate EMIT against known plumes.

## 2026-10-05 — devin (GLM) — METHOD-0002 v0.4 Santa Bárbara per-nucleus (NOT validated)
- FIRMS 90 días (N20+S-NPP), 11.480 hotspots; clustering single-link eps 0.01° (~1,1 km) → 9 núcleos; 8 detectados en ≥30% de los días (top: 4.327 detecciones, 97,8% de días). Control Bajo Grande: 0 núcleos.
- C3 (70% de OGIM a 1,5 km) falla: 47/78 = 60,3% → NO validada (C1/C2/C4 pasan). Corrección de implementación centroide→pertenencia (criterio sin cambio). Diagnóstico: 3 km 73,1%, 5 km 91,0%. Sin observación de dossier.
- Bug corregido: los chunks FIRMS de 5 días repiten encabezado (parsear por bloque); nota de memoria actualizada. Pre-registro 4c34ab0; figura + manifiesto en repo.
- Open: v0.5 (radio justificado por precisión OGIM o match por instalación; separar flaring de quema de biomasa; métricas integradas de FRP). Validados: METHOD-0002 (diferencial/densidad), METHOD-0003 (objeto brillante).

## 2026-10-05 — devin (GLM) — METHOD-0002 v0.5 Santa Bárbara (VALIDADO, alcance limitado)
- v0.4 falló por un match OGIM a 1,5 km injustificado: la dispersión interna de las coords OGIM llega a 17 km (Santa Bárbara Sur), 10,3 (Santa Bárbara), 9,3 (Jusepín). v0.5 sustituye ese criterio por discriminadores propios: persistencia + estacionariedad (mediana del desvío diario ≤1 km) + actividad nocturna.
- Resultado: 9 núcleos; 8 en ≥30% de 90 días; mediana noche 87,3%; 8/8 persistentes estacionarios; control Bajo Grande 0 → VALIDADO (alcance: fuentes térmicas fijas, persistentes, nocturnas). OGIM co-locación descriptiva (91% a 5 km). Pre-registro abcfccf.
- Observación Derived añadida a AST-0012 (núcleos, persistencia, FRP medio/máx, noche, deriva). FRP = potencia radiativa por pasada, no volumen. Figura + manifiesto en repo.
- Open: v0.6 opcional (match por instalación con fuente independiente; métrica FRP integrada en el tiempo). Validados: METHOD-0002 (diferencial/densidad + núcleos fijos), METHOD-0003 (objeto brillante).

## 2026-10-06 — devin (GLM) — Fundación: explicador de plataforma + tablero de métodos
- Creado `docs/foundation/PLATFORM.md` (+ `.es.md`): one-pager ejecutivo "cómo funciona VEIO" — 4 capas, ejemplo Santa Bárbara de punta a punta, métodos de un vistazo, semáforo de estado, qué podemos/no podemos afirmar, brechas y glosario. Diagrama `figures/pipeline.svg`.
- Creado `docs/methods/STATUS.md` (+ `.es.md`): una fila por método (pregunta, insumo DS, procesamiento llano, estado de validación, salidas, dossiers) + "qué puede/no puede decir" + cola.
- README EN/ES enlaza ambos como puerta de entrada; línea de estado actualizada.
- Brecha detectada y reflejada: 11/17 activos sin observación propia; 2/4 métodos sin validar; CH4 sin método. Next: definir títulos de columnas/glosario con el steward o arrancar METHOD-0005 (CH4) brief.

## 2026-10-06 — devin (GLM) — Propiedad documental + chequeo de drift en CI
- Respuesta a «¿hay un agente que mantenga los docs?»: no hay rol dedicado; propiedad distribuida. Se formalizó en AGENTS.md §11 (cada rol sus artefactos; task-close refresca STATUS/PLATFORM si cambia estado de método u observación Derived; product-architect dueño de la fundación).
- Nuevo `scripts/check_docs.py` (stdlib) en CI job docs: registry↔archivos, METHOD↔STATUS (EN+ES), citas Derived↔nota de método, huérfanos .es.md. Primera corrida detectó y se corrigió una cita de manifiesto faltante en AST-0014.
- Skills task-close y docs-bilingual actualizadas. Gate docs ahora exige check_docs. Next: Matriz Activo × Evidencia (pieza 3) o brief METHOD-0005.

## 2026-10-06 — devin (GLM) — ADR-001 (sin artefactos generados en el repo) + brief del workbench local
- Decisión (Opción A del steward): el repo público solo guarda código + metadatos + texto; ninguna figura/capa/ráster/JSON derivado se commitea. Se genera en local con la app; el Atlas público futuro usará object storage. Registrado en ADR-001 (Accepted).
- Escrito `docs/briefs/FEATURE-local-workbench-v0.1.md`: docker-compose (web MapLibre + api/worker FastAPI + tiles TiTiler + volumen ./data); usuario investigador; descargar→procesar→ver; PUBLIC sin claves en v1; DS-0007 excluido; nada fuera de ./data.
- Migración pendiente (ADR-001): quitar `docs/methods/figures/*.png` del repo, convertir enlaces de figuras en METHOD/dossiers a rutas locales esperadas, ajustar check_docs/link-check. Next: ejecutar esa migración o el brief METHOD-0005 (CH4).

## 2026-10-06 — devin (GLM) — Migración ADR-001 ejecutada (figuras fuera del repo)
- `git rm docs/methods/figures/*.png` (12 figuras). Ahora se generan en local: los scripts 0001 v0.3, 0002 v0.4/v0.5, 0003 v0.1 escriben la figura en su salida `data/derived/method-*/`.
- Notas METHOD-0001..0004 y dossiers AST-0009/0012/0014: referencias de figuras convertidas a rutas locales esperadas (código en línea), no archivos del repo.
- `check_docs.py` ampliado: falla si hay cualquier ráster/figura commiteada (ADR-001). El SVG del pipeline se mantiene (fuente dibujada a mano, no generada). Registry↔archivos, METHOD↔STATUS, citas Derived, huérfanos ES: OK.
- Repo alineado a ADR-001: solo código + metadatos + texto. Next: Matriz Activo × Evidencia o arrancar el workbench (brief ya escrito).

## 2026-10-06 — devin (GLM) — Matriz Activo × Evidencia (detección de brechas)
- Creado `docs/assets/EVIDENCE-MATRIX.md` (+ `.es.md`): 17 activos × métodos; celda ● (Derived validado) / ○ (chequeo visual de método no validado) / ◐ (exploratorio) / — (ninguna). Basada en las observaciones Derived de los dossiers y en los estados de METHOD-0001..0004.
- Brechas expuestas: 11/17 activos sin observación propia (AST-0003,0005,0006,0007,0008,0010,0011,0013,0015,0016,0017); 0001/0004 sin validar; CH4 solo exploratorio; coords [GAP] en 0005–0008/0010/0015.
- `check_docs.py`: nueva regla — todo activo y todo METHOD debe aparecer en la matriz (EN+ES). README y PLATFORM enlazan la matriz. Gate docs OK.
- Next: arrancar el workbench local (brief listo) o brief METHOD-0005 (CH4).

## 2026-10-06 — devin (Claude) — Brief del workbench revisado + plan
- Brief reescrito contra AGENTS/ADR-001/engineering-rules: paquete `veio` con adaptadores primero (regla 13), 2 contenedores sin DB/cola (regla 12), allow-lists de activo/método validado, choke point de niveles, 127.0.0.1 + fs read-only, etiqueta "re-ejecución local ≠ observación VEIO", reproducción vs valores de referencia del METHOD-0003.
- Nuevo `docs/briefs/PLAN-local-workbench-v0.1.md`: fases P0–P5 (ADR-002/003 → paquete → API → web → CI → validación) + alineación mecánica sin agentes nuevos (lectura en runtime, código compartido, reglas nuevas en check_docs, contract tests).
- Open: 3 decisiones del steward (ADRs, YAML de referencia vs ADR-001, basemap). Next: redactar ADR-002/003.
