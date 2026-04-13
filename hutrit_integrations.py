"""
Hutrit Intelligence OS — Módulo de Integraciones
Funciones de acción real: email, Instagram, prospección, Notion, Google Maps
"""

import os
import json
import time
import urllib.request
import urllib.parse
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

RESEND_API_KEY     = os.getenv("RESEND_API_KEY", "")
IG_USER_ID         = os.getenv("INSTAGRAM_USER_ID", "")
IG_ACCESS_TOKEN    = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
APIFY_API_KEY      = os.getenv("APIFY_API_KEY", "")
NOTION_TOKEN       = os.getenv("NOTION_TOKEN", "")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

IG_API_VERSION = "v19.0"
IG_BASE_URL    = f"https://graph.facebook.com/{IG_API_VERSION}"


# ─── 1. RESEND — Email ──────────────────────────────────────────────────────

def send_email(to: str, subject: str, html: str, from_email: str = "onboarding@resend.dev") -> dict:
    """
    Envía un email via Resend API.
    Returns: {"success": bool, "id": str, "error": str}
    """
    if not RESEND_API_KEY:
        return {"success": False, "id": "", "error": "RESEND_API_KEY no configurada en .env"}
    try:
        import resend as resend_sdk
        resend_sdk.api_key = RESEND_API_KEY
        response = resend_sdk.Emails.send({
            "from": from_email,
            "to": [to] if isinstance(to, str) else to,
            "subject": subject,
            "html": html,
        })
        return {"success": True, "id": response.get("id", ""), "error": ""}
    except Exception as e:
        return {"success": False, "id": "", "error": str(e)}


# ─── 2. INSTAGRAM — Graph API ───────────────────────────────────────────────

def _ig_post(endpoint: str, params: dict):
    params["access_token"] = IG_ACCESS_TOKEN
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(f"{IG_BASE_URL}{endpoint}", data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.request.HTTPError as e:
        err = json.loads(e.read().decode())
        return {"error": err.get("error", {}).get("message", str(err))}


def _ig_get(endpoint: str, params: dict = None):
    params = params or {}
    params["access_token"] = IG_ACCESS_TOKEN
    qs = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{IG_BASE_URL}{endpoint}?{qs}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.request.HTTPError as e:
        err = json.loads(e.read().decode())
        return {"error": err.get("error", {}).get("message", str(err))}


def publish_instagram_single(image_url: str, caption: str) -> dict:
    """
    Publica una imagen única en Instagram.
    Returns: {"success": bool, "post_id": str, "error": str}
    """
    if not IG_ACCESS_TOKEN:
        return {"success": False, "post_id": "", "error": "INSTAGRAM_ACCESS_TOKEN no configurado"}

    result = _ig_post(f"/{IG_USER_ID}/media", {"image_url": image_url, "caption": caption})
    if not result or "id" not in result:
        err = result.get("error", "Error creando container") if result else "Sin respuesta"
        return {"success": False, "post_id": "", "error": err}

    container_id = result["id"]
    status_code = None
    for _ in range(24):
        time.sleep(5)
        status = _ig_get(f"/{container_id}", {"fields": "status_code,status"})
        status_code = status.get("status_code") if status else None
        if status_code == "FINISHED":
            break
        elif status_code in ("ERROR", "EXPIRED"):
            return {"success": False, "post_id": "", "error": f"Container falló: {status_code}"}

    if status_code != "FINISHED":
        return {"success": False, "post_id": "", "error": "Timeout esperando container (120s)"}

    pub = _ig_post(f"/{IG_USER_ID}/media_publish", {"creation_id": container_id})
    if pub and "id" in pub:
        return {"success": True, "post_id": pub["id"], "error": ""}
    err = pub.get("error", "Error en media_publish") if pub else "Sin respuesta"
    return {"success": False, "post_id": "", "error": err}


def publish_instagram_carousel(image_urls: list, caption: str, progress_cb=None) -> dict:
    """
    Publica un carousel (2-10 imágenes) en Instagram.
    progress_cb: callable(str) para reportar progreso al caller.
    Returns: {"success": bool, "post_id": str, "error": str}
    """
    if not IG_ACCESS_TOKEN:
        return {"success": False, "post_id": "", "error": "INSTAGRAM_ACCESS_TOKEN no configurado"}

    if not 2 <= len(image_urls) <= 10:
        return {"success": False, "post_id": "", "error": f"Carousel: necesita 2-10 imágenes (recibí {len(image_urls)})"}

    def log(msg):
        if progress_cb:
            progress_cb(msg)

    log(f"[1/4] Creando {len(image_urls)} containers de imágenes...")
    children_ids = []
    for i, url in enumerate(image_urls, 1):
        log(f"  Slide {i}/{len(image_urls)}: {url[:60]}...")
        result = _ig_post(f"/{IG_USER_ID}/media", {"image_url": url, "is_carousel_item": "true"})
        if not result or "id" not in result:
            err = result.get("error", "Error desconocido") if result else "Sin respuesta"
            return {"success": False, "post_id": "", "error": f"Slide {i}: {err}"}
        children_ids.append(result["id"])
        time.sleep(1)

    log("[2/4] Creando container del carousel...")
    container = _ig_post(f"/{IG_USER_ID}/media", {
        "media_type": "CAROUSEL",
        "children": ",".join(children_ids),
        "caption": caption,
    })
    if not container or "id" not in container:
        err = container.get("error", "Error creando carousel") if container else "Sin respuesta"
        return {"success": False, "post_id": "", "error": err}

    container_id = container["id"]

    log("[3/4] Esperando procesamiento (puede tardar hasta 2 min)...")
    status_code = None
    for i in range(24):
        time.sleep(5)
        status = _ig_get(f"/{container_id}", {"fields": "status_code,status"})
        status_code = status.get("status_code") if status else None
        log(f"  Estado ({(i+1)*5}s): {status_code}")
        if status_code == "FINISHED":
            break
        elif status_code in ("ERROR", "EXPIRED"):
            return {"success": False, "post_id": "", "error": f"Container falló: {status_code}"}

    if status_code != "FINISHED":
        return {"success": False, "post_id": "", "error": "Timeout (120s) esperando container"}

    log("[4/4] Publicando en Instagram...")
    pub = _ig_post(f"/{IG_USER_ID}/media_publish", {"creation_id": container_id})
    if pub and "id" in pub:
        return {"success": True, "post_id": pub["id"], "error": ""}
    err = pub.get("error", "Error en media_publish") if pub else "Sin respuesta"
    return {"success": False, "post_id": "", "error": err}


# ─── 3. APIFY — Búsqueda web de prospectos ──────────────────────────────────

def search_companies_apify(query: str, max_results: int = 10) -> dict:
    """
    Busca empresas via Apify Google Search Scraper.
    Returns: {"success": bool, "results": list[dict], "error": str}
    """
    if not APIFY_API_KEY:
        return {"success": False, "results": [], "error": "APIFY_API_KEY no configurada"}
    try:
        from apify_client import ApifyClient
        client = ApifyClient(APIFY_API_KEY)
        run = client.actor("apify/google-search-scraper").call(run_input={
            "queries": query,
            "maxPagesPerQuery": 1,
            "resultsPerPage": min(max_results, 10),
            "countryCode": "es",
            "languageCode": "es",
        })
        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            for r in item.get("organicResults", []):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "description": r.get("description", ""),
                })
        return {"success": True, "results": results[:max_results], "error": ""}
    except Exception as e:
        return {"success": False, "results": [], "error": str(e)}


# ─── 4. NOTION — Pipeline CRM ───────────────────────────────────────────────

_NOTION_HEADERS = lambda: {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def list_notion_databases() -> dict:
    """Lista databases accesibles por la integración."""
    if not NOTION_TOKEN:
        return {"success": False, "databases": [], "error": "NOTION_TOKEN no configurado"}
    try:
        resp = requests.post(
            "https://api.notion.com/v1/search",
            headers=_NOTION_HEADERS(),
            json={"filter": {"value": "database", "property": "object"}},
            timeout=10,
        )
        resp.raise_for_status()
        dbs = [
            {
                "id": db["id"],
                "name": (db.get("title") or [{}])[0].get("plain_text", "Sin nombre"),
            }
            for db in resp.json().get("results", [])
        ]
        return {"success": True, "databases": dbs, "error": ""}
    except Exception as e:
        return {"success": False, "databases": [], "error": str(e)}


def save_company_to_notion(database_id: str, empresa: dict) -> dict:
    """
    Guarda una empresa en Notion.
    empresa: {"nombre", "ciudad"?, "nicho"?, "web"?, "email"?, "diagnostico"?}
    """
    if not NOTION_TOKEN:
        return {"success": False, "page_id": "", "error": "NOTION_TOKEN no configurado"}

    properties = {
        "Nombre": {"title": [{"text": {"content": empresa.get("nombre", "")[:2000]}}]},
    }
    for notion_field, key in [("Ciudad", "ciudad"), ("Nicho", "nicho"), ("Web", "web"),
                                ("Email", "email"), ("Diagnóstico", "diagnostico")]:
        val = str(empresa.get(key, ""))
        if val:
            properties[notion_field] = {"rich_text": [{"text": {"content": val[:2000]}}]}

    try:
        resp = requests.post(
            "https://api.notion.com/v1/pages",
            headers=_NOTION_HEADERS(),
            json={"parent": {"database_id": database_id}, "properties": properties},
            timeout=10,
        )
        resp.raise_for_status()
        return {"success": True, "page_id": resp.json().get("id", ""), "error": ""}
    except requests.HTTPError as e:
        try:
            msg = e.response.json().get("message", str(e))
        except Exception:
            msg = str(e)
        return {"success": False, "page_id": "", "error": msg}
    except Exception as e:
        return {"success": False, "page_id": "", "error": str(e)}


def save_email_to_notion(database_id: str, email_data: dict) -> dict:
    """
    Guarda un email enviado en Notion.
    email_data: {"to", "subject", "empresa"?, "resend_id"?}
    """
    if not NOTION_TOKEN:
        return {"success": False, "page_id": "", "error": "NOTION_TOKEN no configurado"}

    from datetime import datetime, timezone

    properties = {
        "Asunto":       {"title":     [{"text": {"content": email_data.get("subject", "")[:2000]}}]},
        "Destinatario": {"rich_text": [{"text": {"content": email_data.get("to", "")}}]},
        "Empresa":      {"rich_text": [{"text": {"content": email_data.get("empresa", "")}}]},
        "Fecha":        {"date":      {"start": datetime.now(timezone.utc).isoformat()}},
        "Resend ID":    {"rich_text": [{"text": {"content": email_data.get("resend_id", "")}}]},
    }

    try:
        resp = requests.post(
            "https://api.notion.com/v1/pages",
            headers=_NOTION_HEADERS(),
            json={"parent": {"database_id": database_id}, "properties": properties},
            timeout=10,
        )
        resp.raise_for_status()
        return {"success": True, "page_id": resp.json().get("id", ""), "error": ""}
    except requests.HTTPError as e:
        try:
            msg = e.response.json().get("message", str(e))
        except Exception:
            msg = str(e)
        return {"success": False, "page_id": "", "error": msg}
    except Exception as e:
        return {"success": False, "page_id": "", "error": str(e)}


# ─── 5. GOOGLE MAPS — Prospección por ciudad ────────────────────────────────

def prospect_by_city(ciudad: str, nicho: str, max_results: int = 8) -> dict:
    """
    Busca empresas por ciudad y sector usando Google Places API.
    Returns: {"success": bool, "prospectos": list[dict], "error": str}
    """
    if not GOOGLE_MAPS_API_KEY:
        return {"success": False, "prospectos": [], "error": "GOOGLE_MAPS_API_KEY no configurada"}

    query = f"{nicho} en {ciudad}, España"
    try:
        resp = requests.get(
            "https://maps.googleapis.com/maps/api/place/textsearch/json",
            params={"query": query, "key": GOOGLE_MAPS_API_KEY},
            timeout=10,
        )
        places = resp.json().get("results", [])
    except Exception as e:
        return {"success": False, "prospectos": [], "error": str(e)}

    prospectos = []
    for place in places[:max_results]:
        nombre   = place.get("name", "")
        rating   = place.get("rating", 0)
        place_id = place.get("place_id", "")
        web = telefono = ""

        if place_id:
            try:
                det = requests.get(
                    "https://maps.googleapis.com/maps/api/place/details/json",
                    params={
                        "place_id": place_id,
                        "fields": "website,formatted_phone_number",
                        "key": GOOGLE_MAPS_API_KEY,
                    },
                    timeout=8,
                ).json().get("result", {})
                web      = det.get("website", "")
                telefono = det.get("formatted_phone_number", "")
            except Exception:
                pass

        prospectos.append({
            "nombre":    nombre,
            "ciudad":    ciudad,
            "nicho":     nicho,
            "rating":    rating,
            "web":       web,
            "telefono":  telefono,
            "email":     "",
            "estrategia": "Mejora de Performance" if rating < 4.2 else "Escalabilidad con Talento LATAM",
        })

    return {"success": True, "prospectos": prospectos, "error": ""}
