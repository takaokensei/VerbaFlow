"""
Aplicação Streamlit principal do VerbaFlow.
"""
import os
import re
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from crewai import Crew, Process
import sys
from io import StringIO

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Importar estilos customizados
from src.styles import inject_custom_css, apply_page_config

# Aplicar configuração e estilos
apply_page_config()
inject_custom_css()

from src.utils import (
    fetch_newsgroups_samples,
    clean_text,
    load_custom_csv,
    extract_ground_truth_from_filename,
    get_text_from_file
)
from src.agents import (
    get_llm,
    get_llm_with_fallback,
    create_analyst_agent,
    create_researcher_agent,
    create_editor_agent
)
from src.tasks import (
    create_classification_task,
    create_enrichment_task,
    create_reporting_task
)
from src.config import get_config
from src.models import ClassificationOutput
import json


def extract_category_robust(text: str) -> str:
    """
    Extrai a categoria do output do modelo com parsing robusto.
    Tenta múltiplos padrões regex para encontrar 'Category: <nome>'.
    Também procura no relatório final por "Categoria Identificada:".
    
    Args:
        text: Texto do output do modelo
    
    Returns:
        Categoria extraída ou string vazia
    """
    if not text:
        return ""
    
    # Padrões regex para tentar (em ordem de especificidade)
    patterns = [
        r'Category:\s*([^\n\r]+)',  # Padrão básico
        r'Category\s*:\s*([^\n\r]+)',  # Com espaços variáveis
        r'Categoria\s+Identificada:\s*([^\n\r]+)',  # Do relatório final
        r'Categoria:\s*([^\n\r]+)',  # Em português
        r'Category\s*=\s*([^\n\r]+)',  # Com igual
        r'Final\s+Category:\s*([^\n\r]+)',  # Com prefixo
        r'Classified\s+as:\s*([^\n\r]+)',  # Alternativo
        r'categoria\s+identificada[:\s]+([^\n\r]+)',  # Case insensitive
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            category = match.group(1).strip()
            # Limpar pontuação extra no final e aspas
            category = re.sub(r'[.,;:!?"\']+$', '', category)
            category = category.strip('"\'')
            # Verificar se é uma categoria válida do 20 Newsgroups
            valid_categories = [
                'alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc',
                'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'comp.windows.x',
                'misc.forsale', 'rec.autos', 'rec.motorcycles',
                'rec.sport.baseball', 'rec.sport.hockey', 'sci.crypt',
                'sci.electronics', 'sci.med', 'sci.space',
                'soc.religion.christian', 'talk.politics.guns',
                'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc'
            ]
            # Verificar se a categoria extraída corresponde a uma válida
            if any(cat.lower() == category.lower() for cat in valid_categories):
                return category
            # Se não corresponder exatamente, retornar mesmo assim (pode ser variação)
            if category:
                return category
    
    return ""


# Título principal com tipografia elegante
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="font-family: 'Cormorant Garamond', serif; font-size: 3.5rem; font-weight: 600; 
               color: #1A1A1A; letter-spacing: -0.02em; margin-bottom: 0.5rem;">
        VerbaFlow
    </h1>
    <p style="font-family: 'Inter', sans-serif; font-size: 1.1rem; color: #666666; 
              font-weight: 400; margin-top: 0;">
        Sistema Multi-Agente para Classificação e Enriquecimento de Textos
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Carregar valores do .env como valores padrão
    groq_key_env = os.getenv("GROQ_API_KEY", "")
    tavily_key_env = os.getenv("TAVILY_API_KEY", "")
    
    groq_key = st.text_input(
        "Groq API Key",
        value=groq_key_env if groq_key_env else "",
        type="password",
        help="Chave de API do Groq. Se deixar vazio, usa o valor do arquivo .env"
    )
    
    tavily_key = st.text_input(
        "Tavily API Key",
        value=tavily_key_env if tavily_key_env else "",
        type="password",
        help="Chave de API do Tavily. Se deixar vazio, usa o valor do arquivo .env"
    )
    
    st.markdown("---")
    st.markdown("### 🤖 Modelo Groq")
    
    model_choice = st.selectbox(
        "Selecione o modelo:",
        [
            "llama-3.3-70b-versatile (Melhor qualidade, mais tokens)",
            "llama-3.1-8b-instant (Mais rápido, menos tokens)",
            "mixtral-8x7b-32768 (Alternativa)"
        ],
        help="Modelos menores consomem menos tokens e são mais rápidos"
    )
    
    # Extrair nome do modelo
    if "llama-3.3-70b" in model_choice:
        selected_model = "llama-3.3-70b-versatile"
    elif "llama-3.1-8b" in model_choice:
        selected_model = "llama-3.1-8b-instant"
    else:
        selected_model = "mixtral-8x7b-32768"
    
    # Salvar API keys nas variáveis de ambiente
    # Se o usuário digitou algo, usa isso. Senão, mantém o valor do .env
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key
    elif groq_key_env:
        os.environ["GROQ_API_KEY"] = groq_key_env
    
    if tavily_key:
        os.environ["TAVILY_API_KEY"] = tavily_key
    elif tavily_key_env:
        os.environ["TAVILY_API_KEY"] = tavily_key_env
    
    os.environ["GROQ_MODEL"] = selected_model
    
    # Mostrar status das chaves
    st.markdown("---")
    if groq_key_env or groq_key:
        st.success("✅ Groq API Key configurada")
    else:
        st.warning("⚠️ Groq API Key não encontrada")
    
    if tavily_key_env or tavily_key:
        st.success("✅ Tavily API Key configurada")
    else:
        st.info("ℹ️ Tavily API Key opcional (enriquecimento não funcionará sem ela)")
    
    # Histórico de execuções
    st.markdown("---")
    st.markdown("### 📜 Histórico de Execuções")
    
    if 'execution_history' not in st.session_state:
        st.session_state['execution_history'] = []
    
    if st.session_state['execution_history']:
        for i, hist_item in enumerate(reversed(st.session_state['execution_history'][-5:]), 1):
            with st.expander(f"Execução {i}: {hist_item.get('category', 'N/A')} - {hist_item.get('timestamp', '')[:16]}", expanded=False):
                st.write(f"**Categoria:** {hist_item.get('category', 'N/A')}")
                st.write(f"**Status:** {'✅ Correto' if hist_item.get('correct', False) else '❌ Incorreto'}")
                if st.button(f"Ver detalhes", key=f"hist_{i}"):
                    st.session_state['view_history_item'] = hist_item
    else:
        st.info("Nenhuma execução ainda. Execute uma classificação para ver o histórico.")
    
    st.markdown("---")
    st.markdown("### 📊 Fonte de Dados")
    
    data_source = st.radio(
        "Selecione a fonte de dados:",
        ["20 Newsgroups (Amostras)", "CSV Customizado (6 Classes)"],
        index=0
    )


# Área principal
# Verificar se temos Groq API Key (do .env ou da sidebar)
groq_key_available = os.getenv("GROQ_API_KEY")
if not groq_key_available:
    st.warning("""
    ⚠️ **Groq API Key não encontrada!**
    
    Configure de uma das seguintes formas:
    1. **Arquivo .env:** Adicione `GROQ_API_KEY=sua_chave_aqui` no arquivo `.env`
    2. **Sidebar:** Digite a chave no campo "Groq API Key" na barra lateral
    """)
    st.stop()

# Seleção de dados
if data_source == "20 Newsgroups (Amostras)":
    st.subheader("📰 Dataset 20 Newsgroups")
    
    if st.button("🔄 Carregar Amostras Aleatórias"):
        with st.spinner("Baixando amostras do dataset 20 Newsgroups..."):
            try:
                samples = fetch_newsgroups_samples(num_samples=5)
                st.session_state['samples'] = samples
                st.success(f"✅ {len(samples)} amostras carregadas com sucesso!")
            except Exception as e:
                st.error(f"❌ Erro ao carregar amostras: {e}")
    
    if 'samples' in st.session_state and st.session_state['samples']:
        sample_files = st.session_state['samples']
        selected_file = st.selectbox(
            "Selecione uma amostra:",
            options=sample_files,
            format_func=lambda x: os.path.basename(x)
        )
        
        if selected_file:
            # Carregar texto
            raw_text = get_text_from_file(selected_file)
            ground_truth = extract_ground_truth_from_filename(selected_file)
            
            # Exibir texto e ground truth
            st.markdown("### 📄 Texto Original")
            st.text_area("", raw_text, height=200, disabled=True, key="raw_text_display")
            
            st.markdown(f"### 🏷️ Categoria Real (Ground Truth)")
            st.info(f"**{ground_truth}**")
            
            # Executar VerbaFlow
            if st.button("🚀 Executar VerbaFlow", type="primary", use_container_width=True):
                if not tavily_key:
                    st.warning("⚠️ Tavily API Key é necessária para enriquecimento completo.")
                
                # Status step-by-step com feedback visual rico
                with st.status("🚀 Iniciando VerbaFlow...", expanded=True) as status:
                    try:
                        # Step 1: Preparação
                        status.update(label="🔄 Limpando e preparando texto...", state="running")
                        cleaned_text = clean_text(raw_text)
                        
                        # Step 2: Configuração LLM
                        status.update(label="⚙️ Configurando LLM (tentando Groq, fallback Gemini)...", state="running")
                        if "OPENAI_API_KEY" in os.environ:
                            original_openai_key = os.environ.pop("OPENAI_API_KEY", None)
                        
                        selected_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
                        try:
                            llm = get_llm_with_fallback(model_name=selected_model)
                            llm_provider = "Groq"
                        except Exception as e:
                            # Tentar Gemini como fallback
                            config = get_config()
                            if config.use_gemini_fallback and config.google_api_key:
                                llm = get_llm(provider="gemini")
                                llm_provider = "Gemini (Fallback)"
                                status.update(label=f"⚠️ Groq falhou, usando {llm_provider}...", state="running")
                            else:
                                raise
                        
                        # Step 3: Criar agentes
                        status.update(label="🤖 Criando agentes especializados...", state="running")
                        analyst = create_analyst_agent(llm)
                        researcher = create_researcher_agent(llm)
                        editor = create_editor_agent(llm)
                        
                        # Step 4: Criar tasks
                        status.update(label="📋 Criando tasks e pipeline...", state="running")
                        # Preparar few-shot examples do histórico (se disponível)
                        few_shot_examples = []
                        if 'execution_history' in st.session_state and st.session_state['execution_history']:
                            for hist in st.session_state['execution_history'][-3:]:  # Últimos 3
                                if 'text_sample' in hist and 'category' in hist:
                                    few_shot_examples.append({
                                        'text': hist['text_sample'],
                                        'category': hist['category'],
                                        'reasoning': hist.get('reasoning', '')
                                    })
                        
                        task1 = create_classification_task(analyst, cleaned_text, few_shot_examples)
                        task2 = create_enrichment_task(researcher, task1)
                        task3 = create_reporting_task(editor, task1, task2)
                        
                        crew = Crew(
                            agents=[analyst, researcher, editor],
                            tasks=[task1, task2, task3],
                            process=Process.sequential,
                            verbose=True
                        )
                        
                        # Step 5: Executar Task 1 - Classificação
                        status.update(label="🕵️ [Task 1/3] Analisando texto com Chain of Thought...", state="running")
                        old_stdout = sys.stdout
                        sys.stdout = StringIO()
                        
                        try:
                            result = crew.kickoff()
                        finally:
                            sys.stdout = old_stdout
                        
                        status.update(label="✅ Análise completa! Processando resultados...", state="complete")
                    
                    except Exception as e:
                        error_str = str(e)
                        status.update(label=f"❌ Erro: {str(e)[:50]}...", state="error")
                        
                        # Tratamento especial para rate limit
                        if "429" in error_str or "rate_limit" in error_str.lower() or "Rate limit" in error_str:
                            st.error("""
                            ## ⚠️ Rate Limit Atingido
                            
                            Você atingiu o limite diário de tokens do Groq (100,000 tokens/dia no tier gratuito).
                            
                            **Soluções:**
                            
                            1. **Aguardar:** O limite será resetado em algumas horas (geralmente à meia-noite UTC)
                            
                            2. **Usar modelo menor:** Tente usar `llama-3.1-8b-instant` na sidebar - ele consome muito menos tokens
                            
                            3. **Upgrade:** Faça upgrade para Dev Tier em https://console.groq.com/settings/billing
                            
                            4. **Reduzir prompts:** Os prompts CoT são detalhados e consomem muitos tokens. 
                               Você pode simplificar temporariamente.
                            """)
                            
                            st.info(f"**Modelo atual:** {os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')}")
                            st.info("💡 **Dica:** Tente novamente com `llama-3.1-8b-instant` - é mais rápido e consome ~10x menos tokens!")
                        else:
                            st.error(f"❌ Erro durante execução: {e}")
                            with st.expander("🔍 Detalhes do Erro"):
                                st.exception(e)
                        st.stop()
                
                # Extrair categoria com parsing robusto
                result_str = str(result)
                
                # Tentar extrair da task de classificação primeiro (mais confiável)
                # O resultado do crew pode conter múltiplas tasks, vamos procurar em todas
                predicted_category = extract_category_robust(result_str)
                
                # Se não encontrou, tentar buscar no output da task1 diretamente
                if not predicted_category and hasattr(result, 'tasks_output'):
                    for task_output in result.tasks_output:
                        predicted_category = extract_category_robust(str(task_output))
                        if predicted_category:
                            break
                
                # Se ainda não encontrou, buscar no texto completo com padrões mais flexíveis
                if not predicted_category:
                    # Procurar por padrões como "talk.politics.misc" ou "sci.space" diretamente no texto
                    category_pattern = r'\b(' + '|'.join([
                        'alt\.atheism', 'comp\.graphics', 'comp\.os\.ms-windows\.misc',
                        'comp\.sys\.ibm\.pc\.hardware', 'comp\.sys\.mac\.hardware', 'comp\.windows\.x',
                        'misc\.forsale', 'rec\.autos', 'rec\.motorcycles',
                        'rec\.sport\.baseball', 'rec\.sport\.hockey', 'sci\.crypt',
                        'sci\.electronics', 'sci\.med', 'sci\.space',
                        'soc\.religion\.christian', 'talk\.politics\.guns',
                        'talk\.politics\.mideast', 'talk\.politics\.misc', 'talk\.religion\.misc'
                    ]) + r')\b'
                    match = re.search(category_pattern, result_str, re.IGNORECASE)
                    if match:
                        predicted_category = match.group(1)
                
                # Layout de duas colunas para resultados
                st.markdown("---")
                st.markdown("## 📊 Resultados da Análise")
                
                col_left, col_right = st.columns([1, 1])
                
                with col_left:
                    st.markdown("### 📄 Texto Original")
                    st.markdown(f"""
                    <div style="background-color: #F5F5F5; padding: 1.5rem; border-radius: 8px; 
                                border-left: 4px solid #4A90E2; max-height: 400px; overflow-y: auto;">
                        <p style="font-family: 'Inter', monospace; font-size: 0.9rem; line-height: 1.6; 
                                  color: #1A1A1A; white-space: pre-wrap;">{raw_text[:1000]}{'...' if len(raw_text) > 1000 else ''}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"**🏷️ Categoria Real (Ground Truth):**")
                    st.markdown(f'<span class="category-badge">{ground_truth}</span>', unsafe_allow_html=True)
                
                with col_right:
                    st.markdown("### ✅ Validação da Classificação")
                    
                    # Comparar categorias (case-insensitive)
                    is_correct = predicted_category.lower() == ground_truth.lower() if predicted_category else False
                    
                    if is_correct:
                        st.markdown("""
                        <div class="success-indicator">
                            ✅ Classificação Correta!
                        </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                    else:
                        st.markdown("""
                        <div class="error-indicator">
                            ❌ Classificação Incorreta
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Métricas
                    st.metric("Categoria Real", ground_truth)
                    st.metric("Categoria Prevista", predicted_category if predicted_category else "Não encontrada")
                
                # Relatório completo em seção expandível
                st.markdown("---")
                # Usar HTML customizado para evitar problema de ícone
                st.markdown("""
                <details open style="background-color: #F5F5F5; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                    <summary style="font-weight: 600; font-size: 1.1rem; cursor: pointer; padding: 0.5rem;">
                        📋 Relatório Enriquecido Completo
                    </summary>
                    <div style="margin-top: 1rem; padding: 1rem; background-color: white; border-radius: 4px;">
                """, unsafe_allow_html=True)
                st.markdown(result_str)
                st.markdown("""
                    </div>
                </details>
                """, unsafe_allow_html=True)
                
                # Salvar resultado na sessão
                st.session_state['last_result'] = {
                    'ground_truth': ground_truth,
                    'predicted': predicted_category,
                    'is_correct': is_correct,
                    'report': result_str
                }

else:  # CSV Customizado
    st.subheader("📊 CSV Customizado (6 Classes)")
    
    csv_path = "data/raw/Base_dados_textos_6_classes.csv"
    
    if not os.path.exists(csv_path):
        st.warning(f"⚠️ Arquivo CSV não encontrado em: {csv_path}")
        st.info("Por favor, coloque o arquivo 'Base_dados_textos_6_classes.csv' na pasta data/raw/")
    else:
        df = load_custom_csv(csv_path)
        
        if not df.empty:
            # Assumir que o CSV tem colunas 'texto' e 'categoria' (ou similar)
            # Tentar detectar automaticamente
            text_col = None
            category_col = None
            
            for col in df.columns:
                col_lower = col.lower()
                if 'text' in col_lower or 'texto' in col_lower:
                    text_col = col
                if 'categor' in col_lower or 'class' in col_lower or 'label' in col_lower:
                    category_col = col
            
            if text_col and category_col:
                st.dataframe(df.head(), use_container_width=True)
                
                selected_idx = st.selectbox(
                    "Selecione um registro:",
                    options=range(len(df)),
                    format_func=lambda x: f"Registro {x+1}: {df.iloc[x][category_col]}"
                )
                
                if selected_idx is not None:
                    raw_text = str(df.iloc[selected_idx][text_col])
                    ground_truth = str(df.iloc[selected_idx][category_col])
                    
                    st.markdown("### 📄 Texto Original")
                    st.text_area("", raw_text, height=200, disabled=True)
                    
                    st.markdown(f"### 🏷️ Categoria Real (Ground Truth)")
                    st.info(f"**{ground_truth}**")
                    
                    if st.button("🚀 Executar VerbaFlow", type="primary"):
                        # Similar ao fluxo acima, mas adaptado para CSV
                        st.info("Funcionalidade para CSV customizado - implementação similar ao 20 Newsgroups")
            else:
                st.error("❌ Não foi possível detectar automaticamente as colunas 'texto' e 'categoria' no CSV.")
                st.info("Colunas encontradas: " + ", ".join(df.columns.tolist()))
        else:
            st.error("❌ Erro ao carregar CSV ou arquivo vazio.")

