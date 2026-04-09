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
Habilidades: Marketing (Buffer), Ventas (Resend), Data (CSV/MD).
"""

def orquestar(prompt):
    if "ANTHROPIC_API_KEY" not in st.secrets:
        return "⚠️ Error: Falta la API Key en Streamlit Secrets."
    
    try:
        client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        sistema = f"Eres el CEO de Hutrit. Coordina estas habilidades: {MAPA_HUTRIT}."
        
        # Usamos Haiku para asegurar conexión inmediata tras la recarga
        response = client.messages.create(
            model="claude-3-haiku-20240307", 
            max_tokens=2000,
            system=sistema,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        error_msg = str(e).lower()
        if "credit balance" in error_msg:
            return "🚨 EL SALDO SIGUE SIN ACTIVARSE: Anthropic aún no libera tus 5$ para la API. Espera unos minutos más."
        return f"❌ Error de conexión: {str(e)}"

def enviar_a_buffer(texto, redes):
    WEBHOOK_URL = "https://hook.us2.make.com/eddmr643b21lxtqjri2e74gkrdgv0c7j"
    payload = {"contenido": texto, "plataformas": redes, "autor": "Adam - Hutrit OS"}
    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        return r.status_code == 200
    except: return False

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
            with st.spinner("Hutrit conectando con la mente de Claude..."):
                r = orquestar(p)
                st.markdown(r)
                st.session_state.messages.append({"role": "assistant", "content": r})

# --- TAB MARKETING ---
with tab_mkt:
    st.subheader("Publicación vía Buffer")
    post_content = st.text_area("Copy del Post:", height=200)
    redes_sel = st.multiselect("Canales:", ["LinkedIn", "Instagram", "TikTok"])
    if st.button("🚀 ENVIAR A BUFFER"):
        if post_content and redes_sel:
            if enviar_a_buffer(post_content, redes_sel):
                st.success("✅ ¡Enviado a la cola de Buffer!")
            else: st.error("Error en conexión con Make.")

# --- TAB VENTAS ---
with tab_ventas:
    st.subheader("Base de Prospección")
    path_csv = Path("research/seguimiento_hutrit.csv")
    if path_csv.exists():
        df = pd.read_csv(path_csv)
        st.dataframe(df, use_container_width=True)
    else: st.info("Sube tu archivo .csv a la carpeta /research.")

# --- TAB ARCHIVOS ---
with tab_docs:
    st.subheader("Descargas (MD/CSV)")
    archivos = list(Path(".").rglob("*.md")) + list(Path(".").rglob("*.csv"))
    if archivos:
        sel = st.selectbox("Seleccionar archivo:", archivos)
        contenido = sel.read_text(encoding="utf-8")
        st.text_area("Vista previa:", contenido, height=200)
        st.download_button(f"⬇️ Descargar {sel.suffix.upper()}", contenido, file_name=sel.name)
    if st.button("🔄 Actualizar"): st.rerun()

# --- TAB CREATIVOS ---
with tab_creativos:
    st.subheader("Inspiración Hutrit")
    st.write("Analizando estilos en /social...")
    if st.button("🎨 Generar Concepto"):
        st.info("Función lista para conectar con Nano Banana.")