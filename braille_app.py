import streamlit as st
import openai
import os
from typing import List
from openai import OpenAI
from datetime import datetime
import pandas as pd

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

st.title("Evaluación de Listening: Louis Braille")

nombre = st.session_state.nombre if "nombre" in st.session_state else st.text_input("Escribe tu nombre completo")

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
        progreso = 0
        total_preguntas = len(PREGUNTAS)
        respuestas_correctas = 0
        respuestas_usuario = []
        for i, (pregunta, correcta, opciones) in enumerate(PREGUNTAS):
            progreso = int((i / total_preguntas) * 100)
            st.progress(progreso, text=f"Pregunta {i+1} de {total_preguntas}")
            st.write(f"**{pregunta}**")
            opcion = st.radio("Selecciona una opción:", opciones, index=None, key=f"preg{i}")
            respuestas_usuario.append((opcion, correcta))

        st.progress(100, text="¡Has llegado al final de las preguntas!")
        if st.button("Enviar respuestas de opción múltiple"):
            preguntas_omitidas = [idx+1 for idx, (resp, _) in enumerate(respuestas_usuario) if resp is None]
            if preguntas_omitidas:
                st.warning(f"Te faltó contestar la(s) pregunta(s): {', '.join(map(str, preguntas_omitidas))}. Por favor respóndelas antes de continuar.")
                st.stop()
            for seleccion, correcta in respuestas_usuario:
                if seleccion.startswith(correcta):
                    respuestas_correctas += 1

            calif_objetiva = (respuestas_correctas / len(PREGUNTAS)) * 100
            st.session_state.calif_objetiva = calif_objetiva

            st.success(f"Tu calificación en preguntas de opción múltiple es: {calif_objetiva}/100")

            archivo = "resultados.csv"
            if not os.path.exists(archivo):
                pd.DataFrame(columns=["Nombre", "Fecha", "Habilidad", "GPT", "OpcionMultiple"]).to_csv(archivo, index=False)

            if "calif_objetiva" in st.session_state and "calificacion_abierta" in st.session_state:
                st.markdown("---")
                st.header("Resultado final")

                promedio_general = round((st.session_state.calificacion_abierta + st.session_state.calif_objetiva) / 2, 2)
                st.write(f"**Promedio general:** {promedio_general}/100")

                if promedio_general >= 90:
                    st.balloons()
                    st.success("\U0001F3C5 ¡Felicidades! Has obtenido la medalla de oro por tu excelente desempeño.")
                elif promedio_general >= 75:
                    st.success("\U0001F948 Muy bien hecho. Has obtenido la medalla de plata.")
                elif promedio_general >= 60:
                    st.success("\U0001F949 Buen esfuerzo. Has obtenido la medalla de bronce.")
                else:
                    st.info("\U0001F3AF Sigue practicando. ¡Cada intento te acerca más a la meta!")
                st.write(f"**Nombre del estudiante:** {nombre}")
                st.write(f"**Comprensión general (GPT):** {st.session_state.calificacion_abierta}/100")
                st.write(f"**Opción múltiple:** {st.session_state.calif_objetiva}/100")

                frase = "¡Excelente trabajo! Cada paso que das te acerca a tus metas. \U0001F31F"
                if st.session_state.calificacion_abierta < 50:
                    frase = "¡No te rindas! Estás aprendiendo algo nuevo y eso ya es un gran logro. \U0001F680"
                elif st.session_state.calif_objetiva < 60:
                    frase = "¡Tú puedes mejorar! Sigue practicando, vas por buen camino. \U0001F4DA"

                st.info(frase)

                nueva_fila = {
                    "Nombre": nombre,
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Habilidad": "Listening",
                    "GPT": st.session_state.calificacion_abierta,
                    "OpcionMultiple": st.session_state.calif_objetiva
                }
                df = pd.read_csv(archivo).drop(columns=[col for col in ["Puntaje"] if col in pd.read_csv(archivo).columns])
                df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
                df.to_csv(archivo, index=False)
                st.success("Resultado guardado correctamente. Tu práctica ha sido registrada exitosamente en el sistema.")

                historial = df[df["Nombre"] == nombre]
                st.markdown("### \U0001F4C8 Historial de tus intentos")
                st.dataframe(historial.sort_values("Fecha", ascending=False).reset_index(drop=True))

                if not historial.empty:
                    st.line_chart(historial.sort_values("Fecha")[["GPT", "OpcionMultiple"]].reset_index(drop=True))

                    prompt_feedback = f"""
Eres un maestro que analiza el progreso de un estudiante a lo largo del tiempo.
Este es su historial de puntajes en comprensión lectora (GPT) y opción múltiple:

{historial[['Fecha', 'GPT', 'OpcionMultiple']].to_string(index=False)}

Escribe un mensaje de retroalimentación breve y motivador en español que le diga al estudiante cómo va, si ha mejorado, y qué puede hacer para mejorar más.
"""
                    try:
                        feedback_response = client.chat.completions.create(
                            model="gpt-4",
                            messages=[
                                {"role": "system", "content": "Eres un maestro alentador."},
                                {"role": "user", "content": prompt_feedback}
                            ]
                        )
                        feedback = feedback_response.choices[0].message.content.strip()
                        st.markdown("### \U0001F9E0 Retroalimentación personalizada")
                        st.info(feedback)
                    except Exception as e:
                        st.warning("No se pudo generar retroalimentación personalizada.")
