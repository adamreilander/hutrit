import streamlit as st
import anthropic
import pandas as pd
from pathlib import Path
import os
import resend
import requests

# --- 1. CONFIGURACIÓN DE MARCA HUTRIT ---
st.set_page_config(page_title="Hutrit Intelligence OS", layout="wide", page_icon="📈")

# Estética Premium: Navy, Red & Dark Mode
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

# --- 2. MOTOR DE INTELIGENCIA (EL CEREBRO) ---
MAPA_HUTRIT = """
Capacidades Disponibles:
- Marketing: Publicación en Buffer (vía Make), /market-ads, /market-seo, /market-social.
- Ventas: Envío de correos reales con Resend, /sdr-quality-audit.
- Creativos: Inspiración en carpeta /social para Nano Banana.
- Archivos: Lectura de CSV en /research para prospección.
"""

def orquestar(prompt):
    if "ANTHROPIC_API_KEY" not in st.secrets:
        return "⚠️ Error: Configura la API Key de Anthropic en los Secrets de Streamlit."
    
    try:
        client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        sistema = f"Eres el CEO de Hutrit. Coordina estas habilidades: {MAPA_HUTRIT}. Eres un sistema operativo ejecutor."
        
        # Uso de 'latest' para asegurar estabilidad y evitar BadRequestError
        response = client.messages.create(
            model="claude-3-5-sonnet-latest", 
            max_tokens=2000,
            system=sistema,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"❌ Error en la orquestación: {str(e)}"

def enviar_a_buffer(texto, redes):
    # Webhook de Make vinculado a Buffer
    WEBHOOK_URL = "https://hook.us2.make.com/eddmr643b21lxtqjri2e74gkrdgv0c7j"
    payload = {"contenido": texto, "plataformas": redes, "autor": "Adam - Hutrit OS"}
    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        return r.status_code == 200
    except:
        return False

# --- 3. ESTRUCTURA DE LA APP (TABS) ---
st.title("Hutrit Intelligence OS 🤖")
tab_chat, tab_mkt, tab_ventas, tab_docs, tab_creativos = st.tabs([
    "💬 Orquestador Central", "📲 Marketing & Buffer", "💼 Ventas (Outreach)", "📂 Archivos & CSV", "🎨 Nano Banana"
])

# --- TAB 1: EL CHAT MAESTRO ---
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

# --- TAB 2: MARKETING & BUFFER ---
with tab_mkt:
    st.subheader("Publicación Directa a Redes Sociales")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        post_content = st.text_area("Copy del Post:", height=200, placeholder="Pega aquí el contenido...")
    with col_b:
        redes_sel = st.multiselect("Canales:", ["LinkedIn", "Instagram", "TikTok", "Facebook"])
        if st.button("🚀 ENVIAR A BUFFER"):
            if post_content and redes_sel:
                if enviar_a_buffer(post_content, redes_sel):
                    st.success("✅ ¡Enviado a la cola de Buffer!")
                else:
                    st.error("❌ Error de conexión con Make.")
            else:
                st.warning("Escribe el copy y selecciona redes.")

# --- TAB 3: VENTAS (RESEND) ---
with tab_ventas:
    st.subheader("Envío de Emails Personalizados")
    path_csv = Path("research/seguimiento_hutrit.csv")
    if path_csv.exists():
        df = pd.read_csv(path_csv)
        st.dataframe(df, use_container_width=True)
        empresa = st.selectbox("Selecciona empresa:", df['Empresa'].tolist())
        datos_c = df[df['Empresa'] == empresa].iloc[0]
        if st.button(f"📧 ENVIAR CORREO A {empresa}"):
            if pd.notnull(datos_c['Email']):
                try:
                    resend.api_key = st.secrets["RESEND_API_KEY"]
                    resend.Emails.send({
                        "from": "Adam de Hutrit <onboarding@resend.dev>",
                        "to": [datos_c['Email']],
                        "subject": f"Propuesta Estratégica para {empresa}",
                        "html": f"<p>Hola {empresa}, basándonos en las tendencias actuales...</p>"
                    })
                    st.success(f"Enviado a {datos_c['Email']}")
                except Exception as e: st.error(f"Error: {e}")
            else:
                st.warning("⚠️ Sin email.")
    else:
        st.info("Falta el archivo de prospección en /research.")

# --- TAB 4: DOCUMENTOS ---
with tab_docs:
    st.subheader("Auditorías y Reportes")
    reportes = list(Path(".").rglob("*.md"))
    if reportes:
        sel = st.selectbox("Archivo:", reportes)
        st.download_button("⬇️ Descargar .txt", sel.read_text(encoding="utf-8"), file_name=f"{sel.stem}.txt")

# --- TAB 5: CREATIVOS ---
with tab_creativos:
    st.subheader("Inspiración de Carpeta /social")
    if st.button("🎨 Generar Concepto con Nano Banana"):
        st.info("Analizando creativos previos para mantener el estilo Hutrit...")