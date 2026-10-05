# VEIO — Observatorio de Infraestructura Energética de Venezuela

**Resumen:** Un observatorio geoespacial abierto que documenta la evolución de la infraestructura energética de Venezuela con evidencia temporal reproducible. Primera vertical: Oil & Gas. El primer producto es un Atlas público; el artefacto central es el **Asset Dossier** — lo que sabemos, de dónde proviene, qué procesamos, qué observamos y qué no podemos afirmar.

## Principios
- **DATO → PROCESAMIENTO → OBSERVACIÓN → INTERPRETACIÓN** — nunca se mezclan. Ver `AGENTS.md` §2 (en inglés) para las reglas de redacción.
- Datos abiertos, metodología abierta, procesamiento reproducible, procedencia documentada.
- Filtro de licencias: ningún dataset sin licencia, atribución y derechos de redistribución verificados; si hay dudas → DISPLAY ONLY / RESTRICTED.
- Ética: sin acusaciones, sin afirmaciones no verificadas, sin atribución de responsabilidades. Lenguaje técnico y descriptivo.

## Mapa del repositorio
| Ruta | Contenido |
|---|---|
| `AGENTS.md` | Reglas para cualquier agente de IA (fuente única; `CLAUDE.md` la importa) |
| `.claude/skills/` | 13 skills de rol (leídas por Devin, Claude Code, OpenCode) |
| `docs/engineering-rules.md`, `docs/security.md`, `docs/architecture/scalability.md` | Base de ingeniería y seguridad |
| `docs/adr/` | Registros de decisiones de arquitectura |
| `docs/foundation/` | Fundación técnica y de producto |
| `docs/datasets/`, `registry/datasets.csv` | Fichas y matriz de datasets |
| `templates/` | Plantillas de fichas, ADR, briefs y dossiers |
| `.agents/memory/` | Trampas conocidas para agentes |
| `research/LOG.md` | Bitácora de sesiones entre herramientas |

El repositorio privado complementario `veio-internal` contiene material RESTRICTED (fondos, socios, notas de datos sensibles). Aquí solo se referencia, nunca se copia.

## Estado
Sprint 0 — Discovery y Fundación. Aún no hay código de producto; ver `docs/foundation/` y el roadmap.

## Contribuir
Ver `CONTRIBUTING.md`. Los aportes siguen un flujo de revisión (Enviado → En revisión → Validado/Rechazado/Reemplazado) con historial preservado.

## Licencia
- Código: Apache-2.0 (`LICENSE`).
- Documentación, metodología y metadatos: CC BY 4.0 (`LICENSE-docs`).
- Los datasets conservan sus propias licencias — revisa siempre la ficha del dataset y la atribución del mapa.

## Seguridad
Ver `SECURITY.md`. Reporta vulnerabilidades en privado vía GitHub security advisories — nunca en issues públicos.
