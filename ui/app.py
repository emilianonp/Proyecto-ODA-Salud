import streamlit as st
import requests

API_URL = "http://localhost:8000/query"

st.title("ODA Salud")

question = st.text_input("Pregunta sobre tus documentos")
if st.button("Preguntar") and question:
    with st.spinner('Consultando...'):
        resp = requests.post(API_URL, json={"question": question})
        if resp.status_code == 200:
            data = resp.json()
            st.write(data.get("answer"))
            st.write("Documentos relacionados:")
            for doc in data.get("documents", []):
                st.write(f"- {doc.get('ruta_archivo')}")
        else:
            st.error(f"Error: {resp.text}")
