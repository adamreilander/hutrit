import streamlit as st
import os

st.set_page_config(page_title="Hutrit CEO", page_icon="🚀")

st.title("Hutrit: Growth Engine 📈")

# Verificación de llaves (solo para ti, no se ven en la web)
if "APIFY_API_KEY" in st.secrets:
    st.sidebar.success("✅ Conectado a la Agencia")
else:
    st.sidebar.error("⚠️ Faltan las llaves en Secrets")

st.markdown("---")
st.write("Bienvenido, Adam. El sistema está listo para operar fuera de VS Code.")

if st.button("🔍 Iniciar Escaneo de LinkedIn"):
    st.write("Conectando con el scraper...")
    # Prueba simple
    st.balloons()