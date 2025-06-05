import streamlit as st
import datetime
import pandas as pd
import os

st.title("🎧 Ejercicio de Listening - Count on Me")
st.markdown("**Escucha la canción y responde las preguntas.**")

# Nombre del estudiante
nombre = st.text_input("Escribe tu nombre para comenzar:")

# Reproducir audio
if os.path.exists("count on me.mp3"):
    audio_file = open("count on me.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
else:
    st.warning("El archivo de audio no fue encontrado. Asegúrate de que 'count on me.mp3' esté en el mismo directorio.")

# Mostrar letra opcional
with st.expander("Ver letra de la canción"):
    st.write("""
If you ever find yourself stuck in the middle of the sea  
I'll sail the world to find you  
If you ever find yourself lost in the dark and you can't see  
I'll be the light to guide you  
We find out what we're made of  
When we are called to help our friends in need  
You can count on me like one, two, three, I'll be there  
And I know when I need it  
I can count on you like four, three, two and you'll be there  
'Cause that's what friends are supposed to do, oh, yeah.
""")

# Preguntas
respuestas = {
    "p1": st.radio("1. What will the singer do if you are stuck in the middle of the sea?", 
                   ["A) Swim alone", "B) Sail the world to find you", "C) Call for help", "D) Stay at home"]),
    "p2": st.radio("2. What does the singer promise to be if you're lost in the dark?", 
                   ["A) A flashlight", "B) A star", "C) The light to guide you", "D) The moon"]),
    "p3": st.radio("3. When do we find out what we're made of?", 
                   ["A) When we win a prize", "B) When we are called to help our friends in need", 
                    "C) When we study hard", "D) When we play games"]),
    "p4": st.radio("4. How can you count on the singer?", 
                   ["A) Like five, six, seven", "B) Like one, two, three", "C) Like ten, eleven, twelve", "D) Like seven, eight, nine"]),
    "p5": st.radio("5. What is the song mostly about?", 
                   ["A) Traveling", "B) Friendship and support", "C) School", "D) Weather"])
}

# Validar respuestas
respuestas_correctas = {
    "p1": "B) Sail the world to find you",
    "p2": "C) The light to guide you",
    "p3": "B) When we are called to help our friends in need",
    "p4": "B) Like one, two, three",
    "p5": "B) Friendship and support"
}

# Evaluación
if st.button("Registrar mi resultado"):
    if not nombre:
        st.warning("Por favor, escribe tu nombre.")
    else:
        puntaje = sum(respuestas[key] == respuestas_correctas[key] for key in respuestas)
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nuevo_resultado = pd.DataFrame([{
            "Nombre": nombre,
            "Fecha": fecha,
            "Puntaje": puntaje,
            "Habilidad": "Listening"
        }])

        # Guardar o anexar resultados
        archivo = "resultados_listening.csv"
        if os.path.exists(archivo):
            resultados = pd.read_csv(archivo)
            resultados = pd.concat([resultados, nuevo_resultado], ignore_index=True)
        else:
            resultados = nuevo_resultado

        resultados.to_csv(archivo, index=False)
        st.success(f"Resultado guardado. ¡Obtuviste {puntaje} de 5 puntos!")
