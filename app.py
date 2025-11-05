import streamlit as st
import hashlib, time, json, secrets

# ---------------------- PREPARACIÓN BÁSICA ----------------------
st.set_page_config(page_title="Acta Digital", page_icon="📝")

# ---------------------- FUNCIONES CORE --------------------------
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

def count_votes():
    yes, no = 0, 0
    try:
        with open("votes.json") as f:
            for line in f:
                v = json.loads(line)
                if v["vote"] == "Sí":
                    yes += 1
                else:
                    no += 1
    except FileNotFoundError:
        pass
    return yes, no

# ----------------------- UI PRINCIPAL --------------------------
st.title("Registro de Documentos Digitales")

# Prompt 4 — Registro de documento
st.subheader("1) Registrar Documento")
owner = st.text_input("Propietario")
content = st.text_area("Contenido del documento")

if st.button("Registrar"):
    if owner.strip() == "" or content.strip() == "":
        st.error("Completa todos los campos antes de registrar")
    else:
        record = {"owner": owner, "hash": get_hash(content), "time": time.time()}
        with open("blockchain.json", "a") as f:
            f.write(json.dumps(record) + "\n")
        st.success("Documento registrado con éxito ✅")

# Prompt 5 — Verificación de integridad
st.subheader("2) Verificar si ya existe este documento")
texto_verificar = st.text_area("Pega aquí contenido a verificar")

if st.button("Verificar"):
    if verify(texto_verificar):
        st.success("✅ Este documento ya estaba registrado.")
    else:
        st.error("❌ No existe registro previo para este documento.")

# Prompt 6 — Firma Digital
st.subheader("3) Claves Criptográficas")
private_key = secrets.token_hex(16)
public_key = get_hash(private_key)
st.write("Tu clave pública:", public_key)
st.caption("La clave pública identifica. La privada te permite firmar.")

# Prompt 7 — Votación de validez por hash
st.header("4) Votación de validez (simulación DAO)")
doc_hash = st.text_input("Hash del documento a votar")
vote = st.radio("¿Es válido?", ["Sí", "No"])

if st.button("Votar"):
    with open("votes.json", "a") as f:
        f.write(json.dumps({"hash": doc_hash, "vote": vote}) + "\n")
    st.success("Voto registrado 🗳️")

# Prompt 8 — Resultado Votación
if st.button("Ver resultado"):
    y, n = count_votes()
    st.write(f"Sí: {y} | No: {n}")

# Prompt 10 — Reflexión final
st.write("---")
st.write("### Reflexión Final")
st.write("""
Has construido un prototipo completo donde:

- Se registra la existencia de algo (prueba de existencia)
- Se verifica integridad con hash
- Se firma digitalmente con claves
- Se vota su validez colectivamente

Pero… ¿quién garantiza que esa decisión sea justa?

Este módulo demuestra que el código ejecuta decisiones,
pero no puede comprender sus consecuencias éticas.

**La tecnología no es neutral.**
""")

