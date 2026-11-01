import streamlit as st
import google.generativeai as genai

# Configuração da página do Streamlit
st.set_page_config(page_title="Meu Chatbot Gemini", page_icon="🤖")
st.title("🤖 Meu Chatbot Pessoal")

# Configuração da API do Gemini (Recomendado: Salvar como variável de ambiente no deployment)
# Para rodar localmente, substitua pelo seu token ou configure no sistema
api_key = st.sidebar.text_input("Insira sua Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # Inicializa o modelo Gemini
    # Usando a convenção padrão para o modelo principal de chat atual (flash)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Inicializa o histórico do chat na sessão do Streamlit se não existir
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibe as mensagens anteriores do histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Campo de entrada para o usuário digitar
    if prompt := st.chat_input("Como posso te ajudar hoje?"):
        # Exibe a mensagem do usuário
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Gera a resposta usando o Gemini
        try:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                
                # Conversão rápida para o formato esperado pelo modelo (opcional se usar chat session)
                response = model.generate_content(prompt)
                
                full_response = response.text
                message_placeholder.markdown(full_response)
                
            # Salva a resposta no histórico
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Erro ao gerar resposta: {e}")
else:
    st.info("Por favor, insira sua API Key do Gemini na barra lateral para começar.")
