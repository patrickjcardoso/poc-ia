import streamlit as st
import requests

# URL da sua API Gateway integrada com Lambda
API_URL = "https://d9v1sfn4v7.execute-api.us-east-1.amazonaws.com/poc-brinquedosbandeirantes-bedrock"

st.set_page_config(page_title="POC Chatbot Industrial (Bedrock)", page_icon="🤖", layout="centered")

st.markdown("""
# 🤖 Chatbot Industrial Brinquedos Bandeirantes
Converse com a base de conhecimento estruturada da Brinquedos Bandeirantes via Amazon Bedrock.
""")

st.markdown("""
<div style='background-color:#fafafa;padding:10px;border-radius:8px;'>
Esta é uma demonstração de POC com integração AWS Lambda, Bedrock e Redshift/S3.
</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.container():
    st.markdown("#### Faça uma pergunta:")
    prompt = st.text_input("", placeholder="Digite sua pergunta (ex: Qual a descrição do item 1221?)", key="user_input")

    if st.button("Enviar", use_container_width=True) or prompt:
        if prompt:
            # Exibe pergunta no chat
            st.session_state.chat_history.append(("user", prompt))

            # Chama a API
            try:
                response = requests.post(
                    API_URL,
                    headers={"Content-Type": "application/json"},
                    json={"prompt": prompt}
                )
                if response.status_code == 200:
                    resposta = response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text
                    if isinstance(resposta, dict):
                        resposta = resposta.get("body", resposta)
                    st.session_state.chat_history.append(("bot", resposta.strip()))
                else:
                    st.session_state.chat_history.append(("bot", f"Erro: {response.text}"))
            except Exception as e:
                st.session_state.chat_history.append(("bot", f"Erro ao acessar a API: {str(e)}"))

# Histórico de chat estilizado
st.markdown("---")
st.markdown("#### Histórico de Conversa:")

for who, msg in st.session_state.chat_history:
    if who == "user":
        st.markdown(f"<div style='color:#333;background:#eef;font-weight:bold;padding:6px 12px;border-radius:5px; margin-bottom:5px;'>🧑‍💼 {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='color:#004D40;background:#E0F2F1;padding:6px 12px;border-radius:5px;margin-bottom:10px;'>🤖 {msg}</div>", unsafe_allow_html=True)

# Rodapé
st.markdown("""
---
<div style="text-align:center;color:#AAA;">
POC Brinquedos Bandeirantes &nbsp;|&nbsp; AWS GenAI &nbsp;|&nbsp; Desenvolvido por Patrick Cardoso
</div>
""", unsafe_allow_html=True)
