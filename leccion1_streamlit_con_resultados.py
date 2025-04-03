
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Lección 1 – ¿Qué hice ayer?", layout="centered")
st.title("📝 Lección 1 – ¿Qué hice ayer?")
st.subheader("Evaluación interactiva de inglés")

st.markdown("""
Esta app te ayudará a practicar y evaluar lo aprendido en la Lección 1.
Responde cada sección con atención.
""")

# Sección 1: Gramática
st.header("📘 Parte 1: Gramática – Past Simple")
score = 0

q1 = st.radio("1. Yesterday I ___ (wake up) at 7:00.", ["wake", "woke", "waked"])
if q1 == "woke":
    score += 1

q2 = st.radio("2. I ___ (eat) cereal for breakfast.", ["ate", "eated", "eat"])
if q2 == "ate":
    score += 1

q3 = st.radio("3. Then I ___ (go) to the park.", ["goed", "went", "go"])
if q3 == "went":
    score += 1

q4 = st.radio("4. I ___ (play) with my dog.", ["played", "play", "playd"])
if q4 == "played":
    score += 1

q5 = st.radio("5. I ___ (watch) a cartoon in the evening.", ["watch", "watched", "watching"])
if q5 == "watched":
    score += 1

# Sección 2: Lectura
st.header("📖 Parte 2: Comprensión de lectura")
st.markdown("""
**Texto:**
> Yesterday was a busy day. I woke up at 7:00. I had breakfast with my family. Then I walked to the park and played soccer.
> At noon, I ate lunch and watched a cartoon. In the evening, I did my homework and helped my mom in the kitchen. I went to bed at 9:30.
""")

q6 = st.radio("6. What time did I wake up?", ["7:00", "9:00", "8:30"])
if q6 == "7:00":
    score += 1

q7 = st.radio("7. What did I do in the park?", ["I walked my dog", "I played soccer", "I ate lunch"])
if q7 == "I played soccer":
    score += 1

q8 = st.radio("8. What did I watch?", ["a movie", "a cartoon", "a documentary"])
if q8 == "a cartoon":
    score += 1

q9 = st.radio("9. Who did I help?", ["my dad", "my teacher", "my mom"])
if q9 == "my mom":
    score += 1

q10 = st.radio("10. What time did I go to bed?", ["9:30", "10:30", "8:30"])
if q10 == "9:30":
    score += 1

# Sección de audio
st.header("🎧 Parte 3: Listening")
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

# Sección de escritura
st.header("✍️ Parte 4: Escritura")
text = st.text_area("Escribe 5 oraciones sobre lo que hiciste ayer usando: First, Then, After that, Finally...")

# Resultados
st.header("📊 Resultado")
st.markdown(f"**Tu puntaje es:** {score} / 10")

if score == 10:
    st.success("¡Excelente trabajo! Dominas este tema.")
elif score >= 7:
    st.info("¡Muy bien! Aún puedes repasar un poco más.")
else:
    st.warning("Necesitas practicar más. ¡Tú puedes!")

if text:
    st.markdown("Has escrito:")
    st.write(text)

# Guardar resultados
if st.button("📥 Guardar resultado de hoy"):
    today = datetime.now().strftime("%Y-%m-%d")
    results_path = "resultados_angel.csv"
    new_row = pd.DataFrame([[today, score, text]], columns=["Fecha", "Puntaje", "Escritura"])
    if os.path.exists(results_path):
        df = pd.read_csv(results_path)
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row
    df.to_csv(results_path, index=False)
    st.success("Resultado guardado correctamente.")

# Mostrar progreso si existe
if os.path.exists("resultados_angel.csv"):
    st.header("📈 Historial de avances")
    df = pd.read_csv("resultados_angel.csv")
    st.dataframe(df)
