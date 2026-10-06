# Matriz Activo × Evidencia

**Idea central:** Qué activos de los 17 tienen una observación propia de VEIO, por método. **Las celdas vacías son las brechas** — y son los próximos trabajos.

Leyenda: **●** observación Derived de un método **validado** (usada en el dossier) · **○** chequeo visual/de ubicación de un método **no validado** (no es una observación de cambio) · **◐** exploratorio (sin método validado) · **—** ninguna.

Métodos: METHOD-0001 óptico · METHOD-0002 térmico · METHOD-0003 radar · METHOD-0004 luces · CH4 (propuesto).

| AST | Activo | 0001 Óptico | 0002 Térmico | 0003 Radar | 0004 Luces | CH4 | Notas / siguiente |
|---|---|---|---|---|---|---|---|
| AST-0001 | CRP Paraguaná | — | ● | — | — | — | Amuay 284 hotspots / 27 d; Cardón ninguno a 5 km [coords de antorchas GAP] |
| AST-0002 | El Palito | — | ● | — | — | — | 36 hotspots / 18 d; co-locado con OGIM "LECHOSO" (~4 km) |
| AST-0003 | Morón | — | — | — | — | — | sin método aplicado aún; potencial CH4 [GAP] |
| AST-0004 | Bajo Grande | — | ● | — | — | — | 0 hotspots / 30 d (observación de ausencia; no prueba a nivel de sitio) |
| AST-0005 | Petro San Félix | — | — | — | — | — | coords del upgrader [GAP]; sin método aplicado |
| AST-0006 | Sinovensa | — | — | — | — | — | planta de mezcla; sin método aplicado |
| AST-0007 | Petrocedeño | — | — | — | — | — | incendio 2025-11 no detectable a 20 m (METHOD-0001 v0.3, no validado) |
| AST-0008 | Petropiar | — | — | — | — | — | coords del upgrader [GAP]; sin método aplicado |
| AST-0009 | Lagunillas | ○ | — | ● | — | — | objeto radar nuevo persistente 2025-09-01 (compatible con Alula); chequeo de ubicación (0001 ○) |
| AST-0010 | Quiriquire | — | — | — | — | — | coords de campo [GAP]; sin método aplicado |
| AST-0011 | Jusepín | — | — | — | — | — | detecciones OGIM son source-recorded; sin observación propia |
| AST-0012 | Santa Bárbara | — | ● | — | — | ◐ | 1.046 hotspots / 30 d; v0.5: 9 núcleos, 8 persistentes; CH4 EMIT exploratorio |
| AST-0013 | Boquerón | — | — | — | — | — | una detección OGIM (source-recorded); sin método aplicado |
| AST-0014 | José / TAECJAA | ○ | ● | — | — | — | 750 hotspots / 30 d; prueba de incendio no validada (0001 v0.3); chequeo de ubicación (0001 ○) |
| AST-0015 | La Salina | — | — | — | — | — | mapeo del terminal [GAP]; sin método aplicado |
| AST-0016 | Temblador | — | — | — | — | — | estado [GAP]; candidato a reemplazo |
| AST-0017 | Offshore (Dragon + 4) | — | — | — | — | — | 5 registros, 1 identificado; sin método aplicado |

## Cómo leerla
- Un **●** exige un método pre-registrado que pasó sus pruebas; la observación vive en `Change indicators` del dossier y cita un manifiesto.
- Un **○** es un chequeo visual de subproducto (p. ej. confirmar una ubicación), etiquetado como tal; **no** es evidencia de cambio.
- **—** no significa "sin actividad" — significa que **todavía no produjimos una observación**. Ausencia de evidencia, no evidencia de ausencia.

## Brechas que expone
- **11 de 17 activos** sin observación propia de VEIO: AST-0003, 0005, 0006, 0007, 0008, 0010, 0011, 0013, 0015, 0016, 0017.
- Los métodos **0001 (óptico)** y **0004 (luces)** no están validados → filas enteras de "—" que ningún método llena hoy.
- El metano es solo exploratorio (AST-0012), sin método.
- Coordenadas `[GAP]` bloquean varios activos (0005–0008, 0010, 0015).

## Cómo se mantiene verdadera
`scripts/check_docs.py` falla en CI si algún activo de `registry/assets.csv` o algún `METHOD-####` falta en esta matriz (y en su gemela en inglés).
