import streamlit as st
from playwright_login import baixar_html_prova
import os


st.set_page_config(page_title="📥 Downloader de HTML - Gran", layout="centered")

st.title("📥 Downloader de HTML da Prova - Backoffice Gran")
st.info("⚠️ Faça login no Gran Conta. A sessão será salva para acessos futuros.")

# 🔥 Variáveis para controle do estado
if 'html' not in st.session_state:
    st.session_state.html = None
    st.session_state.file_name = None


with st.form("formulario"):
    email = st.text_input("Seu E-mail Gran", type="default")
    senha = st.text_input("Sua Senha Gran", type="password")
    id_prova = st.text_input("ID da Prova (número que aparece no link)", placeholder="Ex: 192414")

    submitted = st.form_submit_button("🔽 Baixar HTML da Prova")

    if submitted:
        if not email or not senha or not id_prova:
            st.error("❌ Preencha todos os campos.")
        else:
            with st.spinner("🔐 Fazendo login e acessando a prova..."):
                try:
                    html = baixar_html_prova(email, senha, id_prova)

                    file_name = f"prova_{id_prova}.html"
                    with open(file_name, "w", encoding="utf-8") as f:
                        f.write(html)

                    st.success(f"✅ HTML da prova {id_prova} baixado com sucesso!")

                    # Salva no estado para download fora do form
                    st.session_state.html = html
                    st.session_state.file_name = file_name

                except Exception as e:
                    st.error(f"❌ Ocorreu um erro: {e}")

# 🔥 🔥 🔥 BOTÃO DE DOWNLOAD FORA DO FORM 🔥 🔥 🔥
if st.session_state.html:
    with open(st.session_state.file_name, "rb") as f:
        st.download_button(
            label="📄 Baixar HTML",
            data=f,
            file_name=st.session_state.file_name,
            mime="text/html",
        )