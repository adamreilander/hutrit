# Hutrit Agent — Setup Guide

Este repositorio contiene el agente de marketing de Hutrit. Funciona con **Claude Code** (CLI, Desktop App, o VS Code Extension).

---

## Requisitos

- [Claude Code](https://claude.ai/code) instalado (cualquier versión)
- [Python + uv](https://docs.astral.sh/uv/getting-started/installation/) para los MCP servers
- Una API Key de Google Gemini (para generación de imágenes)

---

## Instalación rápida

### 1. Clonar el repo

```bash
git clone https://github.com/adamreilander/Hutrit
cd Hutrit
```

### 2. Configurar el MCP server de imágenes (nano-banana)

Instalar el servidor:

```bash
pip install nano-banana-mcp
# o con uv:
uvx nanobanana-mcp-server@latest
```

Crear el archivo `.mcp.json` en la raíz del proyecto (ya hay un `.mcp.json.example`):

```bash
cp .mcp.json.example .mcp.json
```

Editar `.mcp.json` y rellenar tu API key y ruta de imágenes:

```json
{
  "mcpServers": {
    "nano-banana": {
      "command": "nano-banana-mcp",
      "env": {
        "GEMINI_API_KEY": "TU_GEMINI_API_KEY_AQUI",
        "IMAGE_OUTPUT_DIR": "/ruta/a/Hutrit/social"
      }
    }
  }
}
```

> Obtén tu Gemini API key en [aistudio.google.com](https://aistudio.google.com/app/apikey) — es gratis.

### 3. Abrir Claude Code en el directorio

**Desde terminal:**
```bash
claude
```

**Desde VS Code:**
Abrir la carpeta `Hutrit` y activar la extensión Claude Code.

**Desde Desktop App:**
Abrir Claude Code y navegar a la carpeta `Hutrit`.

---

## El agente arranca automáticamente

Claude Code lee `CLAUDE.md` al iniciar. El agente tiene cargado:

- Contexto de marca Hutrit (B2B y Hutrit Club B2C)
- SOPs de marketing y contenido
- Skills especializados (social, email, ads, SEO, etc.)
- Routing inteligente entre agentes y skills

---

## Variables de entorno opcionales

Crea un archivo `.env` en la raíz para activar integraciones externas:

```bash
# Make.com webhook (publicar en LinkedIn e Instagram)
MAKE_WEBHOOK_URL=https://hook.us2.make.com/tu_webhook_aqui

# Resend (envío de emails)
RESEND_API_KEY=re_tu_key_aqui
```

> `.env` está en `.gitignore` — nunca se sube al repo.

---

## Estructura del repo

```
_context/       → Archivos de marca, audiencias, mensajería y tono
_sop/           → Procedimientos operativos estándar
_templates/     → Plantillas reutilizables
ads/            → Reportes y análisis de campañas
research/       → Auditorías e investigación de mercado
social/         → Imágenes y contenido para redes sociales
CLAUDE.md       → Instrucciones del agente (se carga automáticamente)
```

---

## Uso desde claude.ai web (sin acciones)

Si quieres usar el conocimiento de marca sin ejecutar acciones:

1. Ve a [claude.ai](https://claude.ai) → **Projects** → Nuevo proyecto
2. Pega el contenido de `_context/brand_verview.md` como instrucciones del proyecto
3. El agente conocerá la marca pero no podrá publicar, enviar emails, ni generar imágenes

Para acciones reales (publicar, enviar emails, generar imágenes) necesitas Claude Code.
