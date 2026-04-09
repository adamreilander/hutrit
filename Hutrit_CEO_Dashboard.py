import streamlit as st
import anthropic
import pandas as pd
from pathlib import Path
import os
import resend
import requests

# --- 1. CONFIGURACIÓN DE MARCA HUTRIT ---
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

# --- 2. MOTOR DE INTELIGENCIA (EL CEREBRO) ---
MAPA_HUTRIT = """
Capacidades Disponibles:
- Marketing: Publicación en Buffer (vía Make), /market-ads, /market-seo, /market-social, /market-emails.
- Ventas: Envío de correos reales con Resend, /sdr-quality-audit, /prospect-mining, /call-prep.
- Creativos: /social-creative-designer (Nano Banana).
- Scripts Python: prospector.py (Maps), researcher.py, linkedin_metrics.py.
- Archivos: Lectura/Escritura de CSV y conversión de reportes MD a TXT.
"""

def orquestar(prompt):
    if "ANTHROPIC_API_KEY" not in st.secrets:
        return "⚠️ Error: Configura la API Key de Anthropic en los Secrets de Streamlit."
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    sistema = f"Eres el CEO de Hutrit. Coordina estas habilidades: {MAPA_HUTRIT}. Eres un sistema operativo ejecutor."
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        system=sistema,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def enviar_a_buffer(texto, redes):
    # TU URL REAL DE MAKE
    WEBHOOK_URL = "https://hook.us2.make.com/eddmr643b21lxtqjri2e74gkrdgv0c7j"
    payload = {
        "contenido": texto, 
        "plataformas": redes, 
        "autor": "Adam - Hutrit OS"
    }
    try:
        r = requests.post(WEBHOOK_URL, json=payload)
        return r.status_code == 200
    except:
        return False

# --- 3. ESTRUCTURA DE LA APP (TABS) ---
st.title("Hutrit Intelligence OS 🤖")
tab_chat, tab_mkt, tab_ventas, tab_docs, tab_creativos = st.tabs([
    "💬 Orquestador Central", "📲 Marketing & Buffer", "💼 Ventas (Outreach)", "📂 Archivos & CSV", "🎨 Nano Banana"
])

with tab_chat:
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if p := st.chat_input("¿Qué misión ejecutamos hoy, Adam?"):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            with st.spinner("Hutrit pensando..."):
                r = orquestar(p)
                st.markdown(r)
                st.session_state.messages.append({"role": "assistant", "content": r})

with tab_mkt:
    st.subheader("Publicación Directa a Redes (Buffer)")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        post_content = st.text_area("Copy del Post:", height=200, placeholder="Pega aquí el contenido generado...")
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

with tab_ventas:
    st.subheader("Prospección y Envío de Emails (Resend)")
    path_csv = Path("research/seguimiento_hutrit.csv")
    if path_csv.exists():
        df = pd.read_csv(path_csv)
        st.dataframe(df, use_container_width=True)
        empresa = st.selectbox("Seleccionar empresa:", df['Empresa'].tolist())
        datos_c = df[df['Empresa'] == empresa].iloc[0]
        if st.button(f"📧 ENVIAR PROPUESTA A {empresa}"):
            if pd.notnull(datos_c['Email']):