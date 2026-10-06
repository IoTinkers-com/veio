# Tablero de estado de métodos

**Idea central:** Una fila por geo-método — la pregunta que responde, su insumo, su procesamiento en lenguaje llano, su estado de validación y qué alimenta. El detalle técnico queda en `docs/methods/METHOD-####.md`.

Leyenda — **Validado** · **Alcance limitado** (validado solo para una afirmación acotada) · **Pre-registrado** (diseño comprometido, sin correr) · **No validado** · **Exploratorio**.

| Método | Pregunta (una línea) | Insumo | Procesamiento (llano) | Estado | Salidas | Alimenta dossiers |
|---|---|---|---|---|---|---|
| **0001** Óptico | ¿Cambió la superficie del terreno? | DS-0001 Sentinel-2 · DS-0003 Landsat | Compositos antes/después con máscara de nubes; cambio NDVI / dNBR | **No validado** (v0.3, 2026-10-05) | `data/derived/method-0001/v0.3/` | ninguno |
| **0002** Térmico | ¿Hay flaring persistente? | DS-0004 FIRMS (VIIRS) | Contar hotspots por activo; agrupar en núcleos; persistencia, % noche, FRP | **Validado** (v0.3 diferencial/densidad; v0.5 núcleos fijos, alcance limitado) | `data/derived/method-0002/v0.5/` | AST-0001, 0002, 0004, 0012, 0014 |
| **0003** Radar | ¿Apareció un objeto duro nuevo bajo nubes? | DS-0002 Sentinel-1 RTC | Persistencia de brillo por escena; objetos brillantes nuevos sobre agua | **Alcance limitado** (v0.1, 2026-10-05) | `data/derived/method-0003/v0.1/` | AST-0009 |
| **0004** Luces nocturnas | ¿Suben o bajan las luces? | DS-0005 VIIRS Black Marble (VNP46) | Tendencias de radiancia diaria/mensual por AOI | **No validado** (v0.2) | `data/derived/method-0004/v0.2/` | ninguno |
| *CH4 (propuesto)* | ¿Hay mejora de metano? | DS-0013 TROPOMI · DS-0014 EMIT | Mejora por píxel (ppm·m); todavía no es un método VEIO | **Exploratorio** | `data/derived/asset-zoom/AST-0012-*/methane/` | ninguno |

## Cómo leer un estado
- **Validado / Alcance limitado** → pasó pruebas pre-registradas y puede aparecer en un dossier como **Derived**.
- **No validado** → el resultado negativo queda registrado; el método **no** se usa para afirmaciones de dossier. Un rediseño puede venir como nueva versión pre-registrada.
- **Pre-registrado** → el diseño se compromete en git *antes* de ejecutar.
- **Exploratorio** → pista ad-hoc sin método validado; nunca una observación de dossier.

## Qué puede y qué no puede decir cada método
| Método | Puede decir | No puede decir |
|---|---|---|
| 0002 Térmico | "actividad térmica persistente compatible con flaring"; conteos, persistencia, fracción nocturna | volumen de gas, causa, operador, prueba de ausencia en un punto |
| 0003 Radar | "apareció un objeto nuevo persistente y brillante sobre agua" | qué *es* el objeto (plataforma / buque / estructura) |
| 0001 Óptico | (pendiente de validación) | — |
| 0004 Luces | (pendiente de validación) | — |

## En cola (sin ejecutar aún)
- **CH4 (METHOD-0005)** — requiere feature brief antes de implementar; validar EMIT contra plumas conocidas.
- **METHOD-0001 v0.4** — controles de tierra corregidos (criterio por área compartida; control negativo sobre la huella de la instalación).
- **METHOD-0004 v0.3** — AOIs más grandes, estadística robusta, enmascarar flaring antes de las pruebas de evento.
- **METHOD-0003 v0.2** — presencia de buques en terminal con verdad de base independiente; máscara de clutter portuario.
- **METHOD-0002 v0.6 (opcional)** — match por instalación contra fuente independiente; FRP integrada en el tiempo.
