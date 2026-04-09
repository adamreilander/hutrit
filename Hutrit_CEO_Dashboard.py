import streamlit as st
import anthropic
import pandas as pd
from pathlib import Path
import os
import resend
import requests

# --- 1. CONFIGURACIÓN DE MARCA HUTRIT ---
st.set_page_config(page_title="Hutrit Intelligence OS", layout="wide", page_icon="📈")

# Estética Premium Hutrit
st.markdown("""
    <style>
    :root { --hutrit-navy: #0e1117; --hutrit-red: #ff4b4b; }
    .stApp { background-color: var(--hutrit-navy); color: white; }
    .stTabs [data-baseweb="tab-list"] { background-color: #1e2130; border-radius: 10px; padding: 5px; gap: 10px; }
    .stTabs [data-baseweb="tab"] { height: 45px; color: #a1a1a1; }
    .stTabs [aria-selected="true"] { border-bottom: 2px solid var(--hutrit-red) !important; color: white !important; }
    .stButton>button { background-color: var(--hutrit-red); color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #1e2130; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE INTELIGENCIA ---
MAPA_HUTRIT = """
Capacidades: 
- Marketing (Buffer/Make via webhook).
- Ventas (Resend API).
- Creativos (Inspiración en carpeta /social).
- Data: Generación de reportes MD y archivos CSV.
"""

def orquestar(prompt):
    if "ANTHROPIC_API_KEY" not in st.secrets:
        return "⚠️ Error: Falta la API Key en los Secrets de Streamlit."
    
    try:
        client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        sistema = f"Eres el CEO de Hutrit. Coordina estas habilidades: {MAPA_HUTRIT}. Eres un sistema operativo ejecutor."
        
        response = client.messages.create(
            model="claude-3-5-sonnet-latest", 
            max_tokens=3000,
            system=sistema,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        error_msg = str(e).lower()
        if "credit balance" in error_msg or "400" in error_msg:
            return "🚨 EL SALDO SIGUE BAJO: Anthropic aún no procesa tu recarga de $5.00. Espera 5 min y refresca la app."
        return f"❌ Error técnico: {str(e)}"

def enviar_a_buffer(texto, redes):
    WEBHOOK_URL = "https://hook.us2.make.com/eddmr643b21lxtqjri2e74gkrdgv0c7j"
    payload = {"contenido": texto, "plataformas": redes, "autor": "Adam - Hutrit OS"}
    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        return r.status_code == 200
    except:
        return False

# --- 3. INTERFAZ ---
st.title("Hutrit Intelligence OS 🤖")

tab_chat, tab_mkt, tab_ventas, tab_docs, tab_creativos = st.tabs([
    "💬 Orquestador", "📲 Marketing", "💼 Ventas", "📂 Archivos", "🎨 Creativos"
])

# --- TAB ORQUESTADOR ---
with tab_chat:
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if p := st.chat_input("¿Misión de hoy?"):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            with st.spinner("Hutrit procesando datos y tendencias..."):
                r = orquestar(p)
                st.markdown(r)
                st.session_state.messages.append({"role": "assistant", "content": r})

# --- TAB MARKETING ---
with tab_mkt:
    st.subheader("Publicación vía Buffer")
    post_content = st.text_area("Copy del Post:", height=250)
    redes_sel = st.multiselect("Canales:", ["LinkedIn", "Instagram", "TikTok"])
    if st.button("🚀 ENVIAR A BUFFER"):
        if post_content and redes_sel:
            if enviar_a_buffer(post_content, redes_sel):
                st.success("✅ ¡Enviado correctamente!")
            else: st.error("Error de conexión.")

# --- TAB VENTAS ---
with tab_ventas:
    st.subheader("Outreach B2B")
    path_csv = Path("research/seguimiento_hutrit.csv")
    if path_csv.exists():
        df = pd.read_csv(path_csv)
        st.dataframe(df, use_container_width=True)
    else: st.info("Sube tu CSV para ver la lista de prospección.")

# --- TAB ARCHIVOS ---
with tab_docs:
    st.subheader("Gestión de Reportes y CSV")
    archivos = list(Path(".").rglob("*.md")) + list(Path(".").rglob("*.csv"))
    if archivos:
        sel = st.selectbox("Elegir archivo:", archivos)
        contenido = sel.read_text(encoding="utf-8")
        st.text_area("Previsualización:", contenido, height=200)
        st.download_button(f"⬇️ Descargar {sel.suffix.upper()}", contenido, file_name=sel.name)
    if st.button("🔄 Refrescar"): st.rerun()

# --- TAB CREATIVOS ---
with tab_creativos:
    st.subheader("Visuales de Marca")
    if st.button("🎨 Crear concepto"):
        st.info("Buscando inspiración en carpeta /social...")