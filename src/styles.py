"""
Estilos customizados para a interface Streamlit do VerbaFlow.
"""
import streamlit as st


def inject_custom_css():
    """
    Injeta CSS customizado para tipografia Cormorant Garamond e tema elegante.
    """
    css = """
    <style>
    /* Importar Cormorant Garamond do Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset e configurações base */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Tema de cores elegante */
    :root {
        --charcoal: #1A1A1A;
        --cream: #FAF9F6;
        --soft-white: #FFFFFF;
        --muted-blue: #4A90E2;
        --muted-green: #50C878;
        --muted-red: #E74C3C;
        --gray-light: #F5F5F5;
        --gray-medium: #E0E0E0;
        --gray-dark: #666666;
    }
    
    /* Estilizar o container principal */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Títulos com Cormorant Garamond - texto branco */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 600;
        color: #FFFFFF !important;
        letter-spacing: -0.02em;
    }
    
    h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 2rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-size: 1.5rem;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
    }
    
    /* Corpo do texto com Inter - texto branco/claro para melhor legibilidade */
    body, p, div, span {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--charcoal);
    }
    
    /* Texto principal em branco para melhor contraste */
    .main .block-container {
        color: #FFFFFF;
    }
    
    .main .block-container p,
    .main .block-container div,
    .main .block-container span {
        color: #FFFFFF !important;
    }
    
    /* Inputs e textareas mantêm fundo claro */
    input, textarea, select {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--charcoal);
        background-color: var(--soft-white);
    }
    
    /* Cards elegantes */
    .stCard {
        background-color: var(--soft-white);
        border: 1px solid var(--gray-medium);
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    /* Text areas estilizadas */
    .stTextArea textarea {
        font-family: 'Inter', monospace;
        font-size: 0.9rem;
        line-height: 1.6;
        background-color: var(--gray-light);
        border: 1px solid var(--gray-medium);
        border-radius: 6px;
        padding: 1rem;
    }
    
    /* Botões elegantes */
    .stButton > button {
        background-color: var(--muted-blue);
        color: white;
        font-weight: 500;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button:hover {
        background-color: #357ABD;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(74, 144, 226, 0.3);
    }
    
    /* Métricas estilizadas */
    .stMetric {
        background-color: var(--gray-light);
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid var(--muted-blue);
    }
    
    /* Sidebar estilizada */
    .css-1d391kg {
        background-color: var(--cream);
    }
    
    .css-1d391kg .stTextInput input {
        background-color: var(--soft-white);
        border: 1px solid var(--gray-medium);
    }
    
    /* Indicadores de sucesso/erro */
    .success-indicator {
        background-color: var(--muted-green);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(80, 200, 120, 0.2);
    }
    
    .error-indicator {
        background-color: var(--muted-red);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(231, 76, 60, 0.2);
    }
    
    /* Badge para categorias */
    .category-badge {
        display: inline-block;
        background-color: var(--muted-blue);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        font-size: 0.9rem;
        margin: 0.25rem;
    }
    
    /* Esconder elementos do Streamlit padrão */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Status container */
    .status-container {
        background-color: var(--gray-light);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Markdown estilizado - texto branco */
    .stMarkdown {
        line-height: 1.7;
        color: #FFFFFF !important;
    }
    
    .stMarkdown p,
    .stMarkdown li,
    .stMarkdown div {
        color: #FFFFFF !important;
    }
    
    .stMarkdown code {
        background-color: var(--gray-light);
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        color: var(--charcoal);
    }
    
    /* Métricas com texto branco */
    .stMetric {
        color: #FFFFFF !important;
    }
    
    .stMetric label {
        color: #FFFFFF !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }
    
    .stMetric [data-testid="stMetricDelta"] {
        color: #FFFFFF !important;
    }
    
    /* Scrollbar customizada */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--gray-light);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--gray-dark);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--charcoal);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def apply_page_config():
    """
    Aplica configuração customizada da página.
    """
    st.set_page_config(
        page_title="VerbaFlow - Classificação e Enriquecimento de Textos",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded"
    )

