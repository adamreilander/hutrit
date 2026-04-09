import streamlit as st
import anthropic
import pandas as pd
from pathlib import Path
import os

# --- ESTÉTICA HUTRIT ---
st.set_page_config(page_title="Hutrit Intelligence OS", layout="wide")

st.markdown("""
    <style>
    :root { --hutrit-navy: #0e1117; --hutrit-red: #ff4b4b; }
    .stApp { background-color: var(--hutrit-navy); color: white; }
    .stTabs [data-baseweb="tab-list"] { background-color: #1e2130; border-radius: 10px; padding: 5px; }
    .stTabs [aria-selected="true"] { border-bottom: 2px solid var(--hutrit-red) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MAPA DE HABILIDADES ---
MAPA_HUTRIT = """
- Marketing: /market-ads, /market-seo, /market-social, /market-emails, /market-proposal.
- Ventas: /sdr-quality-audit, /prospect-mining, /call-prep.
- Creativos: /social-creative-designer (Nano Banana).
- Scripts: prospector.py (Google Maps + Emails), linkedin_metrics.py (Apify).
- Especiales: content-creator (multi-formato), data-analyst (CSV/Métricas).
"""

def orquestar(prompt):
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    sistema = f"Eres el CEO de Hutrit. Coordina estas habilidades: {MAPA_HUTRIT}"
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1500,
        system=sistema,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

# --- INTERFAZ ---
st.title("Hutrit Intelligence OS 🤖")
tab1, tab2, tab3 = st.tabs(["💬 Orquestador", "📂 Archivos & CSV", "🎨 Creativos"])

with tab1:
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

with tab2:
    st.subheader("Gestión de Datos y Documentos")
    # Lógica para descargar MD como TXT
    if st.button("🔄 Escanear Carpeta /research"):
        path_res = Path("research")
        if path_res.exists():
            csvs = [f for f in path_res.glob("*.csv")]
            sel_csv = st.selectbox("Actualizar CSV:", csvs)
            if sel_csv:
                df = pd.read_csv(sel_csv)
                st.dataframe(df)
                st.download_button("⬇️ Descargar en TXT", df.to_csv(index=False), "prospectos.txt")

with tab3:
    st.subheader("Nano Banana Engine")
    if st.button("🖼️ Generar Visual con /social-creative-designer"):
        st.info("Conectando con Nano Banana para generar PNG...")