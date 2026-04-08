import streamlit as st
import os
from pathlib import Path

# Configuración de estética profesional navy/red como te gusta
st.set_page_config(page_title="Hutrit Intelligence OS", layout="wide", page_icon="📈")

# Estilo personalizado
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { background-color: #202954; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.title("Hutrit: Unified Command Center 🚀")

# --- ESCANEO DINÁMICO DE HABILIDADES ---
def escanear_agencia():
    # Carpetas que contienen el "poder" de Hutrit
    dominios = {
        "ADS": "ads",
        "SEO": "seo",
        "RESEARCH": "research",
        "SOCIAL": "social",
        "SKILLS": ".claude/skills"
    }
    mapa = {}
    for nombre, carpeta in dominios.items():
        path = Path(carpeta)
        if path.exists():
            # Filtramos solo archivos útiles (.py para scripts, .md para guías/prompts)
            mapa[nombre] = [f for f in path.rglob("*") if f.suffix in [".py", ".md"]]
    return mapa

# --- SIDEBAR: MAPA ESTRATÉGICO ---
st.sidebar.image("https://www.hutrit.com/favicon.ico", width=80)
st.sidebar.title("Hutrit OS")
mapa_habilidades = escanear_agencia()

for dominio, archivos in mapa_habilidades.items():
    with st.sidebar.expander(f"📦 {dominio} ({len(archivos)})"):
        for f in archivos:
            st.write(f"📄 {f.name}")

# --- PANEL DE CONTROL ---
st.subheader("🤖 Ejecutor de Agentes")
orden = st.text_area("¿Cuál es la misión de hoy?", placeholder="Ej: 'Genera una auditoría SEO para Hutrit Club' o 'Crea 5 copies para Meta Ads'...")

# Selección de herramienta
todas_las_skills = []
for d in mapa_habilidades.values(): todas_las_skills.extend(d)

habilidad_activa = st.selectbox("Selecciona la Skill a utilizar:", options=todas_las_skills, format_func=lambda x: f"{x.parent.name} / {x.name}")

if st.button("🔥 ACTIVAR AGENTE"):
    if orden:
        st.info(f"Activando habilidad: **{habilidad_activa.name}**")
        st.success(f"Procesando orden de Adam: '{orden}'")
        # Aquí es donde ocurre la magia: conecta con la API de Claude o lanza el script
        st.balloons()
    else:
        st.warning("Adam, necesito una orden clara para proceder.")

# --- VISOR DE RESULTADOS ---
st.markdown("---")
st.subheader("📂 Centro de Documentación")
repo_folders = ["reports", "presentations", "ads"]
docs = []
for folder in repo_folders:
    p = Path(folder)
    if p.exists(): docs.extend([f for f in p.glob("*.md")])

if docs:
    doc_view = st.selectbox("Ver último entregable:", docs)
    with open(doc_view, "r", encoding="utf-8") as f:
        st.markdown(f.read())
else:
    st.write("Esperando ejecución de la primera misión...")