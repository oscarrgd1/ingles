import streamlit as st
import os

def ejercicio_count_on_me(nombre):
    st.header("🎧 Listening: Count on Me - Bruno Mars")
    
    st.audio("count on me.mp3")

    st.markdown("### Escucha la canción y responde las siguientes preguntas:")

    respuestas_correctas = {
        "¿A dónde navegará el cantante para encontrarte?": "Around the world",
        "¿Qué hará si estás perdido en la oscuridad?": "Be the light to guide you",
        "¿Qué se descubre cuando ayudamos a los amigos?": "What we are made of",
        "¿Qué número dice después de 'You can count on me like'?": "One, two, three",
        "¿Qué frase dice sobre los amigos?": "That's what friends are supposed to do"
    }

    aciertos = 0

    for pregunta, correcta in respuestas_correctas.items():
        respuesta = st.text_input(pregunta, key=pregunta)
        if respuesta:
            if respuesta.strip().lower() in correcta.lower():
                st.success("✅ Correcto")
                aciertos += 1
            else:
                st.error(f"❌ Incorrecto. Respuesta esperada: {correcta}")

    if st.button("Registrar resultados"):
        with open("resultados_listening.csv", "a") as f:
            f.write(f"{nombre},{aciertos},{len(respuestas_correctas)}\n")
        st.success("✅ Resultados registrados con éxito.")
