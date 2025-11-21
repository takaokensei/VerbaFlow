"""
VerbaFlow - Modern UI Styling System
=====================================
Premium Dark Theme com Glassmorphism, Micro-interações e Design System Moderno
Inspirado em interfaces React/Next.js de 2024-2025

Design Trends Aplicados:
- Glassmorphism (frosted glass effect)
- Dark Mode profissional com elevação por camadas
- Gradientes vibrantes e sutis
- Micro-interações e transições suaves
- Tipografia moderna (Inter + Space Grotesk)
- Paleta de cores Material Design Dark

Author: VerbaFlow Team
Version: 2.0.0
"""
import streamlit as st


def inject_custom_css():
    """
    Sistema de CSS avançado com Glassmorphism e Dark Theme profissional.
    Compatível com Streamlit 1.28+
    """
    css = """
    <style>
    /* ============================================
       1. IMPORTS - Fontes Modernas
       ============================================ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');

    /* ============================================
       2. CSS VARIABLES - Design Tokens
       ============================================ */
    :root {
        /* === Cores Base (Material Dark Elevation) === */
        --bg-base: #0a0a0a;
        --bg-surface-1: #121212;
        --bg-surface-2: #1e1e1e;
        --bg-surface-3: #252525;
        --bg-surface-4: #2c2c2c;
        --bg-surface-5: #333333;
        
        /* === Texto === */
        --text-primary: #ffffff;
        --text-secondary: rgba(255, 255, 255, 0.7);
        --text-tertiary: rgba(255, 255, 255, 0.5);
        --text-disabled: rgba(255, 255, 255, 0.38);
        --text-on-light: #1a1a1a;
        
        /* === Cores de Destaque (Vibrant Accents) === */
        --accent-primary: #6366f1;      /* Indigo */
        --accent-primary-hover: #818cf8;
        --accent-secondary: #8b5cf6;    /* Violet */
        --accent-success: #10b981;      /* Emerald */
        --accent-warning: #f59e0b;      /* Amber */
        --accent-error: #ef4444;        /* Red */
        --accent-info: #3b82f6;         /* Blue */
        
        /* === Gradientes === */
        --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
        --gradient-accent: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
        --gradient-success: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        --gradient-surface: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0) 100%);
        
        /* === Glassmorphism === */
        --glass-bg: rgba(255, 255, 255, 0.03);
        --glass-bg-hover: rgba(255, 255, 255, 0.06);
        --glass-border: rgba(255, 255, 255, 0.08);
        --glass-blur: 20px;
        
        /* === Sidebar (Light Theme) === */
        --sidebar-bg: #fafafa;
        --sidebar-text: #1a1a1a;
        --sidebar-text-secondary: #666666;
        --sidebar-border: #e5e5e5;
        --sidebar-input-bg: #ffffff;
        
        /* === Shadows === */
        --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -2px rgba(0, 0, 0, 0.3);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -4px rgba(0, 0, 0, 0.4);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.4);
        --shadow-glow: 0 0 40px rgba(99, 102, 241, 0.15);
        
        /* === Spacing & Sizing === */
        --radius-sm: 6px;
        --radius-md: 10px;
        --radius-lg: 16px;
        --radius-xl: 24px;
        
        /* === Transitions === */
        --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ============================================
       3. RESET & BASE STYLES
       ============================================ */
    *, *::before, *::after {
        box-sizing: border-box;
    }

    /* ============================================
       4. MAIN APP CONTAINER
       ============================================ */
    .stApp {
        background: var(--bg-base);
        background-image: 
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99, 102, 241, 0.15), transparent),
            radial-gradient(ellipse 60% 40% at 100% 100%, rgba(139, 92, 246, 0.1), transparent);
        min-height: 100vh;
    }

    /* Main content area */
    .main .block-container {
        padding: 2rem 3rem 3rem;
        max-width: 1400px;
        color: var(--text-primary);
    }

    /* ============================================
       5. TYPOGRAPHY
       ============================================ */
    /* Headings - Space Grotesk */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Space Grotesk', -apple-system, sans-serif !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }

    h1, .stMarkdown h1 {
        font-size: 2.75rem !important;
        font-weight: 700 !important;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
    }

    h2, .stMarkdown h2 {
        font-size: 1.875rem !important;
        margin-top: 2rem !important;
    }

    h3, .stMarkdown h3 {
        font-size: 1.5rem !important;
        margin-top: 1.5rem !important;
    }

    /* Body text - Inter */
    body, p, div, span, label, li,
    .stMarkdown, .stMarkdown p {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary) !important;
        line-height: 1.6;
    }

    /* Code - JetBrains Mono */
    code, pre, .stCode {
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    }

    /* ============================================
       6. SIDEBAR - Light Theme with Glass
       ============================================ */
    [data-testid="stSidebar"] {
        background: var(--sidebar-bg) !important;
        border-right: 1px solid var(--sidebar-border) !important;
    }

    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 150px;
        background: linear-gradient(180deg, rgba(99, 102, 241, 0.08) 0%, transparent 100%);
        pointer-events: none;
    }

    /* Sidebar text - DARK on light background */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] div {
        color: var(--sidebar-text) !important;
        -webkit-text-fill-color: var(--sidebar-text) !important;
    }

    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li {
        color: var(--sidebar-text-secondary) !important;
    }

    /* Sidebar headings */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        background: none !important;
        -webkit-text-fill-color: var(--sidebar-text) !important;
    }

    /* ============================================
       7. INPUT COMPONENTS - Glassmorphism Style
       ============================================ */
    /* Text inputs & textareas */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: var(--bg-surface-2) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 0.75rem 1rem !important;
        transition: all var(--transition-base) !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15), var(--shadow-md) !important;
        background: var(--bg-surface-3) !important;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-tertiary) !important;
        -webkit-text-fill-color: var(--text-tertiary) !important;
    }

    /* Sidebar inputs - Light theme */
    [data-testid="stSidebar"] .stTextInput > div > div > input,
    [data-testid="stSidebar"] .stTextArea > div > div > textarea {
        background: var(--sidebar-input-bg) !important;
        border: 1px solid var(--sidebar-border) !important;
        color: var(--sidebar-text) !important;
        -webkit-text-fill-color: var(--sidebar-text) !important;
    }

    [data-testid="stSidebar"] .stTextInput > div > div > input:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }

    /* Labels */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stNumberInput label {
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* ============================================
       8. SELECTBOX & MULTISELECT
       ============================================ */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: var(--bg-surface-2) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-md) !important;
    }

    .stSelectbox [data-baseweb="select"] > div {
        background: transparent !important;
        border: none !important;
    }

    .stSelectbox [data-baseweb="select"] > div > div {
        color: var(--text-primary) !important;
    }

    /* Dropdown menu */
    [data-baseweb="popover"] {
        background: var(--bg-surface-3) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-md) !important;
        box-shadow: var(--shadow-xl) !important;
    }

    [data-baseweb="menu"] {
        background: transparent !important;
    }

    [data-baseweb="menu"] li {
        color: var(--text-primary) !important;
        transition: background var(--transition-fast) !important;
    }

    [data-baseweb="menu"] li:hover {
        background: var(--glass-bg-hover) !important;
    }

    /* Sidebar selectbox */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: var(--sidebar-input-bg) !important;
        border-color: var(--sidebar-border) !important;
    }

    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div > div {
        color: var(--sidebar-text) !important;
    }

    /* ============================================
       9. BUTTONS - Modern Gradient Style
       ============================================ */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem 1.5rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.01em;
        cursor: pointer;
        transition: all var(--transition-base) !important;
        box-shadow: var(--shadow-md), 0 0 20px rgba(99, 102, 241, 0.2) !important;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg), var(--shadow-glow) !important;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Secondary buttons */
    .stButton > button[kind="secondary"] {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        box-shadow: none !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: var(--glass-bg-hover) !important;
        box-shadow: var(--shadow-md) !important;
    }

    /* ============================================
       10. ALERTS & NOTIFICATIONS - Glass Cards
       ============================================ */
    .stAlert {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(var(--glass-blur)) !important;
        -webkit-backdrop-filter: blur(var(--glass-blur)) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 1rem 1.25rem !important;
    }

    /* Success */
    .stAlert[data-baseweb="notification"][kind="positive"],
    .element-container:has(.stSuccess) .stAlert {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%) !important;
        border-left: 4px solid var(--accent-success) !important;
    }

    /* Error */
    .stAlert[data-baseweb="notification"][kind="negative"],
    .element-container:has(.stError) .stAlert {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%) !important;
        border-left: 4px solid var(--accent-error) !important;
    }

    /* Warning */
    .stAlert[data-baseweb="notification"][kind="warning"] {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%) !important;
        border-left: 4px solid var(--accent-warning) !important;
    }

    /* Info */
    .stAlert[data-baseweb="notification"][kind="info"] {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%) !important;
        border-left: 4px solid var(--accent-info) !important;
    }

    /* ============================================
       11. CUSTOM VALIDATION BOXES
       ============================================ */
    .success-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-left: 4px solid var(--accent-success);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        margin: 1rem 0;
        color: var(--text-primary);
    }

    .error-box {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-left: 4px solid var(--accent-error);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        margin: 1rem 0;
        color: var(--text-primary);
    }

    .info-box {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(99, 102, 241, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-left: 4px solid var(--accent-primary);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        margin: 1rem 0;
        color: var(--text-primary);
    }

    /* ============================================
       12. REPORT CONTAINER - Glass Card
       ============================================ */
    .report-container {
        background: var(--glass-bg);
        backdrop-filter: blur(var(--glass-blur));
        -webkit-backdrop-filter: blur(var(--glass-blur));
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-xl);
        padding: 2rem 2.5rem;
        margin: 2rem 0;
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
    }

    .report-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    }

    /* ============================================
       13. METRICS - Modern Cards
       ============================================ */
    [data-testid="stMetric"] {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        transition: all var(--transition-base);
    }

    [data-testid="stMetric"]:hover {
        background: var(--glass-bg-hover);
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    [data-testid="stMetric"] label {
        color: var(--text-secondary) !important;
        font-size: 0.875rem !important;
    }

    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricDelta"] {
        font-weight: 500 !important;
    }

    /* ============================================
       14. EXPANDER - Collapsible Sections
       ============================================ */
    /* Esconder ícones Material Icons quebrados APENAS dentro de expanders */
    /* IMPORTANTE: NÃO afetar o sidebar toggle [data-testid="collapsedControl"] */
    .streamlit-expanderHeader [class*="material-icons"]:not([data-testid="collapsedControl"] *),
    .streamlit-expanderHeader [class*="keyboard_double_arrow"]:not([data-testid="collapsedControl"] *),
    .streamlit-expanderHeader button[aria-label*="keyboard"]:not([data-testid="collapsedControl"]),
    .streamlit-expanderHeader [class*="material"]:not([data-testid="collapsedControl"] *),
    .streamlit-expanderHeader [class*="keyboard"]:not([data-testid="collapsedControl"] *) {
        display: none !important;
        visibility: hidden !important;
        font-size: 0 !important;
        width: 0 !important;
        height: 0 !important;
    }
    
    /* Substituir por emoji simples */
    .streamlit-expanderHeader {
        position: relative;
    }
    
    .streamlit-expanderHeader[aria-expanded="false"]::before {
        content: "▶";
        margin-right: 0.5rem;
        font-size: 0.9rem;
        display: inline-block;
    }
    
    .streamlit-expanderHeader[aria-expanded="true"]::before {
        content: "▼";
        margin-right: 0.5rem;
        font-size: 0.9rem;
        display: inline-block;
    }
    
    .streamlit-expanderHeader {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        transition: all var(--transition-base) !important;
    }

    .streamlit-expanderHeader:hover {
        background: var(--glass-bg-hover) !important;
        border-color: var(--accent-primary) !important;
    }

    .streamlit-expanderContent {
        background: var(--bg-surface-2) !important;
        border: 1px solid var(--glass-border) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
    }

    /* ============================================
       15. TABS - Modern Navigation
       ============================================ */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-surface-2);
        border-radius: var(--radius-lg);
        padding: 0.25rem;
        gap: 0.25rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        padding: 0.75rem 1.25rem !important;
        transition: all var(--transition-base) !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: var(--glass-bg) !important;
        color: var(--text-primary) !important;
    }

    .stTabs [aria-selected="true"] {
        background: var(--gradient-primary) !important;
        color: white !important;
    }

    /* ============================================
       16. DATAFRAME & TABLES
       ============================================ */
    .stDataFrame {
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-lg) !important;
        overflow: hidden;
    }

    .stDataFrame [data-testid="stDataFrameResizable"] {
        background: var(--bg-surface-2) !important;
    }

    /* ============================================
       17. SPINNER & LOADING
       ============================================ */
    .stSpinner > div {
        border-color: var(--accent-primary) transparent transparent transparent !important;
    }

    /* ============================================
       18. DIVIDER
       ============================================ */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, var(--glass-border), transparent) !important;
        margin: 2rem 0 !important;
    }

    /* ============================================
       19. SCROLLBAR - Custom Styling
       ============================================ */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-surface-1);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--bg-surface-4);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--bg-surface-5);
    }

    /* ============================================
       20. HIDE DEFAULT STREAMLIT ELEMENTS
       ============================================ */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* ============================================
       20.1. SIDEBAR TOGGLE - Ensure Visibility
       ============================================ */
    /* Garantir que o botão de toggle da sidebar seja sempre visível */
    [data-testid="collapsedControl"],
    button[data-testid="collapsedControl"],
    [data-testid="collapsedControl"] button {
        display: flex !important;
        visibility: visible !important;
        color: var(--text-primary) !important;
        opacity: 1 !important;
    }
    
    [data-testid="collapsedControl"] svg,
    button[data-testid="collapsedControl"] svg {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        width: 24px !important;
        height: 24px !important;
    }
    
    /* Garantir que Material Icons e texto dentro do sidebar toggle NÃO sejam escondidos */
    [data-testid="collapsedControl"] span,
    button[data-testid="collapsedControl"] span,
    button[aria-label*="sidebar"] span {
        display: inline-block !important;
        visibility: visible !important;
        opacity: 1 !important;
        font-size: 24px !important;
        width: auto !important;
        height: auto !important;
        color: var(--text-primary) !important;
        font-family: 'Material Icons' !important;
    }
    
    /* Garantir que texto "keyboard_double_arrow_right" seja renderizado como Material Icon */
    [data-testid="collapsedControl"],
    button[data-testid="collapsedControl"],
    button[aria-label*="sidebar"],
    button[aria-label*="Close sidebar"],
    button[aria-label*="Open sidebar"] {
        font-family: 'Material Icons', sans-serif !important;
    }

    /* ============================================
       21. ANIMATIONS & MICRO-INTERACTIONS
       ============================================ */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    .animate-fade-in {
        animation: fadeIn 0.5s ease-out;
    }

    .animate-pulse {
        animation: pulse 2s infinite;
    }

    /* Skeleton loading effect */
    .skeleton {
        background: linear-gradient(90deg, var(--bg-surface-2) 25%, var(--bg-surface-3) 50%, var(--bg-surface-2) 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: var(--radius-md);
    }

    /* ============================================
       22. UTILITY CLASSES
       ============================================ */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(var(--glass-blur));
        -webkit-backdrop-filter: blur(var(--glass-blur));
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
    }

    .gradient-text {
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .glow {
        box-shadow: var(--shadow-glow);
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def apply_page_config():
    """
    Aplica configuração customizada da página.
    DEVE ser chamado ANTES de qualquer outro comando Streamlit.
    """
    st.set_page_config(
        page_title="VerbaFlow - Classificação e Enriquecimento de Textos",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded"
    )


# ============================================
# HELPER FUNCTIONS - Custom Components
# ============================================

def show_success(message: str, icon: str = "✅"):
    """Exibe uma mensagem de sucesso estilizada."""
    st.markdown(f'''
        <div class="success-box animate-fade-in">
            <span style="font-size: 1.25rem; margin-right: 0.5rem;">{icon}</span>
            <span>{message}</span>
        </div>
    ''', unsafe_allow_html=True)


def show_error(message: str, icon: str = "❌"):
    """Exibe uma mensagem de erro estilizada."""
    st.markdown(f'''
        <div class="error-box animate-fade-in">
            <span style="font-size: 1.25rem; margin-right: 0.5rem;">{icon}</span>
            <span>{message}</span>
        </div>
    ''', unsafe_allow_html=True)


def show_info(message: str, icon: str = "ℹ️"):
    """Exibe uma mensagem informativa estilizada."""
    st.markdown(f'''
        <div class="info-box animate-fade-in">
            <span style="font-size: 1.25rem; margin-right: 0.5rem;">{icon}</span>
            <span>{message}</span>
        </div>
    ''', unsafe_allow_html=True)


def glass_card(content: str, title: str = None):
    """Cria um card com efeito glassmorphism."""
    title_html = f'<h3 style="margin-top: 0; margin-bottom: 1rem;">{title}</h3>' if title else ''
    st.markdown(f'''
        <div class="glass-card animate-fade-in">
            {title_html}
            <div>{content}</div>
        </div>
    ''', unsafe_allow_html=True)


def gradient_header(text: str, subtitle: str = None):
    """Cria um header com texto em gradiente."""
    subtitle_html = f'<p style="color: rgba(255,255,255,0.6); font-size: 1.1rem; margin-top: 0.5rem;">{subtitle}</p>' if subtitle else ''
    st.markdown(f'''
        <div style="text-align: center; margin-bottom: 2rem;" class="animate-fade-in">
            <h1 class="gradient-text" style="font-size: 3rem; margin-bottom: 0;">{text}</h1>
            {subtitle_html}
        </div>
    ''', unsafe_allow_html=True)


def report_container(content: str):
    """Cria um container estilizado para relatórios."""
    st.markdown(f'''
        <div class="report-container animate-fade-in">
            {content}
        </div>
    ''', unsafe_allow_html=True)


def badge(text: str, color: str = "primary"):
    """Cria um badge/tag estilizado."""
    colors = {
        "primary": "var(--accent-primary)",
        "success": "var(--accent-success)",
        "error": "var(--accent-error)",
        "warning": "var(--accent-warning)",
        "info": "var(--accent-info)"
    }
    bg_color = colors.get(color, colors["primary"])
    return f'<span style="background: {bg_color}; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: 500;">{text}</span>' 