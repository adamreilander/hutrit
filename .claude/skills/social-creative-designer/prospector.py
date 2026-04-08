import os
import requests
import json
import csv
from pathlib import Path
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent.parent / ".env")

OUTPUT_CSV = Path(__file__).resolve().parent.parent.parent.parent / "research" / "seguimiento_hutrit.csv"


# ─── Scraping ───────────────────────────────────────────────────────────────

def scrape_web(url):
    """
    Extrae contexto útil del sitio web de un prospecto:
    - Meta descripción
    - Presencia de Meta Pixel
    - Presencia de Google Ads tag
    - LinkedIn de la empresa (si lo linkean)
    - Diagnóstico resumido
    """
    resultado = {
        "meta_descripcion": "N/A",
        "meta_pixel": False,
        "google_ads_tag": False,
        "linkedin_url": "N/A",
        "diagnostico": "Sin web"
    }

    if not url or url == "N/A":
        return resultado

    try:
        resp = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        if resp.status_code != 200:
            resultado["diagnostico"] = f"Error HTTP {resp.status_code}"
            return resultado

        html = resp.text
        soup = BeautifulSoup(html, "html.parser")

        # Meta descripción
        meta = soup.find("meta", attrs={"name": "description"}) or \
               soup.find("meta", attrs={"property": "og:description"})
        if meta and meta.get("content"):
            resultado["meta_descripcion"] = meta["content"].strip()[:200]

        # Meta Pixel
        resultado["meta_pixel"] = "fbevents.js" in html.lower() or "connect.facebook.net" in html.lower()

        # Google Ads / gtag
        resultado["google_ads_tag"] = "googletagmanager.com" in html or "gtag(" in html or "AW-" in html

        # LinkedIn de la empresa
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "linkedin.com/company" in href:
                resultado["linkedin_url"] = href if href.startswith("http") else "https://linkedin.com" + href
                break

        # Diagnóstico
        problemas = []
        if not resultado["meta_pixel"]:
            problemas.append("Sin Meta Pixel")
        if not resultado["google_ads_tag"]:
            problemas.append("Sin Google Ads tag")
        resultado["diagnostico"] = " | ".join(problemas) if problemas else "Web con tracking activo"

    except Exception as e:
        resultado["diagnostico"] = f"Web inalcanzable ({type(e).__name__})"

    return resultado


# ─── Google Places ───────────────────────────────────────────────────────────

def obtener_detalle_place(place_id, api_key):
    """Llama a Place Details para obtener website, teléfono y dirección."""
    url = (
        f"https://maps.googleapis.com/maps/api/place/details/json"
        f"?place_id={place_id}"
        f"&fields=name,rating,website,formatted_phone_number,formatted_address"
        f"&key={api_key}"
    )
    try:
        resp = requests.get(url, timeout=8)
        return resp.json().get("result", {})
    except Exception:
        return {}


# ─── CSV ─────────────────────────────────────────────────────────────────────

COLUMNAS = [
    "Empresa", "Ciudad", "Nicho", "Rating", "Estrategia",
    "Web", "Telefono", "Direccion",
    "Meta_Pixel", "Google_Ads_Tag", "LinkedIn_Empresa",
    "Meta_Descripcion", "Diagnostico_Web"
]

def registrar_prospecto(datos):
    ya_existe = OUTPUT_CSV.exists()
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS)
        if not ya_existe:
            writer.writeheader()
        writer.writerow(datos)


# ─── Main ────────────────────────────────────────────────────────────────────

def ejecutar_agente_hutrit(ciudad="Madrid", nicho="Agencia de Marketing"):
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_MAPS_API_KEY no encontrada en .env")
        return

    query = f"{nicho} en {ciudad}, España"
    search_url = (
        f"https://maps.googleapis.com/maps/api/place/textsearch/json"
        f"?query={query}&key={api_key}"
    )

    print(f"\nBuscando: {query}")
    print("-" * 60)

    try:
        resp = requests.get(search_url, timeout=10)
        places = resp.json().get("results", [])
    except Exception as e:
        print(f"Error en búsqueda: {e}")
        return

    prospectos = []

    for place in places[:8]:
        nombre = place.get("name", "N/A")
        rating = place.get("rating", 0)
        place_id = place.get("place_id", "")

        # Estrategia Hutrit
        estrategia = "Mejora de Performance" if rating < 4.2 else "Escalabilidad con Talento LATAM"

        print(f"\n[{rating}*] {nombre} — {estrategia}")

        # Detalle del lugar (website, teléfono, dirección)
        detalle = obtener_detalle_place(place_id, api_key) if place_id else {}
        web = detalle.get("website", "N/A")
        telefono = detalle.get("formatted_phone_number", "N/A")
        direccion = detalle.get("formatted_address", "N/A")

        print(f"   Web: {web}")

        # Scraping
        scrape = scrape_web(web)
        print(f"   Diagnostico: {scrape['diagnostico']}")
        if scrape["linkedin_url"] != "N/A":
            print(f"   LinkedIn: {scrape['linkedin_url']}")

        datos = {
            "Empresa": nombre,
            "Ciudad": ciudad,
            "Nicho": nicho,
            "Rating": rating,
            "Estrategia": estrategia,
            "Web": web,
            "Telefono": telefono,
            "Direccion": direccion,
            "Meta_Pixel": "Sí" if scrape["meta_pixel"] else "No",
            "Google_Ads_Tag": "Sí" if scrape["google_ads_tag"] else "No",
            "LinkedIn_Empresa": scrape["linkedin_url"],
            "Meta_Descripcion": scrape["meta_descripcion"],
            "Diagnostico_Web": scrape["diagnostico"]
        }

        registrar_prospecto(datos)
        prospectos.append(datos)

    print(f"\n[OK] {len(prospectos)} prospectos guardados en: {OUTPUT_CSV}")
    return json.dumps(prospectos, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    import sys
    ciudad = sys.argv[1] if len(sys.argv) > 1 else "Madrid"
    nicho  = sys.argv[2] if len(sys.argv) > 2 else "Agencia de Marketing"
    ejecutar_agente_hutrit(ciudad, nicho)
