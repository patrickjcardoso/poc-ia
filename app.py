import streamlit as st
import requests

# URL da sua API Gateway/Lambda
API_URL = "https://d9v1sfn4v7.execute-api.us-east-1.amazonaws.com/poc-brinquedosbandeirantes-bedrock"

st.set_page_config(page_title="POC Brinquedos Bandeirantes", page_icon="🧩", layout="centered")

# Exibe a logo do cliente (centralizado)
st.image("logo-bandeirante.png", width=220)  # ajuste o width conforme des

# Título principal (apenas o nome)
st.markdown("""
# POC Brinquedos Bandeirantes
""")

# Inicialização do histórico de chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Botão para limpar o histórico
with st.sidebar:
    if st.button("🗑️ Limpar Histórico"):
        st.session_state.chat_history = []

# Input da pergunta do usuário
st.markdown("#### Faça uma pergunta:")
with st.form(key="chat_form"):
    prompt = st.text_input(
        "",
        placeholder="Digite sua pergunta (ex: Qual a descrição do item 1221?)",
        key="user_input"
    )
    enviar = st.form_submit_button("Enviar")

    if enviar and prompt:
        st.session_state.chat_history.append(("user", prompt))
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

# Histórico de conversa
st.markdown("---")
st.markdown("#### Histórico de Conversa:")

for who, msg in st.session_state.chat_history:
    if who == "user":
        st.markdown(f"<div style='color:#333;background:#eef;font-weight:bold;padding:6px 12px;border-radius:5px; margin-bottom:5px;'>👤 {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='color:#004D40;background:#E0F2F1;padding:6px 12px;border-radius:5px;margin-bottom:10px;'>🤖 {msg}</div>", unsafe_allow_html=True)

# Rodapé
st.markdown("""
---
<div style="text-align:center;color:#AAA;">
Brinquedos Bandeirantes &nbsp;|&nbsp; AWS &nbsp;|&nbsp; desenvolvido por O2B
</div>
""", unsafe_allow_html=True)
