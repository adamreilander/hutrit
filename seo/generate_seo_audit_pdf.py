# -*- coding: utf-8 -*-
"""
SEO Audit PDF Generator -- hutrit.com
Generates a professional PDF report from the SEO audit content.
Brand colors: #004949 (dark teal), #12A562 (green)
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

# ?? Brand colors ???????????????????????????????????????????????????????????????
TEAL   = (0,   73,  73)   # #004949
GREEN  = (18, 165,  98)   # #12A562
WHITE  = (255, 255, 255)
LIGHT  = (245, 248, 248)  # very light teal tint for alternating rows
DARK   = (30,  30,  30)   # near-black body text
GREY   = (100, 100, 100)  # secondary text
BORDER = (200, 210, 210)  # table border

OUTPUT_PATH = r"c:\Users\Admin\Documents\Hutrit\seo\SEO-AUDIT-hutrit.pdf"


# ?? Custom PDF class ???????????????????????????????????????????????????????????
class AuditPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(18, 18, 18)
        self._toc_entries = []   # (title, page)

    # ?? Header / Footer ??????????????????????????????????????????????????????
    def header(self):
        if self.page_no() == 1:
            return
        # Thin teal top bar
        self.set_fill_color(*TEAL)
        self.rect(0, 0, 210, 6, "F")
        self.set_y(10)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*GREY)
        self.cell(0, 5, "SEO AUDIT -- hutrit.com -- Abril 2026", align="L",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-14)
        # Thin bottom rule
        self.set_draw_color(*TEAL)
        self.set_line_width(0.4)
        self.line(18, self.get_y(), 192, self.get_y())
        self.ln(1)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GREY)
        self.cell(0, 5, f"Página {self.page_no()}", align="C")

    # ?? Helpers ???????????????????????????????????????????????????????????????
    def section_break(self):
        """Force a new page for a major section."""
        self.add_page()

    def cover_page(self):
        self.add_page()
        # Full-bleed teal top half
        self.set_fill_color(*TEAL)
        self.rect(0, 0, 210, 148, "F")

        # Logo area -- wordmark text
        self.set_xy(0, 40)
        self.set_font("Helvetica", "B", 36)
        self.set_text_color(*WHITE)
        self.cell(210, 14, "hutrit", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("Helvetica", "", 13)
        self.set_text_color(*GREEN)
        self.cell(210, 8, "hutrit.com", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Title block
        self.ln(12)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*WHITE)
        self.cell(210, 12, "SEO AUDIT", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 14)
        self.cell(210, 8, "Reporte completo de visibilidad orgánica", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Score badge -- green circle area
        self.ln(10)
        cx, cy, r = 105, 118, 18
        self.set_fill_color(*GREEN)
        self.ellipse(cx - r, cy - r, r * 2, r * 2, "F")
        self.set_xy(0, cy - 10)
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*WHITE)
        self.cell(210, 8, "14/100", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 9)
        self.cell(210, 5, "Score  |  Grado F", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Lower white area metadata
        self.set_xy(0, 155)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*DARK)
        meta = [
            ("Dominio",  "hutrit.com"),
            ("Fecha",    "Abril 2026"),
            ("Revisión", "Julio 2026"),
        ]
        for label, value in meta:
            self.cell(105, 8, f"{label}:", align="R",
                      new_x=XPos.RIGHT, new_y=YPos.LAST)
            self.set_font("Helvetica", "B", 11)
            self.cell(105, 8, f"  {value}", align="L",
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_font("Helvetica", "", 11)

        # Thin green accent bar across the middle
        self.set_fill_color(*GREEN)
        self.rect(0, 148, 210, 2.5, "F")

    def h1(self, text):
        """Major section heading -- full-width teal band."""
        self.set_fill_color(*TEAL)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 13)
        self.cell(0, 10, f"  {text}", fill=True,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)
        self.set_text_color(*DARK)

    def h2(self, text):
        """Sub-section heading with green left accent bar."""
        self.set_fill_color(*GREEN)
        self.rect(18, self.get_y(), 3, 7, "F")
        self.set_xy(23, self.get_y())
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*TEAL)
        self.cell(0, 7, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)
        self.set_text_color(*DARK)

    def h3(self, text):
        """Tertiary heading."""
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*TEAL)
        self.cell(0, 6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)
        self.set_text_color(*DARK)

    def body(self, text):
        """Paragraph body text with word-wrap."""
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK)
        self.multi_cell(0, 5.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1.5)

    def bullet(self, text, indent=5, symbol="-"):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK)
        self.set_x(self.l_margin + indent)
        self.cell(5, 5.5, symbol, new_x=XPos.RIGHT, new_y=YPos.LAST)
        self.multi_cell(0, 5.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def status_badge(self, status, x, y, w=28, h=5.5):
        """Render a colored OK / FALLA badge."""
        ok = status.strip().upper() == "OK"
        self.set_fill_color(*(GREEN if ok else (220, 50, 47)))
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 8)
        self.set_xy(x, y)
        self.cell(w, h, status.strip(), fill=True, align="C")

    def table(self, headers, rows, col_widths=None, stripe=True):
        """Render a styled table."""
        usable = 174  # 210 - 2*18 margins
        if col_widths is None:
            w = usable / len(headers)
            col_widths = [w] * len(headers)

        row_h = 6.5

        # Header row
        self.set_fill_color(*TEAL)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 8.5)
        self.set_draw_color(*TEAL)
        self.set_line_width(0.1)
        for i, (hdr, cw) in enumerate(zip(headers, col_widths)):
            self.cell(cw, row_h + 1, f" {hdr}", border=1, fill=True,
                      new_x=XPos.RIGHT, new_y=YPos.LAST)
        self.ln(row_h + 1)

        # Data rows
        self.set_text_color(*DARK)
        self.set_font("Helvetica", "", 8.5)
        self.set_draw_color(*BORDER)

        # Detect if the last row is a totals row (starts with bold marker)
        for r_idx, row in enumerate(rows):
            is_total = str(row[0]).startswith("**")
            is_stripe = stripe and (r_idx % 2 == 1)

            if is_total:
                self.set_fill_color(*TEAL)
                self.set_text_color(*WHITE)
                self.set_font("Helvetica", "B", 8.5)
                fill = True
            elif is_stripe:
                self.set_fill_color(*LIGHT)
                fill = True
            else:
                self.set_fill_color(*WHITE)
                fill = True

            row_start_y = self.get_y()
            max_lines = 1
            # Pre-calculate lines needed per cell
            lines_per_cell = []
            for cell_val, cw in zip(row, col_widths):
                text = str(cell_val).replace("**", "").strip()
                lines_per_cell.append(text)

            actual_h = row_h  # single-line height

            for i, (text, cw) in enumerate(zip(lines_per_cell, col_widths)):
                self.set_xy(self.l_margin + sum(col_widths[:i]), row_start_y)
                if is_total:
                    self.set_fill_color(*TEAL)
                    self.set_text_color(*WHITE)
                    self.set_font("Helvetica", "B", 8.5)
                elif is_stripe:
                    self.set_fill_color(*LIGHT)
                    self.set_text_color(*DARK)
                    self.set_font("Helvetica", "", 8.5)
                else:
                    self.set_fill_color(*WHITE)
                    self.set_text_color(*DARK)
                    self.set_font("Helvetica", "", 8.5)
                self.cell(cw, actual_h, f" {text}", border=1, fill=fill,
                          new_x=XPos.RIGHT, new_y=YPos.LAST)
            self.ln(actual_h)

        self.set_draw_color(*TEAL)
        self.ln(3)
        self.set_text_color(*DARK)

    def callout(self, text, color=None):
        """Highlighted callout box."""
        if color is None:
            color = TEAL
        self.set_fill_color(*LIGHT)
        self.set_draw_color(*color)
        self.set_line_width(0.6)
        # Left accent
        x, y = self.get_x(), self.get_y()
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*color)
        # Draw thick left border
        self.set_draw_color(*color)
        self.set_line_width(2)
        line_h = len(self.multi_cell(0, 5.5, text, dry_run=True, output="LINES")) * 5.5 + 4
        self.line(x, y, x, y + line_h)
        self.set_line_width(0.1)
        self.set_fill_color(*LIGHT)
        self.rect(x, y, 174, line_h, "F")
        self.set_xy(x + 4, y + 2)
        self.multi_cell(170, 5.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)
        self.set_text_color(*DARK)


# ?? Build PDF ??????????????????????????????????????????????????????????????????
def build_pdf():
    pdf = AuditPDF()

    # ?? COVER ??????????????????????????????????????????????????????????????????
    pdf.cover_page()

    # ?? PAGE 2: EXECUTIVE DIAGNOSIS ????????????????????????????????????????????
    pdf.section_break()
    pdf.h1("DIAGNÓSTICO EJECUTIVO")

    pdf.callout(
        "hutrit.com es una SPA (Single Page Application) renderizada 100% en JavaScript del "
        "lado del cliente. Cuando Google, Bing o cualquier crawler visita el sitio, solo recibe "
        "código JavaScript minificado con etiquetas de analytics -- sin título, sin descripción, "
        "sin headings, sin texto indexable, sin sitemap.",
        color=TEAL
    )

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 6, "Consecuencia directa:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(*DARK)
    pdf.body(
        "El sitio está prácticamente ausente de los resultados de búsqueda para todas las "
        "palabras clave de su mercado."
    )

    pdf.h3("Prueba concreta -- site:hutrit.com (Abril 2026)")
    pdf.bullet("Solo 3 URLs indexadas: la homepage, el subdominio de mail, y una URL con parámetro UTM de LinkedIn.")
    pdf.bullet('Ningún resultado aparece al buscar "hutrit reclutamiento LATAM" ni términos relacionados.')
    pdf.bullet("Competidores directos (Interfell, Loopae, WeRemoto, Talently) dominan todos los términos relevantes.")

    # ?? SCORE TABLE ????????????????????????????????????????????????????????????
    pdf.ln(4)
    pdf.h1("SCORE GENERAL: 14 / 100")

    headers = ["Categoría", "Score", "Peso"]
    rows = [
        ["SEO Técnico",                  "5/30",   "30%"],
        ["On-Page / Contenido indexable","2/25",   "25%"],
        ["Estrategia de contenido",      "0/20",   "20%"],
        ["Autoridad y backlinks",        "4/15",   "15%"],
        ["E-E-A-T",                      "3/10",   "10%"],
        ["**TOTAL",                      "**14/100",""],
    ]
    pdf.table(headers, rows, col_widths=[110, 32, 32])

    # ?? TECHNICAL AUDIT ????????????????????????????????????????????????????????
    pdf.section_break()
    pdf.h1("AUDITORÍA TÉCNICA")

    pdf.h2("Renderizado y Crawlabilidad -- CRÍTICO")
    tech_checks = [
        ("Renderizado del lado del servidor (SSR/SSG)", "FALLA -- 100% client-side JS"),
        ("Contenido indexable sin JS", "FALLA -- Sin texto, headings ni links en HTML estático"),
        ("Googlebot ve lo mismo que el usuario", "FALLA -- Divergencia total"),
    ]
    for label, result in tech_checks:
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_x(pdf.l_margin)
        ok = result.strip().upper().startswith("OK")
        pdf.set_fill_color(*(GREEN if ok else (220, 50, 47)))
        pdf.set_text_color(*WHITE)
        badge_w = 14
        pdf.cell(badge_w, 6, "OK" if ok else "FALLA", fill=True, align="C",
                 new_x=XPos.RIGHT, new_y=YPos.LAST)
        pdf.set_text_color(*DARK)
        pdf.set_fill_color(*WHITE)
        pdf.cell(0, 6, f"  {label}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    pdf.h2("Sitemap y robots.txt")
    sitemap_checks = [
        ("robots.txt existe", "OK"),
        ("robots.txt apunta al sitemap", "FALLA"),
        ("sitemap.xml existe", "FALLA -- devuelve 404"),
        ("Sitemap enviado a Search Console", "FALLA"),
    ]
    for label, result in sitemap_checks:
        ok = result.strip().upper().startswith("OK")
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_x(pdf.l_margin)
        pdf.set_fill_color(*(GREEN if ok else (220, 50, 47)))
        pdf.set_text_color(*WHITE)
        pdf.cell(14, 6, "OK" if ok else "FALLA", fill=True, align="C",
                 new_x=XPos.RIGHT, new_y=YPos.LAST)
        pdf.set_text_color(*DARK)
        pdf.cell(0, 6, f"  {label}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    pdf.h2("Meta Tags -- Homepage")
    meta_headers = ["Elemento", "Estado", "Recomendado"]
    meta_rows = [
        ["Title tag",        "FALLA", "Hutrit -- Talento Remoto LATAM para Empresas Europeas"],
        ["Meta description", "FALLA", "Conectamos empresas españolas y europeas con talento LATAM full-time..."],
        ["Canonical tag",    "FALLA", "https://hutrit.com/"],
        ["Open Graph",       "FALLA", "Todos los tags OG ausentes"],
        ["Twitter Card",     "FALLA", "Ausente"],
        ["Schema Markup",    "FALLA", "Organization, Service, FAQ -- todos ausentes"],
    ]
    pdf.table(meta_headers, meta_rows, col_widths=[38, 22, 114])

    pdf.h2("URLs Indexadas -- Abril 2026")
    pdf.body(
        "Solo 3 páginas indexadas en total:\n"
        "  - https://www.hutrit.com/\n"
        "  - https://mail.hutrit.com/  (no debería indexarse)\n"
        "  - https://hutrit.com/?trk=...  (URL con parámetro UTM -- duplicado)"
    )

    # ?? COMPETITIVE ANALYSIS ???????????????????????????????????????????????????
    pdf.section_break()
    pdf.h1("ANÁLISIS DE COMPETENCIA")

    comp_headers = ["Empresa", "Fortaleza SEO"]
    comp_rows = [
        ["Interfell",      "Blog robusto, 8+ años, 50k+ profesionales en base de datos, múltiples páginas de servicio"],
        ["Loopae",         'Homepage bien optimizada, H1 claro: "Agencia de Reclutamiento de Talento Remoto en LATAM"'],
        ["WeRemoto",       'Job board con SEO fuerte -- aparece para "appointment setter trabajo remoto"'],
        ["Talently",       "Fuerte en tech, UI clara"],
        ["RemoteLatinos",  'Dominan en inglés el nicho LATAM hiring'],
    ]
    pdf.table(comp_headers, comp_rows, col_widths=[38, 136])

    pdf.callout(
        "Hutrit no aparece en ninguna búsqueda del sector.\n\n"
        "Ventana de oportunidad: Nadie domina el nicho \"ventas remotas LATAM ? empresas europeas\" "
        "en español. Hutrit puede ser la referencia editorial en ese espacio.",
        color=GREEN
    )

    # ?? KEYWORDS ???????????????????????????????????????????????????????????????
    pdf.section_break()
    pdf.h1("KEYWORDS OBJETIVO")

    pdf.h2("B2B -- Empresas")
    b2b_headers = ["Keyword", "Intención", "Prioridad"]
    b2b_rows = [
        ["contratar talento remoto LATAM",       "Comercial",     "Primaria"],
        ["agencia reclutamiento remoto LATAM",   "Comercial",     "Primaria"],
        ["staffing remoto latinoamerica",         "Comercial",     "Secundaria"],
        ["contratar appointment setter LATAM",   "Transaccional", "Oportunidad"],
        ["reclutamiento remoto España LATAM",    "Comercial",     "Secundaria"],
    ]
    pdf.table(b2b_headers, b2b_rows, col_widths=[90, 42, 42])

    pdf.h2("B2C -- Talento")
    b2c_headers = ["Keyword", "Intención", "Prioridad"]
    b2c_rows = [
        ["trabajo remoto empresas europeas LATAM", "Comercial",    "Primaria"],
        ["trabajo remoto dólares LATAM",           "Informacional","Secundaria"],
        ["appointment setter trabajo remoto",      "Informacional","Oportunidad"],
        ["lead qualifier trabajo remoto",          "Informacional","Oportunidad"],
    ]
    pdf.table(b2c_headers, b2c_rows, col_widths=[90, 42, 42])

    # ?? ACTION PLAN: PHASE 1 ???????????????????????????????????????????????????
    pdf.section_break()
    pdf.h1("PLAN DE ACCIÓN")

    pdf.h2("FASE 1 -- CRÍTICO (Semana 1-2): Hacer el sitio indexable")

    pdf.h3("Acción 1.1 -- Resolver renderizado JS")
    pdf.body(
        "El problema raíz: Google solo ve JavaScript. No hay HTML con contenido.\n\n"
        "Opciones:"
    )
    pdf.bullet("Prerender.io (~$45/mes): Solución puente -- sirve HTML a crawlers sin reescribir el frontend. Implementación en 1-2 días. RECOMENDADO PARA ARRANCAR.")
    pdf.bullet("Migrar a Next.js/Nuxt.js con SSR: Solución permanente y óptima. 2-4 semanas.")
    pdf.bullet("Static Site Generation (Astro): Ideal si el contenido no cambia frecuentemente.")

    pdf.h3("Acción 1.2 -- Crear sitemap.xml")
    pdf.body(
        "Crear /public/sitemap.xml con todas las URLs del sitio e incluir las rutas:\n"
        "/, /como-funciona, /roles, /empresas, /blog"
    )

    pdf.h3("Acción 1.3 -- Actualizar robots.txt")
    pdf.bullet("Agregar línea: Sitemap: https://hutrit.com/sitemap.xml")
    pdf.bullet("Bloquear: /app/, /dashboard/, /api/")
    pdf.bullet("Bloquear parámetros UTM: /*?trk=*, /*?utm_*")

    pdf.h3("Acción 1.4 -- Implementar meta tags estáticos")
    pdf.body("Agregar por cada ruta: title, meta description, canonical, Open Graph, Twitter Card")
    pdf.body(
        "Ejemplo homepage:\n"
        '  Title: "Hutrit -- Talento Remoto LATAM para Empresas Europeas" (55 chars)\n'
        '  Description: "Conectamos empresas españolas y europeas con talento LATAM full-time. '
        'Proceso curado, perfiles validados y contratación ágil en ventas, tech y marketing." (155 chars)'
    )

    pdf.h3("Acción 1.5 -- Schema Markup JSON-LD")
    pdf.body("Implementar en el head:")
    pdf.bullet("Organization (nombre, URL, logo, redes, contacto)")
    pdf.bullet("WebSite + SearchAction")
    pdf.bullet("Service (descripción del servicio de reclutamiento)")

    pdf.h3("Acción 1.6 -- Registrar en Google Search Console y Bing Webmaster Tools")
    pdf.body("Verificar propiedad, enviar sitemap, solicitar indexación manual de homepage, activar alertas de cobertura.")

    # ?? PHASE 2 ????????????????????????????????????????????????????????????????
    pdf.section_break()
    pdf.h2("FASE 2 -- ALTA PRIORIDAD (Mes 1-2): Páginas de servicio")

    pdf.h3("Acción 2.1 -- Crear páginas de servicio dedicadas (B2B)")
    p2_headers = ["URL", "Keyword objetivo"]
    p2_rows = [
        ["/empresas",                  "contratar talento remoto LATAM"],
        ["/como-funciona",             "cómo contratar remotamente LATAM"],
        ["/roles/appointment-setter",  "contratar appointment setter LATAM"],
        ["/roles/lead-qualifier",      "lead qualifier remoto LATAM"],
        ["/roles/hiring-advisor",      "hiring advisor remoto"],
    ]
    pdf.table(p2_headers, p2_rows, col_widths=[60, 114])
    pdf.body("Cada página debe tener: title único, H1 con keyword, 300-600 palabras, Schema Service, CTA claro.")

    pdf.h3("Acción 2.2 -- Crear página Hutrit Club B2C dedicada")
    pdf.body(
        'URL: /club -- Keyword: "trabajo remoto empresas europeas LATAM"\n'
        "Incluir roles disponibles con descripción, salario y requisitos. Agregar JobPosting schema para vacantes activas."
    )

    pdf.h3("Acción 2.3 -- Limpiar indexación")
    pdf.bullet("Bloquear mail.hutrit.com con robots noindex")
    pdf.bullet("Bloquear URLs con parámetros UTM (?trk=*, ?utm_*)")

    # ?? PHASE 3 ????????????????????????????????????????????????????????????????
    pdf.section_break()
    pdf.h2("FASE 3 -- ESTRATEGIA DE CONTENIDO (Mes 2-4): Autoridad orgánica")

    pdf.h3("Acción 3.1 -- Lanzar blog en hutrit.com/blog")
    pdf.body("Cadencia: 2 artículos por mes (calidad > cantidad)")

    pdf.h3("Artículos prioritarios B2B")
    blog_b2b = [
        ("Cómo contratar talento remoto en LATAM desde España: guía completa 2026",
         "contratar talento remoto LATAM España"),
        ("Cuánto cuesta un Appointment Setter en LATAM: guía de salarios 2026",
         "salario appointment setter LATAM"),
        ("Las 5 mejores agencias de reclutamiento remoto en LATAM para empresas europeas",
         "agencias reclutamiento remoto LATAM"),
        ("Appointment Setter vs. Lead Qualifier: cuál contratar primero",
         "appointment setter vs lead qualifier"),
    ]
    blog_headers = ["Artículo", "Keyword objetivo"]
    pdf.table(blog_headers, blog_b2b, col_widths=[100, 74])

    pdf.h3("Artículos prioritarios B2C")
    blog_b2c = [
        ("Cómo conseguir trabajo remoto con empresas europeas desde LATAM en 2026",
         "trabajo remoto empresas europeas LATAM"),
        ("Appointment Setter: qué es, cuánto gana y cómo entrar al rol",
         "qué es appointment setter trabajo remoto"),
        ("Guía para preparar tu perfil de LinkedIn para trabajo remoto internacional",
         "linkedin trabajo remoto internacional"),
        ("Lead Qualifier en remoto: el rol que más crece en ventas B2B",
         "lead qualifier trabajo remoto B2B"),
    ]
    pdf.table(blog_headers, blog_b2c, col_widths=[100, 74])

    pdf.h3("Acción 3.2 -- FAQ Schema en páginas clave")
    pdf.body(
        "Implementar FAQPage schema en homepage y páginas de servicio. Genera rich snippets "
        "y aumenta probabilidad de citación por modelos de IA."
    )

    # ?? PHASE 4 ????????????????????????????????????????????????????????????????
    pdf.section_break()
    pdf.h2("FASE 4 -- AUTORIDAD Y AEO (Mes 3-6): Dominar el espacio")

    pdf.h3("Acción 4.1 -- Link Building")
    lb_headers = ["Táctica", "Impacto"]
    lb_rows = [
        ["Registrar en G2, Clutch, Bark como agencia de reclutamiento", "Alto -- links de autoridad"],
        ['Contactar autores de rankings "mejores agencias LATAM 2026"', "Alto -- tráfico referido + backlink"],
        ["Guest posts en blogs de RR.HH. de España/LATAM", "Medio-Alto"],
        ["Publicar Guía Salarial Ventas Remotas LATAM 2026", "Muy Alto -- recurso linkeable natural"],
        ["Nota de prensa sobre datos del sector", "Alto -- autoridad de dominio"],
    ]
    pdf.table(lb_headers, lb_rows, col_widths=[110, 64])

    pdf.h3("Acción 4.2 -- Optimización para IA (AEO/GEO)")
    pdf.body("Para ser citado por ChatGPT, Claude, Gemini y Perplexity:")
    aeo_items = [
        "Crear perfil en Crunchbase/Wikipedia -- fuentes que los modelos aprenden",
        "Publicar datos propios del sector -- citables por IA",
        "Aparecer en al menos 3 rankings externos",
        "Consistencia de nombre y datos en todos los directorios",
        "FAQ públicas con preguntas literales que los usuarios hacen a modelos de IA",
        "Menciones en LinkedIn Pulse y Medium -- indexados y usados como fuentes",
    ]
    for item in aeo_items:
        pdf.bullet(item)

    # ?? QUICK WINS ?????????????????????????????????????????????????????????????
    pdf.section_break()
    pdf.h1("QUICK WINS -- Primeras 2 Semanas")

    qw_headers = ["Acción", "Tiempo estimado", "Impacto"]
    qw_rows = [
        ["Implementar Prerender.io",                    "1-2 días",    "CRÍTICO"],
        ["Crear sitemap.xml",                           "1 hora",      "CRÍTICO"],
        ["Actualizar robots.txt",                       "15 minutos",  "CRÍTICO"],
        ["Agregar title y meta description estáticos",  "2-4 horas",   "CRÍTICO"],
        ["Registrar en Google Search Console",          "30 minutos",  "CRÍTICO"],
        ["Agregar Organization schema JSON-LD",         "2-3 horas",   "Alta"],
        ["Bloquear mail.hutrit.com de indexación",      "15 minutos",  "Media"],
        ["Bloquear URLs con parámetros UTM",            "15 minutos",  "Media"],
    ]
    pdf.table(qw_headers, qw_rows, col_widths=[100, 38, 36])

    # ?? KPIs ???????????????????????????????????????????????????????????????????
    pdf.h1("KPIs DE SEGUIMIENTO")

    kpi_headers = ["Métrica", "Hoy", "Meta 3 meses", "Meta 6 meses"]
    kpi_rows = [
        ["Páginas indexadas",                            "3",               "15-20",              "30-50"],
        ['Ranking "contratar talento remoto LATAM"',     "No posicionado",  "Top 20",             "Top 10"],
        ["Tráfico orgánico mensual",                     "~0",              "200-500 sesiones",   "1,000-3,000 sesiones"],
        ["Backlinks de dominio",                         "Desconocido",     "+10 dominios",       "+25 dominios"],
        ["Visibilidad en AI (ChatGPT/Perplexity)",       "No aparece",      "1-2 queries",        "Top 3 en nicho"],
    ]
    pdf.table(kpi_headers, kpi_rows, col_widths=[74, 26, 37, 37])

    # ?? TOOLS STACK ????????????????????????????????????????????????????????????
    pdf.h1("STACK DE HERRAMIENTAS")

    tools_headers = ["Herramienta", "Uso", "Costo"]
    tools_rows = [
        ["Google Search Console",   "Monitoreo de indexación",             "Gratis"],
        ["Bing Webmaster Tools",    "Indexación Bing/Microsoft AI",        "Gratis"],
        ["Prerender.io",            "Pre-rendering para crawlers",         "~$45/mes"],
        ["Ahrefs Webmaster Tools",  "Backlinks y keywords",               "Gratis (limitado)"],
        ["Google PageSpeed Insights","Core Web Vitals",                   "Gratis"],
    ]
    pdf.table(tools_headers, tools_rows, col_widths=[55, 87, 32])

    # ?? FOOTER NOTE ????????????????????????????????????????????????????????????
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*GREY)
    pdf.cell(0, 5, "Auditoría generada: Abril 2026  |  Próxima revisión: Julio 2026", align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ?? SAVE ???????????????????????????????????????????????????????????????????
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    pdf.output(OUTPUT_PATH)
    print(f"PDF saved to: {OUTPUT_PATH}")
    print(f"Pages: {pdf.page_no()}")


if __name__ == "__main__":
    build_pdf()
