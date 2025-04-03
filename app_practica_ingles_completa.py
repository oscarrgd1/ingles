
import streamlit as st
import pandas as pd
import random
from datetime import datetime
import os

st.set_page_config(page_title="Centro de Práctica de Inglés", layout="centered")
st.title("🎓 Centro de Práctica de Inglés para Ángel")

# Menú de navegación
opcion = st.sidebar.radio("Selecciona qué quieres practicar:", [
    "📘 Lección 1 completa",
    "🧠 Gramática - Past Simple (aleatorio)"
])

# -------------------
# OPCIÓN 1: Lección 1 Completa
# -------------------
if opcion == "📘 Lección 1 completa":
    st.header("📘 Lección 1 – ¿Qué hice ayer?")
    st.markdown("Esta actividad te ayudará a practicar lectura, gramática, escritura y listening.")

    score = 0

    # Parte 1: Gramática
    st.subheader("1. Gramática – Past Simple")
    q1 = st.radio("1. Yesterday I ___ (wake up) at 7:00.", ["wake", "woke", "waked"])
    if q1 == "woke": score += 1
    q2 = st.radio("2. I ___ (eat) cereal for breakfast.", ["ate", "eated", "eat"])
    if q2 == "ate": score += 1
    q3 = st.radio("3. Then I ___ (go) to the park.", ["goed", "went", "go"])
    if q3 == "went": score += 1
    q4 = st.radio("4. I ___ (play) with my dog.", ["played", "play", "playd"])
    if q4 == "played": score += 1
    q5 = st.radio("5. I ___ (watch) a cartoon in the evening.", ["watch", "watched", "watching"])
    if q5 == "watched": score += 1

    # Parte 2: Lectura
    st.subheader("2. Comprensión de Lectura")
    st.markdown("""
    > Yesterday was a busy day. I woke up at 7:00. I had breakfast with my family. Then I walked to the park and played soccer.
    > At noon, I ate lunch and watched a cartoon. In the evening, I did my homework and helped my mom in the kitchen. I went to bed at 9:30.
    """)
    q6 = st.radio("6. What time did I wake up?", ["7:00", "9:00", "8:30"])
    if q6 == "7:00": score += 1
    q7 = st.radio("7. What did I do in the park?", ["I walked my dog", "I played soccer", "I ate lunch"])
    if q7 == "I played soccer": score += 1
    q8 = st.radio("8. What did I watch?", ["a movie", "a cartoon", "a documentary"])
    if q8 == "a cartoon": score += 1
    q9 = st.radio("9. Who did I help?", ["my dad", "my teacher", "my mom"])
    if q9 == "my mom": score += 1
    q10 = st.radio("10. What time did I go to bed?", ["9:30", "10:30", "8:30"])
    if q10 == "9:30": score += 1

    # Parte 3: Listening
    st.subheader("3. Escucha y comprende")
    st.audio("leccion1_listening.mp3")

    # Parte 4: Escritura
    st.subheader("4. Escritura")
    text = st.text_area("Escribe 5 oraciones usando: First, Then, After that, Finally...")

    st.markdown(f"### Tu puntaje es: {score} / 10")
    if score == 10:
        st.success("¡Excelente trabajo!")
    elif score >= 7:
        st.info("¡Muy bien hecho!")
    else:
        st.warning("Sigue practicando, ¡tú puedes!")

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

    if os.path.exists("resultados_angel.csv"):
        st.subheader("📈 Historial de resultados")
        df = pd.read_csv("resultados_angel.csv")
        st.dataframe(df)

# -------------------
# OPCIÓN 2: Gramática Aleatoria
# -------------------
elif opcion == "🧠 Gramática - Past Simple (aleatorio)":
    st.header("🧠 Práctica de Gramática – Past Simple")
    df = pd.read_csv("past_simple_questions.csv")
    selected = df.sample(5, random_state=random.randint(1, 1000))
    score = 0

    for i in range(5):
        correct = selected.iloc[i]["Past"]
        options = [correct] + random.sample([x for x in df["Past"].unique() if x != correct], 2)
        random.shuffle(options)
        answer = st.radio(f"{i+1}. {selected.iloc[i]['Sentence']}", options)
        if answer == correct:
            score += 1

    st.markdown(f"### Tu puntaje es: {score} / 5")
    if score == 5:
        st.success("¡Perfecto!")
    elif score >= 3:
        st.info("¡Buen trabajo!")
    else:
        st.warning("Puedes mejorar. ¡Inténtalo otra vez!")
