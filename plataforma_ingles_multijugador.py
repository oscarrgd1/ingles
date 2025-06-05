import streamlit as st
import os
from ejercicio_listening_1 import ejercicio_count_on_me  # Asegúrate que este archivo tenga la función

st.set_page_config(page_title="Práctica de Inglés - Modo Competencia", layout="centered")

st.title("🎧 Plataforma de Práctica de Listening en Inglés")

nombre = st.text_input("Por favor escribe tu nombre para comenzar:")

if nombre:
    st.success(f"¡Bienvenido, {nombre}!")

    actividad = st.selectbox("Selecciona la actividad de Listening que deseas practicar:", [
        "Selecciona una opción",
        "🎵 Ejercicio: Count on Me (Bruno Mars)"
    ])

    if actividad == "🎵 Ejercicio: Count on Me (Bruno Mars)":
        st.markdown("---")
        ejercicio_count_on_me(nombre)
else:
    st.warning("Debes escribir tu nombre para continuar.")
