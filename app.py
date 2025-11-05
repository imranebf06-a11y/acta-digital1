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

st.set_page_config(page_title="Acta Digital", page_icon="📝")
st.title("📝 Acta Digital")

st.write("Completa el acta y luego generaremos un hash como firma digital")

# --- Formulario del Acta ---
fecha = st.date_input("Fecha del Acta")
tema = st.text_input("Tema / Título de la Reunión")
asistentes = st.text_area("Asistentes (separados por línea)")
acuerdos = st.text_area("Acuerdos Finales")

if st.button("Generar Acta + Hash"):
    timestamp = str(time.time())

    # preparamos data como texto para firmar
    contenido = f"{fecha}|{tema}|{asistentes}|{acuerdos}|{timestamp}"

    hash_acta = get_hash(contenido)

    st.write("### Firma generada para esta acta")
    st.write("Timestamp:", timestamp)
    st.write("Hash SHA-256:", hash_acta)

    bloque = {
        "fecha": str(fecha),
        "tema": tema,
        "asistentes": asistentes.split("\n"),
        "acuerdos": acuerdos,
        "timestamp": timestamp,
        "hash": hash_acta
    }

    st.write("### Bloque resultante")
    st.json(bloque)

st.title("📄 Registro de Documentos Digitales")

st.write("Este módulo permite registrar un documento y generar su huella criptográfica (hash) para asegurar integridad.")

owner = st.text_input("Propietario del documento")
content = st.text_area("Contenido del documento")

if st.button("Registrar"):
    if owner.strip() == "" or content.strip() == "":
        st.error("⚠️ Debes completar todos los campos antes de registrar.")
    else:
        timestamp = time.time()
        hashed = get_hash(content)

        record = {
            "owner": owner,
            "content": content,
            "hash": hashed,
            "timestamp": timestamp
        }

        # Guardar registro (append en archivo local)
        with open("blockchain.json", "a") as f:
            f.write(json.dumps(record) + "\n")

        st.success("Documento registrado con éxito ✅")

        st.write("### Bloque generado")
        st.json(record)
st.write("---")
st.subheader("🔎 Verificación de Documento")

texto_verificar = st.text_area("Pega aquí el contenido del documento a verificar")

if st.button("Verificar"):
    if texto_verificar.strip() == "":
        st.error("⚠️ Debes pegar un texto para verificar.")
    else:
        if verify(texto_verificar):
            st.success("✅ Este documento ya estaba registrado (integridad comprobada).")
        else:
            st.error("❌ Documento NO encontrado en la cadena registrada.")
