import streamlit as st
import pandas as pd
from backoffice_parser import parse_gabarito_backoffice
from gemini_parser import parse_gabarito_gemini
from gemini_vision_parser import extrair_gabarito_de_imagem


# 🔥 Configuração
st.set_page_config(page_title="📄 Conferência de Gabaritos", layout="wide")
st.title("📄 Conferência de Gabaritos — Backoffice x Banca")


api_key = st.sidebar.text_input("🔑 API KEY do Gemini", type="password")

st.subheader("🔹 Gabarito do Backoffice")
gabarito_html = st.text_area("📋 Cole aqui o HTML copiado do Backoffice", height=300)

st.subheader("🔸 Gabarito da Banca")
metodo = st.radio("Escolha o método de inserção:", ["📝 Texto da Banca", "🖼️ Imagem da Banca"])

texto_banca = ""
imagem_banca = None

if metodo == "📝 Texto da Banca":
    texto_banca = st.text_area("Cole aqui o texto do gabarito oficial", height=300)
else:
    imagem_banca = st.file_uploader("🔽 Envie a imagem do gabarito (PNG, JPG)", type=["png", "jpg", "jpeg"])


if st.button("🚀 Iniciar Conferência"):
    try:
        if not api_key:
            st.error("🔑 Insira sua API KEY para continuar.")
            st.stop()

        # 🔥 Processar gabarito do Backoffice
        df_back = parse_gabarito_backoffice(gabarito_html)

        # 🔥 Processar gabarito da banca (texto ou imagem)
        if metodo == "📝 Texto da Banca":
            if not texto_banca.strip():
                st.error("⚠️ Texto do gabarito da banca não inserido.")
                st.stop()
            df_banca = parse_gabarito_gemini(texto_banca, api_key=api_key)
        else:
            if not imagem_banca:
                st.error("⚠️ Imagem do gabarito da banca não enviada.")
                st.stop()
            df_banca = extrair_gabarito_de_imagem(imagem_banca, api_key=api_key)

        # 🔥 Comparação
        df_comparado = pd.merge(df_back, df_banca, on='questao', how='outer')
        df_comparado['resultado'] = df_comparado.apply(
            lambda row: '✔️ OK' if row['alternativa_back'].strip().upper() == row['alternativa_banca'].strip().upper()
            else '❌ Divergente',
            axis=1
        )

        # 🔥 Organizar a ordem das colunas
        df_comparado = df_comparado[['id', 'questao', 'alternativa_back', 'alternativa_banca', 'resultado']]

        st.subheader("🔍 Resultado da Conferência")
        st.dataframe(df_comparado)

        csv = df_comparado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Resultado como CSV",
            data=csv,
            file_name="conferencia_gabarito.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Erro ao processar: {e}")
