import streamlit as st

st.set_page_config(page_title="Acta Digital", page_icon="📝")
st.title("📝 Acta Digital")
st.write("Hola, Streamlit está funcionando.")

import streamlit as st
import hashlib, time, json

st.set_page_config(page_title="Acta Digital", page_icon="📝")
st.title("📝 Acta Digital")

st.write("Probando funcionamiento básico con hash + timestamp")

# ejemplo simple: generar un hash de un texto cualquiera
texto = st.text_input("Escribe algo para probar")

if st.button("Generar hash"):
    timestamp = str(time.time())
    data = texto + timestamp
    hash_resultado = hashlib.sha256(data.encode()).hexdigest()

    st.write("### Resultado")
    st.write("Timestamp:", timestamp)
    st.write("Hash SHA-256:", hash_resultado)

    # mostrar cómo quedaría guardado
    bloque = {
        "texto": texto,
        "timestamp": timestamp,
        "hash": hash_resultado
    }
    st.json(bloque)

