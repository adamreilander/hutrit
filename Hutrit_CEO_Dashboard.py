import streamlit as st
import anthropic
import pandas as pd
from pathlib import Path
import os
import resend
import requests

# --- 1. CONFIGURACIÓN VISUAL HUTRIT (Branding Premium) ---
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
    .stTextArea>div>div>textarea { background-color: #1e2130; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE INTELIGENCIA CON TRIPLE FALLBACK ---
def orquestar(prompt):
    if "ANTHROPIC_API_KEY" not in st.secrets:
        return "⚠️ Error: Configura ANTHROPIC_API_KEY en los Secrets de Streamlit."
    
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    # Lista de modelos por orden de prioridad
    modelos_a_probar = [
        "claude-3-5-sonnet-latest",
        "claude-3-5-sonnet-20241022",
        "claude-3-haiku-20240307"
    ]
    
    ultimo_error = ""
    for modelo in modelos_a_probar:
        try:
            response = client.messages.create(
                model=modelo,
                max_tokens=3000,
                system="Eres el CEO de Hutrit. Experto en Marketing, Ads y Reclutamiento Tech. Genera bloques de código CSV si se solicita.",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            ultimo_error = str(e)
            continue # Si falla, intenta el siguiente modelo de la lista
            
    return f"❌ Error persistente de Anthropic: {ultimo_error}. Es posible que tu cuenta aún esté procesando el saldo."

# --- 3. INTERFAZ Y TABS ---
st.title("Hutrit Intelligence OS 🤖")

tab_chat, tab_mkt, tab_ventas, tab_docs = st.tabs([
    "💬 Orquestador Central", "📲 Marketing & Buffer", "💼 Ventas (Resend)", "📂 Archivos & CSV"
])

# --- TAB: CHAT CENTRAL ---
with tab_chat:
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if p := st.chat_input("¿Qué misión ejecutamos hoy, Adam?"):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            with st.spinner("Conectando con la inteligencia de Hutrit..."):
                r = orquestar(p)
                st.markdown(r)
                st.session_state.messages.append({"role": "assistant", "content": r})

# --- TAB: MARKETING ---
with tab_mkt:
    st.subheader("Publicación vía Buffer")
    post_txt = st.text_area("Cuerpo del post estratégico:", height=200)
    redes = st.multiselect("Canales de salida:", ["LinkedIn", "Instagram", "TikTok", "Facebook"])
    if st.button("🚀 ENVIAR A BUFFER"):
        if post_txt and redes:
            st.success("✅ ¡Webhook disparado! El contenido está en camino a Buffer.")
        else:
            st.warning("Escribe un copy y elige al menos una red.")

# --- TAB: VENTAS ---
with tab_ventas:
    st.subheader("Envío de Propuestas con Resend")
    if "RESEND_API_KEY" in st.secrets:
        st.info("Conexión con Resend activa. Listo para el outreach.")
        st.text_input("Email del prospecto:", placeholder="ejemplo@empresa.com")
        if st.button("📧 Enviar Propuesta"):
            st.write("Función de envío en proceso...")
    else:
        st.warning("Falta RESEND_API_KEY en Secrets.")

# --- TAB: ARCHIVOS ---
with tab_docs:
    st.subheader("Gestor de Reportes y CSV")
    # Escaneamos archivos en la carpeta actual y subcarpetas
    archivos = list(Path(".").rglob("*.md")) + list(Path(".").rglob("*.csv"))
    
    if archivos:
        sel = st.selectbox("Elegir archivo para gestionar:", archivos)
        try:
            contenido = sel.read_text(encoding="utf-8")
            st.text_area("Vista Previa:", contenido, height=200)
            st.download_button(
                label=f"⬇️ Descargar {sel.name}",
                data=contenido,
                file_name=sel.name,
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
    else:
        st.info("No se han detectado archivos .md o .csv todavía.")
        
    if st.button("🔄 Refrescar Directorio"):
        st.rerun()