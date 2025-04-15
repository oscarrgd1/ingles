import streamlit as st
import openai
import os
from typing import List

st.set_page_config(page_title="Evaluación de Listening", layout="centered")

from openai import OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Texto completo de la lectura
LECTURA = """
Louis Braille was born in 1809 near Paris. When he was three years old, he had an accident, and he became blind. 
When he was ten, he went to a special school for blind people.

Louis's school library had books with letters that the blind students could feel with their fingers. 
But there weren't very many, because making that kind of book cost a lot of money. 
Louis quickly read all the books in the library. He wanted to read and learn more. 
So, he decided to invent a new way to make letters for blind people. 
He used dots to represent the letters. These dots also stuck up from the pages. 
Louis's system of letters was easier to read. It was also cheaper, so people could make more books.

Louis's system is now known as Braille. You have probably seen Braille letters and numbers in elevators and other public places.
Can you guess how old Louis was when he invented his system? He was only 15!
"""

PREGUNTAS = [
    ("¿Dónde nació Louis Braille?", "c", ["a) En Londres", "b) En Berlín", "c) Cerca de París", "d) En Madrid"]),
    ("¿En qué año nació Louis Braille?", "b", ["a) 1815", "b) 1809", "c) 1799", "d) 1825"]),
    ("¿Qué le sucedió a Louis Braille cuando tenía tres años?", "c", ["a) Perdió a sus padres", "b) Se mudó a París", "c) Tuvo un accidente y quedó ciego", "d) Se enfermó gravemente"]),
    ("¿A qué edad ingresó a una escuela especial para personas ciegas?", "b", ["a) A los cinco años", "b) A los diez años", "c) A los ocho años", "d) A los quince años"]),
    ("¿Cómo eran los libros en la biblioteca de su escuela?", "b", ["a) Libros con ilustraciones en relieve", "b) Libros con letras que se podían sentir con los dedos", "c) Libros leídos en voz alta por maestros", "d) Libros escritos en tinta grande"]),
    ("¿Por qué había pocos libros en la biblioteca?", "c", ["a) Porque estaban en otro idioma", "b) Porque los estudiantes no los leían", "c) Porque eran muy caros de hacer", "d) Porque se dañaban fácilmente"]),
    ("¿Qué hizo Louis cuando terminó de leer todos los libros?", "c", ["a) Se cambió de escuela", "b) Escribió sus propios libros", "c) Decidió inventar un nuevo sistema de letras", "d) Aprendió a leer en otro idioma"]),
    ("¿Qué usó Louis para representar las letras?", "d", ["a) Rayas y puntos", "b) Figuras geométricas", "c) Colores y sombras", "d) Puntos (dots)"]),
    ("¿Por qué era mejor el sistema que inventó Louis?", "c", ["a) Porque era más artístico", "b) Porque tenía dibujos", "c) Porque era más fácil de leer y más barato", "d) Porque tenía sonido"]),
    ("¿Cuántos años tenía Louis cuando inventó su sistema?", "d", ["a) 21", "b) 18", "c) 10", "d) 15"])
]

# Función para calificar la pregunta abierta
def calificar_pregunta_abierta(respuesta_estudiante: str) -> int:
    prompt = f"""
Actúa como un maestro de comprensión de lectura. Evalúa la siguiente respuesta del estudiante basada en el texto que se leyó.
Asigna una calificación del 0 al 100 según cuánto haya comprendido el estudiante. Sé justo y considera si la respuesta refleja
una buena comprensión general del contenido, sin penalizar errores ortográficos menores. Devuelve solo el número.

Texto leído:
{LECTURA}

Respuesta del estudiante:
{respuesta_estudiante}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un experto en comprensión lectora."},
                {"role": "user", "content": prompt}
            ]
        )
        calificacion = int(response.choices[0].message.content.strip())
        return min(max(calificacion, 0), 100)
    except Exception as e:
        st.error(f"Error al calificar la respuesta: {e}")
        return 0

# Función principal
st.title("Evaluación de Listening: Louis Braille")

nombre = st.text_input("Escribe tu nombre completo")

if st.button("Reproducir audio"):
    st.audio("braille.mp3")

if nombre:
    st.markdown("### Pregunta 1: ¿Qué entendiste del audio? (responde en español)")
    respuesta_abierta = st.text_area("Tu respuesta")

    if st.button("Enviar respuesta abierta") and respuesta_abierta.strip():
        calificacion_abierta = calificar_pregunta_abierta(respuesta_abierta)
        st.success(f"Tu calificación de comprensión general es: {calificacion_abierta}/100")
        st.session_state.calificacion_abierta = calificacion_abierta

    if "calificacion_abierta" in st.session_state:
        st.markdown("### Responde las siguientes preguntas de opción múltiple")
        respuestas_correctas = 0
        respuestas_usuario = []
        for i, (pregunta, correcta, opciones) in enumerate(PREGUNTAS):
            st.write(f"**{pregunta}**")
            opcion = st.radio("Selecciona una opción:", opciones, key=f"preg{i}")
            respuestas_usuario.append((opcion, correcta))

        if st.button("Enviar respuestas de opción múltiple"):
            for seleccion, correcta in respuestas_usuario:
                if seleccion.startswith(correcta):
                    respuestas_correctas += 1

            calif_objetiva = (respuestas_correctas / len(PREGUNTAS)) * 100
            st.session_state.calif_objetiva = calif_objetiva

            st.success(f"Tu calificación en preguntas de opción múltiple es: {calif_objetiva}/100")

    if st.button("Registrar inicio de práctica"):
        if "calif_objetiva" in st.session_state and "calificacion_abierta" in st.session_state:
            st.markdown("---")
            st.header("Resultado final")
            st.write(f"**Nombre del estudiante:** {nombre}")
            st.write(f"**Comprensión general (GPT):** {st.session_state.calificacion_abierta}/100")
            st.write(f"**Opción múltiple:** {st.session_state.calif_objetiva}/100")

            frase = "¡Excelente trabajo! Cada paso que das te acerca a tus metas. 🌟"
            if st.session_state.calificacion_abierta < 50:
                frase = "¡No te rindas! Estás aprendiendo algo nuevo y eso ya es un gran logro. 🚀"
            elif st.session_state.calif_objetiva < 60:
                frase = "¡Tú puedes mejorar! Sigue practicando, vas por buen camino. 📚"

            st.info(frase)
        else:
            st.warning("Asegúrate de enviar tanto la respuesta abierta como las de opción múltiple antes de registrar.")
