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
    .stTextArea>div>div>textarea { background-color: #1e2130; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MOTOR DE INTELIGENCIA (ORQUESTADOR) ---
def orquestar(prompt):
    if "ANTHROPIC_API_KEY" not in st.secrets:
        return "⚠️ Error: Configura ANTHROPIC_API_KEY en Secrets."
    
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    try:
        # Usamos la versión estable 20240620 para evitar el error 404 de modelos nuevos
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=3000,
            system="Eres el CEO de Hutrit. Experto en Marketing Ads, Reclutamiento Tech y Data. Si piden un CSV, genéralo en un bloque de código.",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        error_msg = str(e).lower()
        if "credit balance" in error_msg:
            return "🚨 SALDO: Anthropic aún procesa tu recarga. Espera 15 min."
        return f"❌ Error de Sistema: {str(e)}"

# --- 3. FUNCIONES DE HERRAMIENTAS ---
def enviar_a_buffer(texto, redes):
    WEBHOOK_URL = "https://hook.us2.make.com/eddmr643b21lxtqjri2e74gkrdgv0c7j"
    payload = {"contenido": texto, "plataformas": redes, "autor": "Adam - Hutrit OS"}
    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        return r.status_code == 200
    except: return False

# --- 4. INTERFAZ Y NAVEGACIÓN ---
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
            with st.spinner("Hutrit analizando..."):
                r = orquestar(p)
                st.markdown(r)
                st.session_state.messages.append({"role": "assistant", "content": r})

# --- TAB: MARKETING ---
with tab_mkt:
    st.subheader("Publicación vía Buffer")
    post_txt = st.text_area("Copy estratégico:", height=200, placeholder="Pega aquí el contenido generado...")
    redes_sel = st.multiselect("Canales:", ["LinkedIn", "Instagram", "TikTok", "Facebook"])
    if st.button("🚀 ENVIAR A BUFFER"):
        if post_txt and redes_sel:
            if enviar_a_buffer(post_txt, redes_sel):
                st.success("✅ ¡Enviado a Buffer correctamente!")
            else: st.error("Error en conexión con Make.")
        else: st.warning("Completa el post y selecciona redes.")

# --- TAB: VENTAS ---
with tab_ventas:
    st.subheader("Outreach con Resend")
    if "RESEND_API_KEY" in st.secrets:
        st.info("Conexión con Resend activa.")
        email_dest = st.text_input("Email del prospecto:")
        subject = st.text_input("Asunto:")
        mensaje = st.text_area("Cuerpo del correo:")
        if st.button("📧 Enviar Email"):
            try:
                resend.api_key = st.secrets["RESEND_API_KEY"]
                resend.Emails.send({
                    "from": "Adam - Hutrit <onboarding@resend.dev>",
                    "to": [email_dest],
                    "subject": subject,
                    "html": f"<p>{mensaje}</p>"
                })
                st.success("Email enviado.")
            except Exception as e: st.error(f"Error: {e}")
    else:
        st.warning("Falta RESEND_API_KEY en Secrets.")

# --- TAB: ARCHIVOS ---
with tab_docs:
    st.subheader("Gestor de Reportes y CSV")
    # Buscamos archivos en la carpeta actual y /research
    archivos = list(Path(".").rglob("*.md")) + list(Path(".").rglob("*.csv"))
    if archivos:
        sel = st.selectbox("Elegir archivo:", archivos)
        try:
            contenido = sel.read_text(encoding="utf-8")
            st.text_area("Vista Previa:", contenido, height=200)
            st.download_button(f"⬇️ Descargar {sel.name}", contenido, file_name=sel.name)
        except: st.error("No se pudo leer el archivo.")
    
    if st.button("🔄 Refrescar Directorio"): st.rerun()