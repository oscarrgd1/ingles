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
if not os.path.exists(archivo):
    df_init = pd.DataFrame(columns=["Nombre", "Fecha", "Habilidad", "GPT", "OpcionMultiple"])
    df_init.to_csv(archivo, index=False)

# Menú de habilidades
habilidad = st.selectbox("Selecciona la habilidad que quieres practicar:", [
    "Selecciona una...",
    "🎧 Listening",
    "✍️ Writing",
    "🧠 Grammar",
    "🗣 Speaking"
])

# Cargar sección de listening desde otro archivo
def mostrar_listening():
    st.header("🎧 Ejercicio de Listening")
    st.markdown("Aquí va el ejercicio de audio que ayudará a practicar comprensión auditiva.")
    st.info("Ejecutando 'braille_app.py'...")
    try:
        with open("braille_app.py", "r", encoding="utf-8") as f:
            exec(f.read(), globals())
    except FileNotFoundError:
        st.error("No se encontró el archivo 'braille_app.py'. Asegúrate de que esté en la misma carpeta.")
    except Exception as e:
        st.error(f"Ocurrió un error al ejecutar 'braille_app.py': {e}")

if habilidad != "Selecciona una...":
    habilidad_limpia = habilidad.replace("🎧", "").replace("✍️", "").replace("🧠", "").replace("🗣", "").strip()

    if habilidad_limpia == "Listening":
        mostrar_listening()
    else:
        st.info(f"Aquí pronto aparecerá un ejercicio de {habilidad_limpia}. ¡Estamos trabajando en ello!")

# Mostrar tabla comparativa
st.header("📊 Tabla de resultados")
df = pd.read_csv(archivo)
df = df.drop(columns=[col for col in ["Puntaje"] if col in df.columns])
if not df.empty:
    st.dataframe(df)
else:
    st.info("Aún no hay resultados registrados.")
