# Análisis de Plantillas de Marca — Hutrit

> Análisis técnico basado en inspección XML y de píxeles de los tres archivos de plantilla:
> `_templates/Presentacion Empresas.pptx` · `_templates/Carruseles y estaticos linkedin .pptx` · `_templates/Hutrit Club (Carruseles y Estaticos) Instagram.pptx`

---

## Qué se puede y qué no se puede reproducir

### Se puede reproducir directamente
- Sistema de color completo (todos los códigos hexadecimales verificados del XML)
- Familia tipográfica completa (Mulish en sus variantes Heavy, Bold, Semi-Bold, Bold Italics)
- Tamaños de fuente exactos por nivel jerárquico
- Estructura de layouts identificados (portada, contenido, paso, CTA)
- Iconos numerados SVG vectoriales (extraídos, reproducibles)
- Dimensiones exactas de cada formato (LinkedIn/Instagram: 4:5; Presentación: 16:9)
- Patrones de color por tipo de diapositiva (oscuro = portada/cierre, claro = contenido)

### Requiere extracción desde el archivo original — NO omitir ni sustituir
- **Logo de Hutrit y Hutrit Club** — aparece como imagen embebida en múltiples diapositivas; debe extraerse de los archivos originales del media folder (`/ppt/media/`). Si se intenta reemplazar con texto perderá fidelidad de marca.
- **Imágenes fotográficas de personas** — usadas en slides de portada y testimonios; son activos de fotografía que no se regeneran automáticamente.
- **Elementos decorativos de portada complejos** — las portadas de LinkedIn/Instagram tienen ~23 formas superpuestas (capas de imagen con opacidad, desplazamientos, freeforms) que forman una composición imposible de recrear fielmente sin los archivos fuente. Se deben reutilizar desde el original.

### Se simplificaría al recrear
- Las portadas (slide 1 de cada carrusel) usan composiciones de 20-24 capas de imagen; al recrear, se simplificarán a 3-5 capas manteniendo la estructura visual general.

---

## 1. Sistema de Color

### Paleta principal (compartida por los tres archivos)

| Rol | Hex | Descripción |
|-----|-----|-------------|
| **Fondo oscuro primario** | `#004949` | Teal oscuro / verde petróleo — color dominante de marca |
| **Fondo oscuro secundario** | `#005959` | Teal ligeramente más claro (variante de hover/énfasis) |
| **Fondo neutro oscuro** | `#545454` | Gris carbón — diapositivas de transición/testimonio |
| **Acento verde principal** | `#12A562` | Verde brillante — CTA, destacados, fondos de pasos |
| **Acento verde medio** | `#009B58` | Verde esmeralda — variante usada en Instagram |
| **Fondo claro mint** | `#DEF4EA` / `#CFF2DF` | Verde muy claro — fondos de contenido en presentación |
| **Acento rojo** | `#FF3131` / `#DC433A` | Rojo — usado con moderación para urgencia/contraste |
| **Blanco** | `#FFFFFF` | Texto sobre fondos oscuros y en CTAs |
| **Negro/casi negro** | `#000000` / `#000D0D` | Portada y cierre de la presentación empresarial |

### Patrón de uso por tipo de diapositiva

| Tipo de slide | Color de fondo | Color de texto |
|---------------|----------------|----------------|
| Portada del carrusel | `#004949` o `#005959` | `#FFFFFF` |
| Slide de paso/contenido | `#12A562` | `#004949` o `#FFFFFF` |
| Slide de transición/reflejo | `#545454` | `#FFFFFF` |
| CTA / cierre | `#005959` | `#FFFFFF` + `#12A562` como acento |
| Portada de presentación (empresas) | `#000000`/`#000D0D` | `#FFFFFF` |
| Slides de contenido de presentación | `#CFF2DF` | `#004949` + `#545454` |

**Regla general:** Las diapositivas oscuras (`#004949`, `#545454`) se usan para portadas, cierres y slides de impacto emocional. Las diapositivas verdes brillantes (`#12A562`) se usan para pasos numerados y contenido estructurado. Las diapositivas claras mint se usan exclusivamente en la presentación B2B de largo aliento.

---

## 2. Tipografía

### Familia tipográfica
**Mulish** — única familia usada en los tres archivos. Es una fuente sans-serif moderna disponible en Google Fonts.

| Variante | Uso principal |
|----------|---------------|
| **Mulish Heavy** | Títulos principales, encabezados de portada, declaraciones de impacto |
| **Mulish Bold** | Subtítulos, texto de pasos, cuerpo prominente |
| **Mulish Semi-Bold** | Etiquetas secundarias, texto de apoyo |
| **Mulish Bold Italics** | Branding "Club" (Hutrit Club), énfasis decorativo |
| **Mulish** (Regular) | Cuerpo de texto corrido |

### Estilo de texto
- **Todos los títulos principales en MAYÚSCULAS** — sin excepciones en LinkedIn; Instagram mezcla mayúsculas con título capitalizado
- **Sin letra espaciada (letter-spacing)** — el impacto viene del peso, no del tracking
- **Sin subrayados ni líneas decorativas bajo títulos**
- **Alineación**: centrada para títulos de portada; izquierda para contenido de pasos

### Escala tipográfica

| Nivel | Tamaño aproximado | Variante | Contexto |
|-------|-------------------|----------|---------|
| Título de portada principal | 71–74pt | Mulish Heavy | Portadas LinkedIn/Instagram |
| Título de portada Instagram | 90pt | Mulish Bold | CTA final de carrusel |
| Encabezado de sección | 54pt | Mulish Heavy | Introducción de paso/slide de hook |
| Encabezado de contenido | 41–42pt | Mulish Heavy / Bold | Cada slide de contenido |
| Subtítulo / descripción | 39pt | Mulish Bold | Subtítulos de portada |
| Cuerpo destacado | 35–36pt | Mulish Bold / Heavy | Texto de desarrollo en Instagram |
| Cuerpo de apoyo | 31pt | Mulish Heavy | Texto secundario en LinkedIn |
| Etiqueta / label | 23–25pt | Mulish Semi-Bold | Metadatos, labels de paso |
| Logo Hutrit Club (italic) | 32–36pt | Mulish Bold Italics | Branding Club en slides de cierre |

---

## 3. Patrones de Diseño — Layouts Identificados

### Archivo: Carruseles LinkedIn y Carruseles Instagram
(Formato: 4:5 vertical — 1080×1350px equivalente, ~28.6cm × 35.7cm)

#### Layout 1 — Portada de carrusel (Slide 1)
- **Composición compleja**: 20-24 capas superpuestas (imágenes de personas, overlays de color, freeforms, logo, texto)
- **Estructura visual**: imagen de persona en primer plano sobre fondo teal con overlay de color y formas orgánicas
- **Texto**: 1 título grande en MAYÚSCULAS, centrado o alineado a la izquierda inferior
- **Logo**: esquina superior izquierda o inferior derecha (varía por carrusel)
- **Nota**: requiere reutilizar desde el original — no recrear desde cero

#### Layout 2 — Hook / Replanteamiento (slides 2-3)
- Fondo sólido oscuro (`#004949`) o gris (`#545454`)
- 1-2 textboxes de texto grande (41-71pt)
- Sin imágenes (solo texto y fondo de color)
- Texto en blanco, peso Heavy, MAYÚSCULAS
- Puede incluir 1 imagen pequeña decorativa o logo

#### Layout 3 — Slide de paso numerado (slides 4-7)
- Fondo sólido verde `#12A562`
- 3 elementos de texto: número del paso (54pt Heavy), nombre del paso (31pt Heavy), descripción (25pt)
- 1-2 iconos SVG numerados (círculo con número en `#004949` o `#009B58`)
- Imagen de fondo parcial o decorativa (baja opacidad)
- Color de texto: `#004949` sobre verde

#### Layout 4 — Slide de reflexión / pregunta (slides de "mito vs realidad", preguntas)
- Fondo sólido `#545454` (gris)
- 1 bloque de texto grande en blanco
- Sin imágenes — solo tipografía e impacto de color

#### Layout 5 — CTA / Cierre de carrusel
- Fondo `#12A562` o `#005959`
- Texto de llamado a la acción en blanco (90pt para carruseles Instagram)
- "Club" en Mulish Bold Italics como branded element
- Botón o texto "REGÍSTRATE GRATIS" en caja destacada
- Logo en esquina

#### Layout 6 — Testimonio / cita
- Fondo `#545454`
- Texto de cita en blanco, tamaño medio (31-35pt)
- Nombre/cargo debajo en tamaño menor
- Puede incluir imagen de perfil pequeña o sin imágenes

---

### Archivo: Presentacion Empresas
(Formato: 16:9 widescreen — 5333×3000px)

> **Nota importante**: Este archivo está construido 100% con imágenes PNG incrustadas. No tiene texto editable ni colores XML. Cada diapositiva es una imagen completa exportada desde otra herramienta (probablemente Canva o Figma).

#### Portada y cierre (slides 1 y 16)
- Fondo casi negro / teal muy oscuro (`#000000`, `#000D0D`)
- Probable: logo grande, tagline, imagen de persona o elemento gráfico central

#### Slides de contenido (slides 2-15)
- Fondo mint muy claro (`#CFF2DF`, `#B4DCC8`) — versión clara de la paleta de marca
- Probable: texto oscuro, iconos, datos estructurados
- Formato más "documental" y menos impactante que los carruseles sociales

---

## 4. Elementos Decorativos

### Identificados y reproducibles
| Elemento | Descripción | Reproducible |
|----------|-------------|--------------|
| **Iconos numerados SVG** | Círculos con número 1, 2, 3 en `#004949` y `#009B58` | Sí — SVGs disponibles en `/ppt/media/` |
| **Fondos de color sólido** | Rectángulos de fondo en los colores de paleta | Sí — recrear con formas sólidas |
| **Overlays de opacidad** | Rectángulos semi-transparentes sobre imágenes | Sí — con `alphaModFix` o transparencia |
| **Formas orgánicas (freeforms)** | Formas vectoriales irregulares en portadas | Parcialmente — simplificar a formas básicas |

### Identificados pero a extraer del original
| Elemento | Descripción | Acción |
|----------|-------------|--------|
| **Logo Hutrit** | Aparece en slides de portada y CTA | Extraer de `/ppt/media/` del archivo original |
| **Logo Hutrit Club** | Con el estilo italic y marca separada | Extraer de `/ppt/media/` del archivo original |
| **Fotografías de personas** | Imágenes de talento/profesionales en portadas | Extraer de `/ppt/media/` — no reemplazar con stock genérico |
| **Texturas de fondo** | Algunas portadas tienen texturas sutiles superpuestas | Extraer de `/ppt/media/` |

---

## 5. Elementos Recurrentes

### Presentes en la mayoría de los slides (LinkedIn e Instagram)

| Elemento | Posición | Tamaño aprox. | Presencia |
|----------|----------|---------------|-----------|
| **Logo Hutrit / Hutrit Club** | Esquina superior izquierda o inferior derecha | Pequeño (~5-8% del ancho) | Portada + CTA final |
| **"Club"** en Mulish Bold Italics | Integrado como elemento de marca en texto | Variable | Todos los slides de Hutrit Club |
| **"REGÍSTRATE GRATIS"** | Inferior del slide, dentro de caja o como texto destacado | 32-36pt | Slides de CTA |
| **Fondo de color sólido** | Cubre todo el slide | 100% | Todos los slides de contenido |
| **Sin número de página visible** | — | — | Ninguno de los tres archivos usa números de página |
| **Sin pie de página de texto** | — | — | No hay footer de texto recurrente |

### Patrón de logo específico
- **Portada** (slide 1): logo visible, tamaño mediano, integrado en la composición
- **Slides de contenido** (2-n): sin logo
- **CTA/cierre** (último slide): logo visible + branding "Club" + CTA
- **Nota**: el logo NO aparece en todos los slides — solo en portada y cierre

---

## Resumen ejecutivo para recreación

Para recrear cualquier entregable basado en estas plantillas, seguir este orden:

1. **Extraer el logo y las fotografías** del `/ppt/media/` de los archivos originales antes de empezar
2. **Usar Mulish de Google Fonts** en las variantes Heavy, Bold, Semi-Bold y Bold Italics
3. **Aplicar la paleta de colores** según el tipo de slide (ver tabla de patrón de uso)
4. **Simplificar las portadas** a 3-5 capas (fondo + imagen de persona + overlay + texto + logo)
5. **Reutilizar los iconos SVG numerados** directamente desde el media folder
6. **No recrear la Presentacion Empresas desde cero** — al ser 100% imagen, cualquier nueva versión debe editarse en la herramienta fuente (Canva/Figma) y re-exportarse como imágenes
