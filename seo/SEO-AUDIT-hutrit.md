# SEO Audit — hutrit.com
**Fecha:** Abril 2026
**Dominio analizado:** hutrit.com / www.hutrit.com
**Auditado por:** Hutrit Marketing / Claude AI

---

## SEO Health Score: 14/100 — Grado F

> Este score refleja el estado actual del sitio desde la perspectiva de un motor de búsqueda. El problema no es el contenido del negocio — es que ese contenido es invisible para Google.

| Categoría | Score | Peso | Puntos |
|---|---|---|---|
| SEO Técnico | 5/30 | 30% | 1.5/9 |
| On-Page / Contenido indexable | 2/25 | 25% | 0.5/6.25 |
| Estrategia de contenido | 0/20 | 20% | 0/5 |
| Autoridad y backlinks | 4/15 | 15% | 0.6/2.25 |
| E-E-A-T | 3/10 | 10% | 0.3/1 |
| **TOTAL** | | | **~14/100** |

---

## Diagnóstico Ejecutivo

hutrit.com es una **SPA (Single Page Application) renderizada 100% en cliente** con JavaScript. Cuando Google, Bing o cualquier crawler visita el sitio, solo recibe código JavaScript minificado con etiquetas de analytics — sin título, sin descripción, sin headings, sin texto indexable, sin sitemap.

**Consecuencia directa:** El sitio está prácticamente ausente de los resultados de búsqueda para todas las palabras clave de su mercado.

**Prueba concreta — site:hutrit.com (abril 2026):**
- Solo 3 URLs indexadas: la homepage, el subdominio de mail, y una URL con parámetro UTM de LinkedIn
- Ningún resultado aparece al buscar "hutrit reclutamiento LATAM" ni términos relacionados
- Competidores directos (Interfell, Loopae, WeRemoto, Talently) dominan todos los términos relevantes

Esto significa que empresas buscando "contratar talento remoto LATAM" y profesionales buscando "trabajo remoto europa" nunca encuentran Hutrit organicamente. Todo el tráfico depende de canales pagados y redes sociales — un riesgo de negocio significativo.

---

## 1. Auditoría Técnica

### 1.1 Renderizado y Crawlabilidad — CRÍTICO ❌

| Check | Estado | Detalle |
|---|---|---|
| Renderizado del lado del servidor (SSR/SSG) | ❌ FALLA | 100% client-side JS. Google ve solo scripts de analytics |
| Contenido indexable sin JS | ❌ FALLA | Sin texto, headings, ni links en el HTML estático |
| Google puede renderizar JS | ⚠️ RIESGO | Google renderiza JS, pero con retraso y limitaciones — y aun así el contenido dinámico ranquea peor |
| Googlebot ve lo mismo que el usuario | ❌ FALLA | Divergencia total entre vista de usuario y vista de crawler |

**Impacto:** Es el bloqueo raíz de todos los demás problemas. Sin SSR/SSG o pre-rendering, ninguna optimización de contenido tendrá efecto.

---

### 1.2 Sitemap y robots.txt

| Check | Estado | Detalle |
|---|---|---|
| robots.txt existe | ✅ OK | Accesible en hutrit.com/robots.txt |
| robots.txt no bloquea recursos | ✅ OK | `User-agent: * / Disallow:` — permisivo, correcto |
| robots.txt apunta al sitemap | ❌ FALLA | No hay línea `Sitemap:` en robots.txt |
| sitemap.xml existe | ❌ FALLA | hutrit.com/sitemap.xml devuelve 404 |
| Sitemap enviado a Search Console | ❌ FALLA | Sin sitemap, no se puede enviar |

---

### 1.3 Meta Tags (Homepage)

| Elemento | Estado | Valor actual | Recomendado |
|---|---|---|---|
| Title tag | ❌ FALLA | No renderizado para crawlers | `Hutrit — Talento Remoto LATAM para Empresas Europeas` (55 chars) |
| Meta description | ❌ FALLA | No presente | `Conectamos empresas españolas y europeas con talento LATAM full-time. Proceso curado, perfiles validados y contratación ágil.` (125 chars) |
| Canonical tag | ❌ FALLA | No presente | `<link rel="canonical" href="https://hutrit.com/">` |
| Viewport meta | ❌ FALLA | No detectado en HTML estático | `<meta name="viewport" content="width=device-width, initial-scale=1">` |
| Robots meta | ❌ FALLA | No presente | `<meta name="robots" content="index, follow">` |
| Open Graph title | ❌ FALLA | No presente | `Hutrit — Talento Remoto LATAM para Empresas Europeas` |
| Open Graph description | ❌ FALLA | No presente | (misma que meta description) |
| Open Graph image | ❌ FALLA | No presente | Imagen branded 1200×630px |
| Twitter Card | ❌ FALLA | No presente | `summary_large_image` |

---

### 1.4 Schema Markup (Datos Estructurados)

| Schema Type | Estado | Prioridad |
|---|---|---|
| Organization | ❌ FALLA | 🔴 Crítico — identidad de marca para Google y modelos de IA |
| WebSite + SearchAction | ❌ FALLA | 🔴 Crítico — sitelinks search box |
| Service (B2B y B2C) | ❌ FALLA | 🟠 Alta — describe los servicios concretos |
| FAQPage | ❌ FALLA | 🟠 Alta — rich snippets en SERPs + visibilidad en IA |
| BreadcrumbList | ❌ FALLA | 🟡 Media — navegación para subpáginas |
| JobPosting | ❌ FALLA | 🟡 Media — para roles publicados en el sitio |

---

### 1.5 Performance y Core Web Vitals

No es posible medir directamente sin renderizado, pero los factores de riesgo son claros:

| Factor | Estado | Impacto |
|---|---|---|
| Dependencia de JS para renderizar todo el contenido | ❌ RIESGO | LCP alto — el crawler/usuario espera a que JS cargue antes de ver contenido |
| Google Tag Manager + Analytics + Clarity en `<head>` | ⚠️ RIESGO | Scripts de tracking bloquean potencialmente el render inicial |
| Sin CDN confirmado | ❓ Desconocido | Latencia variable según ubicación del usuario |
| Sin imágenes estáticas en HTML inicial | ✅ OK por ahora | No hay CLS por imágenes sin dimensión |

**Recomendación:** Correr PageSpeed Insights (https://pagespeed.web.dev) desde Chrome en modo incógnito para obtener métricas reales de LCP, FID/INP, y CLS.

---

### 1.6 URLs Indexadas (site:hutrit.com — Abril 2026)

```
https://www.hutrit.com/         ← homepage
https://mail.hutrit.com/        ← subdominio mail (no debería estar indexado)
https://hutrit.com/?trk=...     ← URL con parámetro UTM de LinkedIn (duplicado)
```

**Total indexado: 3 páginas.** Para comparación, Interfell tiene cientos de páginas indexadas incluyendo artículos de blog, guías salariales, y páginas de servicio por categoría.

---

## 2. On-Page SEO

### 2.1 Heading Hierarchy

| Elemento | Estado |
|---|---|
| H1 en homepage | ❌ No indexable (renderizado por JS) |
| Estructura H1 → H2 → H3 | ❌ No verificable — el crawler no lo ve |
| H1 contiene keyword principal | ❌ No aplica hasta resolver SSR |

### 2.2 Keyword Targeting

La homepage no está apuntando explícitamente a ninguna keyword desde la perspectiva del crawler. No hay señales semánticas que Google pueda leer.

**Keywords que debería ranquear la homepage:**

| Keyword | Intención | Dificultad estimada | Prioridad |
|---|---|---|---|
| `contratar talento remoto LATAM` | Comercial | Alta | 🔴 Primaria B2B |
| `agencia reclutamiento remoto LATAM` | Comercial | Alta | 🔴 Primaria B2B |
| `staffing remoto latinoamerica` | Comercial | Media-Alta | 🟠 Secundaria B2B |
| `reclutamiento remoto España LATAM` | Comercial | Media | 🟠 Secundaria B2B |
| `contratar appointment setter LATAM` | Transaccional | Media-Baja | 🟠 Oportunidad |
| `trabajo remoto empresas europeas LATAM` | Informacional/Comercial | Media | 🔴 Primaria B2C |
| `trabajo remoto dólares LATAM` | Informacional | Media | 🟠 Secundaria B2C |
| `appointment setter trabajo remoto` | Informacional/Transaccional | Media | 🟠 Oportunidad B2C |

---

## 3. Análisis de Contenido y E-E-A-T

### 3.1 Estado actual del contenido

| Dimensión | Score | Evidencia |
|---|---|---|
| **Experience** (Experiencia) | Weak | No hay casos de éxito, historias de placements, métricas publicadas |
| **Expertise** (Conocimiento) | Weak | Sin blog, sin guías, sin recursos educativos — todo el expertise vive en redes sociales |
| **Authoritativeness** (Autoridad) | Weak | Sin menciones externas de peso en sitios de SEO, sin directorio, poca huella web orgánica |
| **Trustworthiness** (Confianza) | Present | HTTPS activo, presencia verificada en LinkedIn, GTM instalado |

### 3.2 Brecha de contenido vs. competencia

Interfell tiene activo un blog con artículos como:
- "Cómo contratar talento tech remoto en LATAM" (ranquea para terms de alto volumen)
- "Smart Hiring 2026 en 5 claves"
- "Guía salarial TI LATAM 2026" (genera backlinks naturales)
- Podcast "SPK de Interfell"

Hutrit no tiene ninguna página de contenido indexable más allá de la homepage. Toda la producción de contenido está en Instagram y LinkedIn — canales que no transfieren autoridad SEO al dominio.

**Gap crítico:** Hutrit produce contenido de valor (lo vemos en el calendario de contenido), pero ese valor no está en el sitio. Está en plataformas de terceros que retienen el tráfico y la autoridad.

---

## 4. Análisis de Competencia

| Empresa | Fortaleza SEO | Debilidad a explotar |
|---|---|---|
| **Interfell** | Blog robusto, 8+ años, 50k+ profesionales, múltiples sub-páginas de servicio | Muy enfocado en IT — no especializado en ventas/sales roles |
| **Loopae** | Homepage bien optimizada, H1 claro, Google Consent Mode EU implementado | Contenido limitado, no aparece en búsquedas de blog |
| **WeRemoto** | Job board con SEO fuerte — aparece para "appointment setter trabajo remoto" | Es un marketplace, no una agencia curada |
| **Talently** | Fuerte en tech, UI clara | Poco enfoque en sales roles y en mercado europeo |
| **RemoteLatinos** | Dominan "hire from LATAM" en inglés | Mercado anglófono — oportunidad para español |

**Ventana de oportunidad de Hutrit:**
1. Nadie domina el nicho "ventas remotas LATAM → empresas europeas" en español con contenido de calidad
2. El ángulo "comunidad + proceso curado" (vs. marketplace anónimo) es diferenciador con potencial de posicionamiento editorial
3. Los roles específicos (Appointment Setter, Lead Qualifier) tienen búsquedas activas con competencia media-baja en español

---

## 5. AEO/GEO — Visibilidad en Respuestas de IA

**Estado actual:** Hutrit no aparece en respuestas de ChatGPT, Claude, Gemini ni Perplexity cuando alguien pregunta sobre "mejores plataformas para contratar talento LATAM", "cómo contratar appointment setter remoto" o términos similares.

**Por qué:** Los modelos de IA se nutren de:
1. Contenido indexable en la web (artículos, guías, FAQs)
2. Menciones en sitios de autoridad (directorios, rankings, prensa)
3. Datos estructurados (schema Organization, FAQ, Service)
4. Consistencia de información de marca en múltiples fuentes

Hutrit tiene poco de lo anterior. Sin contenido indexable, sin menciones en rankings del sector, y sin schema, los modelos de IA no tienen material para citar a Hutrit.

---

## 6. Plan de Acción Priorizado

---

### 🔴 FASE 1 — Crítico (Mes 1): Hacer el sitio indexable

> Sin completar esta fase, todo lo demás es irrelevante. Es el prerequisito técnico.

#### Acción 1.1 — Resolver el problema de renderizado (JS SPA)

**Problema:** Google solo ve JavaScript. No hay HTML con contenido.

**Opciones ordenadas por impacto/costo:**

| Opción | Esfuerzo | Costo | Impacto |
|---|---|---|---|
| **A) Pre-rendering con Prerender.io** | Bajo — 1-3 días | ~$45/mes | ★★★★ — Sirve HTML estático a crawlers sin reescribir el frontend |
| **B) Migrar a Next.js/Nuxt.js con SSR** | Alto — 2-4 semanas | Dev time | ★★★★★ — Solución permanente y óptima para performance |
| **C) Implementar Static Site Generation (Astro/Next)** | Medio — 1-2 semanas | Dev time | ★★★★★ — Ideal si el contenido no cambia frecuentemente |
| **D) Prerender manual con react-snap o similar** | Medio | Sin costo extra | ★★★ — Genera HTML estático en build time |

**Recomendación:** Empezar con **Prerender.io** como solución puente mientras se planea la migración a Next.js/Nuxt.js. Prerender intercepta las peticiones de crawlers y les sirve HTML pre-renderizado.

---

#### Acción 1.2 — Crear sitemap.xml

Crear `/public/sitemap.xml` con todas las URLs del sitio. Estructura mínima:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://hutrit.com/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://hutrit.com/como-funciona</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://hutrit.com/roles</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://hutrit.com/empresas</loc>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://hutrit.com/blog</loc>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>
```

---

#### Acción 1.3 — Actualizar robots.txt

```
User-agent: *
Disallow: /app/
Disallow: /dashboard/
Disallow: /api/

Sitemap: https://hutrit.com/sitemap.xml
```

---

#### Acción 1.4 — Implementar meta tags estáticos por página

Para cada ruta del sitio, implementar meta tags únicos. Ejemplo para homepage:

```html
<!-- Básicos -->
<title>Hutrit — Talento Remoto LATAM para Empresas Europeas</title>
<meta name="description" content="Conectamos empresas españolas y europeas con talento LATAM full-time. Proceso curado, perfiles validados y contratación ágil en ventas, tech y marketing.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://hutrit.com/">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:title" content="Hutrit — Talento Remoto LATAM para Empresas Europeas">
<meta property="og:description" content="Conectamos empresas españolas y europeas con talento LATAM full-time. Proceso curado, perfiles validados y contratación ágil.">
<meta property="og:image" content="https://hutrit.com/og-image.jpg">
<meta property="og:url" content="https://hutrit.com/">
<meta property="og:locale" content="es_ES">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Hutrit — Talento Remoto LATAM para Empresas Europeas">
<meta name="twitter:image" content="https://hutrit.com/og-image.jpg">
```

---

#### Acción 1.5 — Implementar Schema Markup (JSON-LD)

Agregar en el `<head>` de la homepage:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://hutrit.com/#organization",
      "name": "Hutrit",
      "url": "https://hutrit.com",
      "logo": "https://hutrit.com/logo.png",
      "description": "Plataforma de reclutamiento remoto que conecta talento LATAM con empresas europeas.",
      "foundingLocation": "Madrid, España",
      "sameAs": [
        "https://www.linkedin.com/company/hutrit",
        "https://www.instagram.com/hutrit.club"
      ],
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer support",
        "email": "hola@hutrit.com"
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://hutrit.com/#website",
      "url": "https://hutrit.com",
      "name": "Hutrit",
      "publisher": {"@id": "https://hutrit.com/#organization"},
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://hutrit.com/buscar?q={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    },
    {
      "@type": "Service",
      "name": "Reclutamiento de Talento Remoto LATAM",
      "provider": {"@id": "https://hutrit.com/#organization"},
      "description": "Servicio de reclutamiento remoto que conecta profesionales latinoamericanos con empresas europeas en roles de ventas, tecnología y marketing.",
      "areaServed": ["España", "Europa"],
      "serviceType": "Staffing Remoto"
    }
  ]
}
```

---

#### Acción 1.6 — Registrar en Google Search Console y Bing Webmaster Tools

1. Verificar propiedad de hutrit.com en [Google Search Console](https://search.google.com/search-console)
2. Enviar sitemap.xml
3. Solicitar indexación manual de la homepage
4. Registrar también en [Bing Webmaster Tools](https://www.bing.com/webmasters)
5. Activar alerta de errores de cobertura de indexación

---

### 🟠 FASE 2 — Alta Prioridad (Mes 1-2): Contenido SEO Base

> Una vez que el sitio es crawleable, estas páginas deben existir para capturar tráfico transaccional.

#### Acción 2.1 — Crear páginas de servicio dedicadas (B2B)

| URL | Keyword objetivo | Intención |
|---|---|---|
| `/empresas` | "contratar talento remoto LATAM", "agencia reclutamiento remoto" | Comercial |
| `/como-funciona` | "cómo contratar remotamente LATAM" | Informacional/Comercial |
| `/roles/appointment-setter` | "contratar appointment setter LATAM", "appointment setter remoto" | Transaccional |
| `/roles/lead-qualifier` | "lead qualifier remoto LATAM" | Transaccional |
| `/roles/hiring-advisor` | "hiring advisor remoto" | Transaccional |

Cada página debe tener:
- Title tag único con keyword
- H1 con keyword principal
- 300-600 palabras de contenido real
- Schema Service
- CTA claro

#### Acción 2.2 — Crear página Hutrit Club (B2C) dedicada

URL: `https://hutrit.club` (si el dominio existe) o `/club`

- Keyword objetivo: "trabajo remoto empresas europeas LATAM", "trabajo remoto dólares"
- Separar visualmente el pitch B2C del B2B
- Incluir los roles disponibles con descripción, salario y requisitos
- Schema JobPosting si hay vacantes activas

#### Acción 2.3 — Eliminar el subdominio mail.hutrit.com de los resultados de búsqueda

`mail.hutrit.com` aparece en los resultados indexados de Google. Agregar:
```
# En robots.txt del subdominio mail.hutrit.com:
User-agent: *
Disallow: /
```
O usar meta robots `noindex` en el HTML de ese subdominio.

#### Acción 2.4 — Limpiar URLs con parámetros UTM

`hutrit.com/?trk=public_post-text` está indexada como página duplicada. Agregar al robots.txt o usar canonical para consolidar:
```
Disallow: /*?trk=*
Disallow: /*?utm_*
```

---

### 🟡 FASE 3 — Estrategia de Contenido (Mes 2-4): Autoridad Orgánica

> Esta fase construye el activo SEO de largo plazo: tráfico orgánico sostenible.

#### Acción 3.1 — Lanzar blog en hutrit.com/blog o blog.hutrit.com

**Cadencia recomendada:** 2 artículos por mes (calidad > cantidad)

**Pilares de contenido y artículos prioritarios:**

**Pilar B2B — Para empresas:**
| Artículo | Keyword objetivo | Volumen potencial |
|---|---|---|
| "Cómo contratar talento remoto en LATAM desde España: guía completa 2026" | contratar talento remoto LATAM España | Alto |
| "Cuánto cuesta un Appointment Setter en LATAM: guía de salarios 2026" | salario appointment setter LATAM | Medio |
| "Las 5 mejores agencias de reclutamiento remoto en LATAM para empresas europeas" | agencias reclutamiento remoto LATAM | Medio-Alto |
| "Appointment Setter vs. Lead Qualifier: cuál contratar primero" | appointment setter vs lead qualifier | Medio |
| "Cómo reducir el tiempo de contratación remota a menos de 3 semanas" | contratar remoto rápido LATAM | Bajo-Medio |

**Pilar B2C — Para talento:**
| Artículo | Keyword objetivo | Volumen potencial |
|---|---|---|
| "Cómo conseguir trabajo remoto con empresas europeas desde LATAM en 2026" | trabajo remoto empresas europeas LATAM | Alto |
| "Appointment Setter: qué es, cuánto gana y cómo entrar al rol" | qué es appointment setter trabajo remoto | Medio-Alto |
| "Guía para preparar tu perfil de LinkedIn para trabajo remoto internacional" | LinkedIn trabajo remoto internacional | Medio |
| "Lead Qualifier en remoto: el rol que más crece en ventas B2B" | lead qualifier trabajo remoto | Medio |
| "Venezuela/Colombia/Argentina: cómo acceder a trabajo remoto con empresas de Europa" | trabajo remoto [país] empresas europeas | Medio por país |

---

#### Acción 3.2 — Optimizar para Featured Snippets

Artículos que respondan preguntas frecuentes con el formato correcto generan snippets en posición 0.

**Ejemplo — Artículo: "¿Qué es un Appointment Setter?"**

```markdown
## ¿Qué es un Appointment Setter?

Un Appointment Setter es un profesional de ventas que se encarga de contactar 
prospectos calificados, generar interés en un producto o servicio, y agendar 
reuniones o demostraciones para el equipo de cierre. Es el primer eslabón del 
pipeline de ventas en empresas B2B modernas.

**Funciones principales:**
- Prospecting y contacto inicial (email, LinkedIn, llamada)
- Calificación básica del prospecto (¿encaja con el ICP?)
- Agendado de reunión con el ejecutivo de ventas o CEO
- Seguimiento hasta confirmar la cita

**Salario promedio:** $800 - $1,500 USD/mes para profesionales LATAM en roles remotos.
```

Este formato de respuesta directa + lista + dato específico maximiza las probabilidades de capturar el snippet.

---

#### Acción 3.3 — Implementar FAQ Schema en páginas clave

Agregar FAQPage schema en la homepage, página de empresas, y páginas de roles. Esto genera rich snippets en Google y aumenta la probabilidad de ser citado por modelos de IA.

```json
{
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "¿Cómo funciona el proceso de reclutamiento de Hutrit?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "El proceso de Hutrit tiene 4 pasos: (1) La empresa define el perfil ideal, (2) Hutrit activa su red de talento LATAM y filtra candidatos, (3) Se presentan 3-5 perfiles curados en menos de 3 semanas, (4) La empresa hace la selección final y Hutrit gestiona la incorporación remota."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cuánto cuesta contratar a través de Hutrit?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Hutrit trabaja con modelo de fee de colocación. El costo es significativamente menor que contratar a través de agencias locales europeas, con acceso a talento LATAM altamente calificado a salarios competitivos internacionalmente."
      }
    },
    {
      "@type": "Question",
      "name": "¿En qué países de LATAM recluta Hutrit?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Hutrit tiene presencia activa en Venezuela, Colombia, Argentina, Perú, Ecuador y Bolivia, con foco en talento urbano de alta empleabilidad en roles de ventas, tecnología y marketing."
      }
    }
  ]
}
```

---

### 🔵 FASE 4 — Autoridad y AEO (Mes 3-6): Dominar el espacio

#### Acción 4.1 — Link Building estratégico

| Táctica | Acción | Impacto SEO |
|---|---|---|
| **Directorios de agencias** | Registrar Hutrit en G2, Clutch, Bark.com como agencia de reclutamiento | Alto — links de autoridad + menciones de marca |
| **Rankeos del sector** | Contactar autores de "mejores agencias reclutamiento LATAM 2026" para ser incluidos | Alto — tráfico referido + backlink |
| **Guest posts** | Artículos en blogs de RR.HH. de España o LATAM (InfoJobs blog, Kenjo, etc.) | Medio-Alto |
| **Prensa** | Nota de prensa sobre crecimiento/datos del sector para medios digitales hispanohablantes | Alto — autoridad de dominio |
| **Guía salarial** | Publicar "Guía Salarial Ventas Remotas LATAM 2026" — generará backlinks naturales | Muy Alto — recurso linkeable |

#### Acción 4.2 — Optimización para IA (AEO/GEO)

Para que Hutrit sea citado por ChatGPT, Claude, Gemini y Perplexity:

1. **Crear una Wikipedia/Crunchbase entry** — Los modelos de IA aprenden de estas fuentes de alta autoridad
2. **Publicar datos propios del sector** — "X% del talento LATAM busca trabajo con empresas europeas" — citables por IA
3. **Aparecer en al menos 3 rankings externos** — Los modelos aprenden de listas y comparativas
4. **Consistencia de NAP** (Name, Address, Phone) en todos los directorios y la web
5. **FAQ públicas con preguntas literales** que los usuarios hacen a los modelos de IA:
   - "¿Qué es Hutrit?"
   - "¿Cómo funciona Hutrit Club?"
   - "¿Cuánto cobra Hutrit por una contratación?"
6. **Menciones en LinkedIn Pulse y Medium** — indexados por buscadores y utilizados como fuentes por modelos

---

## 7. Resumen de Quick Wins (Primeras 2 Semanas)

| Acción | Esfuerzo | Tiempo estimado | Impacto |
|---|---|---|---|
| Implementar Prerender.io | Bajo (plugin/config) | 1-2 días | 🔴 Crítico |
| Crear sitemap.xml | Muy bajo | 1 hora | 🔴 Crítico |
| Actualizar robots.txt con `Sitemap:` | Muy bajo | 15 min | 🔴 Crítico |
| Agregar title/meta description estáticos | Bajo | 2-4 horas | 🔴 Crítico |
| Registrar en Google Search Console | Muy bajo | 30 min | 🔴 Crítico |
| Agregar Organization schema JSON-LD | Bajo | 2-3 horas | 🟠 Alta |
| Agregar canonical tags por ruta | Bajo | 1-2 horas | 🟠 Alta |
| Bloquear mail.hutrit.com de indexación | Muy bajo | 15 min | 🟡 Media |
| Bloquear URLs con parámetros UTM | Muy bajo | 15 min | 🟡 Media |

---

## 8. KPIs de Seguimiento

| Métrica | Estado Actual | Meta 3 meses | Meta 6 meses |
|---|---|---|---|
| Páginas indexadas (site:hutrit.com) | 3 | 15-20 | 30-50 |
| Ranking para "contratar talento remoto LATAM" | No posicionado | Top 20 | Top 10 |
| Tráfico orgánico mensual | ~0 estimado | 200-500 sesiones | 1,000-3,000 sesiones |
| Backlinks de dominio | Desconocido | +10 dominios referidos | +25 dominios |
| Visibilidad en AI (ChatGPT/Perplexity) | No aparece | Mencionado en 1-2 queries | Top 3 en queries de nicho |
| Core Web Vitals — LCP | No medido | < 2.5s | < 1.8s |

---

## 9. Stack de Herramientas Recomendado

| Herramienta | Uso | Costo |
|---|---|---|
| **Google Search Console** | Monitoreo de indexación y clicks | Gratis |
| **Bing Webmaster Tools** | Indexación en Bing/Microsoft AI | Gratis |
| **Prerender.io** | Pre-rendering para crawlers (puente hasta SSR) | ~$45/mes |
| **Ahrefs Webmaster Tools** (gratis) | Monitoreo de backlinks y keywords | Gratis (limitado) |
| **Ubersuggest / Semrush** | Investigación de keywords | $29-129/mes |
| **Google PageSpeed Insights** | Core Web Vitals | Gratis |
| **Schema Markup Validator** | Validar JSON-LD | Gratis |
| **Screaming Frog** (gratis hasta 500 URLs) | Auditoría técnica crawl | Gratis |

---

## 10. Conclusión

hutrit.com tiene un negocio real con diferenciadores claros en un mercado en crecimiento. El problema de SEO es 90% técnico, no estratégico. La buena noticia: los problemas técnicos tienen soluciones concretas y la competencia no ha saturado aún el nicho de "ventas remotas LATAM → Europa".

La prioridad es clara:
1. **Hacer el sitio indexable** (Fase 1) — sin esto, nada más importa
2. **Crear páginas de destino para cada servicio** (Fase 2) — captura tráfico de alto valor inmediatamente
3. **Construir autoridad con contenido** (Fase 3) — el activo SEO que trabaja 24/7 sin costo variable

Con 3-6 meses de ejecución consistente, Hutrit puede pasar de ser invisible en búsquedas a aparecer en los primeros resultados para los términos que sus clientes y candidatos buscan activamente.

---

*Auditoría generada: Abril 2026 | Próxima revisión recomendada: Julio 2026*
