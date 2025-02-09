import streamlit as st
from utils.utils_summarizer import summarize_video
import time

# Configuração da página
st.set_page_config(
    page_title="Podcast Summarizer",
    page_icon="🎙️",
    layout="wide"
)

# CSS personalizado
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .success-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #D1FAE5;
        color: #065F46;
    }
    .error-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #FEE2E2;
        color: #991B1B;
    }
    </style>
    """, unsafe_allow_html=True)

# Título e descrição
st.title("🎙️ Podcast Summarizer")
st.markdown("""
    Transforme longas transcrições de podcasts em resumos concisos e informativos.
    Basta colar o link do YouTube e deixar a IA fazer a mágica! 🪄
""")

# Container principal
with st.container():
    api_key = st.text_input(
        "🔑 API Key do Google Cloud",
        type="password",
        help="Insira sua API key do Google Cloud para usar o Gemini"
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        video_url = st.text_input(
            "🎥 URL do YouTube",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Cole aqui o link do vídeo do YouTube que você quer resumir"
        )

    with col2:
        if st.button("📝 Gerar Resumo", disabled=not (video_url and api_key)):
            if not video_url.startswith("https://www.youtube.com/"):
                st.error("❌ Por favor, insira uma URL válida do YouTube")
            else:
                try:
                    with st.spinner("Gerando resumo... Isso pode levar alguns segundos ⏳"):
                        summary = summarize_video(video_url, api_key)
                        
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        
                        progress_bar.empty()
                        
                        st.markdown("### ✨ Resumo Gerado")
                        st.markdown(f"""
                            <div class="success-message">
                                {summary}
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("### 📤 Compartilhar")
                        col1, col2, col3 = st.columns(3)
                        col1.button("📋 Copiar")
                        col2.button("📧 Email")
                        col3.button("💾 Salvar PDF")
                        
                except Exception as e:
                    st.markdown(f"""
                        <div class="error-message">
                            ❌ Erro ao gerar resumo: {str(e)}
                            <br>Verifique a URL e a API key e tente novamente.
                        </div>
                    """, unsafe_allow_html=True)

# Sidebar com informações adicionais
with st.sidebar:
    st.header("ℹ️ Sobre")
    st.markdown("""
        **Como usar:**
        1. Cole sua API key do Google Cloud
        2. Insira a URL do vídeo do YouTube
        3. Clique em 'Gerar Resumo'
        4. Aguarde o processamento
        5. Copie ou compartilhe o resultado!
        
        **Recursos:**
        - Suporte a múltiplos idiomas
        - Resumos concisos e precisos
        - Interface intuitiva
        
        **Precisa de ajuda?**
        [Documentation 📚](https://docs.example.com)
        [Support 💬](https://support.example.com)
    """)
    
    st.markdown("### 📊 Estatísticas")
    col1, col2 = st.columns(2)
    col1.metric("Vídeos Resumidos", "1.2K")
    col2.metric("Tempo Economizado", "300h")

st.markdown("---")
st.markdown(
    "Made with ❤️ by Your Team | [GitHub](https://github.com) | [Report Bug](https://github.com/issues)"
)
