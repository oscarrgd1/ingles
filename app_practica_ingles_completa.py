
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Plataforma de Inglés", layout="centered")
st.title("🎓 Plataforma de práctica de inglés")

# Estado de sesión para nombre del usuario
if "nombre" not in st.session_state:
    st.session_state.nombre = ""

# Pantalla de ingreso de nombre
if not st.session_state.nombre:
    st.header("👤 Ingreso de jugador")
    nombre = st.text_input("Escribe tu nombre para comenzar:")
    if st.button("🚀 Empezar"):
        if nombre.strip() == "":
            st.warning("Por favor escribe un nombre.")
        else:
            st.session_state.nombre = nombre.strip().title()
            st.success(f"¡Bienvenido, {st.session_state.nombre}!")
            st.rerun()
    st.stop()

# Mostrar saludo
st.success(f"Hola {st.session_state.nombre}, elige una actividad:")

# Archivo donde se guardarán resultados
archivo = "resultados.csv"

# Asegurar que el archivo existe
if not os.path.exists(archivo):
    df_init = pd.DataFrame(columns=["Nombre", "Fecha", "Habilidad", "Puntaje"])
    df_init.to_csv(archivo, index=False)

# Menú de habilidades
habilidad = st.selectbox("Selecciona la habilidad que quieres practicar:", [
    "Selecciona una...",
    "🎧 Listening",
    "✍️ Writing",
    "🧠 Grammar",
    "🗣 Speaking"
])

if habilidad != "Selecciona una...":
    st.info(f"Aquí pronto aparecerá un ejercicio de {habilidad}. ¡Estamos trabajando en ello!")

    # Registrar entrada con puntaje vacío
    if st.button("Registrar inicio de práctica"):
        df = pd.read_csv(archivo)
        nueva_fila = {
            "Nombre": st.session_state.nombre,
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Habilidad": habilidad.replace("🎧", "").replace("✍️", "").replace("🧠", "").replace("🗣", "").strip(),
            "Puntaje": ""
        }
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        df.to_csv(archivo, index=False)
        st.success("Inicio de práctica registrado.")

# Mostrar tabla comparativa
st.header("📊 Tabla de resultados")
df = pd.read_csv(archivo)
if not df.empty:
    st.dataframe(df)
else:
    st.info("Aún no hay resultados registrados.")
