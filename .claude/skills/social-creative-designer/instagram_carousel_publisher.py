"""
Instagram Carousel Publisher — Hutrit
Publica carousels de multiples imagenes en Instagram via Graph API.
Uso: py instagram_carousel_publisher.py
"""

import urllib.request
import urllib.parse
import json
import time
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent.parent / ".env")

IG_USER_ID = os.getenv("INSTAGRAM_USER_ID", "17841462682190554")
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
API_VERSION = "v19.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


def api_post(endpoint, params):
    params["access_token"] = ACCESS_TOKEN
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}{endpoint}", data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.request.HTTPError as e:
        error = json.loads(e.read().decode())
        print(f"API Error {e.code}: {error.get('error', {}).get('message', str(error))}")
        return None


def api_get(endpoint, params=None):
    params = params or {}
    params["access_token"] = ACCESS_TOKEN
    qs = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{BASE_URL}{endpoint}?{qs}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.request.HTTPError as e:
        error = json.loads(e.read().decode())
        print(f"API Error {e.code}: {error.get('error', {}).get('message', str(error))}")
        return None


def create_carousel_item(image_url):
    """Crea un container de item para el carousel. Devuelve creation_id."""
    result = api_post(f"/{IG_USER_ID}/media", {
        "image_url": image_url,
        "is_carousel_item": "true",
    })
    if result and "id" in result:
        return result["id"]
    return None


def create_carousel_container(children_ids, caption):
    """Crea el container del carousel con todos los items y caption."""
    result = api_post(f"/{IG_USER_ID}/media", {
        "media_type": "CAROUSEL",
        "children": ",".join(children_ids),
        "caption": caption,
    })
    if result and "id" in result:
        return result["id"]
    return None


def check_container_status(container_id):
    """Verifica si el container esta listo para publicar."""
    result = api_get(f"/{container_id}", {"fields": "status_code,status"})
    if result:
        return result.get("status_code"), result.get("status")
    return None, None


def publish_carousel(container_id):
    """Publica el carousel. Devuelve el post ID."""
    result = api_post(f"/{IG_USER_ID}/media_publish", {
        "creation_id": container_id,
    })
    if result and "id" in result:
        return result["id"]
    return None


def publicar_carousel(image_urls, caption, max_wait=120):
    """
    Flujo completo de publicacion de carousel en Instagram.

    Args:
        image_urls: lista de URLs publicas de imagenes (2-10 slides)
        caption: texto del post con hashtags
        max_wait: segundos maximos esperando que el container este listo

    Returns:
        post_id si exitoso, None si fallo
    """
    if not ACCESS_TOKEN:
        print("ERROR: INSTAGRAM_ACCESS_TOKEN no encontrado en .env")
        return None

    if len(image_urls) < 2 or len(image_urls) > 10:
        print(f"ERROR: El carousel debe tener entre 2 y 10 imagenes (tienes {len(image_urls)})")
        return None

    print(f"Publicando carousel con {len(image_urls)} slides...")

    # Paso 1: Crear containers individuales para cada imagen
    print("\n[1/3] Creando containers de imagenes...")
    children_ids = []
    for i, url in enumerate(image_urls, 1):
        print(f"  Slide {i}: {url[:60]}...")
        item_id = create_carousel_item(url)
        if not item_id:
            print(f"  ERROR: No se pudo crear el container para slide {i}")
            return None
        children_ids.append(item_id)
        print(f"  OK -> {item_id}")
        time.sleep(1)  # Evitar rate limiting

    # Paso 2: Crear container del carousel
    print("\n[2/3] Creando container del carousel...")
    container_id = create_carousel_container(children_ids, caption)
    if not container_id:
        print("ERROR: No se pudo crear el container del carousel")
        return None
    print(f"  Container ID: {container_id}")

    # Paso 3: Esperar a que el container este listo
    print("\n[3/3] Esperando procesamiento...")
    elapsed = 0
    while elapsed < max_wait:
        time.sleep(5)
        elapsed += 5
        status_code, status = check_container_status(container_id)
        print(f"  Status ({elapsed}s): {status_code} - {status}")
        if status_code == "FINISHED":
            break
        elif status_code in ("ERROR", "EXPIRED"):
            print(f"ERROR: El container fallo con status {status_code}")
            return None

    if status_code != "FINISHED":
        print(f"ERROR: Timeout esperando el container ({max_wait}s)")
        return None

    # Paso 4: Publicar
    print("\n[4/4] Publicando...")
    post_id = publish_carousel(container_id)
    if post_id:
        print(f"\nOK! Carousel publicado. Post ID: {post_id}")
        print(f"Ver en: https://www.instagram.com/hutrit_club/")
        return post_id
    else:
        print("ERROR: No se pudo publicar el carousel")
        return None


if __name__ == "__main__":
    # Test: carousel de los 5 slides del carrusel de abril 8
    # "5 frases que arruinan tu perfil de LinkedIn"
    slides = [
        "https://i.imgur.com/VrxNZZW.png",  # Slide 1 - Cover
        "https://i.imgur.com/0jFac2v.png",  # Slide 2 - Frase 1
        "https://i.imgur.com/XSM4Hon.png",  # Slide 3 - Frase 2
        "https://i.imgur.com/BMIHwZ0.png",  # Slide 4 - Frase 3
        "https://i.imgur.com/L03IZxE.png",  # Slide 5 - CTA
    ]

    caption = """Tu perfil de LinkedIn dice mas sobre ti de lo que crees.
Y a veces, lo que dice no te ayuda.

Estas 5 frases son las mas comunes en perfiles LATAM - y las que mas oportunidades cuestan.

Desliza y reescribe la tuya.

Hutrit Club conecta talento latinoamericano con empresas europeas que ya saben lo que buscan. Listo para que te encuentren?

hutrit.com

#HutritClub #LinkedInTips #TalentoLATAM #EmpleoRemoto #PerfilProfesional #BusquedaDeEmpleo #MarketingDigital #DesarrolloProfesional #TrabajoRemoto #LATAM"""

    publicar_carousel(slides, caption)
