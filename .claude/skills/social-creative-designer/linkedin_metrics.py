import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent.parent / ".env")

HUTRIT_LINKEDIN = "https://www.linkedin.com/company/hutrit/"


def obtener_metricas_linkedin(perfil_url=HUTRIT_LINKEDIN, limit=10):
    api_key = os.getenv("APIFY_API_KEY")
    if not api_key:
        print("ERROR: APIFY_API_KEY no encontrada en .env")
        return []

    client = ApifyClient(api_key)
    print(f"Conectando con Apify para: {perfil_url}")
    print("Esperando resultados...\n")

    run_input = {
        "startUrls": [{"url": perfil_url}],
        "maxItems": limit
    }

    try:
        run = client.actor("harvestapi/linkedin-company-posts").call(run_input=run_input)
    except Exception as e:
        print(f"Error al ejecutar actor Apify: {e}")
        return []

    resultados = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        texto = item.get("text", "") or ""
        resultados.append({
            "texto_completo": texto,
            "preview": texto[:80].replace("\n", " ") + "..." if len(texto) > 80 else texto,
            "likes": item.get("totalReactions") or 0,
            "comentarios": item.get("commentsCount") or 0,
            "shares": item.get("sharesCount") or 0,
            "url": item.get("url", "N/A")
        })

    return resultados


def analizar_y_mostrar(resultados):
    if not resultados:
        print("No se encontraron posts.")
        return None

    por_comentarios = sorted(resultados, key=lambda x: x["comentarios"], reverse=True)
    por_likes       = sorted(resultados, key=lambda x: x["likes"],       reverse=True)

    print("=" * 65)
    print(f"POSTS ANALIZADOS: {len(resultados)}")
    print("=" * 65)

    print("\n--- TOP 3 POR COMENTARIOS ---")
    for i, p in enumerate(por_comentarios[:3], 1):
        print(f"{i}. [{p['comentarios']} comentarios | {p['likes']} likes] {p['preview']}")

    print("\n--- TOP 3 POR LIKES ---")
    for i, p in enumerate(por_likes[:3], 1):
        print(f"{i}. [{p['likes']} likes | {p['comentarios']} comentarios] {p['preview']}")

    ganador = por_comentarios[0]
    print("\n" + "=" * 65)
    print("POST CON MAS COMENTARIOS:")
    print(f"  Comentarios : {ganador['comentarios']}")
    print(f"  Likes       : {ganador['likes']}")
    print(f"  URL         : {ganador['url']}")
    print(f"  Texto       :\n{ganador['texto_completo'][:400]}")
    print("=" * 65)

    return ganador


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else HUTRIT_LINKEDIN
    datos = obtener_metricas_linkedin(url)
    analizar_y_mostrar(datos)
