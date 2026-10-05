# Contribuir — VEIO

Gracias por tu interés en un observatorio abierto de la infraestructura energética de Venezuela. Esta guía te hace productivo en ~10 minutos.

## Preparación
```bash
git clone https://github.com/IoTinkers-com/veio && cd veio
git config core.hooksPath .githooks   # activa escaneo de secretos + chequeo de skills
```
Aún no hay dependencias de ejecución (Sprint 0). CI corre escaneo de secretos y chequeos de documentación.

## Cómo se trabaja
1. **Elige o propone una tarea.** Las funcionalidades significativas requieren un feature brief (`templates/feature-brief.md`) escrito por el Product Architect antes de implementar.
2. **Una tarea = un commit.** Actualiza `CHANGELOG.md` (y los docs de API cuando existan) en el mismo commit.
3. **Control de calidad antes de cerrar:** typecheck → lint → test → build (las etapas se activan con el stack; Sprint 0 = docs + escaneo de secretos).
4. **Revisiones:** scientific-review (afirmaciones vs evidencia) y web-security (cuando hay código) deben pasar antes del merge.
5. **Docs bilingües:** los documentos humanos existen como `X.md` (EN) + `X.es.md` (ES), actualizados en el mismo commit.

## Reglas que debes conocer
- Lee `AGENTS.md` — obliga a humanos y agentes por igual. Aspectos clave: DATO → PROCESAMIENTO → OBSERVACIÓN → INTERPRETACIÓN nunca se mezclan; no se inventan datasets ni licencias; filtro de licencias (redistribución dudosa → DISPLAY ONLY/RESTRICTED); sin acusaciones ni afirmaciones no verificadas; solo se publican ubicaciones de infraestructura ya públicas.
- Reglas de ingeniería: `docs/engineering-rules.md` (cada regla tiene su chequeo). Seguridad: `docs/security.md`.
- Decisiones: un ADR por decisión (`docs/adr/`); se reemplaza, nunca se edita.
- Trampas conocidas: `.agents/memory/` — añade una nota cuando descubras una.

## Aportar observaciones/evidencia (desde el Sprint 5)
Los aportes incluyen: colaborador, fuente, fecha, ubicación, evidencia, método, licencia, descripción. Flujo: Enviado → En revisión → Validado / Rechazado / Reemplazado, con historial preservado.

## Estilo de commits
Mensaje imperativo; trailer `Assisted-by: <herramienta>` cuando un agente de IA hizo el trabajo (ej. `Assisted-by: Devin`). Nunca `Co-Authored-By` ni `Generated with`.

## Conducta
Ver `CODE_OF_CONDUCT.md`. Reporta problemas de seguridad en privado (ver `SECURITY.md`).
