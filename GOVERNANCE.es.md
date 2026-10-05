# Gobernanza — VEIO

## Principios
1. **Transparencia:** métodos, fuentes y procesamiento documentados y públicos (salvo material RESTRICTED, cuya existencia y reglas son públicas aunque el contenido no).
2. **Reproducibilidad:** todo resultado derivado puede re-ejecutarse desde sus entradas, parámetros y versiones registrados.
3. **Atribución:** cada dataset y colaborador es acreditado; el mapa muestra siempre la atribución y licencia por capa.
4. **Corrección:** los errores se corrigen con enmiendas fechadas y visibles; las observaciones reemplazadas quedan enlazadas, nunca borradas en silencio.
5. **Versionado:** datasets, procesamiento y decisiones versionados (identificadores DS/OBS/ADR + processing_version).
6. **Independencia editorial:** las interpretaciones se separan de las observaciones; financiadores y socios no tienen control editorial sobre los hallazgos.
7. **Conflicto de interés:** los revisores declaran conflictos; las declaraciones se registran con la revisión.

## Roles
- **Steward:** IoTinkers aloja y mantiene el proyecto; no presume ser dueño de los aportes de la comunidad.
- **Maintainers:** derechos de merge; hacen cumplir los filtros (scientific-review, web-security, task-close).
- **Reviewers:** validan aportes y dossiers.
- **Contributors:** envían observaciones/evidencia con licencia y método.

## Toma de decisiones
- Decisiones técnicas/de producto: ADR (una decisión = un ADR; se reemplaza, nunca se edita).
- Evolución de la gobernanza comunitaria (IP, marcas, acuerdos de contribución): documentada en `veio-internal/legal/` hasta su ratificación pública.

## Niveles de información
PUBLIC / RESEARCH / RESTRICTED según `AGENTS.md` §7. El material RESTRICTED vive solo en el repositorio privado complementario; sus reglas de manejo son públicas, su contenido no.

## Licencia de los productos
Código Apache-2.0; documentación/metodología/metadatos CC BY 4.0; datasets bajo sus propias licencias con atribución visible.
