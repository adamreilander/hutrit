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
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE INTELIGENCIA (ORQUESTADOR) ---
def orquestar(prompt):
    if "ANTHROPIC_API_KEY" not in st.secrets:
        return "⚠️ Error: Configura ANTHROPIC_API_KEY en Secrets."
    
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    try:
        # Usamos Claude 3 Sonnet (v3.0) para asegurar compatibilidad inmediata con cuenta nueva
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=3000,
            system="Eres el CEO de Hutrit. Experto en Marketing y Data. Genera el CSV solicitado en un bloque de código.",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        error_msg = str(e).lower()
        if "404" in error_msg:
            return "❌ Anthropic aún no asigna modelos a tu Key. Intenta con una nueva Key o espera 30 min."
        return f"❌ Error de Sistema: {str(e)}"

# --- 3. INTERFAZ COMPLETA ---
st.title("Hutrit Intelligence OS 🤖")

tab_chat, tab_mkt, tab_ventas, tab_docs = st.tabs([
    "💬 Orquestador", "📲 Marketing", "💼 Ventas", "📂 Archivos"
])

with tab_chat:
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if p := st.chat_input("¿Misión para hoy?"):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            with st.spinner("Hutrit procesando..."):
                r = orquestar(p)
                st.markdown(r)
                st.session_state.messages.append({"role": "assistant", "content": r})

with tab_mkt:
    st.subheader("Publicación vía Buffer")
    post_txt = st.text_area("Copy:", height=200)
    if st.button("🚀 ENVIAR A BUFFER"):
        st.info("Webhook listo para enviar a Buffer.")

with tab_docs:
    st.subheader("Archivos CSV / MD")
    archivos = list(Path(".").rglob("*.md")) + list(Path(".").rglob("*.csv"))
    if archivos:
        sel = st.selectbox("Archivo:", archivos)
        st.download_button(f"Descargar {sel.name}", sel.read_text(encoding="utf-8"), file_name=sel.name)