import streamlit as st
import anthropic
import pandas as pd
from pathlib import Path
import os
import resend

# --- 1. CONFIGURACIÓN DE MARCA Y ESTÉTICA ---
st.set_page_config(page_title="Hutrit Intelligence OS", layout="wide", page_icon="📈")

st.markdown("""
    <style>
    :root { --hutrit-navy: #0e1117; --hutrit-red: #ff4b4b; }
    .stApp { background-color: var(--hutrit-navy); color: white; }
    .stTabs [data-baseweb="tab-list"] { background-color: #1e2130; border-radius: 10px; padding: 5px; gap: 10px; }
    .stTabs [data-baseweb="tab"] { height: 45px; color: #a1a1a1; }
    .stTabs [aria-selected="true"] { border-bottom: 2px solid var(--hutrit-red) !important; color: white !important; }
    .stButton>button { background-color: var(--hutrit-red); color: white; border-radius: 8px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE INTELIGENCIA ---
MAPA_HUTRIT = """
Capacidades del Sistema:
- Marketing: /market-ads, /market-seo, /market-social, /market-emails, /market-proposal.
- Ventas: Envío real vía Resend, /sdr-quality-audit, /prospect-mining, /call-prep.
- Creativos: /social-creative-designer (Nano Banana).
- Scripts Locales: prospector.py (Google Maps), linkedin_metrics.py (Apify).
- Archivos: Lee/Escribe CSV en /research y convierte MD a TXT.
"""

def orquestar(prompt):
    if "ANTHROPIC_API_KEY" not in st.secrets:
        return "⚠️ Error: Configura ANTHROPIC_API_KEY en Secrets."
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    sistema = f"Eres el CEO de Hutrit. Coordina estas habilidades: {MAPA_HUTRIT}. Actúa como un sistema operativo ejecutor."
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1500,
        system=sistema,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

# --- 3. INTERFAZ MULTI-PESTAÑA ---
st.title("Hutrit Intelligence OS 🤖")
tab_chat, tab_mkt, tab_ventas, tab_docs, tab_creativos = st.tabs([
    "💬 Orquestador", "🚀 Marketing & SEO", "💼 Ventas (Resend)", "📂 Archivos", "🎨 Nano Banana"
])

# --- TAB 1: ORQUESTADOR ---
with tab_chat:
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if p := st.chat_input("¿Qué misión ejecutamos hoy, Adam?"):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            r = orquestar(p)
            st.markdown(r)
            st.session_state.messages.append({"role": "assistant", "content": r})

# ---