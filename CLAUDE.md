# CLAUDE.md — Hutrit Marketing Workspace

## Propósito del Workspace

Este workspace apoya las operaciones de marketing, contenido, comunicación, marca y campañas de Hutrit. Está diseñado para ser estructurado, escalable y consistente con los estándares de marca de la empresa.

---

## Estructura del Workspace

```
_context/       → Archivos base de marca, empresa, audiencias, mensajería y tono
_sop/           → Procedimientos operativos estándar para flujos de trabajo de marketing
_templates/     → Plantillas reutilizables para entregables recurrentes
ads/            → Reportes y análisis de campañas publicitarias
presentations/  → Presentaciones internas y externas
reports/        → Reportes de desempeño, análisis y métricas
research/       → Investigación de mercado, competidores y audiencias
seo/            → Estrategia y entregables de SEO
social/         → Contenido para redes sociales
```

---

## Contexto de Marca

Hutrit es una marca con ecosistema dual:
- **Hutrit** (B2B): conecta empresas con talento remoto full-time de LATAM
- **Hutrit Club** (B2C): conecta a profesionales latinoamericanos con empresas reales

El archivo principal de contexto de marca es [`_context/brand_verview.md`](_context/brand_verview.md). Debe cargarse siempre que se trabaje en tareas de contenido, mensajería, campañas o comunicación.

---

## Reglas de Operación

### Contexto
- Siempre carga los archivos relevantes desde `_context/` antes de ejecutar cualquier tarea de marketing o contenido
- No asumas detalles de marca: léelos desde los archivos de contexto en tiempo de ejecución
- Si el archivo de contexto relevante no existe, solicítalo al usuario antes de proceder

### Voz y Comunicación
- Toda comunicación debe reflejar la personalidad de marca: profesional, moderna, humana, cercana, ágil, curada, confiable, ambiciosa e internacional
- Equilibra siempre cercanía humana con solidez profesional
- Usa los pilares de comunicación como guía: talento real, empresas reales, conexión confiable, crecimiento profesional, agilidad con criterio
- Adapta el tono según la audiencia: más consultivo y directo para empresas (B2B), más cercano y motivador para talento (B2C)

### Entregables
- Guarda los entregables finales en la carpeta correspondiente a su tipo (`ads/`, `social/`, `reports/`, etc.)
- Nunca guardes borradores o trabajo en proceso como entregables finales
- Usa las plantillas en `_templates/` cuando estén disponibles
- Sigue los SOPs en `_sop/` para tareas con procedimiento definido

### SOPs y Agentes
- Los SOPs deben ser operativos, claros y reutilizables; los detalles de marca se cargan desde `_context/` en tiempo de ejecución
- Los agentes deben tener roles claros y no solapados
- No hardcodees detalles de marca dentro de SOPs o agentes reutilizables
- Cada agente debe cargar contexto relevante de `_context/` al ejecutarse

### Código y Automatización
- Si se crean scripts o herramientas, deben estar documentados y ser reutilizables
- Prioriza soluciones simples y mantenibles sobre abstracciones innecesarias

---

## Audiencias Clave

| Audiencia | Segmento | Foco |
|-----------|----------|------|
| Empresas que contratan | B2B | Tech, Marketing, Ventas — buscan eficiencia y confianza |
| Talento LATAM | B2C | Tech, Marketing, Diseño, Producto, Data, Ventas — buscan oportunidades reales |

---

## Pilares de Comunicación

1. **Talento real** — perfiles validados con experiencia demostrable
2. **Empresas reales** — oportunidades auténticas, no promesas vacías
3. **Conexión confiable** — Hutrit como facilitador estructurado
4. **Crecimiento profesional** — visión de evolución y desarrollo
5. **Agilidad con criterio** — velocidad sin improvisación

---

## Notas para Agentes e IA

- El contexto de marca principal está en `_context/brand_verview.md`
- Hutrit tiene enfoque B2B y B2C simultáneamente — distingue siempre la audiencia antes de producir contenido
- La contratación remota se presenta como algo estructurado y profesional, nunca improvisado
- El talento latinoamericano es una fortaleza de marca, no solo un diferenciador de precio
- Ante dudas sobre tono o mensajería, vuelve al archivo de contexto — no improvises

---

## Routing: Agentes, Skills y Ejecución Directa

Este workspace tiene dos sub-agentes y un conjunto de skills especializados. La regla principal es: **usa el recurso más simple que pueda cumplir la tarea**. No delegues a un agente si un skill o una respuesta directa bastan.

---

### Cuándo NO delegar a un agente

Si la tarea es una sola acción concreta con un output definido, ejecútala directamente con el skill correspondiente o responde en línea. No spin-up de agentes para:

- Generar una imagen o carrusel visual → usa el skill `social-creative-designer` directamente
- Escribir un copy corto, un headline, o un caption → responde en línea o usa `market-copy`
- Analizar una métrica puntual que el usuario ya interpretó → responde en línea
- Ejecutar una tarea de un solo paso bien definida con un skill del suite `market-*`
- Responder preguntas sobre marca, audiencia o posicionamiento → lee `_context/` y responde directamente

---

### Agente: `data-analyst`

**Delega aquí cuando:**
- El usuario entrega datos crudos (CSV, tabla, métricas exportadas) y necesita análisis, no solo lectura
- La tarea requiere múltiples pasos: limpieza de datos → identificación de tendencias → anomalías → recomendaciones priorizadas
- Se necesita un reporte estructurado con Executive Summary, dashboard de KPIs y action items (no un resumen rápido)
- Hay datos de múltiples canales o períodos que requieren síntesis y comparación cross-channel
- El usuario necesita que alguien "entienda qué está pasando" en una campaña, no solo que liste números

**No delegar cuando:**
- El usuario solo pide que leas un número o compares dos cifras que él ya tiene claras
- La tarea es formatear o presentar datos que ya están interpretados
- Solo se necesita una tabla o visualización simple sin análisis diagnóstico

**Output esperado:** reporte guardado en `ads/` o `reports/` según el tipo de datos

---

### Agente: `content-creator`

**Delega aquí cuando:**
- El usuario da un brief, tema u objetivo y necesita contenido en **múltiples formatos o canales** en una sola operación (blog + social + lead magnet, por ejemplo)
- La tarea requiere decisión estratégica: qué formatos usar, qué ángulo tomar, cómo adaptar el tono por canal
- Se necesita un paquete de contenido completo para una campaña o lanzamiento
- El brief es abierto ("crea contenido para atraer diseñadores LATAM") y requiere que el agente interprete, priorice y ejecute con criterio propio

**No delegar cuando:**
- El usuario pide un solo tipo de contenido con formato y destino claros → usa el skill `market-*` correspondiente directamente:
  - Solo un post de redes sociales → `market-social` o `social-creative-designer`
  - Solo copy para un anuncio → `market-ads`
  - Solo copy para una landing page → `market-landing`
  - Solo un email o secuencia → `market-emails`
  - Solo un reporte de marketing → `market-report`

**Output esperado:** entregables guardados en las carpetas correspondientes según tipo (`social/`, `seo/`, `ads/`, etc.)

---

### Skills disponibles — referencia rápida de uso directo

| Skill | Cuándo usarlo directamente (sin agente) |
|-------|----------------------------------------|
| `social-creative-designer` | Generar carruseles o imágenes PNG para redes sociales — una sesión, un output visual |
| `market-ads` | Crear copy o creativos para anuncios de pago con brief claro |
| `market-copy` | Redactar copy de marca: headlines, taglines, descripciones, mensajes clave |
| `market-emails` | Escribir una secuencia de emails o un email puntual |
| `market-landing` | Analizar o crear copy para una landing page específica |
| `market-social` | Generar un calendario o set de posts de texto para redes sociales |
| `market-report` | Producir un reporte de marketing en formato Markdown o PDF |
| `market-seo` | Auditoría SEO de contenido existente |
| `market-brand` | Análisis de voz de marca o generación de guías de tono |
| `market-audit` | Auditoría general de marketing (orquesta múltiples skills internamente) |
| `market-launch` | Playbook de lanzamiento para un producto o servicio |

---

### Árbol de decisión rápido

```
¿La tarea tiene datos crudos que necesitan análisis diagnóstico?
  └─ Sí → data-analyst

¿La tarea pide contenido en múltiples formatos desde un brief abierto?
  └─ Sí → content-creator

¿La tarea pide imágenes o visuales sociales?
  └─ Sí → social-creative-designer (skill directo)

¿La tarea pide un entregable de texto en un solo formato bien definido?
  └─ Sí → skill market-* correspondiente (directo)

¿La tarea es una pregunta, consulta de marca, o requiere una respuesta corta?
  └─ Sí → responde en línea, lee _context/ si hace falta
```
