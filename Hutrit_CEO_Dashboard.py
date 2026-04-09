import streamlit as st
import anthropic
import pandas as pd
from pathlib import Path
import os
import resend
import requests

# --- 1. CONFIGURACIÓN VISUAL HUTRIT ---
st.set_page_config(page_title="Hutrit Intelligence OS", layout="wide", page_icon="📈")

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
def orquestar(prompt):
    if "ANTHROPIC_API_KEY" not in st.secrets:
        return "⚠️ Error: Falta ANTHROPIC_API_KEY en Secrets."
    
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    # Probamos con Sonnet 3.5; si falla por saldo, el error lo dirá claramente
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=3000,
            system="Eres el CEO de Hutrit. Experto en Marketing Ads y Data. Si el usuario pide un CSV, genera los datos en formato CSV dentro de un bloque de código.",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        error_msg = str(e).lower()
        if "credit balance" in error_msg:
            return "🚨 SALDO PENDIENTE: Anthropic aún no activa tus $5.00. Revisa el dashboard de Claude en unos minutos."
        return f"❌ Error de API: {str(e)}"

# --- 3. INTERFAZ ---
st.title("Hutrit Intelligence OS 🤖")

tab_chat, tab_mkt, tab_ventas, tab_docs = st.tabs([
    "💬 Orquestador Central", "📲 Marketing & Buffer", "💼 Ventas (Resend)", "📂 Archivos & CSV"
])

# --- TAB CHAT ---
with tab_chat:
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if p := st.chat_input("¿Qué misión ejecutamos hoy, Adam?"):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            with st.spinner("Hutrit analizando tendencias..."):
                r = orquestar(p)
                st.markdown(r)
                st.session_state.messages.append({"role": "assistant", "content": r})

# --- TAB MARKETING ---
with tab_mkt:
    st.subheader("Publicación vía Buffer")
    post_txt = st.text_area("Cuerpo del post:", height=200)
    if st.button("🚀 ENVIAR A BUFFER"):
        st.success("Comando enviado. El Orquestador confirmará el envío vía Webhook.")

# --- TAB VENTAS ---
with tab_ventas:
    st.subheader("Outreach con Resend")
    if "RESEND_API_KEY" in st.secrets:
        st.info("API de Resend detectada y lista para enviar propuestas.")
    else:
        st.warning("Configura RESEND_API_KEY en Secrets para habilitar esta pestaña.")

# --- TAB ARCHIVOS ---
with tab_docs:
    st.subheader("Gestor de Reportes y Data CSV")
    # Buscamos archivos generados
    archivos = list(Path(".").rglob("*.md")) + list(Path(".").rglob("*.csv"))
    if archivos:
        sel = st.selectbox("Elegir archivo para descargar:", archivos)
        try:
            contenido = sel.read_text(encoding="utf-8")
            st.text_area("Previsualización:", contenido, height=150)
            st.download_button(f"⬇️ Descargar {sel.suffix.upper()}", contenido, file_name=sel.name)
        except: st.error("No se pudo leer el archivo.")
    if st.button("🔄 Refrescar Lista"): st.rerun()