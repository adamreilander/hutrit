import streamlit as st
import anthropic # Asegúrate de tenerlo en requirements.txt
import os
from pathlib import Path

# Configuración de página
st.set_page_config(page_title="Hutrit Intelligence Chat", layout="centered", page_icon="🤖")

# --- MOTOR DE INTELIGENCIA ---
def obtener_contexto_agencia():
    # Esta función le dice a la IA qué archivos tienes disponibles
    contexto = "Tienes acceso a las siguientes carpetas y habilidades en Hutrit:\n"
    for folder in ["ads", "seo", "social", "research", ".claude/skills"]:
        path = Path(folder)
        if path.exists():
            files = [f.name for f in path.rglob("*") if f.suffix in [".py", ".md"]]
            contexto += f"- {folder.upper()}: {', '.join(files)}\n"
    return contexto

# --- INTERFAZ ESTILO CHAT ---
st.title("Hutrit Intelligence OS 🎙️")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto (como Gemini/Claude)
if prompt := st.chat_input("¿Qué misión ejecutamos hoy, Adam?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta de la IA
    with st.chat_message("assistant"):
        if "ANTHROPIC_API_KEY" in st.secrets:
            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
            contexto = obtener_contexto_agencia()
            
            # La IA decide qué hacer basándose en tus archivos reales
            full_prompt = f"{contexto}\n\nOrden del usuario: {prompt}\n\nResponde como el sistema operativo de Hutrit. Di qué habilidades usarás y ejecuta el razonamiento."
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": full_prompt}]
            )
            respuesta_texto = response.content[0].text
            st.markdown(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
        else:
            st.error("⚠️ Falta configurar la ANTHROPIC_API_KEY en Secrets de Streamlit.")