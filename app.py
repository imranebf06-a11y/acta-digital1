import streamlit as st
import hashlib, time, json

# ---------- FUNCIONES ----------
def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def verify(content):
    h = get_hash(content)
    try:
        with open("blockchain.json") as f:
            for line in f:
                r = json.loads(line)
                if r["hash"] == h:
                    return True
    except FileNotFoundError:
        return False
    return False

# ---------- INTERFAZ ----------
st.set_page_config(page_title="Acta Digital", page_icon="📝")
st.title("📝 Acta Digital")

st.write("Completa el acta y genera su firma digital (hash) para probar integridad.")

# --- Formulario del Acta ---
fecha = st.date_input("Fecha del Acta")
tema = st.text_input("Tema / Título de la Reunión")
asistentes = st.text_area("Asistentes (uno por línea)")
acuerdos = st.text_area("Acuerdos Finales")

if st.button("Generar Acta + Hash"):
    if tema.strip() == "" or asistentes.strip() == "" or acuerdos.strip() == "":
        st.error("⚠️ Debes completar todos los campos antes de generar el acta.")
    else:
        timestamp = str(time.time())
        contenido = f"{fecha}|{tema}|{asistentes}|{acuerdos}|{timestamp}"
        hash_acta = get_hash(contenido)

        bloque = {
            "fecha": str(fecha),
            "tema": tema,
            "asistentes": asistentes.split("\n"),
            "acuerdos": acuerdos,
            "timestamp": timestamp,
            "hash": hash_acta
        }

        # guardar el bloque en cadena local
        with open("blockchain.json", "a") as f:
            f.write(json.dumps(bloque) + "\n")

        st.success("✅ Acta registrada correctamente")
        st.write("### Firma generada (Hash)")
        st.write(hash_acta)
        st.write("### Bloque Registrado")
        st.json(bloque)

st.write("---")
st.subheader("🔎 Verificación de Documento Existente")

texto_verificar = st.text_area("Pega aquí el contenido completo de un documento para verificar")

if st.button("Verificar"):
    if texto_verificar.strip() == "":
        st.error("⚠️ Debes pegar contenido para verificar.")
    else:
        if verify(texto_verificar):
            st.success("✅ El documento ya estaba registrado (integridad comprobada).")
        else:
            st.error("❌ No existe este documento registrado anteriormente.")

